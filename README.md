# IoT Predictive Maintenance — Contextual Failure Prediction System

An end-to-end machine learning system that predicts industrial machine failures from IoT sensor telemetry, engineered to handle severe class imbalance and remain robust under noisy real-world conditions.

---

## 👥 Team Members

* Abinaya S (Team Leader)
* Himanshu Rawat
* Nagammai Subramaniyan
* N. Yogeshwaran

---

## 📌 Problem Statement

Industrial IoT machines continuously generate high-frequency sensor data — temperature, rotational speed, torque, tool wear, and vibration signals. In real-world operations, machine failures are rare but costly: they occur unpredictably, disrupt production schedules, and are expensive to diagnose after the fact.

Traditional reactive maintenance ("fix it when it breaks") leads to unplanned downtime and inflated repair costs. A predictive system that flags an impending failure *before* it happens allows maintenance teams to intervene proactively, minimizing both downtime and unnecessary inspections.

---

## 🎯 Objective

* Predict machine failure from sensor and contextual data using supervised machine learning.
* Optimize for **recall on the minority (failure) class**, since missed failures are far more costly than false alarms in an industrial setting.
* Select a **decision threshold** deliberately, rather than defaulting to 0.5, to balance false alarms against missed maintenance windows.
* Ensure the model remains reliable when sensor readings are noisy — a realistic condition in deployed IoT environments.

---

## 🧩 Solution Overview

The system is built as a sequential pipeline, moving from raw sensor data to a deployable inference layer:

1. **Data Ingestion** — Raw industrial sensor logs (e.g. AI4I-style predictive maintenance data) are ingested for processing.
2. **Preprocessing** — Cleaning, type handling, and consolidation of raw sensor readings.
3. **Feature Engineering** — Derived features from sensor signals (e.g. temperature differentials, load-adjusted torque, wear ratios) to give the model more predictive signal than raw readings alone.
4. **Context Fusion** — External/environmental context (ambient temperature, load density) is fused with internal telemetry to capture factors that influence failure beyond the machine's internal state.
5. **Class Imbalance Handling (SMOTE)** — Since failures are a small minority of the dataset, SMOTE is applied **strictly within training folds** during cross-validation to avoid data leakage into validation/test sets.
6. **Model Training (LightGBM)** — A gradient-boosted tree classifier is trained on the engineered feature set, chosen for its strong performance on tabular, imbalanced data.
7. **Cross-Validation** — Model performance is validated using a stratified cross-validation strategy to ensure stable, generalizable results across folds.
8. **Threshold Tuning** — Instead of using the default 0.5 cutoff, the decision threshold is tuned using precision-recall analysis to reflect the real cost tradeoff between false alarms and missed failures.
9. **Noise Robustness Evaluation** — The model is stress-tested against synthetically injected sensor noise to verify it holds up under imperfect, real-world data conditions.
10. **Model Serialization** — The final trained model is serialized (`.joblib`) for reuse without retraining.
11. **Inference Pipeline** — A standalone runnable script (`app.py`) loads the trained model and serves predictions on new/test data.

---

## 🔬 Machine Learning Pipeline

| Stage | Description |
|---|---|
| **EDA** | Exploratory analysis of sensor distributions, correlations, and failure patterns across machine types. |
| **Feature Engineering** | Construction of derived sensor features and contextual variables to improve separability between healthy and failing states. |
| **Model Training** | LightGBM classifier trained on the engineered, fused dataset. |
| **Evaluation Metrics** | **Macro F1**, Precision, and Recall are used as primary evaluation metrics, given the class imbalance. |
| **Hyperparameter Tuning** | Model hyperparameters (tree depth, learning rate, number of leaves, class weighting) tuned to improve minority-class detection. |
| **Threshold Optimization** | Precision-recall tradeoff analysis used to select an operating threshold aligned with maintenance decision costs, rather than the default 0.5. |

---

## ⭐ Key Features of This Project

* ✅ **SMOTE applied inside cross-validation folds only** — prevents synthetic oversampling from leaking information into validation data.
* ✅ **LightGBM classifier** — efficient gradient boosting suited to structured/tabular sensor data.
* ✅ **Precision-recall based threshold tuning** — decision threshold is chosen deliberately, not defaulted.
* ✅ **Noise robustness testing** — model behavior evaluated under injected sensor noise to simulate real deployment conditions.
* ✅ **Modular, reproducible pipeline** — clearly separated stages from raw data to inference, mirroring a production ML workflow.
* ✅ **Standalone inference layer** — `app.py` and `config.py` provide a clean, dependency-light way to run the trained model without touching the training/research code.

---

## 🛠️ Tech Stack

* **Python**
* **Pandas** — data manipulation
* **NumPy** — numerical computation
* **Scikit-learn** — cross-validation, evaluation metrics
* **LightGBM** — gradient boosting classifier
* **Matplotlib** — visualization (precision-recall curves, threshold analysis, distributions)
* **Joblib** — model serialization

---

## 📊 Model Performance

Model performance is evaluated primarily using **Macro F1 score**, which balances performance across both the majority (healthy) and minority (failure) classes — a more meaningful metric than raw accuracy given the class imbalance in industrial failure data.

* **Primary metric:** Macro F1
* **Threshold selection:** Chosen from precision-recall tradeoff analysis to favor stability of F1 across a range of plausible operating points, rather than a fixed 0.5 cutoff.
* **Secondary evaluation:** Model behavior under injected noise was assessed to confirm predictions remain stable and reliable outside idealized clean-data conditions.

*(Exact metric values are available in the `results/metrics/` directory from the actual evaluation runs — refer to those artifacts for specific figures.)*

---

## 📁 Project Structure

```
demo mimic pm proj/
│
├── data/
│   ├── raw/            # Original, unprocessed sensor datasets
│   └── processed/      # Cleaned, feature-engineered, and fused datasets
│
├── notebooks/
│   ├── 01_eda/                        # Exploratory data analysis
│   ├── 02_feature_engineering/        # Feature construction and validation
│   ├── 03_context_fusion/             # External context integration
│   ├── 04_modeling/                   # Model training, SMOTE, cross-validation
│   ├── 05_evaluation/                 # Model evaluation and health scoring
│   ├── 06_threshold_tuning/           # Precision-recall based threshold selection
│   └── 07_noise_robustness/           # Noise sensitivity analysis
│
├── results/
│   ├── metrics/         # Evaluation metrics, trained model artifacts (.joblib)
│   ├── models/          # Additional serialized model files
│   └── plots/           # Generated visualizations (confusion matrices, PR curves, etc.)
│
├── docs/
│   └── reports_weekly/  # Weekly progress reports from all team members
│
├── app.py               # Inference entry point
├── config.py             # Centralized path and configuration settings
├── run_pipeline.py       # CLI wrapper for a full demo inference run
├── requirements.txt      # Inference dependencies
└── README.md
```

---

## ▶️ How to Run the Project

**1. Install dependencies**
```bash
pip install -r requirements.txt
```

**2. Run inference**
```bash
python app.py
```

**Optional — custom threshold or sample size:**
```bash
python app.py --threshold 0.35 --rows 20
```

**Optional — run the full demo pipeline with step-by-step output:**
```bash
python run_pipeline.py
```

**Expected output:** the script loads the trained model and test dataset, runs inference, and prints failure probabilities alongside classified predictions (e.g. `Healthy` / `Failure Risk`) for sample rows, plus summary evaluation metrics.

---

## ⚙️ Inference System

`app.py` is the production-facing entry point of this project:

1. Loads the trained LightGBM model from `results/metrics/`.
2. Loads the held-out test dataset from `data/processed/`.
3. Runs `predict_proba` to generate failure probabilities for each sample.
4. Applies a configurable decision threshold (default `0.5`) to classify each sample as **Healthy** or **Failure Risk**.
5. Prints a clean summary of predictions, along with sample-level failure probabilities.

All paths and configuration values are centralized in `config.py`, keeping the inference layer independent from the research/training notebooks.

---

## 🌍 Real-World Impact

* **Reduces unplanned machine downtime** by flagging failure risk ahead of time.
* **Improves maintenance scheduling** by shifting from reactive to proactive servicing.
* **Lowers operational costs** associated with emergency repairs and production halts.
* **Applicable across manufacturing and industrial IoT settings** where sensor telemetry is already being collected but not yet used predictively.

---

## 🚀 Future Improvements

* **Streamlit dashboard** for interactive, non-technical exploration of predictions and failure probabilities.
* **Real-time sensor streaming integration** to move from batch inference to continuous monitoring.
* **Automated model retraining pipeline** (MLOps extension) to keep the model current as new failure data accumulates.
* **Containerized deployment using Docker** for consistent, portable deployment across environments.


