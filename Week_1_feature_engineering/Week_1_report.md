# Week 1 Report – Feature Engineering and Signal Processing

## Project

Manufacturing & Automotive – Contextual Predictive Maintenance (IoT Edge AI)

## Team Member

Member 4 (Abinaya) – Feature Engineering

## Week 1 Objective

The objective of Week 1 was to perform feature engineering on the AI4I Predictive Maintenance Dataset by creating statistical and domain-driven features from machine telemetry data. These features will support future contextual data fusion and predictive maintenance modeling.


# Day 1 – Feature Engineering Setup (#30)

### Tasks Completed

* Created the feature engineering notebook.
* Researched rolling window techniques for time-series sensor data.
* Studied variance-based feature generation.
* Planned feature engineering workflow.
* Documented the feature development strategy.

### Outcome

Established the feature engineering pipeline and identified important sensor variables for feature creation.


# Day 2 – Rolling Mean Features (#31)

### Tasks Completed

* Created rolling mean features for Air Temperature.
* Created rolling mean features for Process Temperature.
* Applied rolling window calculations.
* Validated generated feature values.
* Documented implementation process.

### Features Created

* rolling_air_temp_win3
* rolling_air_temp_win5
* rolling_process_temp_win3

### Outcome

Rolling mean features were generated to capture short-term temperature trends and reduce sensor noise.


# Day 3 – Rolling Standard Deviation Features (#32)

### Tasks Completed

* Researched standard deviation based signal features.
* Studied variability measurement techniques for sensor data.
* Evaluated feature engineering approaches for industrial telemetry.
* Planned implementation for future statistical features.
* Documented observations.

### Outcome

Improved understanding of signal variability and statistical feature generation for predictive maintenance applications.


# Day 4 – Variance Features (#33)

### Tasks Completed

* Generated variance-based features.
* Created window-based variance indicators.
* Validated calculations.
* Compared feature behavior across windows.
* Documented findings.

### Features Created

* rolling_air_temp_variance_win3
* rolling_air_temp_variance_win5
* rolling_process_temp_variance_win3

### Additional Engineered Features

* temp_dif
* Speed_torque_ratio
* stress_index
* torque_change_rate
* wear_speed

### Outcome

Variance features were created to measure operational stability and sensor fluctuation patterns.


# Day 5 – Week 1 Feature Report (#34)

### Tasks Completed

* Combined all engineered features into a single dataset.
* Prepared the preliminary feature engineering pipeline.
* Performed testing and validation.
* Documented feature generation process.
* Completed Week 1 report and closed assigned issues.

### Final Feature Set

#### Original Features

* Air temperature [K]
* Process temperature [K]
* Rotational speed [rpm]
* Torque [Nm]
* Tool wear [min]

#### Engineered Features

* temp_dif
* Speed_torque_ratio
* stress_index
* torque_change_rate
* wear_speed

#### Rolling Mean Features

* rolling_air_temp_win3
* rolling_air_temp_win5
* rolling_process_temp_win3

#### Variance Features

* rolling_air_temp_variance_win3
* rolling_air_temp_variance_win5
* rolling_process_temp_variance_win3


# Week 1 Summary

Successfully completed the Feature Engineering module for Week 1. Developed domain-driven features, rolling mean features, and variance-based statistical features from IoT telemetry data. The processed dataset is prepared for Week 2 Contextual Data Fusion, where external environmental and operational data will be integrated with machine telemetry for predictive maintenance analysis.

