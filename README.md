# Context-Aware Predictive Maintenance using Machine Learning

## Team Information

### Group Number

**Group No: 4**

### Team Members

| Name                  | Role        |
| --------------------- | ----------- |
| Abinaya S             | Team Leader |
| Himanshu Rawat        | Team Member |
| Nagammai Subramaniyan | Team Member |
| N. Yogeshwaran        | Team Member |

### Domain

**Data Science & Machine Learning**

---

# Project Overview

Predictive Maintenance is a proactive maintenance strategy that uses machine learning and sensor data to predict equipment failures before they occur. Traditional maintenance approaches often lead to unexpected breakdowns, increased downtime, and higher operational costs.

This project aims to develop a Context-Aware Predictive Maintenance system using the AI4I Predictive Maintenance Dataset. The project combines machine telemetry data, feature engineering techniques, contextual analysis, and machine learning experiments to improve machine failure prediction performance.

The ultimate goal is to identify early warning signs of machine degradation and support proactive maintenance decisions that reduce downtime and maintenance costs.

---

# Problem Statement

Industrial machines generate large volumes of sensor data during operation. However, machine failures are relatively rare events, making failure prediction a challenging task.

The key challenges include:

* Highly imbalanced failure data
* Weak individual feature correlations
* Complex interactions between sensor variables
* Need for contextual understanding of machine behavior

This project addresses these challenges through feature engineering, contextual analysis, and ablation studies.

---

# Dataset Information

### Dataset

AI4I 2020 Predictive Maintenance Dataset

### Dataset Size

* Total Records: 10,000
* Total Features: 14
* Target Variable: Machine Failure

### Failure Distribution

| Class   | Count |
| ------- | ----- |
| Normal  | 9661  |
| Failure | 339   |

Failure Rate: 3.4%

The dataset is highly imbalanced, making Recall and F1 Score important evaluation metrics.

---

# Project Workflow

```text
Data Collection
       ↓
Exploratory Data Analysis
       ↓
Feature Engineering
       ↓
Context Analysis
       ↓
Contextual Feature Creation
       ↓
Ablation Study
       ↓
Model Evaluation
       ↓
Performance Comparison
```

---

# Week 1 Activities

## Day 1 - Exploratory Data Analysis and Rolling Features

### Activities

* Loaded and inspected dataset
* Checked for missing values
* Visualized sensor distributions
* Created rolling statistical features

### Features Created

* Rolling Mean
* Rolling Standard Deviation
* Rolling Variance

Generated across five sensor variables using a rolling window of 5 observations.

### Outcome

15 statistical features were engineered to capture machine behavior trends and variability.

---

## Day 2 - Correlation Analysis and Feature Engineering

### Activities

* Generated correlation heatmap
* Studied feature relationships
* Identified highly correlated variables

### Key Findings

* Air Temperature and Process Temperature show strong positive correlation (0.88)
* Rotational Speed and Torque show strong negative correlation (-0.88)
* Target correlations are relatively weak

### New Features

* Temperature Difference
* Power
* Tool Wear Rate

---

## Day 3 - Outlier Analysis and Encoding

### Activities

* Performed boxplot analysis
* Conducted outlier detection
* Encoded Machine Type

### New Features

* Heat Stress Index
* Speed-Torque Ratio
* Wear Per Rotation

---

## Week 1 Summary

### Total Engineered Features

* 15 Rolling Statistical Features
* 6 Domain-Specific Features

Total New Features Created: 21

---

# Week 2 Activities

## Day 1 - Contextual Data Exploration

### Activities

* Machine Type Analysis
* Air Temperature Analysis
* Process Temperature Analysis
* Failure Distribution Analysis

### Findings

* Type L machines are the most common
* Temperature distributions are approximately normal
* Failures occur across all machine types

---

## Day 2 - Context Correlation Analysis

### Activities

* Correlation Analysis
* Context-Sensor Relationship Study
* Heatmap Visualization

### Findings

* Torque and Tool Wear show stronger relationships with machine failure
* Machine Type has weak correlation with failure
* Context information provides supplementary predictive insights

---

## Day 3 - Context Impact Study

### Activities

* Comparative analysis between failed and non-failed machines
* Feature impact assessment

### Findings

* Failed machines generally exhibit higher torque
* Failed machines show increased tool wear
* Contextual information influences machine behavior

---

## Day 4 - Ablation Study Design

### Experiment A - Baseline Model

Features Used:

* Air Temperature
* Process Temperature
* Rotational Speed
* Torque
* Tool Wear

Purpose:

To establish baseline predictive performance using only machine sensor data.

### Experiment B - Context-Aware Model

Features Used:

* Baseline Features
* Machine Type

Purpose:

To evaluate the contribution of contextual information.

### Evaluation Metrics

* Accuracy
* Precision
* Recall
* F1 Score
* ROC-AUC

---

## Day 5 - Ablation Study Results

### Activities

* Trained Baseline Model
* Trained Context-Aware Model
* Generated Predictions
* Compared Performance Metrics
* Evaluated Confusion Matrices

### Key Findings

* Context features improved predictive performance
* Recall improved for failure detection
* F1 Score improved compared to baseline
* Context variables contribute useful predictive signals

### Conclusion

The ablation study successfully demonstrated that contextual information improves machine failure prediction performance.

---

# Key Technical Concepts Applied

## Exploratory Data Analysis (EDA)

* Distribution Analysis
* Class Imbalance Analysis
* Correlation Analysis
* Outlier Detection

## Feature Engineering

* Rolling Mean
* Rolling Variance
* Rolling Standard Deviation
* Temperature Difference
* Power
* Tool Wear Rate
* Heat Stress Index
* Speed-Torque Ratio
* Wear Per Rotation

## Context Analysis

* Machine Type Impact
* Context Correlation Study
* Context Contribution Assessment

---

# Business Impact

The proposed system helps organizations:

* Reduce unexpected machine failures
* Minimize operational downtime
* Improve maintenance planning
* Reduce maintenance costs
* Increase equipment reliability
* Improve production efficiency

By predicting failures before they occur, organizations can shift from reactive maintenance to proactive maintenance strategies.

---

# Future Work

* Advanced Machine Learning Models
* Ensemble Learning Techniques
* Real-Time IoT Integration
* Time-Series Forecasting
* Explainable AI (XAI)
* Predictive Maintenance Dashboard Development
* Deployment on Cloud Platforms

---

# Conclusion

This project demonstrates the effectiveness of combining exploratory data analysis, feature engineering, contextual analysis, and machine learning techniques for predictive maintenance. The ablation study validates that contextual information improves predictive performance, supporting the development of more reliable and intelligent maintenance systems for industrial environments.
