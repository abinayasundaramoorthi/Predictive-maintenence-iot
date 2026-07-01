# Notebook I/O Mapping

This document maps notebooks to the files they read and write (observed during audit). It is provisional — I inspected every Week* folder and captured the most commonly used notebooks and their inputs/outputs. Each entry records: Notebook path, Inputs (files read), Outputs (files written), Run-order notes, and Provenance (SHA256 from docs/checksums.csv where applicable).

Notes
- I preserved all notebooks *in place* and did not modify them.
- Where notebooks reference absolute local paths (e.g., C:\\Users\\delta\\...), I list the path and a recommended repo-relative replacement.
- Use docs/checksums.csv as the canonical SHA256 manifest for dataset/model artifacts.

1) Week2_Himanshu/Week2.ipynb (and related Day notebooks)
- Inputs:
  - Week2_Himanshu/ai4i2020.csv (sha: f602454c...)
- Outputs:
  - Week2_Himanshu/ai4i_fused_week2.csv (sha: 76978d2c...)
- Notes:
  - Produces fused dataset consumed by Week3 training notebooks.
  - Recommended canonical read: pandas.read_csv("Week2_Himanshu/ai4i2020.csv", encoding="utf-8-sig")

2) Week_2_Abinaya/day1.ipynb .. day5.ipynb
- Inputs:
  - dataset/predictive_maintenance.csv (sha: 9f0ede0b...)
  - Local paths observed in notebooks: C:\\Users\\ABINAYA\\Downloads\\predictive_maintenance.csv — replace with repo-relative path above.
- Outputs:
  - Week_2_Abinaya/Fusion_dataset.csv (sha: 4acc3d56...)
  - Week_2_Abinaya/fusion_pipeline_output.csv (sha: df16564f...)
- Notes:
  - Uses timestamp generation and fusion steps. fusion_pipeline_output_consolidated.csv is an identical copy (same sha).

3) Week3_Himanshu/Day1.ipynb, Day3.ipynb (Modeling)
- Inputs:
  - Week3_Himanshu/ai4i_fused_week2.csv (sha: 76978d2c...)
- Outputs:
  - Week3_Himanshu/week3_final_model.joblib (sha: 3c8b3f45...)
  - Week3_Himanshu/week3_*.csv results (CV results, tuning results) (various shas in docs/checksums.csv)
- Notes:
  - Uses lightgbm and imbalanced-learn; recommends running after Week2 fused dataset is available.

4) Week3_yogesh/Day3_LightGBM.ipynb
- Inputs:
  - ai4i_fused_week2.csv (repo-relative; several copies exist — use Week2_Himanshu copy or one with sha 76978d2c...)
- Outputs:
  - Week3_yogesh/lightgbm_model.pkl (sha: c7464dd9...)
  - Week3_yogesh/predictions.csv (sha: 2754be37...)
- Notes:
  - Notebook includes SHAP/feature importance outputs (shap_summary.png)

5) Week_3_Abinaya/Day_1.ipynb
- Inputs:
  - fusion_pipeline_output_consolidated.csv (sha: df16564f...)
- Outputs:
  - Evaluation outputs, plots (refer to folder)
- Notes:
  - Uses target column named "Target" in this notebook; be mindful of target column naming differences across week folders.

6) Week_1_* notebooks (feature engineering / EDA)
- Inputs:
  - ai4i2020.csv (some notebooks reference dataset/predictive_maintenance.csv or local paths)
- Outputs:
  - Feature sets or derived CSVs inside their Week1 folders (feature_engineering outputs)
- Notes:
  - These notebooks produce the engineered features used downstream; ensure run-order: Week1 -> Week2 -> Week3

7) Notebooks that use %run or import other notebooks
- Observed: Week_2_Abinaya/day4.ipynb uses "%run day3.ipynb" — requires day3.ipynb to have been executed or available in same runtime.
- Recommendation: Convert dependent notebook logic into explicit scripts or ensure run-order is documented.

8) Absolute local paths observed (examples)
- C:\\Users\\delta\\Predictive-maintenence-iot\\dataset\\ai4i2020.csv
- C:\\Users\\ABINAYA\\Downloads\\predictive_maintenance.csv

Replace with repo-relative paths in reproducible runs, e.g.:
- dataset/predictive_maintenance.csv
- Week2_Himanshu/ai4i2020.csv

Provenance reference (checksums)
- Use docs/checksums.csv as the canonical map from path -> SHA256. Example entries:
  - Week2_Himanshu/ai4i2020.csv -> f602454c133d...
  - Week2_Himanshu/ai4i_fused_week2.csv -> 76978d2ccb01...
  - Week3_Himanshu/week3_final_model.joblib -> 3c8b3f4550f2...

Run-order guidance (recommended)
1. Run Week1 notebooks (feature engineering) to generate feature definitions.
2. Run Week2 notebooks (context fusion and dataset generation) using Week1 outputs where applicable.
3. Run Week3 modeling notebooks (training & evaluation) using fused dataset from Week2.

If you'd like, I will continue to produce a full line-by-line mapping for every notebook (each read/write cell) and mark whether cells depend on hidden state; this will be a longer pass. Reply CONFIRM to request the exhaustive mapping.
