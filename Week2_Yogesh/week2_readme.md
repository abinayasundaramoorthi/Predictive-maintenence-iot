# Week 2 - Contextual Data Fusion and Feature Engineering

## Day 1 - External Context Simulation
1. Simulated Ambient_temperature using normal distribution (mean=295K, std=3).
2. Simulated Load_density using uniform distribution (0.3 to 1.0).
3. Created temperature_gap feature - factory heat vs outside weather.
4. Created load_stress feature - machine power multiplied by factory busy-ness.

## Day 2 - Feature Validation
1. Checked correlation of all 8 engineered features with Target.
2. Highest correlation: power (0.176) - close to but does not exceed Torque (0.19).
3. temp_difference showed negative correlation (-0.112) - opposite of hypothesis.
4. Created effective_power feature - power divided by ambient temperature.
5. effective_power scored 0.145 - lower than power alone.

## Day 3 - Ablation Study
1. Conducted ablation study to prove external features improve prediction.
2. Model A - only 5 original sensors - Macro F1: 0.679.
3. Model B - 5 sensors + 8 engineered features - Macro F1: 0.693.
4. Improvement of 0.014 proves engineered features help prediction.
5. Added StandardScaler to fix convergence warning.
6. fit_transform on train data, transform on test data to avoid data leakage.

## Day 4 - Timestamp Based Data Fusion
1. Added simulated timestamp column using pd.date_range.
2. Each row gets one timestamp - one reading per minute.
3. Time range covers 2024-01-01 08:00 to 2024-01-08 06:39.
4. Merged internal sensor data with external context based on timestamps.
5. Final dataset has 16 columns - 10 original + 6 new features.
