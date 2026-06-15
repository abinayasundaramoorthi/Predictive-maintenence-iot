# Failure Analysis Report

## Overview
- Total records: 10000
- Total failures: 339
- Failure rate: 3.39%

## Failure Type Breakdown
| Type | Full Name | Count | % of Total |
|------|-----------|-------|-----------|
| TWF | Tool Wear Failure | 46 | 0.46% |
| HDF | Heat Dissipation Failure | 115 | 1.15% |
| PWF | Power Failure | 95 | 0.95% |
| OSF | Overstrain Failure | 98 | 0.98% |
| RNF | Random Failure | 19 | 0.19% |

## Key Observations
- Dataset is highly imbalanced — only ~3.4% failures
- Oversampling (SMOTE) will be needed in the modeling phase
- Heat Dissipation and Tool Wear are the most common failure modes
