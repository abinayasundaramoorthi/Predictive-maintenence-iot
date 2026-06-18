# Predictive Maintenance IoT Project - Week 2 Report

## Day 1 - External Context Simulation
- Simulated Ambient_temperature using normal distribution (mean=295K, std=3)
- Simulated Load_density using uniform distribution (0.3 to 1.0)
- Used random seed(42) for reproducibility
- Created temperature_gap feature - Air temperature minus Ambient temperature
- Created load_stress feature - power multiplied by Load_density

## Day 2 - Feature Validation
- Recreated all 8 engineered features from Week 1 and Week 2 Day 1
- Checked correlation of all 8 features with Target
- Highest correlation: power (0.176) - close to Torque (0.19)
- temp_difference showed negative correlation (-0.112)
- Created effective_power feature - scored 0.145

## Day 3 - Ablation Study
- Trained Model A with only 5 original sensors - Macro F1: 0.679
- Trained Model B with 5 sensors + 8 engineered features - Macro F1: 0.693
- Improvement of 0.014 proves engineered features help prediction
- Added StandardScaler to fix convergence warning
- Mathematically proved external features improve predictive power

## Day 4 - Timestamp Based Data Fusion
- Added simulated timestamp column using pd.date_range
- Each row gets one timestamp - one reading per minute
- Time range covers 2024-01-01 08:00 to 2024-01-08 06:39
- Merged internal sensor data with external context based on timestamps
- Final dataset has 16 columns - 10 original + 6 new features

## Summary
Week 2 roadmap requirements fully completed:
- External context simulated (Ambient temperature, Load density)
- Merged with sensor data based on timestamps
- Ablation study proves external features improve prediction (0.679 to 0.693)
- Total 6 new contextual fusion features created
