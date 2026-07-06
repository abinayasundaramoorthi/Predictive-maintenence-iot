
# WEEK 4: Noise Sensitivity Analysis and Threshold Tuning

## 4.1 Overview

Week 4 addressed real-world deployment challenges. Sensors drift, readings are noisy, and the default 0.5 decision threshold is rarely the right trade-off for an imbalanced maintenance problem. This week empirically characterised model robustness under synthetic sensor noise, plotted full Precision-Recall curves, and selected a deployment threshold using an explicit cost-of-failure argument.

---

## 4.2 Day 1 — A Genuine Held-Out Test Set

### 4.2.1 Why Not Reuse week3_final_model.joblib?

The Week 3 final model was deliberately fit on 100% of the data to maximise training signal. Testing its noise robustness on any subset of that same data would be testing on rows the model already memorised — the degradation numbers would be meaningless.

**Solution:** A fresh 80/20 stratified split. A separate evaluation model — same approach and hyperparameters as the Week 3 winner — was trained on the 80% only. The 20% held-out set remained completely unseen for all of Week 4's experiments.


# Train sizes verified:
# Train: 8000 rows, failure rate ~3.39%
# Test:  2000 rows, failure rate ~3.40%

eval_model = build_model(best_params, WINNING_APPROACH, y_train)
eval_model.fit(X_train, y_train)


### 4.2.2 Clean Baseline (No Noise)

The evaluation model was scored on the unmodified held-out test set. This is the reference line every noise level is compared against.

| Metric | Clean baseline |
|---|---|
| Recall | *(from week4_clean_baseline.csv)* |
| Precision | *(from week4_clean_baseline.csv)* |
| F1 | *(from week4_clean_baseline.csv)* |
| ROC-AUC | *(from week4_clean_baseline.csv)* |
| PR-AUC | *(from week4_clean_baseline.csv)* |

**Files saved:** `week4_eval_model.joblib`, `week4_X_test.csv`, `week4_y_test.csv`, `week4_clean_baseline.csv`

---

## 4.3 Day 2 — Synthetic Noise Injection

### 4.3.1 Design of the Noise Model

Gaussian noise was added to each continuous sensor feature, scaled to that feature's own standard deviation. This ensures the disturbance is proportionally comparable across sensors with very different physical ranges (e.g., temperature in Kelvin vs. torque in Nm).


> **Critical design constraint:** Noise was injected only into the held-out test set. The evaluation model was never retrained or modified. Any performance change is caused purely by noisier input — the only fair way to isolate the effect of sensor degradation.

### 4.3.2 Noise Sensitivity Results

> Fill in from `week4_noise_sensitivity.csv`

### 4.3.3 Reading the Sensitivity Curve

- **Flat lines** across noise levels: model decisions barely depend on small sensor fluctuations — genuinely robust signal
- **Steep early drop** (performance falls sharply at 5–10%): model leans on fine-grained precision that real-world drift would wipe out
- **Recall and precision dropping at different rates:** directly affects threshold selection in Day 4

**Files saved:** `week4_noise_sensitivity.csv`, `week4_noise_sensitivity.png`

### 4.3.4 Limitation

This noise model uses independent Gaussian noise per feature, which is a simplification. Real sensor degradation is often correlated across features (e.g., a failing thermocouple drifts steadily rather than jittering randomly). This experiment measures a reasonable first-order robustness signal, not a worst-case guarantee.

---

## 4.4 Day 3 — Precision-Recall Curves

### 4.4.1 Why PR Curves Instead of ROC?

ROC curves incorporate true negatives. With failures under 4% of the data, true negatives are so abundant that ROC curves appear near-perfect even when the model struggles with rare failure cases. Precision-Recall curves focus exclusively on the positive class — the appropriate tool for imbalanced maintenance classification.

### 4.4.2 What Was Plotted

- **Clean data PR curve:** full range of thresholds on the unmodified held-out test set
- **30%-noise PR curve:** same model, same thresholds, worst-case noise applied — overlaid on the same axes
- **Random baseline:** horizontal line at the dataset's failure rate (a model with no predictive power sits here)


### 4.4.3 Key Question

Does the noisy curve sit uniformly below the clean one (degradation across all thresholds), or only in a specific region? If the curves diverge most at high-recall settings, that is exactly where the threshold choice from Day 4 is riskiest under real-world noise.

**Files saved:** `week4_pr_curve_clean.csv`, `week4_pr_curve_noisy.csv`, `week4_pr_curves.png`

---

## 4.5 Day 4 — Cost-Based Threshold Selection

### 4.5.1 The Cost Trade-Off

The default 0.5 probability threshold treats false positives and false negatives as equally costly. In a predictive maintenance setting this is wrong:

| Error Type | Consequence | Relative Cost |
|---|---|---|
| **False Negative** (missed failure) | Unplanned downtime, emergency repair, safety risk | **HIGH** |
| **False Positive** (false alarm) | Unnecessary inspection, wasted crew time | LOW |

Because missing a failure costs far more than a false alarm, the optimal threshold is usually well **below** 0.5.

### 4.5.2 Method 1 — Target Recall

Find the lowest threshold on the clean-data PR curve that achieves ≥ 90% recall. Among all thresholds meeting that constraint, pick the one with the highest precision.

**Reasoning:** "We must catch at least 90% of real failures" is a directly interpretable commitment to the maintenance team, with the highest achievable precision at that recall level.

### 4.5.3 Method 2 — F-beta Score (β = 2)

Maximise an F-beta score that weights recall twice as heavily as precision. Used as a cross-check: if both methods produce similar thresholds, the choice is robust.

### 4.5.4 Final Chosen Threshold

> Default 0.5 threshold is shown below for comparison

### 4.5.5 Threshold Robustness Under Noise

The chosen threshold was applied **unchanged** to both clean and 30%-noise probability scores. In production you fix a threshold once — this table shows whether it holds up:

| Metric | Clean data | 30% noise |
|---|---|---|
| Recall | *(from week4_threshold_comparison.csv)* | *(from week4_threshold_comparison.csv)* |
| Precision | *(your result)* | *(your result)* |
| F1 | *(your result)* | *(your result)* |
| False alarms (FP) | *(your result)* | *(your result)* |
| Missed failures (FN) | *(your result)* | *(your result)* |

> If missed failures increase substantially under noise, this is a deployment risk worth flagging in the model documentation.

**Files saved:** `week4_threshold_decision.csv`, `week4_threshold_comparison.csv`

---

## 4.6 Day 5 — Documentation and GitHub

### 4.6.1 Deliverables Completed

| Deliverable | Description |
|---|---|
| `README.md` | Repository structure, reproduction steps, key engineering decisions, limitations |
| `week4_summary.md` | Per-week written results summary |
| `predict_new_data.py` | Standalone inference script — raw sensor CSV in, maintenance flags out |
| `index.html` | Project website — animated sensor waveform, pipeline overview, metrics, tech stack |

### 4.6.2 How to Run Predictions on New Data

Input CSV must have columns: `Type`, `Air temperature [K]`, `Process temperature [K]`, `Rotational speed [rpm]`, `Torque [Nm]`, `Tool wear [min]`, `timestamp`

> **Why use Week 3 model + Week 4 threshold together?**
> The Week 3 model was fit on 100% of data (best possible model). The Week 4 threshold was validated on genuinely unseen data (honest validation). Using either artifact alone misses one of these properties.

---

## 4.7 Files Produced — Week 4

| File | Description |
|---|---|
| `week4_eval_model.joblib` | Evaluation model — fit on 80% only for honest testing |
| `week4_X_test.csv` | Held-out test features — genuinely unseen during training |
| `week4_y_test.csv` | Held-out test labels |
| `week4_clean_baseline.csv` | Model metrics on the clean (no-noise) test set |
| `week4_noise_sensitivity.csv` | Recall / Precision / F1 / PR-AUC at each of 5 noise levels |
| `week4_noise_sensitivity.png` | Plot: metric scores vs. injected noise level |
| `week4_pr_curve_clean.csv` | Full PR curve data — clean condition |
| `week4_pr_curve_noisy.csv` | Full PR curve data — 30% noise condition |
| `week4_pr_curves.png` | Overlay plot: clean vs. noisy PR curves |
| `week4_threshold_decision.csv` | Chosen deployment threshold and method used |
| `week4_threshold_comparison.csv` | Recall / Precision / FP / FN — clean vs. 30% noise |
| `predict_new_data.py` | Production inference script for new sensor readings |
| `README.md` | Complete project documentation for the GitHub repository |
| `week4_noise_threshold_tuning.ipynb` | Full notebook — Days 1–5 |

---
---

# CONCLUSIONS

## Technical Achievements

| Area | What was done |
|---|---|
| **End-to-end pipeline** | Raw telemetry → data fusion → imbalanced classification → noise-tested, threshold-tuned deployment artifact |
| **Leakage prevention** | Three distinct leakage risks identified and mitigated across four weeks |
| **Statistical rigour** | Ablation study (Week 2) with paired t-test + Wilcoxon + Cohen's d; 5-fold stratified CV; dual threshold-selection methods |
| **Honest reporting** | Simulated external context and Gaussian noise model acknowledged as limitations throughout |

## Key Engineering Decisions

| Decision | Wrong approach | Correct approach |
|---|---|---|
| Failure-mode flags | Include TWF/HDF/PWF/OSF/RNF as features | Drop all five — they directly define the target |
| SMOTE in CV | Apply SMOTE before splitting | Chain inside imblearn Pipeline — resamples only training fold |
| Eval vs. deploy model | Reuse week3_final_model for Week 4 testing | Separate eval model on 80% split so 20% is genuinely unseen |
| Threshold selection | Default 0.5 | Cost-justified: target ≥90% recall, cross-checked with F-beta |

## Limitations

- External context (ambient temperature, load density) is **simulated**, not measured from real sensors
- Noise model uses **independent Gaussian** per feature; real sensor drift is often correlated and non-stationary
- Dataset is **synthetic** (AI4I was procedurally generated); failure patterns may not match a specific real machine type

## Deployment Usage

```bash
# Production prediction
python predict_new_data.py new_sensor_readings.csv

# Uses:
#   week3_final_model.joblib        — fit on 100% of historical data
#   week4_threshold_decision.csv    — validated on held-out, cost-justified
