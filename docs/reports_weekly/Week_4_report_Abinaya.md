# Week 4 — Threshold Tuning Analysis  
## Member 4 | Abinaya S | Predictive Maintenance IoT Project  

---

## 📌 Project Overview

This project focuses on optimizing the **decision threshold** for a machine learning-based predictive maintenance system.

The model outputs a probability of machine failure. A decision threshold is used to convert this probability into a binary classification:

- Failure
- No Failure

While 0.50 is commonly used as a default threshold, it is not optimal for imbalanced datasets. This work evaluates multiple thresholds to identify the most effective operating point based on both **model performance and business impact**.

---

## 📊 Dataset

- **Source:** Prediction outputs from Member 3’s Logistic Regression + SMOTE model  
- **File:** `member3_day1_w4results.csv`  
- **Test size:** 2,000 records  
- **Failure rate:** 3.4% (68 actual failures)  
- **Features used:**  
  - `Actual` (Ground Truth)  
  - `Failure Probability` (Model Output)  

---

## ⚙️ Methodology

The workflow is structured into five stages:

### Day 1 — Framework Setup
- Loaded prediction dataset
- Validated model probability outputs
- Implemented threshold-based prediction function
- Implemented confusion matrix utility function
- Verified baseline model output at threshold = 0.50

**Baseline Confusion Matrix (0.50):**

|               | Predicted 0 | Predicted 1 |
|--------------|------------|------------|
| Actual 0     | 1865       | 67         |
| Actual 1     | 2          | 66         |

---

### Day 2 — Threshold Evaluation

- Evaluated thresholds from **0.10 to 0.85**
- Computed:
  - Precision
  - Recall
  - F1 Score
  - Confusion matrix components (TP, FP, TN, FN)
- Identified optimal threshold using **F1 Score**

**Key Result:**  
- Best Threshold = **0.80**  
- Best F1 Score = **0.9353**

---

### Day 3 — Confusion Matrix Analysis

- Generated confusion matrices for key thresholds:
  - 0.30
  - 0.50
  - 0.70
  - 0.80

**Observations:**

| Threshold | FP | FN | Insight |
|----------|----|----|--------|
| 0.30 | 159 | 1 | High recall, many false alarms |
| 0.50 | 67  | 2 | Baseline model behavior |
| 0.70 | 23  | 3 | Balanced improvement |
| 0.80 | 6   | 3 | Best operational balance |

---

### Day 4 — Business Decision Analysis

- Compared False Positives vs False Negatives across thresholds
- Evaluated operational cost trade-offs
- Selected final threshold based on:
  - Minimum total error
  - High recall requirement
  - Practical deployment feasibility

**Total Error Comparison:**

| Threshold | FP | FN | Total Errors |
|----------|----|----|-------------|
| 0.30 | 159 | 1 | 160 |
| 0.40 | 99  | 1 | 100 |
| 0.50 | 67  | 2 | 69 |
| 0.60 | 38  | 2 | 40 |
| 0.70 | 23  | 3 | 26 |
| 0.80 | 6   | 3 | **9** |

---

### Day 5 — Final Review

- Consolidated all results
- Validated optimal threshold selection
- Generated final performance summary plot
- Documented final recommendation for deployment

---

## 🏆 Final Model Recommendation

### ✅ Optimal Threshold: **0.80**

### Performance at Threshold 0.80:

- True Positives: 65 / 68 (95.6%)
- False Positives: 6
- False Negatives: 3
- Precision: 0.9155
- Recall: 0.9559
- F1 Score: 0.9353

---

## 📈 Business Interpretation

In predictive maintenance systems:

- **False Negative (FN):** Missed failure → high operational risk (downtime, repair cost)
- **False Positive (FP):** False alarm → minor inspection cost

This creates an asymmetric cost structure where **FN is significantly more expensive than FP**.

### Trade-off Analysis:

Moving from threshold 0.30 to 0.80 results in:

- 153 fewer false alarms
- Only 2 additional missed failures
- Significant improvement in precision
- Strong improvement in overall system usability

---

## 🎯 Final Decision Rule

```
If Failure Probability ≥ 0.80 → Predict FAILURE
Else → Predict NO FAILURE
```

---

## 📦 Deliverables

| Deliverable | Status |
|------------|--------|
| Threshold evaluation table | `threshold_results.csv` |
| Confusion matrix analysis | Completed |
| FP vs FN comparison | Completed |
| Business decision framework | Completed |
| Final threshold recommendation | 0.80 |

---

## 🗂 Repository Structure

```
Week4/
│
├── Day1_Threshold_Framework.ipynb
├── Day2_Threshold_Evaluation.ipynb
├── Day3_Confusion_Matrix_Analysis.ipynb
├── Day4_Business_Decision_Analysis.ipynb
├── Day5_Final_Review.ipynb
│
├── member3_day1_w4results.csv
├── threshold_results.csv
└── README.md
```

---

## 🧠 Key Learnings

- Threshold tuning significantly impacts classification performance
- Accuracy alone is insufficient for imbalanced datasets
- Confusion matrix analysis is essential for model interpretability
- Business cost structure should guide model decision thresholds
- Precision-Recall trade-off is critical in real-world ML systems

---

## 📌 Conclusion

This project demonstrates how systematic threshold tuning can significantly improve a machine learning model’s real-world performance.

By moving from a default threshold (0.50) to an optimized threshold (0.80), the model achieves a better balance between detection capability and operational efficiency, making it suitable for deployment in predictive maintenance systems.

---