const ROLE_ORDER = ["STANDARDS", "PROFESSIONAL_TEAM_REPORT", "VENDOR_SUBMISSION"];
const ROLE_LABELS = {
  STANDARDS: "Standards",
  PROFESSIONAL_TEAM_REPORT: "Professional Team report",
  VENDOR_SUBMISSION: "RMS submission",
};

const ROLE_CLASSES = {
  STANDARDS: "standards",
  PROFESSIONAL_TEAM_REPORT: "team",
  VENDOR_SUBMISSION: "vendor",
};

const state = { data: null, activeId: "Q8", filter: "" };

const el = (id) => document.getElementById(id);

function escapeHtml(value = "") {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function shortStatus(status) {
  return status === "SUPPORTED" ? "Supported" : "Unresolved";
}

function renderQuestionList() {
  const list = el("question-list");
  const query = state.filter.trim().toLowerCase();
  const cases = state.data.cases.filter((item) => item.question.toLowerCase().includes(query));
  if (!cases.length) {
    list.innerHTML = '<p class="empty-state">No frozen question matches this filter.</p>';
    return;
  }

  list.innerHTML = cases.map((item, index) => {
    const unresolved = item.status !== "SUPPORTED";
    return `
      <button class="question-button" type="button" data-question-id="${escapeHtml(item.id)}" aria-current="${item.id === state.activeId}">
        <span class="question-index">${String(index + 1).padStart(2, "0")}</span>
        <span class="question-copy">${escapeHtml(item.question)}</span>
        <span class="question-mini-status ${unresolved ? "unresolved" : ""}">${shortStatus(item.status)}</span>
      </button>`;
  }).join("");

  list.querySelectorAll("button[data-question-id]").forEach((button) => {
    button.addEventListener("click", () => {
      state.activeId = button.dataset.questionId;
      render();
      if (window.matchMedia("(max-width: 760px)").matches) {
        el("answer-panel").scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });
  });
}

function citationButton(source) {
  const pageLabel = source.page_label || (source.pages || []).join(", ");
  return `
    <button class="citation-chip" type="button" data-evidence-ref="${escapeHtml(source.evidence_ref)}" aria-label="Show source ${escapeHtml(source.evidence_ref)}, page ${escapeHtml(pageLabel)}">
      ${escapeHtml(source.evidence_ref)} · p.${escapeHtml(pageLabel)}
      <svg aria-hidden="true" viewBox="0 0 24 24"><path d="m9 18 6-6-6-6"/></svg>
    </button>`;
}

function evidenceCard(source) {
  const spans = (source.source_spans || []).map((span) => `<blockquote>${escapeHtml(span.quote)}</blockquote>`).join("");
  const link = source.source_links?.[0];
  return `
    <details class="evidence-card" id="source-${escapeHtml(source.evidence_ref)}" data-evidence-card="${escapeHtml(source.evidence_ref)}">
      <summary>
        <div class="source-meta">
          <span class="source-ref">${escapeHtml(source.evidence_ref)}</span>
          <span class="source-page">PAGE ${escapeHtml(source.page_label)}</span>
        </div>
        <p class="source-preview">“${escapeHtml(source.text)}”</p>
      </summary>
      <div class="source-detail">
        <p class="source-section"><strong>${escapeHtml(source.document_name)}</strong><br>${escapeHtml(source.section_label || "Document body")}</p>
        <div class="span-list" aria-label="Exact source spans">${spans}</div>
        ${link ? `<a class="open-source" href="${escapeHtml(link)}" target="_blank" rel="noopener noreferrer">
          Open original PDF · p.${escapeHtml(source.page_label)}
          <svg aria-hidden="true" viewBox="0 0 24 24"><path d="M14 4h6v6m0-6-9 9"/><path d="M19 13v6H5V5h6"/></svg>
        </a>` : ""}
      </div>
    </details>`;
}

function focusEvidence(ref) {
  document.querySelectorAll("[data-evidence-card]").forEach((card) => card.classList.remove("highlighted"));
  const card = document.querySelector(`[data-evidence-card="${CSS.escape(ref)}"]`);
  if (!card) return;
  card.open = true;
  card.classList.add("highlighted");
  card.scrollIntoView({ behavior: "smooth", block: "center" });
  card.querySelector("summary")?.focus({ preventScroll: true });
  window.setTimeout(() => card.classList.remove("highlighted"), 2400);
}

function renderActiveCase() {
  const item = state.data.cases.find((entry) => entry.id === state.activeId) || state.data.cases[0];
  const unresolved = item.status !== "SUPPORTED";
  const statusCard = el("status-card");

  el("case-number").textContent = `Question ${item.id.slice(1).padStart(2, "0")}`;
  el("active-question").textContent = item.question;
  statusCard.classList.toggle("unresolved", unresolved);
  el("status-label").textContent = unresolved ? "Unresolved from retrieved evidence" : "Supported by retrieved evidence";
  el("status-explanation").textContent = unresolved
    ? "The retrieved bundle does not establish the requested link or comparison. This does not show that the fixed corpus lacks the evidence or that the event did not occur."
    : "The answer below is supported by the cited assertions in the retrieved bundle.";
  el("claim-count").textContent = `${item.claims.length} ${item.claims.length === 1 ? "claim" : "claims"}`;

  el("claims").innerHTML = item.claims.map((claim, index) => `
    <article class="claim">
      <span class="claim-number">Claim ${String(index + 1).padStart(2, "0")}</span>
      <p>${escapeHtml(claim.text)}</p>
      <div class="citation-row" aria-label="Sources for claim ${index + 1}">
        ${claim.sources.map(citationButton).join("")}
      </div>
    </article>`).join("");

  const groups = ROLE_ORDER.map((role) => {
    const sources = item.sources.filter((source) => source.document_role === role);
    if (!sources.length) return "";
    return `
      <section class="evidence-group" aria-labelledby="group-${role}">
        <h3 class="evidence-group-title" id="group-${role}"><span class="role-dot ${ROLE_CLASSES[role]}"></span>${ROLE_LABELS[role]}</h3>
        <div class="evidence-stack">${sources.map(evidenceCard).join("")}</div>
      </section>`;
  }).join("");
  el("evidence-groups").innerHTML = groups || '<p class="empty-state">No cited sources were returned for this answer.</p>';
  el("evidence-count").textContent = `${item.sources.length} ${item.sources.length === 1 ? "source" : "sources"}`;

  document.querySelectorAll("button[data-evidence-ref]").forEach((button) => {
    button.addEventListener("click", () => focusEvidence(button.dataset.evidenceRef));
  });
}

function render() {
  renderQuestionList();
  renderActiveCase();
  const url = new URL(window.location.href);
  url.searchParams.set("case", state.activeId);
  history.replaceState(null, "", url);
}

async function init() {
  try {
    const response = await fetch("./data/demo.json");
    if (!response.ok) throw new Error(`Data request failed: ${response.status}`);
    state.data = await response.json();
    const requested = new URL(window.location.href).searchParams.get("case")?.toUpperCase();
    if (state.data.cases.some((item) => item.id === requested)) state.activeId = requested;
    render();
    el("question-filter").addEventListener("input", (event) => {
      state.filter = event.target.value;
      renderQuestionList();
    });
  } catch (error) {
    el("active-question").textContent = "The preserved demo data could not be loaded.";
    el("claims").innerHTML = `<p class="empty-state">${escapeHtml(error.message)}</p>`;
    el("status-card").hidden = true;
  }
}

init();
