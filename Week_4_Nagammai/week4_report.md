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

# Week 4 Day 3 Findings

## Tasks Completed
- Analyzed decision thresholds.
- Generated Threshold vs Precision plot.
- Generated Threshold vs Recall plot.
- Compared Precision and Recall across thresholds.
- Calculated F1 Score for each threshold.
- Identified the optimal decision threshold.
- Exported threshold analysis results.

## Key Findings
- Increasing the threshold generally improves Precision but decreases Recall.
- Lower thresholds detect more machine failures but may increase false positives.
- Higher thresholds reduce false alarms but may miss some actual failures.
- The optimal threshold is the one that provides the best balance between Precision and Recall, as indicated by the highest F1 Score.

# Week 4 Day 4 Findings

## Tasks Completed
- Evaluated threshold performance using Precision, Recall, and F1 Score.
- Identified the threshold that maximizes Recall.
- Identified the threshold that maximizes Precision.
- Selected the balanced threshold using the highest F1 Score.
- Compared different threshold strategies.
- Generated deployment recommendations for predictive maintenance.

## Key Findings
- Lower thresholds improve Recall by detecting more machine failures but increase false alarms.
- Higher thresholds improve Precision by reducing false alarms but may miss actual failures.
- The balanced threshold provides an effective compromise between Precision and Recall.
- Different operational environments may require different threshold strategies.

