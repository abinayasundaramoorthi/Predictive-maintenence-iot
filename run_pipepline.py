"""
run_pipeline.py
----------------
Simple CLI wrapper for a one-command project demo.

This does not contain any new logic — it just calls app.py's
functions in sequence and prints a short demo banner, so a viva
panel can run one command and see the full flow end-to-end.

Usage:
    python run_pipeline.py
"""

import config
from app import load_model, load_test_data, run_inference, summarize_results


def demo_run():
    print("\n" + "#" * 60)
    print("# IoT PREDICTIVE MAINTENANCE — END-TO-END DEMO RUN")
    print("#" * 60)

    print("\n[STEP 1] Loading trained model...")
    model = load_model(config.MODEL_PATH)

    print("\n[STEP 2] Loading test dataset...")
    X_test, y_test = load_test_data(config.X_TEST_PATH, config.Y_TEST_PATH)

    print("\n[STEP 3] Running inference...")
    predictions, probabilities = run_inference(
        model, X_test, config.DEFAULT_THRESHOLD
    )

    print("\n[STEP 4] Summarizing results...")
    summarize_results(
        predictions,
        probabilities,
        y_test,
        config.DEFAULT_THRESHOLD,
        config.NUM_SAMPLE_ROWS_TO_SHOW,
    )

    print("[DONE] Demo pipeline finished successfully.\n")


if __name__ == "__main__":
    demo_run()
