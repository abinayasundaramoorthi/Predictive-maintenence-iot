# Week 4 - Noise Sensitivity Analysis and Robustness Evaluation

## My Role: Member 2 - Robustness Evaluation

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
