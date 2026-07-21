# Predictive Maintenance — Web Dashboard (`webapp/`)

A self-contained Flask dashboard added on top of the existing Predictive
Maintenance project. **Nothing outside this folder is modified** — the
dashboard imports and reuses the project's existing `config.py` and the
model-loading functions already defined in the project's `app.py`.

---

## v1.1.0 — what changed and why

The previous build of this dashboard could crash with
`could not convert string to float: ''` whenever a row was left blank
(e.g. after clicking **+ Add Row**, or after changing the threshold).

**Root cause:** the sample/"Load Sample" buttons only ever filled the
*first* table row, "Add Row" created every new row with empty-string
defaults for every numeric field, and the **Predict** button sent every
row's raw values straight to the backend — including those empty
strings — which then hit `float("")` in `build_feature_row()` and
raised a raw Python exception that leaked into the UI. Because only the
first row usually had real data in it, it looked like "only the first
machine can ever be predicted."

**The fix, entirely inside `webapp/`:**

1. **Client-side validation before anything is sent.** Every row is
   checked in the browser first; a row with a blank required cell is
   marked `⚠ Missing: <field>` directly in the sheet and is **never**
   sent to the server — so the server-side `float("")` crash simply
   can't happen anymore.
2. **Server-side validation as a second line of defense**
   (`webapp/utils/api.py::validate_raw_input`). No code path in the
   backend calls `float()` on a raw value anymore; everything goes
   through `_clean_numeric()`, which turns a bad value into one clean,
   human-readable message — never a Python traceback.
3. **One batched request instead of N sequential ones.** `Predict All`
   now calls a single `/api/predict-batch` endpoint with every valid
   row. The backend builds one feature matrix, runs `predict_proba`
   once, and computes SHAP once for the whole sheet — this is what
   guarantees **every machine gets its own SHAP explanation**, not
   just the first, and is why 50-row sheets resolve in one pass
   instead of feeling "stuck loading."
4. **A bad row never blocks a good row.** The batch endpoint validates
   and scores every row independently and returns a per-row
   ok/error outcome in the original order, so 2 bad rows out of 20
   still return 18 clean predictions.
5. **Results now live in the sheet itself.** Status, Health Score,
   Failure Type, and Confidence are columns in the same row as the
   machine's inputs (with color-coded row highlighting). A **▾**
   button on each row expands its SHAP chart, failure detail, and
   recommended action directly beneath that row — not in a separate
   list disconnected from the table.
6. **Changing the threshold no longer touches the table.** It
   re-labels the Status/Confidence of already-predicted rows using the
   probability already returned by the model — entirely client-side,
   no request, no reset, Machine ID/Shift/row order untouched.
7. **"Generate Rows" (5 / 10 / 20 / 50) and every sample button** now
   pull real rows from the project's own held-out test set
   (`data/processed/week4_X_test.csv`) via `get_sample_rows()` /
   `get_random_test_sample()` — always fully populated, never
   fabricated, never blank.
8. Footer trimmed to just **"Predictive Maintenance Dashboard"** and
   the version number, as requested.

---

## What this is

* A professional, industrial-styled web UI for running the trained
  LightGBM model interactively.
* A true spreadsheet: enter machines, click **Predict All**, and see
  status/health/failure-type/confidence appear inline, per row, with
  an expandable SHAP explanation attached to each machine.
* A dashboard landing page, a reports/export page, a model information
  page, and an about page.

## What this is **not**

* It does not retrain, refactor, or duplicate the training pipeline.
* It does not change any existing file, folder, or import in the
  parent project — `webapp/utils/api.py` only *imports*
  `config.py` and `app.py` from the project root, read-only.
* The "Failure Type" shown is a **transparent, rule-based heuristic**
  derived from the AI4I 2020 dataset's own published domain thresholds
  (tool wear / heat dissipation / power / overstrain) — the trained
  model itself is a binary classifier and does not predict failure
  categories. This is documented on the **Model Information** page in
  the app itself.
* "Download PDF Report" uses the browser's print-to-PDF (a dedicated
  print stylesheet is included) rather than a separate server-side PDF
  library, to keep the additional dependency footprint minimal.

---

## Folder structure

```
webapp/
├── app.py                  # Flask entry point (routes + API endpoints)
├── requirements.txt        # ONLY the extra deps needed for the web layer
├── README.md                # this file
├── utils/
│   └── api.py               # validation, batch inference, SHAP, health
│                             # scoring, failure-mode heuristic, sampling
├── templates/
│   ├── base.html             # shared layout (sidebar, trimmed footer)
│   ├── index.html            # dashboard landing page
│   ├── prediction.html       # spreadsheet input + inline results
│   ├── reports.html          # recent predictions + export
│   ├── model_info.html       # model/feature/methodology details
│   ├── about.html            # team + project info
│   └── 404.html
└── static/
    ├── css/style.css         # design system (industrial dashboard theme)
    ├── js/script.js          # sheet logic, batch predict, charts, loading UI
    └── images/                # (empty — add a logo here if you like)
```

## Setup

From inside the `webapp/` folder:

```bash
# 1. Install the project's existing dependencies (if not already installed)
pip install -r ../requirements.txt

# 2. Install the additional web-layer dependencies
pip install -r requirements.txt

# 3. Run the dashboard
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

No configuration is required — `webapp/utils/api.py` automatically locates
the parent project's `config.py` and `app.py` (one directory up) and reuses
their existing `MODEL_PATH`, `X_TEST_PATH`, and `Y_TEST_PATH` settings.

## Notes on data used

* **Sample buttons and "Generate Rows"** use real rows pulled from the
  project's own `data/processed/week4_X_test.csv` — not fabricated
  data. Generated rows are always fully populated, so they can never
  trigger a validation error.
* **Model Accuracy** shown on the dashboard is computed once at server
  startup directly from `week4_X_test.csv` / `week4_y_test.csv` — it is
  never a hardcoded or invented number.
* Predictions made in the browser are kept in an in-memory log for the
  session (reports/export/dashboard stats) — no new database is
  introduced, per the brief's minimal-footprint requirement. Restarting
  the Flask server clears this log.

## API endpoints

| Route | Method | Purpose |
|---|---|---|
| `/api/predict-batch` | POST | Predict an entire sheet of rows in one call. Body: `{"rows": [...], "threshold": 0.5}`. Returns a per-row `ok`/`error` outcome, in the original order. |
| `/api/predict` | POST | Single-row convenience wrapper around the same validated path. |
| `/api/generate-rows/<n>` | GET | Returns `n` fully-populated rows sampled from the held-out test set. |
| `/api/sample/<kind>` | GET | `healthy` / `failure` (curated demo values) or `random` (real test-set row). |
| `/api/stats`, `/api/recent`, `/api/export/csv` | GET | Session prediction log / dashboard stats. |
