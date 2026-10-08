/**
 * Credit Risk Intelligence & Real-Time Scoring Engine - Client Logic
 * Author: Guillén Concepción (Senior Data Scientist & MLOps Engineer)
 */

document.addEventListener("DOMContentLoaded", () => {
    initTabs();
    initSimulator();
    loadOverviewData();
    loadStabilityData();
    loadFeaturesData();
    loadDistributionCharts();
});

/* ==============================================================================
   TAB NAVIGATION
   ============================================================================== */
function initTabs() {
    const navButtons = document.querySelectorAll(".nav-btn");
    const panes = document.querySelectorAll(".tab-pane");

    navButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            const targetId = btn.getAttribute("data-tab");

            navButtons.forEach(b => b.classList.remove("active"));
            panes.forEach(p => p.classList.remove("active"));

            btn.classList.add("active");
            const targetPane = document.getElementById(targetId);
            if (targetPane) {
                targetPane.classList.add("active");
            }
        });
    });
}

/* ==============================================================================
   REAL-TIME SIMULATOR
   ============================================================================== */
let simulationTimeout = null;

function initSimulator() {
    const inputIncome = document.getElementById("input-income");
    const inputDti = document.getElementById("input-dti");
    const inputRate = document.getElementById("input-rate");
    const inputEmp = document.getElementById("input-emp");
    const inputAge = document.getElementById("input-age");
    const inputHome = document.getElementById("input-home");
    const inputDefault = document.getElementById("input-default");

    // Labels
    const valIncome = document.getElementById("val-income");
    const valDti = document.getElementById("val-dti");
    const valRate = document.getElementById("val-rate");
    const valEmp = document.getElementById("val-emp");
    const valAge = document.getElementById("val-age");

    function updateLabelsAndSimulate() {
        if (inputIncome && valIncome) valIncome.textContent = `$${Number(inputIncome.value).toLocaleString()}`;
        if (inputDti && valDti) valDti.textContent = `${Math.round(Number(inputDti.value) * 100)}%`;
        if (inputRate && valRate) valRate.textContent = `${Number(inputRate.value).toFixed(2)}%`;
        if (inputEmp && valEmp) valEmp.textContent = `${inputEmp.value} años`;
        if (inputAge && valAge) valAge.textContent = `${inputAge.value} años`;

        // Debounce API calls
        clearTimeout(simulationTimeout);
        simulationTimeout = setTimeout(runSimulation, 60);
    }

    [inputIncome, inputDti, inputRate, inputEmp, inputAge].forEach(slider => {
        if (slider) slider.addEventListener("input", updateLabelsAndSimulate);
    });

    [inputHome, inputDefault].forEach(select => {
        if (select) select.addEventListener("change", updateLabelsAndSimulate);
    });

    // Presets
    const btnPrime = document.getElementById("preset-prime");
    const btnMedium = document.getElementById("preset-medium");
    const btnSubprime = document.getElementById("preset-subprime");

    if (btnPrime) {
        btnPrime.addEventListener("click", () => {
            inputIncome.value = 95000;
            inputDti.value = 0.12;
            inputRate.value = 7.90;
            inputEmp.value = 8;
            inputAge.value = 38;
            inputHome.value = "OWN";
            inputDefault.value = "N";
            updateLabelsAndSimulate();
        });
    }

    if (btnMedium) {
        btnMedium.addEventListener("click", () => {
            inputIncome.value = 52000;
            inputDti.value = 0.24;
            inputRate.value = 12.50;
            inputEmp.value = 3;
            inputAge.value = 29;
            inputHome.value = "RENT";
            inputDefault.value = "N";
            updateLabelsAndSimulate();
        });
    }

    if (btnSubprime) {
        btnSubprime.addEventListener("click", () => {
            inputIncome.value = 24000;
            inputDti.value = 0.48;
            inputRate.value = 19.50;
            inputEmp.value = 0;
            inputAge.value = 22;
            inputHome.value = "RENT";
            inputDefault.value = "Y";
            updateLabelsAndSimulate();
        });
    }

    // Initial evaluation
    updateLabelsAndSimulate();
}

async function runSimulation() {
    const payload = {
        person_income: parseFloat(document.getElementById("input-income").value),
        person_age: parseFloat(document.getElementById("input-age").value),
        person_emp_length: parseFloat(document.getElementById("input-emp").value),
        loan_int_rate: parseFloat(document.getElementById("input-rate").value),
        loan_percent_income: parseFloat(document.getElementById("input-dti").value),
        person_home_ownership: document.getElementById("input-home").value,
        cb_person_default_on_file: document.getElementById("input-default").value
    };

    try {
        const response = await fetch("/api/simulate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error("Error en simulación");
        const data = await response.json();
        renderSimulationResults(data);
    } catch (err) {
        console.error("Simulation request error:", err);
    }
}

function renderSimulationResults(data) {
    const scoreElem = document.getElementById("result-score");
    const probElem = document.getElementById("result-prob");
    const probMeter = document.getElementById("meter-prob-fill");
    const oddsElem = document.getElementById("result-odds");
    const tierElem = document.getElementById("result-tier");
    const badgeElem = document.getElementById("result-decision-badge");
    const textElem = document.getElementById("result-decision-text");
    const recElem = document.getElementById("result-recommendation");
    const driversElem = document.getElementById("result-drivers-list");
    const gaugeFill = document.getElementById("gauge-fill");

    if (scoreElem) scoreElem.textContent = data.score;
    if (probElem) probElem.textContent = `${data.default_probability_pct.toFixed(2)}%`;
    if (probMeter) probMeter.style.width = `${Math.min(data.default_probability_pct, 100)}%`;

    // Compute Odds
    const p = Math.max(0.001, data.default_probability_pct / 100);
    const odds = (1 - p) / p;
    if (oddsElem) oddsElem.textContent = odds >= 1 ? `${odds.toFixed(1)} : 1` : `1 : ${(1 / odds).toFixed(1)}`;

    if (tierElem) tierElem.textContent = data.tier;
    if (recElem) recElem.textContent = data.recommendation;

    // Decision Badge Color
    if (badgeElem && textElem) {
        badgeElem.className = "decision-badge";
        textElem.textContent = data.decision;

        if (data.score >= 670) {
            badgeElem.classList.add("badge-approved");
        } else if (data.score >= 530) {
            badgeElem.classList.add("badge-review");
        } else {
            badgeElem.classList.add("badge-rejected");
        }
    }

    // Radial Gauge Animation
    if (gaugeFill) {
        const totalLen = 251.2;
        const ratio = Math.max(0, Math.min(1, (data.score - 300) / (850 - 300)));
        const offset = totalLen * (1 - ratio);
        gaugeFill.style.strokeDashoffset = offset;

        if (data.score >= 740) {
            gaugeFill.style.stroke = "#10b981"; // Emerald
        } else if (data.score >= 650) {
            gaugeFill.style.stroke = "#38bdf8"; // Cyan
        } else if (data.score >= 550) {
            gaugeFill.style.stroke = "#f59e0b"; // Amber
        } else {
            gaugeFill.style.stroke = "#f43f5e"; // Rose
        }
    }

    // Drivers
    if (driversElem && data.drivers) {
        driversElem.innerHTML = data.drivers.map(d => `
            <div class="driver-item ${d.impact}">
                <span>${d.factor}</span>
                <span class="driver-points">${d.points > 0 ? '+' : ''}${d.points} pts</span>
            </div>
        `).join("");
    }
}

/* ==============================================================================
   OVERVIEW & SPLITS DATA
   ============================================================================== */
async function loadOverviewData() {
    try {
        const res = await fetch("/api/overview");
        if (!res.ok) return;
        const data = await res.json();

        // Update KPIs
        const kpiTotal = document.getElementById("kpi-total");
        const kpiDef = document.getElementById("kpi-default-rate");
        const kpiAuc = document.getElementById("kpi-auc");
        const kpiGini = document.getElementById("kpi-gini");

        if (kpiTotal) kpiTotal.textContent = data.kpis.total_records.toLocaleString();
        if (kpiDef) kpiDef.textContent = `${data.kpis.global_default_rate}%`;
        if (kpiAuc) kpiAuc.textContent = data.kpis.test_auc.toFixed(4);
        if (kpiGini) kpiGini.textContent = data.kpis.test_gini.toFixed(4);

        // Splits Table
        const tbody = document.getElementById("table-splits-body");
        if (tbody && data.splits) {
            tbody.innerHTML = data.splits.map(s => `
                <tr>
                    <td><strong>${s.split}</strong></td>
                    <td>${s.observations.toLocaleString()}</td>
                    <td>${((s.observations / data.kpis.total_records) * 100).toFixed(1)}%</td>
                    <td>${s.defaults.toLocaleString()}</td>
                    <td><span class="pill-badge pill-mod">${s.default_rate}%</span></td>
                    <td>${s.purpose}</td>
                </tr>
            `).join("");
        }

        // Render Splits Chart
        renderSplitsChart(data.splits);
    } catch (err) {
        console.error("Overview fetch error:", err);
    }
}

function renderSplitsChart(splits) {
    const canvas = document.getElementById("chart-splits");
    if (!canvas) return;

    new Chart(canvas, {
        type: "bar",
        data: {
            labels: splits.map(s => s.split),
            datasets: [
                {
                    label: "Tasa de Default (%)",
                    data: splits.map(s => s.default_rate),
                    backgroundColor: "rgba(56, 189, 248, 0.75)",
                    borderColor: "#38bdf8",
                    borderWidth: 1.5,
                    borderRadius: 6,
                    yAxisID: "y"
                },
                {
                    label: "Volumen (Observaciones)",
                    data: splits.map(s => s.observations),
                    type: "line",
                    borderColor: "#a5b4fc",
                    backgroundColor: "rgba(165, 180, 252, 0.2)",
                    borderWidth: 2,
                    pointBackgroundColor: "#6366f1",
                    pointRadius: 5,
                    yAxisID: "y1"
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { mode: "index", intersect: false },
            scales: {
                x: {
                    grid: { color: "rgba(255, 255, 255, 0.05)" },
                    ticks: { color: "#94a3b8" }
                },
                y: {
                    type: "linear",
                    display: true,
                    position: "left",
                    min: 0,
                    max: 30,
                    title: { display: true, text: "Tasa de Impago (%)", color: "#38bdf8" },
                    grid: { color: "rgba(255, 255, 255, 0.05)" },
                    ticks: { color: "#94a3b8" }
                },
                y1: {
                    type: "linear",
                    display: true,
                    position: "right",
                    grid: { drawOnChartArea: false },
                    title: { display: true, text: "Volumen", color: "#a5b4fc" },
                    ticks: { color: "#94a3b8" }
                }
            },
            plugins: {
                legend: { labels: { color: "#f8fafc" } }
            }
        }
    });
}

/* ==============================================================================
   FEATURE DISCRIMINATION CHARTS
   ============================================================================== */
async function loadDistributionCharts() {
    try {
        const res = await fetch("/api/distributions");
        if (!res.ok) return;
        const data = await res.json();

        // 1. Home Ownership Chart
        const ctxOwner = document.getElementById("chart-ownership");
        if (ctxOwner && data.home_ownership) {
            new Chart(ctxOwner, {
                type: "bar",
                data: {
                    labels: data.home_ownership.map(d => d.category),
                    datasets: [{
                        label: "Tasa de Default (%)",
                        data: data.home_ownership.map(d => d.default_rate),
                        backgroundColor: [
                            "#f43f5e", // RENT (Highest risk)
                            "#3b82f6", // MORTGAGE
                            "#10b981", // OWN (Lowest risk)
                            "#94a3b8"  // OTHER
                        ],
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { grid: { display: false }, ticks: { color: "#94a3b8" } },
                        y: {
                            min: 0,
                            max: 40,
                            grid: { color: "rgba(255, 255, 255, 0.05)" },
                            ticks: { color: "#94a3b8", callback: v => `${v}%` }
                        }
                    },
                    plugins: { legend: { display: false } }
                }
            });
        }

        // 2. Loan Grades Chart
        const ctxGrades = document.getElementById("chart-grades");
        if (ctxGrades && data.loan_grade) {
            new Chart(ctxGrades, {
                type: "line",
                data: {
                    labels: data.loan_grade.map(d => `Grado ${d.grade}`),
                    datasets: [{
                        label: "Tasa de Impago (%)",
                        data: data.loan_grade.map(d => d.default_rate),
                        borderColor: "#38bdf8",
                        backgroundColor: "rgba(56, 189, 248, 0.15)",
                        fill: true,
                        tension: 0.3,
                        pointBackgroundColor: "#38bdf8",
                        pointRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { grid: { color: "rgba(255, 255, 255, 0.05)" }, ticks: { color: "#94a3b8" } },
                        y: {
                            min: 0,
                            max: 100,
                            grid: { color: "rgba(255, 255, 255, 0.05)" },
                            ticks: { color: "#94a3b8", callback: v => `${v}%` }
                        }
                    },
                    plugins: { legend: { display: false } }
                }
            });
        }
    } catch (err) {
        console.error("Distribution charts error:", err);
    }
}

/* ==============================================================================
   STABILITY & PSI DATA
   ============================================================================== */
async function loadStabilityData() {
    try {
        const res = await fetch("/api/stability");
        if (!res.ok) return;
        const data = await res.json();

        // PSI Splits Table
        const tbody = document.getElementById("table-psi-splits-body");
        if (tbody && data.splits_psi) {
            tbody.innerHTML = data.splits_psi.map(row => `
                <tr>
                    <td><code>${row.variable}</code></td>
                    <td>${row.train_vs_test.toFixed(4)}</td>
                    <td>${row.train_vs_oot.toFixed(4)}</td>
                    <td>${row.test_vs_oot.toFixed(4)}</td>
                    <td><span class="badge-stable">✓ ${row.status} (&lt; 0.10)</span></td>
                </tr>
            `).join("");
        }

        // Year to Year PSI Chart
        const ctxY2Y = document.getElementById("chart-y2y-psi");
        if (ctxY2Y && data.y2y_psi) {
            new Chart(ctxY2Y, {
                type: "line",
                data: {
                    labels: data.y2y_psi.map(d => d.year),
                    datasets: [
                        {
                            label: "person_income",
                            data: data.y2y_psi.map(d => d.person_income),
                            borderColor: "#38bdf8",
                            borderWidth: 2,
                            tension: 0.2
                        },
                        {
                            label: "person_emp_length",
                            data: data.y2y_psi.map(d => d.person_emp_length),
                            borderColor: "#34d399",
                            borderWidth: 2,
                            tension: 0.2
                        },
                        {
                            label: "loan_percent_income",
                            data: data.y2y_psi.map(d => d.loan_percent_income),
                            borderColor: "#fbbf24",
                            borderWidth: 2,
                            tension: 0.2
                        },
                        {
                            label: "loan_int_rate",
                            data: data.y2y_psi.map(d => d.loan_int_rate),
                            borderColor: "#f43f5e",
                            borderWidth: 2,
                            tension: 0.2
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { grid: { color: "rgba(255, 255, 255, 0.05)" }, ticks: { color: "#94a3b8" } },
                        y: {
                            min: 0,
                            max: 0.08,
                            grid: { color: "rgba(255, 255, 255, 0.05)" },
                            ticks: { color: "#94a3b8" },
                            title: { display: true, text: "Índice PSI (Umbral Crítico = 0.10)", color: "#94a3b8" }
                        }
                    },
                    plugins: {
                        legend: { labels: { color: "#f8fafc" } }
                    }
                }
            });
        }
    } catch (err) {
        console.error("Stability fetch error:", err);
    }
}

/* ==============================================================================
   VARIABLE SELECTION (7 FEATURES)
   ============================================================================== */
async function loadFeaturesData() {
    try {
        const res = await fetch("/api/features");
        if (!res.ok) return;
        const data = await res.json();

        const tbody = document.getElementById("table-final-features-body");
        if (tbody && data.final_features) {
            tbody.innerHTML = data.final_features.map((f, idx) => `
                <tr>
                    <td><strong>${idx + 1}</strong></td>
                    <td><code>${f.name}</code></td>
                    <td><span class="pill-badge ${f.type === 'Continua' ? 'pill-mid' : 'pill-mod'}">${f.type}</span></td>
                    <td><strong>${f.label}</strong></td>
                    <td>
                        <div style="display: flex; align-items: center; gap: 0.5rem;">
                            <div class="meter-bar" style="width: 80px;">
                                <div class="meter-fill" style="width: ${f.importance * 100 * 2.5}%;"></div>
                            </div>
                            <span style="font-family: var(--font-mono); font-size: 0.78rem;">${(f.importance * 100).toFixed(0)}%</span>
                        </div>
                    </td>
                    <td>${f.role}</td>
                </tr>
            `).join("");
        }
    } catch (err) {
        console.error("Features fetch error:", err);
    }
}
