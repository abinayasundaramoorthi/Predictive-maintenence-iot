# Predictive Maintenance - IoT Dataset

## Day 1 EDA Observations

1. Dataset loaded successfully with 10,000 rows and 10 columns.
2. No null values found in any column.
3. Target variable is Machine Failure (0 = No Failure, 1 = Failure).
4. Only 3.4% of machines failed - dataset is imbalanced.
5. Rolling mean, standard deviation and variance added for all 5 sensor columns.
6. 15 new features created - total columns increased from 10 to 25.
7. After dropna, dataset reduced to 9992 rows.
8. Train test split done - 7993 train samples, 1999 test samples.

## Day 2 Observations

1. Correlation heatmap shows Air temp and Process temp are strongly related (0.88).
2. Rotational speed and Torque are negatively correlated (-0.88).
3. Target column has very low correlation with all features.
4. Class imbalance found - only 3.4% machine failures (339 out of 10000).
5. New features added - temp_difference, power and tool_wear_rate.
6. temp_difference shows heat gap between environment and machine.
7. Power feature combines speed and torque to show machine load.
8. tool_wear_rate shows how fast tool is getting damaged.

## Day 3 Observations

1. Outlier detection done using boxplots for all 5 sensor columns.
2. Air temperature, Process temperature and Tool wear have no outliers - stable readings.
3. Rotational speed has outliers on the higher side - some machines spin too fast.
4. Torque has outliers on both sides - some machines underloaded or overloaded.
5. Label encoding applied on Type column - L=0, M=1, H=2.
6. New feature heat_stress_index created - Air temperature multiplied by Tool wear.
7. New feature speed_torque_ratio created - Rotational speed divided by Torque.
8. New feature wear_per_rotation created - Tool wear divided by Rotational speed, scaled by 1000.

## Day 4 - Feature Importance & Explainability

1. Recreated all 12 selected features from Day 2.
2. Retrained LightGBM model - confirmed Macro F1: 0.899.
3. Task 1 - Feature Importance Ranking:
   - Most important: Rotational speed (392)
   - 2nd: power (380)
   - 3rd: Torque (352)
   - 4th: Tool wear (312)
   - Least important: wear_per_rotation (0)
4. Task 2 - SHAP Analysis:
   - Used TreeExplainer to explain model predictions
   - SHAP summary plot saved as shap_summary.png
   - Shows which features push prediction towards failure or no failure
5. Task 3 - Fusion Feature Impact:
   - Original sensors importance: 1559 (52.0%)
   - Engineered features importance: 1441 (48.0%)
   - Engineered features contribute 48% of model decisions!
6. Task 4 - Business Interpretation:
   - Top 3 failure indicators: Rotational speed, Power, Torque
   - High power = machine overloaded = failure risk
   - Unusual speed/torque = machine struggling = failure risk
   - LightGBM achieves 0.899 Macro F1 - production ready!
7. Feature importance chart saved as feature_importance.png

## Day 5 - Feature Engineering + LightGBM Final Report

1. Feature Selection Summary:
   - Total original columns: 10
   - Total engineered features created: 11
   - Features removed (weak): 4
   - Final features selected: 12

2. Feature Importance Report:
   - Most important: Rotational speed (392)
   - 2nd: power (380)
   - 3rd: Torque (352)
   - Least important: wear_per_rotation (0)

3. Final Model Performance:
   - LightGBM Macro F1: 0.899
   - Logistic Regression (Week 2): 0.693
   - Improvement: 0.206 (29.8% better!)

4. Key Insights:
   - Engineered features contribute 48% of model decisions
   - LightGBM is production ready with 0.899 Macro F1
