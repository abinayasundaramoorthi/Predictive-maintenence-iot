
# 🔧 Predictive Maintenance System using Machine Learning (LightGBM)

## 📌 Project Objective
This project builds a machine learning-based predictive maintenance system that identifies machine failure using industrial sensor data. The system is designed as a **binary classification problem** to predict whether a machine will fail or not based on operational parameters.

The focus is on:
- Handling imbalanced datasets
- Building robust classification models
- Evaluating trade-offs between Recall, Precision, and F1-score
- Performing failure-level error analysis
- Selecting a model suitable for real-world deployment

---

# 🟢 Data Understanding & Evaluation Framework

## 📥 Data Loading & Schema Understanding

The dataset `fusion_pipeline_output_consolidated.csv` was loaded using pandas with timestamp parsing to preserve temporal structure.

```python
df = pd.read_csv("fusion_pipeline_output_consolidated.csv", parse_dates=["timestamp"])
````

### Technical Purpose:

* Ensures datetime consistency for potential time-based modeling
* Enables structured exploration of machine behavior over time

---

## 🔍 Exploratory Data Analysis (EDA)

The following checks were performed:

* Dataset shape inspection
* Column identification
* Data type validation
* Missing value analysis

### Technical Insight:

This step ensures:

* Data integrity before modeling
* Identification of preprocessing requirements
* Detection of incomplete or noisy features

---

## 🎯 Target Variable Analysis

Target column:

```python
Target
```

Operations performed:

* Frequency count of classes
* Normalized percentage distribution

### Technical Observation:

The dataset is **highly imbalanced**, meaning:

* Majority class = normal operation
* Minority class = failure cases

### ML Impact:

* Accuracy becomes unreliable
* Model bias toward majority class increases
* Requires stratified splitting + class-aware learning

---

## ⚖️ Evaluation Framework Design

A unified evaluation function was created:

```python
def evaluate_model(y_true, y_pred):
```

### Metrics Included:

* Accuracy → Overall correctness
* Precision → False alarm control
* Recall → Failure detection capability
* F1-score → Balanced performance metric
* Confusion Matrix → Error breakdown
* Classification Report → Full performance summary

### Engineering Purpose:

This ensures:

* Standardized model comparison
* Metric-driven decision-making
* Production-grade evaluation consistency

---

## 🧪 Train-Test Split Strategy

```python
train_test_split(..., stratify=y)
```

### Technical Reasoning:

Stratification ensures:

* Equal class distribution in train/test
* Prevents sampling bias
* Maintains real-world class ratio

---

# 🟡 Baseline Model & Feature Engineering

## 🧹 Feature Selection

Dropped columns:

* `timestamp`
* `Product ID`
* `UDI`
* `Failure Type`

### Technical Reason:

These are:

* Identifiers (non-predictive)
* Leakage-prone features
* Non-generalizable attributes

---

## 🔄 Categorical Encoding

```python
pd.get_dummies(X, columns=["Type", "shift"], drop_first=True)
```

### Technical Explanation:

* Converts categorical variables into numerical vectors
* Avoids multicollinearity using `drop_first=True`

---

## 🧼 Feature Sanitization

```python
re.sub(r"[^A-Za-z0-9_]+", "_", col)
```

### Purpose:

* Ensures feature names are LightGBM-compatible
* Removes special characters causing model errors

---

## 🤖 Baseline Model (LightGBM)

```python
LGBMClassifier(random_state=42)
```

### Why LightGBM:

* Gradient boosting framework
* Handles large datasets efficiently
* Built-in handling for feature interactions

---

## ⚖️ Class Imbalance Handling

### Weighted Model:

```python
class_weight="balanced"
```

### Technical Impact:

* Automatically increases weight for minority class
* Reduces bias toward majority class
* Improves recall without manual resampling

---

# 🟠 Model Optimization & Failure Analysis

## 🔬 Hyperparameter Optimization

GridSearchCV was used for tuning:

```python
param_grid = {
    "n_estimators": [100, 200],
    "max_depth": [3, 5, -1],
    "learning_rate": [0.05, 0.1]
}
```

### Optimization Strategy:

Two scoring functions were tested:

---

## 1. Recall-Optimized Model

```python
scoring="recall"
```

### Technical Goal:

Maximize detection of failure cases.

### Outcome:

* High Recall
* Low Precision
* Many false positives

### Interpretation:

Model becomes overly sensitive, flagging too many normal machines as failures.

---

## 2. F1-Optimized Model

```python
scoring="f1"
```

### Technical Goal:

Balance Precision and Recall.

### Outcome:

* Stable Recall
* High Precision
* Reduced false alarms

### Interpretation:

Best trade-off between safety and operational cost.

---

## 📊 Model Comparison Summary

| Model            | Recall   | Precision   | F1 Score     |
| ---------------- | -------- | ----------- | ------------ |
| Baseline         | Moderate | High        | Good         |
| Class Balanced   | Improved | Slight drop | Better       |
| Recall Optimized | Highest  | Low         | Poor balance |
| F1 Optimized     | Strong   | Strong      | Best         |

---

## 🏆 Final Model Selection

Selected Model:

```python
F1-Optimized LightGBM
```

### Technical Justification:

* Maintains strong recall
* Controls false positives
* Stable generalization performance
* Best suited for deployment

---

# 🔍 Failure Analysis (Error Engineering)

## False Positives (FP)

* Normal machines predicted as failure
* Leads to unnecessary maintenance cost

---

## False Negatives (FN)

* Actual failures missed by model
* High-risk operational failure

---

## Failure Type Breakdown

```python
value_counts()
```

### Key Observation:

Most missed failures belong to:

* **Tool Wear Failure**

### Technical Insight:

Model struggles with this failure subtype, indicating:

* Non-linear failure behavior
* Feature sensitivity limitations

---

## Feature Importance Analysis

Extracted from LightGBM:

* Sensor readings
* Operational metrics
* Tool wear parameters

### Purpose:

* Identify key predictive drivers
* Improve model interpretability

---

# 🏭 BUSINESS VIEW (FOR IT & OPERATIONS TEAM)

## 📌 Problem Statement (Business Context)

In industrial environments, unexpected machine failure leads to:

* Production downtime
* Revenue loss
* Maintenance inefficiency

---

## 🎯 What This System Does

This ML system predicts machine failure **before it happens**, enabling:

* Preventive maintenance scheduling
* Reduced machine downtime
* Optimized resource allocation

---

## ⚖️ Business Trade-off Analysis

| Error Type     | Business Impact                       |
| -------------- | ------------------------------------- |
| False Negative | Machine breakdown (high cost)         |
| False Positive | Unnecessary maintenance (medium cost) |

---

## 🏆 Why F1 Model is Selected

The F1-Optimized model was selected because:

* It balances failure detection and operational cost
* It avoids excessive false alarms
* It is stable for real-world deployment

---

## 📊 Business Value Delivered

✔ Reduced unexpected breakdown risk
✔ Improved maintenance planning
✔ Balanced cost vs safety optimization
✔ More reliable prediction system for operations team

---

## 🚀 Final Outcome

The system is production-aligned and provides:

* Predictive failure detection
* Interpretable model behavior
* Balanced operational decision-making support


