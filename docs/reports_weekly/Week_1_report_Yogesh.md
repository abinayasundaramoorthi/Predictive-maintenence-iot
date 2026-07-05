# Week 1 Report - Yogeshwaran
## IoT Telemetry Ingestion and Signal Processing

### Day 1 - EDA and Rolling Features
- Loaded AI4I 2020 dataset (10,000 rows, 10 columns)
- No missing values found
- Created histograms for all 5 sensor columns
- Added rolling mean, std and variance for all 5 sensors (window=5)
- Created 15 new rolling features
- Train test split: 7993 train, 1999 test

### Day 2 - Correlation Analysis and Feature Engineering
- Correlation heatmap: Air temp & Process temp = 0.88
- Rotational speed & Torque = -0.88
- Class imbalance: only 3.4% failures (339/10000)
- Created 3 new features: temp_difference, power, tool_wear_rate

### Day 3 - Outlier Detection and Encoding
- Boxplot outlier detection for all 5 sensors
- Outliers found in Rotational speed and Torque
- Label encoding: Type column (L=0, M=1, H=2)
- Created 3 more features: heat_stress_index, 
  speed_torque_ratio, wear_per_rotation

### Summary
- Total new features: 21 (15 rolling + 6 engineered)
- Best correlation with Target: Torque (0.19)
- GitHub commits: 14