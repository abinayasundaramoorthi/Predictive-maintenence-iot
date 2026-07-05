# Week 4 - Noise Sensitivity Analysis and Robustness Evaluation

## My Role:  Robustness Evaluation

## Day 1 - Evaluation Framework Setup

1. Loaded dataset (10,000 rows, 10 columns)
2. Recreated all 12 selected features from Week 3
3. Retrained LightGBM model successfully
4. Created evaluation framework function covering:
   - Accuracy, Precision, Recall, F1 Score, ROC-AUC
5. Baseline results on clean data:
   - Accuracy: 0.987
   - Precision: 0.891
   - Recall: 0.908
   - F1 Score: 0.899
   - ROC-AUC: 0.973
6. Saved baseline results to CSV file

## Day 2 - Robustness Evaluation on Noisy Datasets

1. Created evaluation function covering all metrics.
2. Ran model on original and 4 noisy datasets (5%, 10%, 15%, 20%).
3. Performance comparison results:

| Dataset | F1 Score | ROC-AUC | F1 Drop |
|---|---|---|---|
| Original (0%) | 0.899 | 0.973 | 0.000 |
| 5% noise | 0.882 | 0.971 | -0.018 |
| 10% noise | 0.843 | 0.972 | -0.056 |
| 15% noise | 0.846 | 0.972 | -0.053 |
| 20% noise | 0.839 | 0.970 | -0.060 |

4. Key finding - even at 20% noise model scores 0.839!
5. F1 drop of only 0.060 at maximum noise - model is ROBUST!
6. Results saved to robustness_results.csv
7. Robustness chart saved as robustness_chart.png

## Day 3 - Detailed Metrics Calculation

1. Calculated all metrics for all noise levels separately.
2. Metrics calculated: Accuracy, Precision, Recall, F1, ROC-AUC.
3. Results:
   - 0% noise: Accuracy=0.987, F1=0.899, ROC-AUC=0.973
   - 5% noise: Accuracy=0.984, F1=0.882, ROC-AUC=0.971
   - 10% noise: Accuracy=0.978, F1=0.843, ROC-AUC=0.972
   - 15% noise: Accuracy=0.979, F1=0.846, ROC-AUC=0.972
   - 20% noise: Accuracy=0.978, F1=0.839, ROC-AUC=0.970
4. Saved detailed metrics to detailed_metrics.csv

## Day 4 - Performance Comparison Charts

1. Created performance comparison table with F1 drop analysis.
2. Created 4 comparison charts:
   - F1 Score vs Noise Level
   - Accuracy vs Noise Level
   - Precision and Recall vs Noise Level
   - ROC-AUC vs Noise Level
3. Charts saved as comparison_charts.png

## Day 5 - Final Review and Submit

1. Loaded saved results from Day 3.
2. Final review summary:
   - Baseline F1: 0.899 (clean data)
   - Maximum noise F1: 0.839 (20% noise)
   - Maximum F1 drop: 0.060
   - ROC-AUC drop minimal (0.973 to 0.970)
3. Key findings:
   - Model maintains 0.839 F1 at 20% noise
   - LightGBM proves robust against sensor noise
   - Model is production ready!

## Additional Features - Machine Health System

Implemented beyond scheduled work:

1. Machine Health Score (0-100):
   - Excellent (90-100), Good (75-89), Warning (50-74)
   - Poor (25-49), Critical (0-24)

2. Maintenance Recommendation Engine:
   - Check cooling system (high temperature)
   - Inspect tool wear (high wear rate)
   - Immediate inspection (critical health score)

3. Remaining Useful Life (RUL) Estimation:
   - Health > 85 → 30+ days
   - Health 70-85 → 14 days
   - Health 50-70 → 7 days
   - Health < 50 → Immediate inspection!

4. Fleet Monitoring Dashboard:
   - 2000 machines monitored
   - Critical: 62, Warning: 1820, Good: 90
   - Saved as health_dashboard.png

File: notebooks/05_evaluation/machine_health_system.ipynb
