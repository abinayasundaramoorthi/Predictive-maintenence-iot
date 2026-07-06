# Week 3 Report - Yogeshwaran
## Imbalanced Classification and LightGBM Modeling

### Day 1 - Fusion Feature Engineering Review
- Reviewed all existing features from Week 1 and Week 2
- Created 3 new additional features:
  - thermal_stress = temp_difference x tool_wear_rate (0.108)
  - power_per_temp = power / Air temperature (0.172)
  - wear_heat_ratio = tool_wear_rate / heat_stress_index (0.074)
- Best new feature: power_per_temp (0.172)

### Day 2 - Feature Selection and Optimization
- Checked correlation of all 11 features with Target
- Applied threshold of 0.10
- Kept 7 strong features, removed 4 weak features
- Finalized 12 features for LightGBM model

### Day 3 - LightGBM Development
- Trained LightGBM with 12 selected features
- Used stratified split, StandardScaler, class_weight='balanced'
- LightGBM Macro F1 Score: 0.899
- 29.8% better than Logistic Regression (0.693)
- Saved model as lightgbm.pkl

### Day 4 - Feature Importance and Explainability
- Most important feature: Rotational speed (392)
- Best engineered feature: power (380)
- SHAP analysis completed
- Engineered features contribute 48% of model decisions!

### Day 5 - Final Report
- Complete Week 3 summary
- All tasks completed!

### Summary
- Final features: 12
- LightGBM Macro F1: 0.899
- Engineered features contribution: 48%
- GitHub commits: 27