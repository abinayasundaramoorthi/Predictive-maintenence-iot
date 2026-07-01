# Infotact Compliance Report

Repository: abinayasundaramoorthi/Predictive-maintenence-iot
Branch: consolidatedbranch (audit artifacts only)

This report evaluates repository compliance with the Infotact Project Execution Handbook and general Data Science & GitHub Version Control Guidelines. Findings are based on a full read-only inspection of all Week* folders, notebooks, reports, datasets, and model artifacts. No files in main were modified.

Summary: PARTIAL compliance. Details below.

1. Week-wise evidence
- Week1: PASS
  - Multiple notebooks and reports found across Week1_* folders (EDA, feature engineering, outlier analysis). Evidence: Week1_Himanshu/Week1.ipynb, Week1_Yogesh/Day1_EDA.ipynb, Week_1_Nagammai/Day1_EDA.ipynb, Week_1_Abinaya/feature_engineering.ipynb, plus markdown reports.
- Week2: PASS
  - Context fusion notebooks and derived datasets found (Week2_Himanshu/ai4i2020.csv, ai4i_fused_week2.csv; Week_2_Abinaya/fusion_pipeline_output.csv). Multiple reports and notebooks present.
- Week3: PASS
  - Model training notebooks, LightGBM experiments, feature importance, model artifacts (week3_final_model.joblib, lightgbm_model.pkl) and evaluation figures present in Week3_Himanshu and Week3_yogesh.
- Week4: FAIL (MISSING)
  - No Week4 folder or Week4 notebooks found in the current repository layout. If Week4 exists under a different name, please indicate the path. Without Week4 evidence the internship deliverable for Week4 is missing.

2. Team contribution evidence
- PARTIAL
  - Per-member week folders exist (Himanshu, Yogesh, Abinaya, Nagammai), which documents individual outputs.
  - Commit-level authorship was not exhaustively checked as part of this initial audit pass; full authorship mapping (git log extraction) can be produced if required. Recommendation: include a CONTRIBUTORS.md or a short team section in README that maps folders to authors and links to GitHub usernames.

3. Documentation quality
- PARTIAL
  - README.md contains a detailed narrative (project vision and Weeks 1–2 summary), and dataset/README.md contains dataset placement instructions.
  - Missing: a concise HOWTO (exact commands to run notebooks), environment/requirements, and canonical dataset location (dataset/ai4i2020.csv missing from expected location). Recommendation: add a top-level quickstart and a note mapping datasets to their current Week* locations.

4. GitHub standards
- FAIL
  - No Issues, no Project board, no CONTRIBUTING.md, no CODEOWNERS, and no automated CI workflows found in main. Recommendation: create a project board and a minimal ISSUE template and CONTRIBUTING.md in consolidatedbranch for review.

5. Reproducibility
- PARTIAL
  - Notebooks contain code and outputs; however, many notebooks reference datasets in per-week folders and there is no centralized requirements.txt or environment.yml to recreate the environment. Recommendation: generate requirements.txt (done in consolidatedbranch), and provide instructions to run notebooks with proper dataset paths.

6. Recommendations (next actions)
- Add docs/repository_audit.md (done) and docs/infotact_compliance_report.md (this file).
- Add docs/dependency_report.md and requirements.txt (created in consolidatedbranch) to support reproducibility.
- Add a brief README improvement on consolidatedbranch that indexes the week folders and explains where datasets and models live.
- Create a GitHub Project board and recommended issues (docs/github_project_setup.md) after review.
- Locate or provide Week4 deliverables if available; if Week4 was intentionally omitted, include a statement in README explaining why.

Signed: GitHub Copilot (acting as Principal ML Engineer / Repo Auditor)
