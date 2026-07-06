"""
config.py
----------
Central configuration for the inference/run layer.

This file ONLY defines paths and settings that already exist in the
project's current folder structure. Nothing here changes, renames,
or restructures the project — it simply points to what's already there.
"""

import os

# ---------------------------------------------------------------------
# Base directory (project root — where this config.py file lives)
# ---------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------
# Model artifact
# ---------------------------------------------------------------------
MODEL_PATH = os.path.join(BASE_DIR, "results", "metrics", "week4_eval_model.joblib")

# ---------------------------------------------------------------------
# Data artifacts
# ---------------------------------------------------------------------
X_TEST_PATH = os.path.join(BASE_DIR, "data", "processed", "week4_X_test.csv")
Y_TEST_PATH = os.path.join(BASE_DIR, "data", "processed", "week4_y_test.csv")  # optional, used if present

# ---------------------------------------------------------------------
# Inference settings
# ---------------------------------------------------------------------
DEFAULT_THRESHOLD = 0.5          # probability cutoff for classifying a "failure"
NUM_SAMPLE_ROWS_TO_SHOW = 10      # how many sample predictions to print
POSITIVE_CLASS_INDEX = 1          # index of the "failure" class in predict_proba output

# ---------------------------------------------------------------------
# Random seed (kept for reproducibility of any sampling in app.py)
# ---------------------------------------------------------------------
RANDOM_SEED = 42
