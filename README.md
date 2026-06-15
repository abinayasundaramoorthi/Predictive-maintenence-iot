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

## Week 2 - Day 1 Observations

1. Started Week 2 - Contextual Data Fusion and Feature Engineering.
2. Simulated external context data since real external data is not available.
3. Created Ambient_temperature column using normal distribution (mean=295K, std=3) - represents outside weather temperature.
4. Created Load_density column using uniform distribution (0.3 to 1.0) - represents factory busy-ness.
5. Used random seed (42) to keep simulated values consistent across runs.
6. Created temperature_gap feature - Air temperature minus Ambient temperature - shows factory heat vs outside weather.
7. Recreated power feature and created load_stress feature - power multiplied by Load_density - shows combined machine and factory-wide stress.
8. Next step - verify if these new fusion features have stronger relationship with Target than individual sensors.
