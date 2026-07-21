/* =====================================================================
   Predictive Maintenance Dashboard — Frontend logic
   Vanilla JS only, no build step required.
   ===================================================================== */

// ---------------------------------------------------------------------
// Sidebar toggle (mobile)
// ---------------------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.getElementById("menuToggle");
  const sidebar = document.getElementById("sidebar");
  if (toggle && sidebar) {
    toggle.addEventListener("click", () => sidebar.classList.toggle("open"));
    document.addEventListener("click", (e) => {
      if (!sidebar.contains(e.target) && !toggle.contains(e.target)) {
        sidebar.classList.remove("open");
      }
    });
  }
});

// ---------------------------------------------------------------------
// Loading overlay
// ---------------------------------------------------------------------
function ensureLoadingOverlay() {
  if (document.getElementById("loading-overlay")) return;
  const overlay = document.createElement("div");
  overlay.id = "loading-overlay";
  overlay.className = "loading-overlay";
  overlay.innerHTML = `
    <div class="loading-box">
      <div class="spinner"></div>
      <div class="loading-text" id="loading-text">Analyzing Machines...</div>
    </div>`;
  document.body.appendChild(overlay);
}

const LOADING_STEPS = [
  "Analyzing Machines...",
  "Running AI Model...",
  "Calculating Health Scores...",
  "Generating Explainable AI...",
  "Complete",
];

async function withLoadingAnimation(promiseFactory) {
  ensureLoadingOverlay();
  const overlay = document.getElementById("loading-overlay");
  const textEl = document.getElementById("loading-text");
  overlay.classList.add("active");

  let stepIndex = 0;
  textEl.textContent = LOADING_STEPS[0];
  const interval = setInterval(() => {
    stepIndex = Math.min(stepIndex + 1, LOADING_STEPS.length - 2);
    textEl.textContent = LOADING_STEPS[stepIndex];
  }, 350);

  try {
    const result = await promiseFactory();
    textEl.textContent = "Complete";
    await new Promise((r) => setTimeout(r, 200));
    return result;
  } finally {
    clearInterval(interval);
    overlay.classList.remove("active");
  }
}

// ---------------------------------------------------------------------
// Small helpers
// ---------------------------------------------------------------------
function escapeHtml(value) {
  return String(value === undefined || value === null ? "" : value)
    .replace(/&/g, "&amp;")
    .replace(/"/g, "&quot;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function showBanner(message, type) {
  const banner = document.getElementById("global-banner");
  if (!banner) return;
  banner.textContent = message;
  banner.className = "global-banner " + (type === "info" ? "banner-info" : "banner-error");
  banner.style.display = "block";
  clearTimeout(banner._pmTimer);
  banner._pmTimer = setTimeout(() => { banner.style.display = "none"; }, 7000);
}

// ---------------------------------------------------------------------
// Prediction console (only active on prediction.html)
// ---------------------------------------------------------------------
window.__predictionPageInit = function () {
  const tbody = document.getElementById("excel-tbody");
  const detailTemplate = document.getElementById("detail-template");
  if (!tbody) return; // not on this page

  let rowCounter = 0;
  const charts = {}; // rowId -> Chart.js instance
  const COLUMN_COUNT = 16; // includes the leading row-number column

  // Renumbers the visible "#" cell on every sheet row so the sequence
  // always matches what's on screen (1, 2, 3 ...), regardless of how a
  // row got there — typed, Healthy/Failure/Random sample, or Generate
  // Rows — and regardless of rows removed in between.
  function renumberRows() {
    const rows = tbody.querySelectorAll("tr.sheet-row");
    rows.forEach((tr, index) => {
      const cell = tr.querySelector('[data-field="row-num"]');
      if (cell) cell.textContent = index + 1;
    });
  }

  // Fields the backend requires as valid numbers for every row. Mirrors
  // webapp/utils/api.py::REQUIRED_NUMERIC_FIELDS so the sheet can catch
  // blank cells locally and never send them to the server at all.
  const REQUIRED_FIELDS = [
    ["air_temp_k", "Air Temp"],
    ["process_temp_k", "Process Temp"],
    ["rotational_speed_rpm", "Rot. Speed"],
    ["torque_nm", "Torque"],
    ["tool_wear_min", "Tool Wear"],
    ["ambient_temp_c", "Ambient Temp"],
    ["load_density_pct", "Production Load"],
  ];

  function machineIdFor(n) {
    return "M-" + String(1000 + n);
  }

  function findRow(rowId) {
    return tbody.querySelector(`tr.sheet-row[data-row-id="${rowId}"]`);
  }

  function findDetailRow(rowId) {
    return tbody.querySelector(`tr.detail-row[data-detail-for="${rowId}"]`);
  }

  // --- Row construction ---
  function addRow(prefill) {
    rowCounter += 1;
    const id = "row-" + rowCounter;

    const defaults = Object.assign(
      {
        machine_id: machineIdFor(rowCounter),
        machine_type: "M",
        air_temp_k: "",
        process_temp_k: "",
        rotational_speed_rpm: "",
        torque_nm: "",
        tool_wear_min: "",
        ambient_temp_c: "",
        load_density_pct: "",
        shift: "Day",
      },
      prefill || {}
    );

    const tr = document.createElement("tr");
    tr.className = "sheet-row";
    tr.dataset.rowId = id;

    tr.innerHTML = `
      <td class="row-num-cell"><span data-field="row-num">${rowCounter}</span></td>
      <td><input type="text" data-key="machine_id" value="${escapeHtml(defaults.machine_id)}"></td>
      <td>
        <select data-key="machine_type">
          <option value="L" ${defaults.machine_type === "L" ? "selected" : ""}>L</option>
          <option value="M" ${defaults.machine_type === "M" ? "selected" : ""}>M</option>
          <option value="H" ${defaults.machine_type === "H" ? "selected" : ""}>H</option>
        </select>
      </td>
      <td><input type="number" step="0.1" data-key="air_temp_k" value="${escapeHtml(defaults.air_temp_k)}" placeholder="300.5"></td>
      <td><input type="number" step="0.1" data-key="process_temp_k" value="${escapeHtml(defaults.process_temp_k)}" placeholder="310.0"></td>
      <td><input type="number" step="1" data-key="rotational_speed_rpm" value="${escapeHtml(defaults.rotational_speed_rpm)}" placeholder="1450"></td>
      <td><input type="number" step="0.1" data-key="torque_nm" value="${escapeHtml(defaults.torque_nm)}" placeholder="40.0"></td>
      <td><input type="number" step="1" data-key="tool_wear_min" value="${escapeHtml(defaults.tool_wear_min)}" placeholder="100"></td>
      <td><input type="number" step="0.1" data-key="ambient_temp_c" value="${escapeHtml(defaults.ambient_temp_c)}" placeholder="24.0"></td>
      <td><input type="number" step="0.1" data-key="load_density_pct" value="${escapeHtml(defaults.load_density_pct)}" placeholder="50.0"></td>
      <td>
        <select data-key="shift">
          <option ${defaults.shift === "Day" ? "selected" : ""}>Day</option>
          <option ${defaults.shift === "Evening" ? "selected" : ""}>Evening</option>
          <option ${defaults.shift === "Night" ? "selected" : ""}>Night</option>
        </select>
      </td>
      <td class="result-cell" data-field="status-cell"><span class="cell-dash">—</span></td>
      <td class="result-cell" data-field="health-cell"><span class="cell-dash">—</span></td>
      <td class="result-cell" data-field="failuretype-cell"><span class="cell-dash">—</span></td>
      <td class="result-cell" data-field="confidence-cell"><span class="cell-dash">—</span></td>
      <td class="actions-cell">
        <div class="actions-inner">
          <button type="button" class="row-action-btn" data-action="details" title="View explanation" disabled>▾</button>
          <button type="button" class="row-action-btn row-remove-btn" data-action="remove" title="Remove row">✕</button>
        </div>
      </td>
    `;

    const detailTr = document.createElement("tr");
    detailTr.className = "detail-row hidden";
    detailTr.dataset.detailFor = id;
    const detailTd = document.createElement("td");
    detailTd.colSpan = COLUMN_COUNT;
    detailTr.appendChild(detailTd);

    tbody.appendChild(tr);
    tbody.appendChild(detailTr);
    renumberRows();
    return tr;
  }

  function readRow(tr) {
    const data = {};
    tr.querySelectorAll("[data-key]").forEach((el) => {
      data[el.dataset.key] = el.value;
    });
    return data;
  }

  function fillFirstRow(sample) {
    if (tbody.querySelectorAll("tr.sheet-row").length === 0) addRow();
    const tr = tbody.querySelector("tr.sheet-row");
    Object.keys(sample).forEach((key) => {
      const el = tr.querySelector(`[data-key="${key}"]`);
      if (el) el.value = sample[key];
    });
  }

  // --- Toolbar actions ---
  document.getElementById("btn-clear").addEventListener("click", () => {
    Object.keys(charts).forEach((k) => { charts[k].destroy(); delete charts[k]; });
    tbody.innerHTML = "";
    addRow();
  });

  async function loadSampleAsNewRow(kind) {
    try {
      const res = await fetch(`/api/sample/${kind}`);
      const data = await res.json();
      if (data.ok) {
        addRow(data.sample);
      } else {
        showBanner(data.error || "Could not load sample.", "error");
      }
    } catch (err) {
      showBanner("Network error while loading sample.", "error");
    }
  }
  document.getElementById("btn-sample-healthy").addEventListener("click", () => { loadSampleAsNewRow("healthy"); closeSampleMenu(); });
  document.getElementById("btn-sample-failure").addEventListener("click", () => { loadSampleAsNewRow("failure"); closeSampleMenu(); });
  document.getElementById("btn-sample-random").addEventListener("click", () => { loadSampleAsNewRow("random"); closeSampleMenu(); });

  // --- "Add Sample" dropdown (consolidates what used to be three
  // separate always-visible buttons into a single toolbar control) ---
  const sampleDropdown = document.getElementById("sample-dropdown");
  const sampleToggle = document.getElementById("btn-sample-toggle");
  function closeSampleMenu() { sampleDropdown && sampleDropdown.classList.remove("open"); }
  if (sampleToggle && sampleDropdown) {
    sampleToggle.addEventListener("click", (e) => {
      e.stopPropagation();
      sampleDropdown.classList.toggle("open");
    });
    document.addEventListener("click", (e) => {
      if (!sampleDropdown.contains(e.target)) closeSampleMenu();
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") closeSampleMenu();
    });
  }

  document.getElementById("btn-generate").addEventListener("click", async () => {
    const n = parseInt(document.getElementById("generate-count").value, 10) || 10;
    await withLoadingAnimation(async () => {
      try {
        const res = await fetch(`/api/generate-rows/${n}`);
        const data = await res.json();
        if (data.ok) {
          data.rows.forEach((sample) => addRow(sample));
        } else {
          showBanner(data.error || "Could not generate rows.", "error");
        }
      } catch (err) {
        showBanner("Network error while generating rows.", "error");
      }
    });
  });

  // --- Threshold: live re-labels already-predicted rows only ---
  // Health score/band never changes (it isn't threshold-dependent) and
  // Machine ID / Shift / row order are never touched — only the
  // Status + Confidence cells for rows that already have a stored
  // probability are recomputed, entirely client-side.
  function applyPredictionStatus(tr, proba, threshold) {
    const isFailure = proba >= threshold;
    const statusCell = tr.querySelector('[data-field="status-cell"]');
    const confCell = tr.querySelector('[data-field="confidence-cell"]');
    const confidence = Math.round((isFailure ? proba : (1 - proba)) * 1000) / 10;

    statusCell.innerHTML = isFailure
      ? '<span class="badge badge-red">⚠ Failure Risk</span>'
      : '<span class="badge badge-green">✓ Healthy</span>';
    confCell.textContent = confidence + "%";
  }

  function currentThreshold() {
    const raw = parseFloat(document.getElementById("threshold-input").value);
    if (isNaN(raw)) return 0.5;
    return Math.min(Math.max(raw, 0), 1);
  }

  function recomputeAllStatuses() {
    const threshold = currentThreshold();
    tbody.querySelectorAll("tr.sheet-row").forEach((tr) => {
      const probStr = tr.dataset.probability;
      if (probStr === undefined || probStr === "") return; // not predicted yet
      applyPredictionStatus(tr, parseFloat(probStr), threshold);
    });
  }
  document.getElementById("threshold-input").addEventListener("input", recomputeAllStatuses);
  document.getElementById("threshold-input").addEventListener("blur", (e) => {
    const clamped = currentThreshold();
    e.target.value = clamped.toFixed(2);
    recomputeAllStatuses();
  });

  // --- Rendering a successful / failed row outcome ---
  function bandColorVar(color) {
    const map = {
      green: "var(--accent-green)",
      "light-green": "var(--accent-green-light)",
      yellow: "var(--accent-yellow)",
      orange: "var(--accent-orange)",
      red: "var(--accent-red)",
    };
    return map[color] || "var(--accent-blue)";
  }

  function rowStatusClassForBand(color) {
    if (color === "green" || color === "light-green") return "row-status-healthy";
    if (color === "yellow") return "row-status-monitor";
    if (color === "orange") return "row-status-risk";
    return "row-status-critical";
  }

  function badgeClassForFailureType(type) {
    if (type === "No Failure") return "badge-green";
    if (type === "Tool Wear Failure" || type === "Power Failure") return "badge-yellow";
    if (type === "Heat Dissipation Failure") return "badge-orange";
    return "badge-red";
  }

  function clearRowStatusClasses(tr) {
    tr.classList.remove("row-status-healthy", "row-status-monitor", "row-status-risk", "row-status-critical", "row-status-error");
  }

  function applyFullResult(tr, result, threshold) {
    clearRowStatusClasses(tr);
    tr.classList.add(rowStatusClassForBand(result.health_band.color));
    tr.dataset.probability = String(result.probability);
    tr._pmResult = result;

    applyPredictionStatus(tr, result.probability, threshold);

    const healthCell = tr.querySelector('[data-field="health-cell"]');
    healthCell.innerHTML =
      `<span class="health-dot" style="background:${bandColorVar(result.health_band.color)};"></span>` +
      `<span class="health-value">${result.health_score}</span>`;

    const failTypeCell = tr.querySelector('[data-field="failuretype-cell"]');
    failTypeCell.innerHTML = `<span class="badge ${badgeClassForFailureType(result.failure_mode.failure_type)}">${escapeHtml(result.failure_mode.failure_type)}</span>`;

    const detailsBtn = tr.querySelector('button[data-action="details"]');
    if (detailsBtn) detailsBtn.disabled = false;

    const detailTr = findDetailRow(tr.dataset.rowId);
    if (detailTr) {
      detailTr.dataset.built = "0";
      if (!detailTr.classList.contains("hidden")) {
        renderDetailContent(tr, detailTr, result);
        detailTr.dataset.built = "1";
      }
    }
  }

  function markRowError(tr, message) {
    if (!tr) return;
    clearRowStatusClasses(tr);
    tr.classList.add("row-status-error");
    tr.dataset.probability = "";
    tr._pmResult = null;

    tr.querySelector('[data-field="status-cell"]').innerHTML =
      `<span class="badge badge-grey" title="${escapeHtml(message)}">⚠ ${escapeHtml(message)}</span>`;
    tr.querySelector('[data-field="health-cell"]').innerHTML = '<span class="cell-dash">—</span>';
    tr.querySelector('[data-field="confidence-cell"]').innerHTML = '<span class="cell-dash">—</span>';
    tr.querySelector('[data-field="failuretype-cell"]').innerHTML = '<span class="cell-dash">—</span>';

    const detailsBtn = tr.querySelector('button[data-action="details"]');
    if (detailsBtn) detailsBtn.disabled = true;
    const detailTr = findDetailRow(tr.dataset.rowId);
    if (detailTr) detailTr.classList.add("hidden");
  }

  function renderDetailContent(tr, detailTr, result) {
    const td = detailTr.querySelector("td");
    td.innerHTML = "";
    const fragment = detailTemplate.content.cloneNode(true);
    const wrapper = document.createElement("div");
    wrapper.appendChild(fragment);
    const inner = wrapper.firstElementChild;
    td.appendChild(inner);

    // Gauge
    const ring = inner.querySelector('[data-field="gauge-ring"]');
    const number = inner.querySelector('[data-field="gauge-number"]');
    const circumference = 314;
    const pct = Math.max(0, Math.min(100, result.health_score));
    const offset = circumference - (pct / 100) * circumference;
    ring.style.stroke = bandColorVar(result.health_band.color);
    requestAnimationFrame(() => {
      ring.style.transition = "stroke-dashoffset 0.8s ease";
      ring.setAttribute("stroke-dashoffset", offset.toFixed(1));
    });
    number.textContent = pct;

    inner.querySelector('[data-field="failure-detail"]').textContent = result.failure_mode.detail;

    const list = inner.querySelector('[data-field="recommendations"]');
    result.recommendations.forEach((r) => {
      const li = document.createElement("li");
      li.textContent = r;
      list.appendChild(li);
    });

    inner.querySelector('[data-field="explain-method"]').textContent =
      "Explainability method: " + result.explanation.method;

    const canvas = inner.querySelector('[data-field="shap-chart"]');
    const rowId = tr.dataset.rowId;
    if (charts[rowId]) { charts[rowId].destroy(); delete charts[rowId]; }

    const labels = result.explanation.top_features.map((f) => f.feature);
    const values = result.explanation.top_features.map((f) => f.impact);
    charts[rowId] = new Chart(canvas, {
      type: "bar",
      data: {
        labels,
        datasets: [{
          data: values,
          backgroundColor: values.map((v) => (v >= 0 ? "rgba(239,68,68,0.7)" : "rgba(59,130,246,0.7)")),
          borderRadius: 4,
        }],
      },
      options: {
        indexAxis: "y",
        responsive: true,
        plugins: { legend: { display: false } },
        scales: {
          x: { ticks: { color: "#93A1B7" }, grid: { color: "rgba(255,255,255,0.06)" } },
          y: { ticks: { color: "#93A1B7", font: { size: 10 } }, grid: { display: false } },
        },
      },
    });
  }

  // --- Row-level actions: expand details / remove row ---
  tbody.addEventListener("click", (e) => {
    const btn = e.target.closest("button[data-action]");
    if (!btn || btn.disabled) return;
    const tr = btn.closest("tr.sheet-row");
    if (!tr) return;
    const rowId = tr.dataset.rowId;

    if (btn.dataset.action === "remove") {
      const detailTr = findDetailRow(rowId);
      if (charts[rowId]) { charts[rowId].destroy(); delete charts[rowId]; }
      if (detailTr) detailTr.remove();
      tr.remove();
      renumberRows();
      return;
    }

    if (btn.dataset.action === "details") {
      const detailTr = findDetailRow(rowId);
      if (!detailTr) return;
      const isHidden = detailTr.classList.contains("hidden");
      if (isHidden) {
        if (detailTr.dataset.built !== "1" && tr._pmResult) {
          renderDetailContent(tr, detailTr, tr._pmResult);
          detailTr.dataset.built = "1";
        }
        detailTr.classList.remove("hidden");
        btn.textContent = "▴";
      } else {
        detailTr.classList.add("hidden");
        btn.textContent = "▾";
      }
    }
  });

  // --- Predict ---
  document.getElementById("btn-predict").addEventListener("click", async () => {
    const rows = Array.from(tbody.querySelectorAll("tr.sheet-row"));
    if (rows.length === 0) return;
    const threshold = currentThreshold();

    // Client-side validation FIRST: a blank/invalid cell is caught here
    // and never leaves the browser, so the backend never has to guard
    // against float("") — the bug can't reach it in the first place.
    const toSend = [];
    rows.forEach((tr) => {
      const data = readRow(tr);
      const missing = REQUIRED_FIELDS.filter(([key]) => {
        const v = data[key];
        return v === undefined || v === null || String(v).trim() === "";
      });
      if (missing.length > 0) {
        markRowError(tr, "Missing: " + missing.map((m) => m[1]).join(", "));
      } else {
        data.row_id = tr.dataset.rowId;
        data.threshold = threshold;
        toSend.push(data);
      }
    });

    if (toSend.length === 0) {
      showBanner("No rows had complete data to predict. Fill in the highlighted fields and try again.", "error");
      return;
    }

    await withLoadingAnimation(async () => {
      try {
        const res = await fetch("/api/predict-batch", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ rows: toSend, threshold }),
        });
        const data = await res.json();

        if (!data.ok) {
          showBanner(data.error || "Prediction failed.", "error");
          return;
        }

        data.results.forEach((item) => {
          const tr = findRow(item.row_id);
          if (!tr) return;
          if (item.ok) {
            applyFullResult(tr, item.result, threshold);
          } else {
            markRowError(tr, item.error);
          }
        });
      } catch (err) {
        toSend.forEach((r) => markRowError(findRow(r.row_id), "Network error contacting the model server."));
      }
    });
  });

  // Start with one blank row
  addRow();
};
