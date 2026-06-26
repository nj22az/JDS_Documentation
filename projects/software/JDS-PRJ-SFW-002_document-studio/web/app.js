// JDS Document Studio — front-end logic.
// Vanilla JS, no build step. Every action is a fetch() to the FastAPI core.

const $ = (id) => document.getElementById(id);

async function getJSON(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error((await res.json()).detail || res.statusText);
  return res.json();
}

async function postJSON(url, body) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : null,
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || JSON.stringify(data));
  return data;
}

function fillSelect(select, values, { placeholder } = {}) {
  select.innerHTML = "";
  if (placeholder) select.append(new Option(placeholder, ""));
  for (const v of values) select.append(new Option(v, v));
}

// --- bootstrap dropdowns ----------------------------------------------------

async function init() {
  const [tax, tmpls] = await Promise.all([
    getJSON("/api/taxonomy"),
    getJSON("/api/templates"),
  ]);

  fillSelect($("category"), tax.categories);
  fillSelect($("domain"), tax.domains, { placeholder: "— none —" });
  fillSelect($("status"), tax.statuses);
  $("status").value = "DRAFT";

  const tsel = $("template");
  tsel.innerHTML = "";
  for (const t of tmpls) {
    const opt = new Option(`${t.number} · ${t.title}`, t.path);
    opt.dataset.type = t.type;
    tsel.append(opt);
  }

  ["category", "domain", "template_type"].forEach((id) =>
    $(id).addEventListener("change", refreshNumber));
  await refreshNumber();

  $("new-doc-form").addEventListener("submit", onCreate);
  $("btn-validate").addEventListener("click", () => runValidate(false));
  $("btn-validate-quick").addEventListener("click", () => runValidate(true));
  document.querySelectorAll("[data-office]").forEach((btn) =>
    btn.addEventListener("click", () => makeOffice(btn.dataset.office)));

  // Edit / Revise panel: registered documents only.
  const reg = await getJSON("/api/registry");
  const esel = $("edit-doc");
  for (const e of reg) esel.append(new Option(`${e.doc_no} · ${e.title}`, e.path));
  esel.addEventListener("change", loadDocument);
  $("btn-save").addEventListener("click", saveBody);
  $("btn-revise").addEventListener("click", reviseDoc);

  checkHealth();
}

// --- health -----------------------------------------------------------------

async function checkHealth() {
  try {
    const h = await getJSON("/api/health");
    if (h.ready) return;
    const gaps = Object.entries(h.dependencies)
      .filter(([, v]) => !v.present).map(([k]) => k);
    const banner = $("health-banner");
    banner.textContent = "Some features need packages that aren't installed: " +
      gaps.join(", ") + ". Run  pip3 install -r requirements.txt  to enable them.";
    banner.hidden = false;
  } catch (err) { /* health is best-effort */ }
}

// --- edit / revise ----------------------------------------------------------

async function loadDocument() {
  const path = $("edit-doc").value;
  const meta = $("edit-meta"), body = $("edit-body");
  if (!path) { meta.hidden = true; body.hidden = true; return; }
  try {
    const doc = await getJSON("/api/document?path=" + encodeURIComponent(path));
    $("edit-rev").textContent = doc.rev || "—";
    meta.hidden = false;
    body.value = doc.content;
    body.hidden = false;
  } catch (err) {
    showEdit("Could not load: " + err.message, true);
  }
}

async function saveBody() {
  const path = $("edit-doc").value;
  if (!path) return;
  try {
    await postJSON("/api/document/save", { path, content: $("edit-body").value });
    showEdit("Saved.", false);
  } catch (err) {
    showEdit("Save failed: " + err.message, true);
  }
}

async function reviseDoc() {
  const path = $("edit-doc").value;
  if (!path) return;
  try {
    const res = await postJSON("/api/revise", {
      path,
      author: $("revise-author").value.trim(),
      description: $("revise-desc").value.trim(),
    });
    $("edit-rev").textContent = res.new_rev;
    $("revise-desc").value = "";
    await loadDocument();
    showEdit(`Bumped ${res.doc_no || "document"} to revision ${res.new_rev} and synced the register.`, false);
  } catch (err) {
    showEdit("Revise failed: " + err.message, true);
  }
}

function showEdit(message, isError) {
  const box = $("edit-result");
  box.className = "result" + (isError ? " error" : "");
  box.textContent = message;
  box.hidden = false;
}

// --- next-number preview ----------------------------------------------------

let lastSuggestedDir = "";

async function refreshNumber() {
  const params = new URLSearchParams({ category: $("category").value });
  if ($("domain").value) params.set("domain", $("domain").value);
  if ($("template_type").value) params.set("template_type", $("template_type").value);
  try {
    const data = await getJSON("/api/next-number?" + params.toString());
    $("next-number").textContent = data.doc_no;
    // Auto-fill the folder only while the user hasn't overridden it (keep them
    // in control, PRO-012 §5). Stop syncing once they type their own path.
    const dir = $("target_dir");
    if (dir.value === "" || dir.value === lastSuggestedDir) {
      dir.value = data.target_dir || "";
    }
    lastSuggestedDir = data.target_dir || "";
  } catch (err) {
    $("next-number").textContent = "—";
  }
}

// --- create -----------------------------------------------------------------

async function onCreate(evt) {
  evt.preventDefault();
  const box = $("create-result");
  const body = {
    template_rel_path: $("template").value,
    target_dir: $("target_dir").value.trim(),
    title: $("title").value.trim(),
    category: $("category").value,
    domain: $("domain").value || null,
    template_type: $("template_type").value.trim() || null,
    status: $("status").value,
    author: $("author").value.trim(),
  };
  try {
    const res = await postJSON("/api/documents", body);
    box.className = "result";
    box.innerHTML = `Created <strong>${res.doc_no}</strong> at <code>${res.path}</code>` +
      ` and registered it. <button id="pdf-btn" type="button">Generate PDF</button>`;
    box.hidden = false;
    $("pdf-btn").addEventListener("click", () => makePdf(res.path, box));
    await refreshNumber();
  } catch (err) {
    box.className = "result error";
    box.textContent = "Could not create: " + err.message;
    box.hidden = false;
  }
}

async function makePdf(path, box) {
  const note = document.createElement("div");
  note.textContent = "Rendering PDF…";
  box.append(note);
  try {
    await postJSON("/api/pdf", { path });
    note.textContent = "PDF generated next to the source file.";
  } catch (err) {
    note.textContent = "PDF failed: " + err.message;
  }
}

// --- validate ---------------------------------------------------------------

async function runValidate(quick) {
  const out = $("validate-output");
  out.hidden = false;
  out.textContent = "Running audit…";
  try {
    const res = await postJSON("/api/validate?quick=" + quick, null);
    out.textContent = res.output;
  } catch (err) {
    out.textContent = "Validation error: " + err.message;
  }
}

// --- office documents -------------------------------------------------------

async function makeOffice(kind) {
  const out = $("office-output");
  out.hidden = false;
  out.textContent = `Generating ${kind}…`;
  try {
    const res = await postJSON("/api/office?kind=" + encodeURIComponent(kind), null);
    out.textContent = res.output || `${kind} generated.`;
  } catch (err) {
    out.textContent = "Office generation error: " + err.message;
  }
}

init().catch((err) => {
  document.body.insertAdjacentHTML("afterbegin",
    `<p style="color:#7B1A1A;padding:12px">Failed to start: ${err.message}</p>`);
});
