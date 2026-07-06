"""
app.py
------
Main entry point for running the trained IoT Predictive Maintenance
model end-to-end (inference only).

What this does:
  1. Loads the trained LightGBM model from results/metrics/
  2. Loads the held-out test set from data/processed/
  3. Runs inference with predict_proba
  4. Applies a configurable probability threshold
  5. Prints sample predictions and failure probabilities

This file does NOT retrain, refactor, or touch the training pipeline.
It is purely a runnable inference/demo layer on top of the existing
project artifacts.

Usage:
    python app.py
    python app.py --threshold 0.35
    python app.py --threshold 0.5 --rows 20
"""

import argparse
import os
import sys

import joblib
import numpy as np
import pandas as pd

import config


def load_model(model_path: str):
    """Load the trained model artifact."""
    if not os.path.exists(model_path):
        print(f"[ERROR] Model file not found at: {model_path}")
        sys.exit(1)
    print(f"[INFO] Loading model from: {model_path}")
    model = joblib.load(model_path)
    print(f"[INFO] Model loaded: {type(model).__name__}")
    return model


def load_test_data(x_path: str, y_path: str = None):
    """Load the test feature set, and labels if available."""
    if not os.path.exists(x_path):
        print(f"[ERROR] Test data file not found at: {x_path}")
        sys.exit(1)
    print(f"[INFO] Loading test features from: {x_path}")
    X_test = pd.read_csv(x_path)

    y_test = None
    if y_path and os.path.exists(y_path):
        y_test = pd.read_csv(y_path).iloc[:, 0]
        print(f"[INFO] Loading test labels from: {y_path}")

    return X_test, y_test


def run_inference(model, X_test: pd.DataFrame, threshold: float):
    """Run predict_proba and apply the decision threshold."""
    print(f"[INFO] Running inference on {len(X_test)} rows...")
    probabilities = model.predict_proba(X_test)[:, config.POSITIVE_CLASS_INDEX]
    predictions = (probabilities >= threshold).astype(int)
    return predictions, probabilities


def summarize_results(predictions, probabilities, y_test, threshold, num_rows):
    """Print a clean, human-readable summary of the run."""
    print("\n" + "=" * 60)
    print("PREDICTIVE MAINTENANCE — INFERENCE SUMMARY")
    print("=" * 60)
    print(f"Threshold used         : {threshold}")
    print(f"Total samples          : {len(predictions)}")
    print(f"Predicted failures     : {int(predictions.sum())}")
    print(f"Predicted healthy      : {int((predictions == 0).sum())}")
    print(f"Avg failure probability: {probabilities.mean():.4f}")

    if y_test is not None:
        from sklearn.metrics import (
            accuracy_score,
            precision_score,
            recall_score,
            f1_score,
        )

        acc = accuracy_score(y_test, predictions)
        prec = precision_score(y_test, predictions, zero_division=0)
        rec = recall_score(y_test, predictions, zero_division=0)
        f1 = f1_score(y_test, predictions, zero_division=0)
        print("-" * 60)
        print("Ground-truth comparison (labels found in data/processed):")
        print(f"  Accuracy  : {acc:.4f}")
        print(f"  Precision : {prec:.4f}")
        print(f"  Recall    : {rec:.4f}")
        print(f"  F1-score  : {f1:.4f}")

    print("-" * 60)
    print(f"Sample predictions (first {num_rows} rows):")
    print("-" * 60)

    sample = pd.DataFrame(
        {
            "row_id": np.arange(min(num_rows, len(predictions))),
            "failure_probability": np.round(probabilities[:num_rows], 4),
            "predicted_label": predictions[:num_rows],
        }
    )
    sample["predicted_status"] = sample["predicted_label"].map(
        {0: "Healthy", 1: "Failure Risk"}
    )
    print(sample.to_string(index=False))
    print("=" * 60 + "\n")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run IoT Predictive Maintenance model inference (demo/viva execution)."
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=config.DEFAULT_THRESHOLD,
        help=f"Probability threshold for classifying a failure (default: {config.DEFAULT_THRESHOLD})",
    )
    parser.add_argument(
        "--rows",
        type=int,
        default=config.NUM_SAMPLE_ROWS_TO_SHOW,
        help=f"Number of sample rows to display (default: {config.NUM_SAMPLE_ROWS_TO_SHOW})",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    model = load_model(config.MODEL_PATH)
    X_test, y_test = load_test_data(config.X_TEST_PATH, config.Y_TEST_PATH)

    predictions, probabilities = run_inference(model, X_test, args.threshold)
    summarize_results(predictions, probabilities, y_test, args.threshold, args.rows)


if __name__ == "__main__":
    main()
