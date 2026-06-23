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
