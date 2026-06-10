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
