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
