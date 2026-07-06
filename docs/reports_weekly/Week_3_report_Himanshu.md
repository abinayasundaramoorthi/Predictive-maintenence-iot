
# WEEK 3: Imbalanced Classification and LightGBM Modeling

## 3.1 Overview

Week 3 addressed the central challenge of predictive maintenance classification: machine failures represent fewer than 4% of all sensor readings in the AI4I 2020 dataset. A naïve model that always predicts "no failure" achieves over 96% accuracy while catching zero real failures — making accuracy an entirely useless metric for this problem.

This week built a rigorous pipeline to handle class imbalance and deliver a LightGBM model evaluated by the metrics that actually matter for maintenance operations: **Recall**, **F1**, **ROC-AUC**, and **PR-AUC**.

---

## 3.2 Day 1 — Proving the Metric Trap

Before any modeling, the imbalance problem was demonstrated concretely using a `DummyClassifier` set to always predict the majority class ("no failure").

### Result

| Metric | Dummy Classifier |
|---|---|
| Accuracy | ~96.6% |
| Recall (failures caught) | **0.0%** |
| F1 Score | **0.0%** |
| Practical use | Zero — catches no failures |

> **Key insight:** Accuracy is a misleading metric for imbalanced problems. A model scoring >96% accuracy can be completely useless for catching real machine failures. All evaluation in Week 3 uses Recall, F1, ROC-AUC, and PR-AUC instead.

### Libraries Installed
```
lightgbm
imbalanced-learn
```

---

## 3.3 Day 2 — Leakage-Aware Features and CV Skeleton

### 3.3.1 The Leakage Risk

The AI4I dataset contains five failure-mode indicator columns:

| Column | Failure Mode |
|---|---|
| TWF | Tool Wear Failure |
| HDF | Heat Dissipation Failure |
| PWF | Power Failure |
| OSF | Overstrain Failure |
| RNF | Random Failure |

These columns **directly define** the target (`Machine failure = 1` when any of them equals 1). Including them as features lets the model read the answer off the input — producing artificially perfect scores that collapse to zero in deployment.

**Action taken:** All five failure-mode flags dropped before any model sees the data.

**Final feature set (11 features):**
- `Type_enc` (label-encoded product quality variant)
- `Air temperature [K]`
- `Process temperature [K]`
- `Rotational speed [rpm]`
- `Torque [Nm]`
- `Tool wear [min]`
- `ambient_temp_K` *(Week 2 engineered)*
- `load_density_pct` *(Week 2 engineered)*
- `temp_differential_K` *(Week 2 engineered)*
- `load_adjusted_torque` *(Week 2 engineered)*
- `wear_per_load` *(Week 2 engineered)*

### 3.3.2 Why Stratified K-Fold

With failures below 4% of rows, a plain random split can place very few — or even zero — failure cases into a fold by chance. `StratifiedKFold` forces each fold to maintain approximately the same failure rate as the full dataset.

```python
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# Each fold verified:
# Fold 1: 2000 rows, failure rate ~3.39%
# Fold 2: 2000 rows, failure rate ~3.40%
# ... consistent across all 5 folds
```

### 3.3.3 Baseline — No Resampling

A plain `LGBMClassifier` (no oversampling, no class weighting) was evaluated across all 5 folds. This is the "before" number that SMOTE and class-weighting must beat.

**Output saved to:** `week3_baseline_cv_results.csv`

---

## 3.4 Day 3 — SMOTE Inside the CV Loop (The Right Way)

### 3.4.1 The Leakage Trap with SMOTE

A common mistake is applying SMOTE to the full dataset before cross-validation. Synthetic minority-class samples generated from the full dataset use information from rows that end up in the test fold — the model indirectly previews test data, inflating recall scores in a way that will not hold in production.

| Approach | Correct? |
|---|---|
| `SMOTE(full dataset)` → `StratifiedKFold` → train/test |
| `StratifiedKFold` → (per fold) `imblearn Pipeline: SMOTE on train fold only` → LightGBM |

### 3.4.2 Implementation

The `imblearn` Pipeline enforces the correct behaviour automatically. During `.fit()` it resamples only the training fold passed in. During `.predict_proba()` it skips resampling entirely — the test fold is never touched by SMOTE.

**Output saved to:** `week3_smote_cv_results.csv`

---

## 3.5 Day 4 — Three-Way Comparison and Hyperparameter Tuning

### 3.5.1 scale_pos_weight vs. SMOTE

LightGBM provides a built-in mechanism — `scale_pos_weight` — that adjusts the loss function to penalise minority-class mistakes more heavily, without generating any synthetic data.

| Mechanism | What it changes | When to use |
|---|---|---|
| SMOTE | The **data** — synthetic failure rows added | When you want balanced training set size |
| `scale_pos_weight` | The **loss function** — each failure weighted more | Simpler, no synthetic data risk |
| Both together 

`scale_pos_weight` was computed **from the training fold only** (not the full dataset) to avoid leaking test-set class balance information
### 3.5.2 Three-Way Comparison

All three approaches evaluated on the **same identical folds** (same `cv` object, `random_state=42`):



### 3.5.3 Hyperparameter Sweep


### 3.6.1 Aggregated Confusion Matrix

Rather than fitting and testing on the same data, the confusion matrix was aggregated across all 5 CV folds. Every row in the dataset is used as a test point exactly once, by a model that never saw it during training — keeping the counts honest.

```
                  Predicted: No Failure   Predicted: Failure
Actual: No Failure        TN                    FP  (false alarm)
Actual: Failure           FN  (missed!)          TP
```

> The most operationally critical cell is **FN** (bottom-left) — these are missed maintenance windows that lead to unplanned downtime.

*Note: This confusion matrix uses the default 0.5 threshold. Deliberate threshold selection was the focus of Week 4.*

**Plot saved to:** `week3_confusion_matrix.png`

### 3.6 Saving the Deployment Model

The final model was fit on **100% of the fused dataset** — maximum possible training signal for deployment.

```python
import joblib

final_model = build_model(best_params, WINNING_APPROACH, y)
final_model.fit(X, y)
joblib.dump(final_model, "week3_final_model.joblib")
```

---

## 3.7 Files Produced — Week 3

| File | Description |
|---|---|
| `week3_baseline_cv_results.csv` | 5-fold CV metrics for plain LightGBM (no resampling) |
| `week3_smote_cv_results.csv` | 5-fold CV metrics for SMOTE + LightGBM pipeline |
| `week3_hyperparameter_tuning_results.csv` | Results of the 3-configuration hyperparameter sweep |
| `week3_final_model_cv_results.csv` | 5-fold CV metrics for the winning tuned model |
| `week3_confusion_matrix.png` | Aggregated confusion matrix across all 5 folds |
| `week3_final_model.joblib` | Deployment model — fit on 100% of the fused dataset |
| `week3_summary.md` | Written methodology and results summary |
| `week3_imbalanced_classification_lightgbm.ipynb` | Full notebook — Days 1–5 |

