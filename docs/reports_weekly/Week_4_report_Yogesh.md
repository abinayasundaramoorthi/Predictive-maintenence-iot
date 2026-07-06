# Week 4 Report - Yogeshwaran
## Noise Sensitivity Analysis and Robustness Evaluation

### My Role: Member 2 - Robustness Evaluation

### Day 1 - Evaluation Framework
- Prepared evaluation framework covering all metrics
- Baseline results on clean data:
  - Accuracy: 0.987
  - Precision: 0.891
  - Recall: 0.908
  - F1 Score: 0.899
  - ROC-AUC: 0.973
- Saved baseline to CSV

### Day 2 - Robustness Evaluation
- Ran model on original and noisy datasets
- Noise levels tested: 5%, 10%, 15%, 20%
- Results:
  - 0% noise: F1 = 0.899
  - 5% noise: F1 = 0.882
  - 10% noise: F1 = 0.843
  - 15% noise: F1 = 0.846
  - 20% noise: F1 = 0.839
- Only 0.060 drop at 20% noise - Model is ROBUST!

### Day 3 - Metrics Calculation
- Calculated all metrics for each noise level
- Saved to detailed_metrics.csv

### Day 4 - Comparison Charts
- Created 4 comparison charts:
  - F1 Score vs Noise Level
  - Accuracy vs Noise Level
  - Precision and Recall vs Noise Level
  - ROC-AUC vs Noise Level
- Saved as comparison_charts.png

### Day 5 - Final Review
- Baseline F1: 0.899
- Maximum noise F1: 0.839 (20% noise)
- Maximum F1 drop: 0.060
- ROC-AUC minimal drop (0.973 to 0.970)
- Model is PRODUCTION READY!

### Additional Features (Beyond Schedule)
- Machine Health Score System (0-100)
- Maintenance Recommendation Engine
- Remaining Useful Life (RUL) Estimation
- Fleet Monitoring Dashboard (2000 machines)
- Results: Critical=62, Warning=1820, Good=90

### Summary
- Model robust at 20% noise: 0.839
- Machine Health System implemented
- GitHub commits: 11+