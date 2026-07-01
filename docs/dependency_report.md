# Dependency Report

This report lists the dependencies observed in the repository notebooks and where they appear (representative notebooks). It was generated during the Phase 1 audit by scanning notebooks for import statements.

Method
- Inspected notebooks across Week* folders and extracted import statements where visible.
- This is an initial per-notebook mapping; some notebooks may contain additional imports not visible in the sampled passes. A full programmatic extraction pass is scheduled as a follow-up if you want exhaustive mapping.

Summary of dependencies (core)
- pandas — used in nearly every notebook for CSV I/O and dataframes (Week2_Himanshu/day4.ipynb, Week3_Himanshu/Day1.ipynb, Week_2_Abinaya/day1.ipynb, etc.)
- numpy — numerical arrays and seeds (Week2_Himanshu/day4.ipynb, Week3_Himanshu/Day1.ipynb)
- scikit-learn (sklearn) — modeling and evaluation (DummyClassifier, train_test_split, metrics, LogisticRegression) (Week3_Himanshu/Day1.ipynb, Week_3_Abinaya/Day_1.ipynb)
- lightgbm — model training in Week3_yogesh/Day3_LightGBM.ipynb and Week3_Himanshu
- imbalanced-learn (imblearn) — SMOTE and pipelines (Week_3_Nagammai/Day4_SMOTE_CV_Integration.ipynb)
- matplotlib, seaborn — visualization (Week_2_Nagammai/Day1_Context_EDA.ipynb)
- joblib, pickle — model persistence (Week3_Himanshu/week3_final_model.joblib, Week3_yogesh/lightgbm_model.pkl)
- shap — feature explanations (Week3_yogesh/feature importance notebooks)

Per-notebook (representative) import mapping
- Week_2_Abinaya/day1.ipynb
  - import pandas as pd
  - import matplotlib.pyplot as plt
  - Reads: predictive_maintenance.csv (local path in notebook)

- Week_2_Abinaya/day4.ipynb
  - import pandas as pd
  - import numpy as np
  - import matplotlib.pyplot as plt
  - Reads: fusion_pipeline_output.csv

- Week3_Himanshu/Day1.ipynb
  - import pandas as pd
  - import numpy as np
  - import lightgbm as lgb
  - import imblearn
  - from sklearn.dummy import DummyClassifier
  - from sklearn.model_selection import train_test_split
  - from sklearn.metrics import accuracy_score, recall_score, f1_score
  - Reads: ai4i_fused_week2.csv

- Week3_Himanshu/Day3.ipynb
  - import pandas as pd
  - import numpy as np
  - import lightgbm as lgb
  - import imblearn
  - Reads: ai4i_fused_week2.csv

- Week_3_Abinaya/Day_1.ipynb
  - import pandas as pd
  - import numpy as np
  - from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
  - Reads: fusion_pipeline_output_consolidated.csv

- Week_3_Nagammai/Day4_SMOTE_CV_Integration.ipynb
  - import pandas as pd
  - import numpy as np
  - import matplotlib.pyplot as plt
  - import seaborn as sns
  - from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate
  - from sklearn.linear_model import LogisticRegression
  - from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
  - from imblearn.pipeline import Pipeline
  - from imblearn.over_sampling import SMOTE
  - Reads: dataset/ai4i2020.csv or repo-local copy

- Week3_yogesh/Day3_LightGBM.ipynb
  - import lightgbm as lgb
  - import pandas as pd
  - import numpy as np
  - from sklearn.model_selection import train_test_split
  - from sklearn.metrics import classification_report
  - Reads: fused dataset and outputs model lightgbm_model.pkl

Notes and gotchas
- Many notebooks reference absolute local Windows paths (C:\Users\delta\...) which must be updated to repository relative paths for reproducibility. I will enumerate those paths in the notebook I/O mapping.
- Some notebooks use %run to re-run other notebooks (e.g., %run day3.ipynb). Running notebooks end-to-end will require a consistent run-order or conversion to scripts.
- BOM in CSV files: use encoding="utf-8-sig" when reading.

Planned follow-up
- I will run a programmatic extraction for every notebook and produce a fully enumerated docs/dependency_report.md (per-notebook imports, cell counts) and then generate a requirements.txt based on the union of observed imports.

