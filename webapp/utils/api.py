"""
webapp/utils/api.py
--------------------
Backend wrapper for the Predictive Maintenance web dashboard.

IMPORTANT: This file does NOT reimplement or retrain the model.
It imports and reuses the existing project's `config.py` and the
model-loading logic already defined in the existing project's
`app.py`, exactly as they are. Nothing in the parent project is
modified, only imported (read-only reuse).

Everything specific to the web layer lives here, isolated inside
webapp/:
  - strict input validation (never lets an empty/invalid value reach
    a raw float() conversion — this is the fix for the
    "could not convert string to float: ''" crash)
  - batch inference (one vectorised model call + one vectorised SHAP
    call for the whole sheet, instead of one HTTP round-trip per row)
  - health scoring / failure-mode heuristics / recommendations
  - per-row SHAP explainability
  - dataset-backed sample & bulk-row generation (real rows pulled
    from the project's own held-out test set, never fabricated)
"""

import os
import sys
import uuid
import random
from datetime import datetime

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------
# Wire up imports to the EXISTING project (read-only reuse)
# ---------------------------------------------------------------------
WEBAPP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(WEBAPP_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import config as project_config          # existing project config.py (untouched)
from app import load_model, load_test_data  # existing project app.py (untouched)

# ---------------------------------------------------------------------
# Load model + reference test data ONCE at import time
# ---------------------------------------------------------------------
_model = load_model(project_config.MODEL_PATH)
_X_test_reference, _y_test_reference = load_test_data(
    project_config.X_TEST_PATH, project_config.Y_TEST_PATH
)

# The exact feature order the model was trained on.
FEATURE_ORDER = [
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]",
    "ambient_temp_C",
    "load_density_pct",
    "ambient_temp_K",
    "temp_differential_K",
    "load_adjusted_torque",
    "wear_per_load",
    "Type_enc",
]

# Type encoding, as fixed by the training-time LabelEncoder
# (alphabetical: H=0, L=1, M=2) — see notebooks/03_context_fusion.
TYPE_ENCODING = {"H": 0, "L": 1, "M": 2}

# Every numeric field the sheet must supply for a valid prediction,
# paired with the human-readable label used in validation messages.
# This list is the single source of truth for validation — nothing
# downstream ever calls float() on a value that hasn't passed through
# _clean_numeric() below.
REQUIRED_NUMERIC_FIELDS = [
    ("air_temp_k", "Air Temp [K]"),
    ("process_temp_k", "Process Temp [K]"),
    ("rotational_speed_rpm", "Rot. Speed [rpm]"),
    ("torque_nm", "Torque [Nm]"),
    ("tool_wear_min", "Tool Wear [min]"),
    ("ambient_temp_c", "Ambient Temp [°C]"),
    ("load_density_pct", "Production Load [%]"),
]

# In-memory prediction log for the "Recent Predictions" table / export.
# (Kept in memory only, by design — no new database is introduced.)
_PREDICTION_LOG = []

# Lazily-built SHAP explainer (built on first use).
_shap_explainer = None

# Used to hand out unique demo machine IDs for generated/sample rows.
_used_machine_ids = set()


def _get_shap_explainer():
    global _shap_explainer
    if _shap_explainer is None:
        import shap
        _shap_explainer = shap.TreeExplainer(_model)
    return _shap_explainer


# =======================================================================
# Validation layer
# -----------------------------------------------------------------------
# This is the fix for the root cause of the dashboard's crashes: every
# raw value coming from the browser passes through here BEFORE it is
# ever converted with float(). Empty strings, missing keys, and
# non-numeric text are all caught here and turned into a single, clean,
# human-readable message — never a raw Python exception string.
# =======================================================================
class ValidationError(Exception):
    """Raised for a bad row of input. The message is always safe to
    show directly to the user — it never contains Python internals."""
    pass


def _clean_numeric(raw_input: dict, key: str, label: str, errors: list):
    """Safely pull a numeric field out of raw_input. Never raises —
    any problem is appended to `errors` instead, so a single row can
    report every problem at once instead of failing on the first."""
    value = raw_input.get(key, None)

    if value is None:
        errors.append(f"{label} is required")
        return None

    if isinstance(value, str):
        value = value.strip()
        if value == "":
            errors.append(f"{label} is required")
            return None

    try:
        number = float(value)
    except (TypeError, ValueError):
        errors.append(f"{label} must be a number")
        return None

    if number != number or number in (float("inf"), float("-inf")):  # NaN / inf guard
        errors.append(f"{label} must be a valid number")
        return None

    return number


def validate_raw_input(raw_input: dict) -> dict:
    """
    Validate one machine row. Returns a dict of clean, guaranteed-valid
    floats (plus a normalised machine_type) on success.

    Raises ValidationError with ONE combined, human-friendly message on
    failure — this is what reaches the UI, never a Python traceback.
    """
    if not isinstance(raw_input, dict):
        raise ValidationError("Malformed row data.")

    errors = []
    cleaned = {}
    for key, label in REQUIRED_NUMERIC_FIELDS:
        cleaned[key] = _clean_numeric(raw_input, key, label, errors)

    machine_type = str(raw_input.get("machine_type") or "M").upper().strip()
    if machine_type not in TYPE_ENCODING:
        machine_type = "M"
    cleaned["machine_type"] = machine_type

    if errors:
        raise ValidationError("Missing or invalid value — " + "; ".join(errors))

    return cleaned


# ---------------------------------------------------------------------
# Feature engineering (mirrors the derivations already used in the
# training notebooks — see notebooks/03_context_fusion)
# ---------------------------------------------------------------------
def _engineered_feature_dict(cleaned: dict) -> dict:
    """cleaned must already have passed validate_raw_input()."""
    air_temp_k = cleaned["air_temp_k"]
    process_temp_k = cleaned["process_temp_k"]
    rpm = cleaned["rotational_speed_rpm"]
    torque = cleaned["torque_nm"]
    tool_wear = cleaned["tool_wear_min"]
    ambient_temp_c = cleaned["ambient_temp_c"]
    load_density_pct = cleaned["load_density_pct"]
    machine_type = cleaned["machine_type"]

    ambient_temp_k = ambient_temp_c + 273.15
    temp_differential_k = air_temp_k - ambient_temp_k
    load_adjusted_torque = torque / (load_density_pct / 100 + 0.01)
    wear_per_load = tool_wear * (load_density_pct / 100)

    return {
        "Air temperature [K]": air_temp_k,
        "Process temperature [K]": process_temp_k,
        "Rotational speed [rpm]": rpm,
        "Torque [Nm]": torque,
        "Tool wear [min]": tool_wear,
        "ambient_temp_C": ambient_temp_c,
        "load_density_pct": load_density_pct,
        "ambient_temp_K": ambient_temp_k,
        "temp_differential_K": temp_differential_k,
        "load_adjusted_torque": load_adjusted_torque,
        "wear_per_load": wear_per_load,
        "Type_enc": TYPE_ENCODING[machine_type],
    }


def build_feature_row(cleaned: dict) -> pd.DataFrame:
    """Single-row convenience wrapper around _engineered_feature_dict."""
    return pd.DataFrame([_engineered_feature_dict(cleaned)], columns=FEATURE_ORDER)


def build_feature_matrix(cleaned_rows: list) -> pd.DataFrame:
    """Vectorised feature build for an entire sheet of validated rows."""
    return pd.DataFrame(
        [_engineered_feature_dict(c) for c in cleaned_rows], columns=FEATURE_ORDER
    )


# ---------------------------------------------------------------------
# Health score / status banding
# ---------------------------------------------------------------------
def health_score_from_probability(failure_probability: float) -> float:
    """Simple, transparent mapping: higher failure probability -> lower health score."""
    return round((1 - failure_probability) * 100, 1)


def health_band(score: float) -> dict:
    if score >= 90:
        return {"label": "Excellent", "color": "green"}
    if score >= 80:
        return {"label": "Healthy", "color": "light-green"}
    if score >= 60:
        return {"label": "Needs Monitoring", "color": "yellow"}
    if score >= 40:
        return {"label": "High Risk", "color": "orange"}
    return {"label": "Critical", "color": "red"}


# ---------------------------------------------------------------------
# Failure-mode heuristic
# ---------------------------------------------------------------------
# NOTE: The trained model is a BINARY classifier (failure / no failure).
# It does not predict a specific failure mode. The categories below are
# derived using the published AI4I 2020 dataset's own domain thresholds
# (tool wear, heat dissipation, power, overstrain, random) so the
# dashboard can offer a plausible, transparent "likely failure mode"
# explanation rather than a second model prediction. This is clearly
# a rule-based add-on, not a model output.
def infer_failure_mode(cleaned: dict) -> dict:
    air_temp_k = cleaned["air_temp_k"]
    process_temp_k = cleaned["process_temp_k"]
    rpm = cleaned["rotational_speed_rpm"]
    torque = cleaned["torque_nm"]
    tool_wear = cleaned["tool_wear_min"]
    machine_type = cleaned["machine_type"]

    overstrain_thresholds = {"L": 11000, "M": 12000, "H": 13000}
    power_w = torque * (rpm * 2 * np.pi / 60)  # torque(Nm) * angular speed(rad/s)

    reasons = []

    if tool_wear >= 200:
        reasons.append(("Tool Wear Failure", f"Tool wear at {tool_wear:.0f} min (>= 200 min threshold)"))

    if (process_temp_k - air_temp_k) < 8.6 and rpm < 1380:
        reasons.append(("Heat Dissipation Failure", "Low temperature differential combined with low rotational speed"))

    if power_w < 3500 or power_w > 9000:
        reasons.append(("Power Failure", f"Estimated power output {power_w:.0f} W outside the safe 3500-9000 W band"))

    threshold = overstrain_thresholds.get(machine_type, 12000)
    if tool_wear * torque > threshold:
        reasons.append(("Overstrain Failure", f"Tool wear x torque ({tool_wear * torque:.0f}) exceeds the {machine_type}-type threshold"))

    if not reasons:
        return {"failure_type": "No Failure", "detail": "No known industrial failure-mode thresholds were triggered."}

    top = reasons[0]
    return {"failure_type": top[0], "detail": top[1], "all_triggered": reasons}


# ---------------------------------------------------------------------
# Explainability (SHAP if available, otherwise model feature_importances_)
# Computed for a WHOLE batch in one call — this is what guarantees every
# machine gets its own explanation, not just the first row.
# ---------------------------------------------------------------------
def explain_batch(feature_matrix: pd.DataFrame, top_n: int = 5) -> list:
    n = len(feature_matrix)
    if n == 0:
        return []

    try:
        explainer = _get_shap_explainer()
        shap_values = explainer.shap_values(feature_matrix)
        values = np.array(shap_values)
        if values.ndim == 3:
            # (n_classes, n_samples, n_features) style output -> take the
            # "failure" class contributions.
            values = values[-1]
        method = "SHAP"
    except Exception:
        # Fallback: global feature importance from the model itself,
        # signed by whether this sample's value is above/below the
        # training-set median (a lightweight, honest approximation).
        importances = getattr(_model, "feature_importances_", np.ones(len(FEATURE_ORDER)))
        medians = _X_test_reference[FEATURE_ORDER].median().values
        direction = np.sign(feature_matrix.values - medians)
        values = importances * direction
        method = "Model Feature Importance (fallback)"

    explanations = []
    for i in range(n):
        contributions = values[i]
        ranked = sorted(
            zip(FEATURE_ORDER, contributions),
            key=lambda pair: abs(pair[1]),
            reverse=True,
        )[:top_n]
        explanations.append({
            "method": method,
            "top_features": [{"feature": f, "impact": float(v)} for f, v in ranked],
        })
    return explanations


# ---------------------------------------------------------------------
# Recommendation text
# ---------------------------------------------------------------------
def recommendation_for(is_failure: bool, failure_type: str) -> list:
    if not is_failure:
        return [
            "Machine operating normally.",
            "Continue scheduled maintenance.",
            "No immediate action required.",
        ]

    mapping = {
        "Tool Wear Failure": ["Replace tool", "Inspect tool holder alignment"],
        "Heat Dissipation Failure": ["Inspect cooling system", "Check airflow around the machine", "Reduce operating load temporarily"],
        "Power Failure": ["Inspect drive/motor power supply", "Check for voltage irregularities"],
        "Overstrain Failure": ["Reduce operating load", "Inspect bearing and drivetrain", "Schedule maintenance immediately"],
        "No Failure": ["Schedule a precautionary inspection", "Monitor sensor trends over the next cycle"],
    }
    return mapping.get(failure_type, ["Schedule maintenance immediately", "Perform full diagnostic inspection"])


# ---------------------------------------------------------------------
# Result assembly for one already-validated, already-scored row
# ---------------------------------------------------------------------
def _assemble_result(raw_input: dict, cleaned: dict, proba: float, threshold: float, explanation: dict) -> dict:
    is_failure = proba >= threshold
    score = health_score_from_probability(proba)
    band = health_band(score)
    failure_mode = infer_failure_mode(cleaned)
    recommendations = recommendation_for(is_failure, failure_mode["failure_type"])
    confidence = round((proba if is_failure else (1 - proba)) * 100, 1)

    return {
        "id": str(uuid.uuid4())[:8],
        "machine_id": (raw_input.get("machine_id") or "N/A"),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Failure Predicted" if is_failure else "Healthy Machine",
        "is_failure": is_failure,
        "failure_probability": round(proba * 100, 2),
        "probability": proba,
        "threshold_used": threshold,
        "health_score": score,
        "health_band": band,
        "confidence": confidence,
        "failure_mode": failure_mode,
        "recommendations": recommendations,
        "explanation": explanation,
        "raw_input": raw_input,
    }


# =======================================================================
# Main batch entry point used by the Flask routes
# -----------------------------------------------------------------------
# Accepts N rows straight from the sheet. Validates every row first
# (never touching float() on bad data), runs ONE vectorised model call
# and ONE vectorised SHAP call across every valid row, and returns a
# result (or a clean per-row error) for EVERY row, in the SAME order
# they were submitted. A bad row never blocks the good rows around it,
# and this never raises for row-level problems — only for something
# truly unexpected, which the Flask route also catches.
# =======================================================================
def run_predictions_batch(rows: list, threshold: float = 0.5) -> list:
    if not isinstance(rows, list):
        raise ValidationError("Malformed request: expected a list of rows.")

    threshold = min(max(float(threshold), 0.0), 1.0)

    output = [None] * len(rows)
    valid_indices = []
    valid_cleaned = []

    for i, raw in enumerate(rows):
        row_id = raw.get("row_id", i) if isinstance(raw, dict) else i
        try:
            cleaned = validate_raw_input(raw)
        except ValidationError as e:
            output[i] = {"row_id": row_id, "ok": False, "error": str(e)}
            continue
        valid_indices.append(i)
        valid_cleaned.append(cleaned)

    if valid_cleaned:
        feature_matrix = build_feature_matrix(valid_cleaned)

        try:
            probabilities = _model.predict_proba(feature_matrix)[:, 1]
        except Exception:
            # The model itself rejected the batch (should not normally
            # happen once validation has passed) — fail those rows
            # cleanly instead of crashing the whole request.
            for idx in valid_indices:
                raw = rows[idx]
                row_id = raw.get("row_id", idx)
                output[idx] = {
                    "row_id": row_id,
                    "ok": False,
                    "error": "The model could not process this row. Please check the values and try again.",
                }
            return output

        explanations = explain_batch(feature_matrix)

        for j, idx in enumerate(valid_indices):
            raw = rows[idx]
            cleaned = valid_cleaned[j]
            row_id = raw.get("row_id", idx)
            proba = float(probabilities[j])
            result = _assemble_result(raw, cleaned, proba, threshold, explanations[j])
            output[idx] = {"row_id": row_id, "ok": True, "result": result}
            _PREDICTION_LOG.append(result)

    return output


def run_prediction(raw_input: dict, threshold: float = 0.5) -> dict:
    """Single-row convenience wrapper (kept for callers that only need
    one machine at a time). Raises ValidationError on bad input, same
    as the batch path — the Flask route turns that into a clean 400."""
    outcome = run_predictions_batch([raw_input], threshold=threshold)[0]
    if not outcome["ok"]:
        raise ValidationError(outcome["error"])
    return outcome["result"]


def get_recent_predictions(limit: int = 25) -> list:
    return list(reversed(_PREDICTION_LOG[-limit:]))


def get_dashboard_stats() -> dict:
    total = len(_PREDICTION_LOG)
    failures = sum(1 for r in _PREDICTION_LOG if r["is_failure"])
    healthy = total - failures
    avg_health = round(np.mean([r["health_score"] for r in _PREDICTION_LOG]), 1) if total else 0.0

    # Model accuracy is reported from the project's own held-out evaluation
    # set (data/processed), not fabricated — computed once at startup.
    model_accuracy = _reference_accuracy()

    return {
        "total_predictions": total,
        "healthy_machines": healthy,
        "failure_predictions": failures,
        "model_accuracy": model_accuracy,
        "avg_health_score": avg_health,
    }


def _reference_accuracy():
    if _y_test_reference is None:
        return None
    X = _X_test_reference[FEATURE_ORDER]
    preds = (_model.predict_proba(X)[:, 1] >= 0.5).astype(int)
    from sklearn.metrics import accuracy_score
    return round(float(accuracy_score(_y_test_reference, preds)) * 100, 2)


# =======================================================================
# Dataset-backed sample generation
# -----------------------------------------------------------------------
# Every sample and every generated row is pulled from the project's own
# held-out test set (data/processed/week4_X_test.csv) — real telemetry
# the model was evaluated on, never fabricated numbers. This also means
# generated rows are ALWAYS fully populated (no blank cells), so they
# can never trigger the empty-string bug.
# =======================================================================
def _next_machine_id() -> str:
    for _ in range(50):
        candidate = f"M-{random.randint(1000, 9999)}"
        if candidate not in _used_machine_ids:
            _used_machine_ids.add(candidate)
            return candidate
    # Extremely unlikely fallback if the random space is exhausted.
    candidate = f"M-{uuid.uuid4().hex[:6].upper()}"
    _used_machine_ids.add(candidate)
    return candidate


def _row_from_reference(row: pd.Series) -> dict:
    type_lookup = {v: k for k, v in TYPE_ENCODING.items()}
    return {
        "machine_id": _next_machine_id(),
        "machine_type": type_lookup.get(int(row["Type_enc"]), "M"),
        "air_temp_k": round(float(row["Air temperature [K]"]), 1),
        "process_temp_k": round(float(row["Process temperature [K]"]), 1),
        "rotational_speed_rpm": round(float(row["Rotational speed [rpm]"]), 0),
        "torque_nm": round(float(row["Torque [Nm]"]), 1),
        "tool_wear_min": round(float(row["Tool wear [min]"]), 0),
        "ambient_temp_c": round(float(row["ambient_temp_C"]), 1),
        "load_density_pct": round(float(row["load_density_pct"]), 1),
        "shift": random.choice(["Day", "Evening", "Night"]),
    }


def get_random_test_sample() -> dict:
    """Pull a single real row from the held-out test set (used by the
    'Random Machine' button)."""
    row = _X_test_reference.sample(1).iloc[0]
    return _row_from_reference(row)


def get_sample_rows(n: int) -> list:
    """Pull N real rows from the held-out test set (used by 'Generate
    Rows'). Always returns fully-populated rows — never blanks."""
    n = max(1, min(int(n), 200))
    pool_size = len(_X_test_reference)
    replace = n > pool_size
    idx = np.random.choice(pool_size, size=n, replace=replace)
    return [_row_from_reference(_X_test_reference.iloc[int(i)]) for i in idx]
