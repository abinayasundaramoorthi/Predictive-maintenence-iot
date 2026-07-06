# Contextual Data Fusion Pipeline for Predictive Maintenance

## Overview

This project focuses on building a contextual data fusion pipeline for a Predictive Maintenance system in a Manufacturing and Automotive environment.

The objective is to enrich machine sensor data with operational context information, perform feature engineering, validate data quality, and prepare a reliable dataset for machine learning and Edge AI applications.



## What Was Done

The project began with timestamp alignment to ensure all records could be consistently merged and analyzed over time.

Additional contextual information was then generated and integrated with the original machine sensor dataset. These contextual variables represent operational conditions such as production load, power quality, maintenance schedules, operator experience, and work shifts.

After merging the datasets, several engineered features were created to capture machine behavior more effectively and provide meaningful signals for predictive maintenance analysis.

The entire workflow was automated through a reusable data fusion pipeline that includes data loading, context generation, data fusion, validation, and output generation.

Finally, multiple quality checks were performed to verify data integrity, timestamp consistency, missing values, duplicate records, and validation logic.



## Features Created

### Context Features

* Shift
* Production Load
* Power Quality Index
* Maintenance Window
* Operator Experience

### Engineered Features

* Wear Load Index
* Temperature Gap
* Power Stress Score

These features provide additional operational context and help improve predictive maintenance analysis.


## Pipeline Workflow

Raw Dataset

↓

Timestamp Alignment

↓
  
Context Feature Generation

↓

Data Fusion

↓

Feature Engineering

↓

Validation and Quality Checks

↓

Final Fused Dataset

## Project Outputs

The project generates:

* Timestamp-aligned dataset
* Context-enriched fusion dataset
* Automated fusion pipeline output
* Data validation reports



## Key Learnings

Through this project, I gained hands-on experience in:

* Data fusion techniques
* Feature engineering
* Data validation
* Pipeline automation
* Predictive maintenance workflows
* Industrial IoT data processing



## Conclusion

A complete contextual data fusion pipeline was successfully developed and validated. The resulting dataset is structured, enriched with operational context, and ready for downstream predictive maintenance model development and Edge AI deployment.
