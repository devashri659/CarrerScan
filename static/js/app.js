/**
 * CareerScan — AI-Powered Job Offer Risk Checker
 * Frontend Application Controller
 */

document.addEventListener("DOMContentLoaded", () => {
  // Initialize Lucide icons
  if (window.lucide) {
    window.lucide.createIcons();
  }

  // State Management
  const state = {
    currentView: "home",
    samples: {},
    historyItems: [],
    currentFilter: "all",
    lastResult: null
  };

  // DOM Elements
  const navHome = document.getElementById("navHome");
  const navHistory = document.getElementById("navHistory");
  const navAbout = document.getElementById("navAbout");
  const historyCounter = document.getElementById("historyCounter");

  const viewHome = document.getElementById("viewHome");
  const viewHistory = document.getElementById("viewHistory");
  const viewAbout = document.getElementById("viewAbout");

  const mobileToggleBtn = document.getElementById("mobileToggleBtn");
  const sidebar = document.getElementById("sidebar");
  const sidebarOverlay = document.getElementById("sidebarOverlay");
  const brandLogoBtn = document.getElementById("brandLogoBtn");

  const userProfileBtn = document.getElementById("userProfileBtn");
  const profileDropdown = document.getElementById("profileDropdown");

  const jobScanForm = document.getElementById("jobScanForm");
  const offerText = document.getElementById("offerText");
  const companyName = document.getElementById("companyName");
  const recruiterEmail = document.getElementById("recruiterEmail");
  const analyzeBtn = document.getElementById("analyzeBtn");
  const btnContent = analyzeBtn.querySelector(".btn-content");
  const btnSpinner = analyzeBtn.querySelector(".btn-spinner");

  const pdfFileInput = document.getElementById("pdfFileInput");
  const fileNameDisplay = document.getElementById("fileNameDisplay");

  const resultsSection = document.getElementById("resultsSection");
  const riskScoreNumber = document.getElementById("riskScoreNumber");
  const circleStroke = document.getElementById("circleStroke");
  const riskBadge = document.getElementById("riskBadge");
  const flagsCountTag = document.getElementById("flagsCountTag");
  const verdictHeadline = document.getElementById("verdictHeadline");
  const verdictSummary = document.getElementById("verdictSummary");
  const mlScamProbVal = document.getElementById("mlScamProbVal");
  const heuristicScoreVal = document.getElementById("heuristicScoreVal");
  const domainStatusVal = document.getElementById("domainStatusVal");
  const domainStatusDesc = document.getElementById("domainStatusDesc");
  const redFlagsContainer = document.getElementById("redFlagsContainer");
  const redFlagsCountLabel = document.getElementById("redFlagsCountLabel");
  const recommendationsList = document.getElementById("recommendationsList");
  const resultsMetaSubtitle = document.getElementById("resultsMetaSubtitle");

  const printReportBtn = document.getElementById("printReportBtn");
  const newScanBtn = document.getElementById("newScanBtn");

  const historyTableBody = document.getElementById("historyTableBody");
  const clearAllHistoryBtn = document.getElementById("clearAllHistoryBtn");
  const filterTabBtns = document.querySelectorAll(".filter-tab-btn");

  // ==================== 1. NAVIGATION & VIEW SWITCHING ====================
  function switchView(viewName) {
    state.currentView = viewName;

    // Update Sidebar Item Active States
    [navHome, navHistory, navAbout].forEach(item => item.classList.remove("active"));
    [viewHome, viewHistory, viewAbout].forEach(view => {
      view.style.display = "none";
      view.classList.remove("active");
    });

    if (viewName === "home") {
      navHome.classList.add("active");
      viewHome.style.display = "block";
      viewHome.classList.add("active");
      window.location.hash = "home";
    } else if (viewName === "history") {
      navHistory.classList.add("active");
      viewHistory.style.display = "block";
      viewHistory.classList.add("active");
      window.location.hash = "history";
      fetchHistory();
    } else if (viewName === "about") {
      navAbout.classList.add("active");
      viewAbout.style.display = "block";
      viewAbout.classList.add("active");
      window.location.hash = "about";
    }

    // Close Mobile Drawer if open
    closeMobileSidebar();
    profileDropdown.classList.remove("open");

    // Refresh icons
    if (window.lucide) {
      window.lucide.createIcons();
    }
  }

  // Sidebar link clicks
  navHome.addEventListener("click", (e) => {
    e.preventDefault();
    switchView("home");
  });

  navHistory.addEventListener("click", (e) => {
    e.preventDefault();
    switchView("history");
  });

  navAbout.addEventListener("click", (e) => {
    e.preventDefault();
    switchView("about");
  });

  brandLogoBtn.addEventListener("click", (e) => {
    e.preventDefault();
    switchView("home");
  });

  // Mobile drawer controls
  function openMobileSidebar() {
    sidebar.classList.add("mobile-open");
    sidebarOverlay.classList.add("active");
  }

  function closeMobileSidebar() {
    sidebar.classList.remove("mobile-open");
    sidebarOverlay.classList.remove("active");
  }

  mobileToggleBtn.addEventListener("click", openMobileSidebar);
  sidebarOverlay.addEventListener("click", closeMobileSidebar);

  // Profile Dropdown Toggle
  userProfileBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    profileDropdown.classList.toggle("open");
  });

  document.addEventListener("click", (e) => {
    if (!profileDropdown.contains(e.target) && !userProfileBtn.contains(e.target)) {
      profileDropdown.classList.remove("open");
    }
  });

  document.querySelectorAll("[data-navigate]").forEach(item => {
    item.addEventListener("click", (e) => {
      e.preventDefault();
      const target = item.getAttribute("data-navigate");
      switchView(target);
    });
  });

  // ==================== 2. QUICK DEMO SAMPLES ====================
  async function loadSamples() {
    try {
      const res = await fetch("/api/samples");
      const data = await res.json();
      if (data.success && data.samples) {
        state.samples = data.samples;
      }
    } catch (err) {
      console.warn("Could not preload samples from API:", err);
    }
  }

  document.querySelectorAll(".sample-pill").forEach(pill => {
    pill.addEventListener("click", () => {
      const sampleKey = pill.getAttribute("data-sample");
      const sample = state.samples[sampleKey];
      if (sample) {
        offerText.value = sample.text;
        companyName.value = sample.company || "";
        recruiterEmail.value = sample.email || "";
        fileNameDisplay.style.display = "none";
        fileNameDisplay.textContent = "";

        showToast(`Loaded "${sample.title}"`, "info");
        offerText.focus();
        offerText.scrollIntoView({ behavior: "smooth", block: "center" });
      }
    });
  });

  // ==================== 3. PDF & FILE UPLOAD ====================
  pdfFileInput.addEventListener("change", async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    fileNameDisplay.textContent = file.name;
    fileNameDisplay.style.display = "inline-block";

    const formData = new FormData();
    formData.append("file", file);

    showToast(`Parsing ${file.name}...`, "info");

    try {
      const res = await fetch("/api/extract-pdf", {
        method: "POST",
        body: formData
      });
      const data = await res.json();

      if (data.success && data.extracted_text) {
        offerText.value = data.extracted_text;
        showToast("Text extracted from document successfully!", "success");
        offerText.scrollIntoView({ behavior: "smooth", block: "center" });
      } else {
        showToast(data.error || "Failed to extract text from file.", "error");
      }
    } catch (err) {
      showToast("Error uploading or extracting document.", "error");
      console.error(err);
    }
  });

  // Drag and drop onto textarea
  offerText.addEventListener("dragover", (e) => {
    e.preventDefault();
    offerText.style.borderColor = "var(--primary-blue)";
    offerText.style.backgroundColor = "var(--primary-blue-light)";
  });

  offerText.addEventListener("dragleave", (e) => {
    e.preventDefault();
    offerText.style.borderColor = "";
    offerText.style.backgroundColor = "";
  });

  offerText.addEventListener("drop", async (e) => {
    e.preventDefault();
    offerText.style.borderColor = "";
    offerText.style.backgroundColor = "";

    const files = e.dataTransfer.files;
    if (files.length > 0) {
      const file = files[0];
      if (file.name.endsWith(".pdf") || file.name.endsWith(".txt")) {
        pdfFileInput.files = files;
        const changeEvent = new Event("change");
        pdfFileInput.dispatchEvent(changeEvent);
      } else {
        showToast("Please drop a .pdf or .txt file.", "error");
      }
    }
  });

  // ==================== 4. FORM SUBMISSION & ANALYSIS ====================
  jobScanForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const textVal = offerText.value.trim();
    const compVal = companyName.value.trim();
    const emailVal = recruiterEmail.value.trim();

    if (!textVal) {
      showToast("Please paste the job offer text or upload a document.", "error");
      offerText.focus();
      return;
    }

    // Set Loading State
    analyzeBtn.disabled = true;
    btnContent.style.display = "none";
    btnSpinner.style.display = "flex";

    try {
      const res = await fetch("/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          text: textVal,
          company: compVal,
          email: emailVal
        })
      });

      const data = await res.json();

      if (data.success && data.result) {
        state.lastResult = data.result;
        renderResults(data.result);
        showToast("Risk analysis complete!", "success");
        updateHistoryCount();
      } else {
        showToast(data.error || "Failed to analyze offer.", "error");
      }
    } catch (err) {
      console.error(err);
      showToast("Network error while connecting to CareerScan backend.", "error");
    } finally {
      analyzeBtn.disabled = false;
      btnContent.style.display = "flex";
      btnSpinner.style.display = "none";
    }
  });

  // ==================== 5. RESULTS DISPLAY & RENDERING ====================
  function renderResults(result) {
    resultsSection.style.display = "block";

    const score = result.risk_score || 0;
    const badgeColor = result.badge_color || "#0866E8";

    // 1. Circular Gauge & Score
    riskScoreNumber.textContent = score;
    circleStroke.setAttribute("stroke-dasharray", `${score}, 100`);
    circleStroke.style.stroke = badgeColor;

    // 2. Verdict Badge & Headline
    riskBadge.textContent = result.risk_level.toUpperCase();
    riskBadge.style.color = badgeColor;
    if (result.risk_level === "High Risk") {
      riskBadge.style.backgroundColor = "var(--high-risk-bg)";
      verdictHeadline.textContent = "High Probability of Employment Fraud";
    } else if (result.risk_level === "Moderate Risk") {
      riskBadge.style.backgroundColor = "var(--warning-bg)";
      verdictHeadline.textContent = "Suspicious Elements Detected — Proceed with Caution";
    } else {
      riskBadge.style.backgroundColor = "var(--success-bg)";
      verdictHeadline.textContent = "Likely Legitimate Employment Offer";
    }

    flagsCountTag.textContent = `${result.flags_count || 0} Red Flags Detected`;
    verdictSummary.textContent = result.summary || "";
    resultsMetaSubtitle.textContent = `Company: ${result.company_name} • Recruiter: ${result.recruiter_email}`;

    // 3. Three Insight Cards
    const mlProba = result.ml_metrics?.scam_probability ?? 0;
    mlScamProbVal.textContent = `${mlProba}%`;

    const heurScore = result.ml_metrics?.heuristic_score ?? 0;
    heuristicScoreVal.textContent = `${heurScore}/100`;

    const domainInfo = result.domain_analysis;
    if (domainInfo) {
      if (domainInfo.is_brand_mismatch) {
        domainStatusVal.textContent = "Impersonation Alert";
        domainStatusVal.style.color = "var(--high-risk-indicator)";
        domainStatusDesc.textContent = "Claimed company does not match email domain.";
      } else if (domainInfo.is_free_provider) {
        domainStatusVal.textContent = "Public Webmail";
        domainStatusVal.style.color = "var(--warning-indicator)";
        domainStatusDesc.textContent = `Recruiter uses @${domainInfo.domain}.`;
      } else if (domainInfo.domain) {
        domainStatusVal.textContent = `@${domainInfo.domain}`;
        domainStatusVal.style.color = "var(--success-indicator)";
        domainStatusDesc.textContent = "Corporate email domain detected.";
      } else {
        domainStatusVal.textContent = "Not provided";
        domainStatusVal.style.color = "var(--secondary-text)";
        domainStatusDesc.textContent = "No recruiter email specified.";
      }
    }

    // 4. Render Red Flags List
    redFlagsContainer.innerHTML = "";
    const flags = result.flags || [];
    redFlagsCountLabel.textContent = flags.length;

    if (flags.length === 0) {
      redFlagsContainer.innerHTML = `
        <div class="empty-state-box" style="padding: 20px;">
          <i data-lucide="shield-check" style="width: 36px; height: 36px; color: var(--success-indicator);"></i>
          <p style="color: var(--secondary-text); margin: 0;">No prominent scam keywords or heuristic red flags were flagged in this offer.</p>
        </div>
      `;
    } else {
      flags.forEach(flag => {
        const severityClass = (flag.severity || "medium").toLowerCase();
        const flagCard = document.createElement("div");
        flagCard.className = `flag-item-card ${severityClass}`;

        flagCard.innerHTML = `
          <div class="flag-top-row">
            <div class="flag-title-group">
              <span class="flag-name">${escapeHtml(flag.title)}</span>
              <span class="flag-category-badge">${escapeHtml(flag.category || "General")}</span>
            </div>
            <span class="severity-pill ${severityClass}">${escapeHtml(flag.severity || "Warning")}</span>
          </div>
          ${flag.snippet ? `<div class="flag-snippet">"${escapeHtml(flag.snippet)}"</div>` : ""}
          <div class="flag-explanation">${escapeHtml(flag.description || "")}</div>
        `;
        redFlagsContainer.appendChild(flagCard);
      });
    }

    // 5. Render Recommendations
    recommendationsList.innerHTML = "";
    const recs = result.recommendations || [];
    recs.forEach(rec => {
      const li = document.createElement("li");
      li.className = "rec-item";
      li.innerHTML = `
        <i data-lucide="check-circle-2" class="rec-bullet-icon"></i>
        <span>${escapeHtml(rec)}</span>
      `;
      recommendationsList.appendChild(li);
    });

    if (window.lucide) {
      window.lucide.createIcons();
    }

    // Smooth scroll down to results
    resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  // Clear / New Scan Button
  newScanBtn.addEventListener("click", () => {
    jobScanForm.reset();
    fileNameDisplay.style.display = "none";
    fileNameDisplay.textContent = "";
    resultsSection.style.display = "none";
    offerText.focus();
    offerText.scrollIntoView({ behavior: "smooth", block: "center" });
  });

  // Print Report Button
  printReportBtn.addEventListener("click", () => {
    window.print();
  });

  // ==================== 6. SCAN HISTORY VIEW ====================
  async function fetchHistory() {
    try {
      const res = await fetch("/api/history");
      const data = await res.json();
      if (data.success && data.scans) {
        state.historyItems = data.scans;
        renderHistoryTable();
        historyCounter.textContent = data.scans.length;
      }
    } catch (err) {
      console.error("Failed to load history:", err);
    }
  }

  async function updateHistoryCount() {
    try {
      const res = await fetch("/api/history");
      const data = await res.json();
      if (data.success && data.scans) {
        historyCounter.textContent = data.scans.length;
      }
    } catch (err) {}
  }

  function renderHistoryTable() {
    const filter = state.currentFilter;
    let filtered = state.historyItems;

    if (filter === "high") {
      filtered = state.historyItems.filter(s => s.risk_level === "High Risk");
    } else if (filter === "moderate") {
      filtered = state.historyItems.filter(s => s.risk_level === "Moderate Risk");
    } else if (filter === "low") {
      filtered = state.historyItems.filter(s => s.risk_level === "Low Risk");
    }

    historyTableBody.innerHTML = "";

    if (filtered.length === 0) {
      historyTableBody.innerHTML = `
        <tr>
          <td colspan="7" class="empty-state-cell">
            <div class="empty-state-box">
              <i data-lucide="inbox" class="empty-icon"></i>
              <p>No scans found matching the selected filter.</p>
            </div>
          </td>
        </tr>
      `;
      if (window.lucide) window.lucide.createIcons();
      return;
    }

    filtered.forEach(scan => {
      const tr = document.createElement("tr");

      let badgeBg = "var(--success-bg)";
      let badgeCol = "var(--success-indicator)";
      if (scan.risk_level === "High Risk") {
        badgeBg = "var(--high-risk-bg)";
        badgeCol = "var(--high-risk-indicator)";
      } else if (scan.risk_level === "Moderate Risk") {
        badgeBg = "var(--warning-bg)";
        badgeCol = "var(--warning-indicator)";
      }

      tr.innerHTML = `
        <td style="white-space: nowrap; font-size: 13px; color: var(--secondary-text);">${escapeHtml(scan.timestamp)}</td>
        <td style="font-weight: 600;">${escapeHtml(scan.company_name || "—")}</td>
        <td style="color: var(--secondary-text);">${escapeHtml(scan.recruiter_email || "—")}</td>
        <td><div class="table-snippet" title="${escapeHtml(scan.snippet)}">${escapeHtml(scan.snippet)}</div></td>
        <td style="font-weight: 700;">${scan.risk_score}%</td>
        <td>
          <span class="table-badge" style="background-color: ${badgeBg}; color: ${badgeCol};">
            ${escapeHtml(scan.risk_level)}
          </span>
        </td>
        <td>
          <div class="table-actions">
            <button type="button" class="table-action-btn view" data-id="${scan.id}" title="View detailed report">
              <i data-lucide="external-link"></i> View
            </button>
            <button type="button" class="table-action-btn delete" data-id="${scan.id}" title="Delete record">
              <i data-lucide="trash"></i>
            </button>
          </div>
        </td>
      `;

      historyTableBody.appendChild(tr);
    });

    // Attach View and Delete action handlers
    historyTableBody.querySelectorAll(".table-action-btn.view").forEach(btn => {
      btn.addEventListener("click", () => {
        const id = btn.getAttribute("data-id");
        viewScanDetails(id);
      });
    });

    historyTableBody.querySelectorAll(".table-action-btn.delete").forEach(btn => {
      btn.addEventListener("click", () => {
        const id = btn.getAttribute("data-id");
        deleteScanItem(id);
      });
    });

    if (window.lucide) window.lucide.createIcons();
  }

  // Filter tabs click
  filterTabBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      filterTabBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      state.currentFilter = btn.getAttribute("data-filter");
      renderHistoryTable();
    });
  });

  // View past report details
  async function viewScanDetails(id) {
    try {
      const res = await fetch(`/api/history/${id}`);
      const data = await res.json();
      if (data.success && data.scan && data.scan.report) {
        switchView("home");
        renderResults(data.scan.report);
        showToast("Loaded past scan report from history.", "info");
      }
    } catch (err) {
      showToast("Error retrieving scan details.", "error");
    }
  }

  // Delete single history item
  async function deleteScanItem(id) {
    if (!confirm("Are you sure you want to delete this scan record?")) return;

    try {
      const res = await fetch(`/api/history/${id}`, { method: "DELETE" });
      const data = await res.json();
      if (data.success) {
        showToast("Scan deleted from history.", "success");
        fetchHistory();
      } else {
        showToast("Failed to delete record.", "error");
      }
    } catch (err) {
      showToast("Network error deleting record.", "error");
    }
  }

  // Clear all history
  clearAllHistoryBtn.addEventListener("click", async () => {
    if (state.historyItems.length === 0) {
      showToast("Scan history is already empty.", "info");
      return;
    }

    if (!confirm("Are you sure you want to delete ALL scan history? This action cannot be undone.")) return;

    try {
      const res = await fetch("/api/history/clear", { method: "POST" });
      const data = await res.json();
      if (data.success) {
        showToast("All history cleared.", "success");
        fetchHistory();
      }
    } catch (err) {
      showToast("Failed to clear history.", "error");
    }
  });

  // ==================== 7. TOAST NOTIFICATION UTILITY ====================
  function showToast(message, type = "info") {
    const container = document.getElementById("toastContainer");
    const toast = document.createElement("div");
    toast.className = `toast ${type}`;

    let iconName = "info";
    if (type === "success") iconName = "check-circle";
    if (type === "error") iconName = "alert-circle";

    toast.innerHTML = `
      <i data-lucide="${iconName}"></i>
      <span>${escapeHtml(message)}</span>
    `;

    container.appendChild(toast);
    if (window.lucide) window.lucide.createIcons();

    setTimeout(() => {
      toast.style.opacity = "0";
      toast.style.transform = "translateX(30px)";
      toast.style.transition = "all 0.3s ease";
      setTimeout(() => toast.remove(), 300);
    }, 3800);
  }

  // Utility to escape HTML strings safely
  function escapeHtml(str) {
    if (str === null || str === undefined) return "";
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  // ==================== 8. INITIALIZATION ====================
  loadSamples();
  updateHistoryCount();

  // Handle URL hash on initial load
  const hash = window.location.hash.replace("#", "");
  if (hash === "history" || hash === "about") {
    switchView(hash);
  } else {
    switchView("home");
  }
});
