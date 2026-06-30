# Week 4 Day 1 Findings

## Tasks Completed
- Loaded trained SMOTE pipeline
- Generated prediction labels
- Extracted prediction probabilities
- Identified high-risk and low-risk machines
- Classified predictions into risk categories
- Reviewed model confidence
- Prepared data for Precision-Recall Curve analysis

## Key Findings
- Each prediction includes a probability score indicating confidence.
- Higher probability values indicate greater likelihood of machine failure.
- Risk categories help prioritize machines requiring maintenance.
- The probability outputs are suitable for Precision-Recall analysis.

# Week 4 Day 2 Findings

## Tasks Completed
- Extracted prediction probabilities from the trained model.
- Generated the Precision-Recall Curve.
- Calculated Average Precision Score.
- Compared Precision and Recall across probability thresholds.
- Identified the threshold with the best F1 Score.
- Exported Precision-Recall results for future analysis.

## Key Findings
- The Precision-Recall Curve provides a better evaluation for imbalanced datasets than accuracy alone.
- Average Precision summarizes the model's overall performance across all thresholds.
- Increasing the decision threshold generally improves Precision but reduces Recall.
- A balanced threshold can improve the model's effectiveness for predictive maintenance.

