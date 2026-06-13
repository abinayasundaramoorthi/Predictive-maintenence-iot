# Predictive Maintenance IoT Project - Week 1 Report

## Day 1 - EDA and Rolling Features
- Loaded dataset (10,000 rows, 10 columns), no missing values
- Created histograms for sensor distributions
- Added rolling mean, std and variance for 5 sensors (window=5) - 15 new features
- Dropped NaN rows (10000 -> 9992), defined X and Y
- Train-test split: 7993 train, 1999 test

## Day 2 - Correlation Analysis and Feature Engineering
- Correlation heatmap: Air temp & Process temp = 0.88, Speed & Torque = -0.88
- Target correlation with sensors is weak (max 0.19 with Torque)
- Class imbalance: only 3.4% failures (339/10000)
- New features: temp_difference, power, tool_wear_rate

## Day 3 - Outlier Detection and Encoding
- Boxplots show outliers in Rotational speed and Torque
- Label encoded Type column (L=0, M=1, H=2)
- New features: heat_stress_index, speed_torque_ratio, wear_per_rotation

## Summary
Total 21 new features engineered (15 rolling + 6 custom).
Week 1 roadmap requirement (rolling mean, std, variance) completed on Day 1.
Additional correlation and outlier analysis completed Days 2-3.
