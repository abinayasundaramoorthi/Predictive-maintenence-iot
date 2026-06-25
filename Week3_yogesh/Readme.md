# Week 3 - Imbalanced Classification and LightGBM Modeling

## Day 1 - Fusion Feature Engineering Review

1. Recreated all Week 1 and Week 2 fusion features.
2. Reviewed correlation of all 8 engineered features with Target.
3. Best existing feature: power (0.176).
4. Created 3 new additional features for Week 3:
   - thermal_stress = temp_difference × tool_wear_rate (0.108)
   - power_per_temp = power ÷ Air temperature (0.172)
   - wear_heat_ratio = tool_wear_rate ÷ heat_stress_index (0.074)
5. power_per_temp (0.172) is strongest new feature - close to power (0.176).
6. Total engineered features now: 11 (8 existing + 3 new).

## Day 2 - Feature Selection & Optimization

1. Recreated all 11 engineered features from Week 1, Week 2 and Week 3 Day 1.
2. Checked correlation of all 11 features with Target.
3. Applied feature selection threshold of 0.10 correlation.
4. KEPT 7 strong features: power (0.176), power_per_temp (0.172), 
   tool_wear_rate (0.130), wear_per_rotation (0.130), 
   temp_difference (0.112), thermal_stress (0.108), heat_stress_index (0.106).
5. REMOVED 4 weak features: load_stress (0.088), wear_heat_ratio (0.074),
   speed_torque_ratio (0.063), temperature_gap (0.059).
6. Finalized 12 features for LightGBM model (5 original sensors + 7 engineered).

## Day 3 - LightGBM Development

1. Installed and imported LightGBM library (version 4.6.0).
2. Used 12 final features selected from Day 2.
3. Applied stratified train-test split (80/20) - ensures equal 
   failure distribution in both sets.
4. Training set: 8000 rows, 271 failures.
5. Testing set: 2000 rows, 68 failures.
6. Trained LightGBM model with class_weight='balanced' to handle imbalance.
7. LightGBM Macro F1 Score: 0.899
8. Classification Report:
   - Class 0 (no failure): F1 = 0.99
   - Class 1 (failure): F1 = 0.81
9. Compared with Week 2 Logistic Regression (0.693) - improvement of 0.206 (29.8% better!)
