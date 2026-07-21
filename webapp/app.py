"""
webapp/app.py
--------------
Flask web dashboard for the IoT Predictive Maintenance project.

This is an ADDITIVE layer only. It does not modify, retrain, or
duplicate anything from the existing project — it imports and reuses
the existing model/config/inference logic through webapp/utils/api.py.

Run with:
    cd webapp
    python app.py

Then open http://127.0.0.1:5000 in a browser.
"""

import io
import csv
import logging
import os

from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    Response,
)

from utils import api

# ---------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------
app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
)
logger = logging.getLogger("webapp")

MODEL_NAME = "LightGBM Classifier"
DATASET_NAME = "AI4I 2020 Predictive Maintenance (contextually fused)"
APP_VERSION = "1.1.0"

MAX_ROWS_PER_REQUEST = 500
MAX_GENERATE_ROWS = 200


def _safe_threshold(value, default=0.5):
    """Never lets a bad threshold value reach the model layer."""
    try:
        t = float(value)
    except (TypeError, ValueError):
        return default
    if t != t:  # NaN
        return default
    return min(max(t, 0.0), 1.0)


# ---------------------------------------------------------------------
# Page routes
# ---------------------------------------------------------------------
@app.route("/")
def dashboard():
    stats = api.get_dashboard_stats()
    recent = api.get_recent_predictions(limit=8)
    return render_template(
        "index.html",
        stats=stats,
        recent=recent,
        active_page="dashboard",
    )


@app.route("/prediction")
def prediction_page():
    return render_template("prediction.html", active_page="prediction")


@app.route("/reports")
def reports_page():
    recent = api.get_recent_predictions(limit=200)
    return render_template("reports.html", recent=recent, active_page="reports")


@app.route("/model-info")
def model_info_page():
    stats = api.get_dashboard_stats()
    return render_template(
        "model_info.html",
        stats=stats,
        model_name=MODEL_NAME,
        dataset_name=DATASET_NAME,
        feature_order=api.FEATURE_ORDER,
        active_page="model-info",
    )


@app.route("/about")
def about_page():
    return render_template(
        "about.html",
        model_name=MODEL_NAME,
        dataset_name=DATASET_NAME,
        version=APP_VERSION,
        active_page="about",
    )


# ---------------------------------------------------------------------
# API routes
# ---------------------------------------------------------------------
@app.route("/api/predict", methods=["POST"])
def api_predict():
    """Single-row prediction. Kept for compatibility; the sheet UI uses
    /api/predict-batch instead so N machines resolve in one round trip."""
    payload = request.get_json(force=True, silent=True)
    if not isinstance(payload, dict):
        return jsonify({"ok": False, "error": "Invalid request format."}), 400

    threshold = _safe_threshold(payload.get("threshold"))
    payload.setdefault("row_id", 0)

    try:
        outcome = api.run_predictions_batch([payload], threshold=threshold)[0]
    except Exception:
        logger.exception("Prediction failed")
        return jsonify({"ok": False, "error": "Internal error while running the model. Please try again."}), 500

    if outcome["ok"]:
        return jsonify({"ok": True, "result": outcome["result"]})
    return jsonify({"ok": False, "error": outcome["error"]}), 400


@app.route("/api/predict-batch", methods=["POST"])
def api_predict_batch():
    """
    Predict an entire sheet of machines in one request.

    Every row is validated independently — a blank or invalid cell in
    one row never blocks, resets, or crashes the prediction of any
    other row. Model inference and SHAP explanation are each computed
    once, vectorised across the whole sheet, so this scales cleanly to
    5, 10, 20, or 50+ rows without the per-row overhead of separate
    HTTP calls.
    """
    payload = request.get_json(force=True, silent=True)
    if not isinstance(payload, dict):
        return jsonify({"ok": False, "error": "Invalid request format."}), 400

    rows = payload.get("rows")
    if not isinstance(rows, list) or len(rows) == 0:
        return jsonify({"ok": False, "error": "No machine rows were submitted."}), 400
    if len(rows) > MAX_ROWS_PER_REQUEST:
        return jsonify({"ok": False, "error": f"Too many rows in a single request (limit {MAX_ROWS_PER_REQUEST})."}), 400

    threshold = _safe_threshold(payload.get("threshold"))

    try:
        results = api.run_predictions_batch(rows, threshold=threshold)
    except Exception:
        logger.exception("Batch prediction failed")
        return jsonify({"ok": False, "error": "Internal error while running the model. Please try again."}), 500

    return jsonify({"ok": True, "results": results})


@app.route("/api/sample/<kind>")
def api_sample(kind):
    try:
        if kind == "healthy":
            sample = {
                "machine_id": "M-HEALTHY-DEMO",
                "air_temp_k": 300.5,
                "process_temp_k": 309.8,
                "rotational_speed_rpm": 1345,
                "torque_nm": 62.7,
                "tool_wear_min": 153,
                "machine_type": "L",
                "ambient_temp_c": 24.5,
                "load_density_pct": 30.0,
                "shift": "Day",
            }
        elif kind == "failure":
            sample = {
                "machine_id": "M-FAILURE-DEMO",
                "air_temp_k": 303.7,
                "process_temp_k": 312.1,
                "rotational_speed_rpm": 1363,
                "torque_nm": 51.8,
                "tool_wear_min": 220,
                "machine_type": "L",
                "ambient_temp_c": 29.5,
                "load_density_pct": 34.1,
                "shift": "Night",
            }
        elif kind == "random":
            sample = api.get_random_test_sample()
        else:
            return jsonify({"ok": False, "error": "Unknown sample kind"}), 400

        return jsonify({"ok": True, "sample": sample})
    except Exception:
        logger.exception("Sample loading failed")
        return jsonify({"ok": False, "error": "Could not load sample."}), 500


@app.route("/api/generate-rows/<int:n>")
def api_generate_rows(n):
    """Bulk-generate N fully-populated rows sourced from the project's
    own held-out test set — real telemetry, never fabricated, and
    never blank (so it can never trigger a validation error)."""
    try:
        n = max(1, min(n, MAX_GENERATE_ROWS))
        rows = api.get_sample_rows(n)
        return jsonify({"ok": True, "rows": rows})
    except Exception:
        logger.exception("Row generation failed")
        return jsonify({"ok": False, "error": "Could not generate sample rows."}), 500


@app.route("/api/stats")
def api_stats():
    return jsonify({"ok": True, "stats": api.get_dashboard_stats()})


@app.route("/api/recent")
def api_recent():
    limit = int(request.args.get("limit", 25))
    return jsonify({"ok": True, "recent": api.get_recent_predictions(limit=limit)})


@app.route("/api/export/csv")
def export_csv():
    recent = api.get_recent_predictions(limit=1000)
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(
        ["Machine ID", "Status", "Failure Probability (%)", "Health Score",
         "Confidence (%)", "Failure Mode", "Timestamp"]
    )
    for r in recent:
        writer.writerow([
            r["machine_id"], r["status"], r["failure_probability"],
            r["health_score"], r["confidence"], r["failure_mode"]["failure_type"],
            r["timestamp"],
        ])

    return Response(
        buffer.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=predictions_export.csv"},
    )


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html", active_page=""), 404


@app.errorhandler(500)
def internal_error(e):
    """Final safety net: no matter what goes wrong, the user never sees
    a Python traceback — API callers get clean JSON, page loads get a
    friendly error page. Full details are always logged server-side."""
    logger.exception("Unhandled server error")
    if request.path.startswith("/api/"):
        return jsonify({"ok": False, "error": "Internal server error. Please try again."}), 500
    return render_template("404.html", active_page=""), 500


if __name__ == "__main__":
    logger.info("Starting Predictive Maintenance dashboard on http://127.0.0.1:5000")
    app.run(debug=False, host="127.0.0.1", port=5000)
