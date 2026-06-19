# Week 2 - Day 1 Context EDA

## Objective
Analyze contextual variables and understand their impact on machine failure.

## Tasks Completed
- Analyzed machine type distribution.
- Visualized air temperature distribution.
- Visualized process temperature distribution.
- Studied machine failure across machine types.
- Saved generated plots.
- Checked seasonality possibility.

## Findings
- Type L machines are most common.
- Temperature variables follow near-normal distributions.
- Machine failures occur in all machine categories.
- No time-based information is available.
- Seasonality analysis cannot be performed.

# Week 2 - Day 2 Correlation Analysis

### Tasks Completed
- Analyzed context variables against machine failure.
- Studied relationships between context and sensor variables.
- Generated correlation heatmaps.
- Saved visualizations.
- Documented observations.

### Findings
- Air and Process Temperature are highly correlated.
- Torque and Tool Wear show stronger association with failure.
- Machine Type has weak correlation with failure.
- Context variables provide useful supplementary information.

# Week 2 Day 3 - Context Impact Study

## Objective
To study how contextual variables influence machine failure.

## Variables Analyzed
- Air Temperature
- Process Temperature
- Torque
- Tool Wear
- Machine Type

## Findings
- Air Temperature shows limited impact on failure.
- Process Temperature has weak influence.
- Torque exhibits stronger variation between failed and non-failed machines.
- Tool Wear tends to be higher in failed machines.
- Machine failures occur across all machine types.

# Week 2 - Day 4 Ablation Study Setup

## Objective
To design experiments for evaluating the contribution of contextual features in machine failure prediction.

## Experiments Defined

### Experiment A - Baseline Model
Features Used:
- Air Temperature
- Process Temperature
- Rotational Speed (RPM)
- Torque
- Tool Wear

Purpose:
- Establish baseline predictive performance using only sensor data.

### Experiment B - Context-Aware Model
Features Used:
- Air Temperature
- Process Temperature
- Rotational Speed (RPM)
- Torque
- Tool Wear
- Machine Type (Context Feature)

Purpose:
- Evaluate the impact of contextual information on prediction performance.

## Dataset Preparation
- Created baseline dataset using sensor features only.
- Created context dataset using sensor and context features.
- Encoded categorical context variables where required.
- Prepared datasets for future model training and evaluation.

## Evaluation Metrics Planned
- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC

## Findings
- Baseline dataset represents traditional predictive maintenance data.
- Context dataset incorporates additional operational information.
- Recall and F1 Score are important due to class imbalance.
- Context features are expected to improve failure detection performance.
- Ablation study will quantify the contribution of contextual variables.

# Week 2 - Day 5 Ablation Study Results

## Objective
Compare the predictive performance of the Baseline and Context models to quantify the impact of contextual features.

## Activities Completed
- Trained Baseline Model
- Trained Context Model
- Generated predictions
- Calculated evaluation metrics
- Measured performance improvements
- Created comparison visualizations
- Analyzed confusion matrices
- Generated final ablation report

## Key Findings
- Context features improved overall predictive performance.
- Recall and F1 Score showed the most meaningful gains.
- Confusion matrix analysis revealed improved failure detection.
- Contextual information contributes useful predictive signals.

## Conclusion
The ablation study demonstrates that adding contextual variables improves machine failure prediction and supports their inclusion in future predictive maintenance models.