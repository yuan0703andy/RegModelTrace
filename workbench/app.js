const ROLE_LABELS = {
  STANDARDS: "Standards",
  PROFESSIONAL_TEAM_REPORT: "Professional Team",
  VENDOR_SUBMISSION: "Vendor submission",
};

const STAGE_LABELS = {
  SEARCHABLE: "Searchable",
  RETRIEVED: "Retrieved",
  RETAINED_AFTER_RANKING: "Retained after ranking",
  INCLUDED_IN_MODEL_CONTEXT: "Included in model context",
  MODEL_SELECTED: "Model selected",
  HOST_RESOLVED: "Host resolved",
  DELIVERED_TO_HUMAN: "Delivered to human",
  HUMAN_VERIFIED: "Human verified",
};

const state = { caseData: null, activeId: null, detail: null, activePage: null };
const el = (id) => document.getElementById(id);

function escapeHtml(value = "") {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function formatScore(value) {
  return value === null || value === undefined ? "-" : Number(value).toFixed(5);
}

function candidateCard(candidate) {
  const active = candidate.candidate_id === state.activeId;
  return `<button class="candidate-card" type="button" data-candidate-id="${escapeHtml(candidate.candidate_id)}" aria-current="${active}">
    <span class="role-dot ${candidate.document_role.toLowerCase()}"></span>
    <span class="candidate-copy">
      <strong>${escapeHtml(ROLE_LABELS[candidate.document_role])} - p.${candidate.pages.join(", ")}</strong>
      <span>${escapeHtml(candidate.text)}</span>
      <small>Role rank ${escapeHtml(candidate.scores.role_rank)}</small>
    </span>
  </button>`;
}

function renderCandidateList() {
  el("candidate-list").innerHTML = state.caseData.candidates.map(candidateCard).join("");
  document.querySelectorAll("[data-candidate-id]").forEach((button) => {
    button.addEventListener("click", () => selectCandidate(button.dataset.candidateId));
  });
}

function renderCaseHeader() {
  const data = state.caseData;
  el("question").textContent = data.question;
  el("run-id").textContent = data.retrieval_run_id;
  el("corpus-id").textContent = data.corpus_snapshot_id;
  el("index-id").textContent = data.index_build_id;
  el("scope").textContent = data.candidate_universe_scope;
  el("candidate-count").textContent = `${data.candidate_count} candidates`;
}

function renderStages(ledger) {
  el("stage-ledger").innerHTML = Object.entries(ledger).map(([stage, item]) => `
    <div class="stage-row ${item.state.toLowerCase().replaceAll("_", "-")}">
      <span class="stage-marker"></span>
      <span>${escapeHtml(STAGE_LABELS[stage])}</span>
      <strong>${escapeHtml(item.state)}</strong>
    </div>`).join("");
}

function renderPage(physicalPage) {
  state.activePage = physicalPage;
  const nav = state.detail.navigation;
  const page = nav.page_views.find((item) => item.physical_page === physicalPage);
  if (!page) return;
  const imageUrl = nav.page_image_url_template.replace("{physical_page}", physicalPage);
  el("page-tabs").querySelectorAll("button").forEach((button) => {
    button.setAttribute("aria-current", String(Number(button.dataset.page) === physicalPage));
  });
  el("open-pdf").href = `${nav.pdf_url}#page=${physicalPage}`;
  const stage = el("page-stage");
  stage.innerHTML = `<div class="page-canvas">
    <img src="${escapeHtml(imageUrl)}" alt="Authoritative PDF physical page ${physicalPage}" />
    ${page.regions.map((region) => `<span class="source-highlight" style="left:${region.left_percent}%;top:${region.top_percent}%;width:${region.width_percent}%;height:${region.height_percent}%"></span>`).join("")}
  </div>`;
}

function renderNavigation(detail) {
  const nav = detail.navigation;
  el("precision-badge").textContent = nav.location_precision;
  el("precision-badge").className = `precision-badge ${nav.location_precision.toLowerCase()}`;
  el("warning-text").textContent = nav.warnings.join(" - ");
  const hasGeometry = nav.page_views.some((page) => page.regions.length > 0);
  const fallback = el("fallback-note");
  fallback.hidden = hasGeometry;
  fallback.textContent = nav.location_precision === "PAGE_ONLY"
    ? "Exact text and geometry are unavailable. Navigation is limited to the verified physical page."
    : "Exact geometry is unavailable. The verified page and source text remain authoritative.";
  el("page-tabs").innerHTML = nav.page_views.map((page) => `
    <button type="button" data-page="${page.physical_page}">Page ${page.physical_page}</button>`).join("");
  el("page-tabs").querySelectorAll("button").forEach((button) => {
    button.addEventListener("click", () => renderPage(Number(button.dataset.page)));
  });
  renderPage(nav.page_views[0].physical_page);
}

function renderDetail() {
  const detail = state.detail;
  el("role-badge").textContent = ROLE_LABELS[detail.document_role];
  el("role-badge").className = `role-badge ${detail.document_role.toLowerCase()}`;
  el("candidate-id").textContent = detail.candidate_id;
  el("document-title").textContent = detail.document_title;
  el("candidate-text").textContent = detail.text;
  el("page-label").textContent = detail.pages.join(", ");
  el("bm25-rank").textContent = detail.scores.bm25_rank ?? "-";
  el("dense-rank").textContent = detail.scores.dense_rank ?? "-";
  el("rrf-score").textContent = formatScore(detail.scores.rrf_score);
  el("role-rank").textContent = detail.scores.role_rank ?? "-";
  el("passage-id").textContent = detail.passage_id;
  el("document-id").textContent = detail.document_id;
  el("source-status").textContent = detail.source_status;
  renderStages(detail.stage_ledger);
  renderNavigation(detail);
}

async function selectCandidate(candidateId) {
  state.activeId = candidateId;
  renderCandidateList();
  el("page-stage").innerHTML = '<div class="page-loading">Resolving authoritative source...</div>';
  const response = await fetch(`/api/candidates/${encodeURIComponent(candidateId)}`);
  if (!response.ok) throw new Error(`Source resolution failed (${response.status})`);
  state.detail = await response.json();
  renderDetail();
  const url = new URL(window.location.href);
  url.searchParams.set("candidate", candidateId);
  history.replaceState(null, "", url);
}

async function init() {
  try {
    const response = await fetch("/api/case");
    if (!response.ok) throw new Error(`Case request failed (${response.status})`);
    state.caseData = await response.json();
    renderCaseHeader();
    const requested = new URL(window.location.href).searchParams.get("candidate");
    const valid = state.caseData.candidates.some((item) => item.candidate_id === requested);
    await selectCandidate(valid ? requested : state.caseData.candidates[0].candidate_id);
  } catch (error) {
    el("question").textContent = "The frozen review case could not be loaded.";
    el("page-stage").innerHTML = `<div class="page-loading error">${escapeHtml(error.message)}</div>`;
  }
}

init();
