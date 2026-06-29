# Predictive Maintenance - IoT Dataset

## Day 1 EDA Observations

1. Dataset loaded successfully with 10,000 rows and 10 columns.
2. No null values found in any column.
3. Target variable is Machine Failure (0 = No Failure, 1 = Failure).
4. Only 3.4% of machines failed - dataset is imbalanced.
5. Rolling mean, standard deviation and variance added for all 5 sensor columns.
6. 15 new features created - total columns increased from 10 to 25.
7. After dropna, dataset reduced to 9992 rows.
8. Train test split done - 7993 train samples, 1999 test samples.

## Day 2 Observations

1. Correlation heatmap shows Air temp and Process temp are strongly related (0.88).
2. Rotational speed and Torque are negatively correlated (-0.88).
3. Target column has very low correlation with all features.
4. Class imbalance found - only 3.4% machine failures (339 out of 10000).
5. New features added - temp_difference, power and tool_wear_rate.
6. temp_difference shows heat gap between environment and machine.
7. Power feature combines speed and torque to show machine load.
8. tool_wear_rate shows how fast tool is getting damaged.

## Day 3 Observations

1. Outlier detection done using boxplots for all 5 sensor columns.
2. Air temperature, Process temperature and Tool wear have no outliers - stable readings.
3. Rotational speed has outliers on the higher side - some machines spin too fast.
4. Torque has outliers on both sides - some machines underloaded or overloaded.
5. Label encoding applied on Type column - L=0, M=1, H=2.
6. New feature heat_stress_index created - Air temperature multiplied by Tool wear.
7. New feature speed_torque_ratio created - Rotational speed divided by Torque.
8. New feature wear_per_rotation created - Tool wear divided by Rotational speed, scaled by 1000.

## Day 4 - Feature Importance & Explainability

1. Recreated all 12 selected features from Day 2.
2. Retrained LightGBM model - confirmed Macro F1: 0.899.
3. Task 1 - Feature Importance Ranking:
   - Most important: Rotational speed (392)
   - 2nd: power (380)
   - 3rd: Torque (352)
   - 4th: Tool wear (312)
   - Least important: wear_per_rotation (0)
4. Task 2 - SHAP Analysis:
   - Used TreeExplainer to explain model predictions
   - SHAP summary plot saved as shap_summary.png
   - Shows which features push prediction towards failure or no failure
5. Task 3 - Fusion Feature Impact:
   - Original sensors importance: 1559 (52.0%)
   - Engineered features importance: 1441 (48.0%)
   - Engineered features contribute 48% of model decisions!
6. Task 4 - Business Interpretation:
   - Top 3 failure indicators: Rotational speed, Power, Torque
   - High power = machine overloaded = failure risk
   - Unusual speed/torque = machine struggling = failure risk
   - LightGBM achieves 0.899 Macro F1 - production ready!
7. Feature importance chart saved as feature_importance.png

## Day 5 - Feature Engineering + LightGBM Final Report

1. Feature Selection Summary:
   - Total original columns: 10
   - Total engineered features created: 11
   - Features removed (weak): 4
   - Final features selected: 12

2. Feature Importance Report:
   - Most important: Rotational speed (392)
   - 2nd: power (380)
   - 3rd: Torque (352)
   - Least important: wear_per_rotation (0)

3. Final Model Performance:
   - LightGBM Macro F1: 0.899
   - Logistic Regression (Week 2): 0.693
   - Improvement: 0.206 (29.8% better!)

4. Key Insights:
   - Engineered features contribute 48% of model decisions
   - LightGBM is production ready with 0.899 Macro F1
# Contextual Predictive Maintenance (IoT Edge AI)
## Project Report — Weeks 1 & 2

---

### Team

| Role | Name |
|---|---|
| Member 1 | Himanshu Rawat |
| Member 2 | N. Yogeshwaran |
| Member 3 | Nagammai Subramaniyan |
| Member 4 (Team Leader) | Abinaya S |

---

## 1. Project Vision

A machine rarely fails in isolation. Internal sensor readings — temperature,
torque, rotational speed, tool wear — tell part of the story, but the conditions
surrounding the machine, such as ambient temperature, operational load, and
shift timing, may explain the rest.

The guiding question behind this project is:

> **Does incorporating external, contextual information meaningfully improve
> failure prediction, or is internal sensor data alone sufficient?**

Week 1 of the project establishes a rigorous, ground-truth understanding of the
internal sensor data on its own. Week 2 introduces external contextual variables
and tests their value through a controlled **ablation study** — comparing
identical models trained with and without context — so that the answer is backed
by evidence rather than assumption.

The most consequential finding from Week 1, which shapes every methodological
decision afterward, is the dataset's **severe class imbalance**: only 339 of
10,000 records (3.39%) represent actual failures. This is why the team adopts
Precision, Recall, F1, and ROC-AUC as the primary evaluation metrics rather than
raw accuracy — a model that never predicts failure would still score
approximately 96.6% accuracy while providing zero operational value.

---

## 2. Week 1 — Exploratory Data Analysis & Feature Foundation

### 2.1 Dataset Understanding

The dataset (10,000 records) was loaded and profiled for structure, data types,
and completeness. The target variable's class distribution was examined first,
before any other analysis — establishing the 3.39% failure rate as the defining
constraint for the entire project's modeling strategy.

### 2.2 Sensor Distribution Analysis

Each core sensor — Air Temperature, Process Temperature, Rotational Speed,
Torque, and Tool Wear — was analyzed individually through histograms and
descriptive statistics. Each variable exhibits a distinct shape: temperature
readings are narrow and centered, rotational speed carries a long right tail,
and tool wear is approximately uniform across its 0–250 minute range. This
shaped how outliers and failure signals were later interpreted for each
variable independently.

### 2.3 Outlier Characterization

A reusable Interquartile Range (IQR) methodology was applied across Temperature,
Torque, and Rotational Speed to identify statistical outliers. Critically, in a
predictive maintenance context, outliers are not treated as data errors to be
removed — an unusually high torque or temperature reading may itself be the
failure signal. Outliers were quantified and retained for downstream modeling
rather than discarded.

### 2.4 Correlation & Feature Significance

A full correlation analysis ranked every sensor variable against the failure
target. **Torque and Tool Wear emerged as the strongest sensor-level predictors
of failure**, while temperature variables showed comparatively weak association
(peak correlation approximately 0.19). This finding directly informed feature
prioritization for all subsequent modeling work.

### 2.5 Feature Engineering

Building on the above, the team engineered an extensive feature set:

- **Rolling statistics** (mean, standard deviation, variance; window size 5)
  across all five core sensors — 15 new features.
- **Derived mechanical features:** `temp_difference`, `power` (rotational speed
  × torque), `tool_wear_rate`, `heat_stress_index`, `speed_torque_ratio`,
  `wear_per_rotation`.
- **Categorical encoding** of machine `Type` (Low / Medium / High) for downstream
  modeling compatibility.

Notable inter-sensor relationships were also identified: Air Temperature and
Process Temperature correlate strongly (0.88), as do Rotational Speed and Torque
(−0.88) — both consistent with expected mechanical behavior.

### 2.6 Week 1 Consolidation

All Week 1 analyses — class distribution, sensor profiling, outlier detection,
and correlation ranking — were consolidated into a single, reviewable pipeline,
confirming completion of every planned exploratory task ahead of contextual
analysis in Week 2.

---

## 3. Week 2 — Contextual Data Fusion & Ablation Study

### 3.1 Contextual Exploration

The team introduced machine `Type` as a contextual (non-sensor) variable and
examined its relationship to failure, alongside a review of whether time-based
or seasonal analysis was feasible. No native timestamp existed in the source
data, so this was addressed explicitly before deeper context work proceeded.

### 3.2 Context-to-Sensor Relationship Analysis

Machine Type was encoded numerically and cross-correlated against both the
failure target and the core sensor variables. **Machine Type showed only a weak
correlation with failure** — an early indicator, later reinforced by the formal
ablation results, that this particular contextual variable carries limited
standalone predictive value.

### 3.3 Context Impact Study

Sensor distributions (Air Temperature, Process Temperature, Torque, Tool Wear)
were compared directly between failed and non-failed machines, alongside a
failure-rate breakdown by machine Type. This confirmed visually what the
correlation analysis suggested numerically: **Torque and Tool Wear show the
clearest separation between failure and non-failure cases**, while Temperature
and Type show only mild differentiation.

### 3.4 External Context Research & Variable Design

To ground the project's simulated contextual variables in realistic industrial
behavior, dedicated research was conducted into:

- **Ambient temperature** — its effect on lubrication viscosity, thermal stress,
  and bearing degradation, with realistic ranges defined by environment type.
- **Operational load density** — categorized from Idle through Peak/Overload,
  based on the principle that sustained high load increases mechanical stress
  and prevents thermal recovery between operating cycles.
- **Engineered interaction features** — including temperature differential and
  load-adjusted torque, designed to capture combined effects rather than
  isolated variables.

This research directly informed which contextual variables were simulated and
how they were expected to relate to specific failure modes (e.g., load-related
features were hypothesized to matter most for power and overstrain failures;
ambient temperature for heat dissipation failures).

### 3.5 Ablation Study Design

A controlled experiment was designed to formally test the project's central
question:

- **Experiment A (Baseline):** model trained on core sensor features only.
- **Experiment B (Context-Enriched):** identical model trained on sensor
  features plus engineered contextual features.

Both experiments used an identical stratified train/test split — preserving the
rare-failure ratio in both partitions — and an identical model architecture,
ensuring that any difference in outcome is attributable solely to the addition
of contextual features.

### 3.6 Ablation Study Findings

Multiple independent runs of this experiment were conducted across the team's
work. **The results are not yet fully consistent and represent the most
important open item from Week 2:**

- One implementation, using a more rigorous cross-validated significance-testing
  approach (paired statistical testing across repeated folds), was designed to
  determine whether any improvement is statistically real or attributable to
  chance — this analysis is built but not yet finalized with a reported
  conclusion.
- A second implementation showed a **small positive improvement** in Macro F1
  (approximately +0.014 to +0.019) when contextual and engineered features were
  added.
- A third independent analysis showed the opposite: **every evaluation metric
  decreased** when the contextual feature was added, including Recall and F1 —
  the two metrics most relevant given the project's class imbalance.

**Conclusion for this review:** the current evidence is mixed and does not yet
support a confident claim in either direction. The effect of contextual features
on model performance is small in magnitude and inconsistent in direction across
independent implementations. This should be resolved through a single,
standardized re-run — using one fixed feature definition, one fixed random seed,
and the statistical significance test already designed — before contextual
features are treated as validated for production modeling in Week 3.

---

## 4. Methodological Notes

- **Two distinct context-fusion approaches were independently developed** within
  the team: one using time-indexed asynchronous merging (matching sensor
  readings to the nearest available external reading in time, simulating a
  realistic multi-source data environment), and one using direct row-aligned
  synthetic context assignment. Both are methodologically valid; the
  asynchronous approach more closely mirrors real-world deployment conditions.
- **Target column naming requires standardization.** Different components of the
  pipeline currently reference the failure target under different column names.
  This should be reconciled before Week 3 modeling work integrates outputs
  across the team.
- **All contextual variables used to date are simulated, not measured.** This is
  appropriate for validating pipeline mechanics and methodology, but it is the
  most plausible explanation for the inconclusive ablation results above —
  synthetic variables generated independently of the failure target inherently
  carry limited real predictive signal. This caveat should accompany all
  downstream results until genuine external data sources are integrated.

---

## 5. Summary & Recommendation

Week 1 delivered a complete, internally consistent foundation: sensor behavior,
outlier characteristics, and correlation structure all converge on the same
conclusion — **Torque and Tool Wear are the dominant failure indicators**, the
dataset is **severely imbalanced**, and these two facts together define the
evaluation strategy for the entire project going forward.

Week 2 successfully designed and partially executed a rigorous, well-reasoned
ablation study, supported by genuine domain research into the contextual
variables being tested. The open item carried into Week 3 is to **finalize and
reconcile the ablation study's result** into a single, statistically validated
conclusion, so that the project's modeling phase proceeds on a confirmed
finding rather than a provisional one.
