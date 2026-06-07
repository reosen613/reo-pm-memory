/* 名刺管理 — 依存ゼロのローカルアプリ。
 * データは localStorage に保存。初回起動時に cards.seed.js から取り込みます。 */
(() => {
  "use strict";

  const STORAGE_KEY = "meishi.cards.v1";
  const AVATAR_COLORS = ["#2f6df0", "#10a37f", "#e0584b", "#7b61ff", "#f5a623",
    "#0a9bb5", "#d6438f", "#5a6573", "#3a7d3a", "#c2772a"];

  // ---- state ----
  let cards = [];
  let activeCompany = "all";
  let query = "";
  let favOnly = false;
  let sortBy = "name";

  // ---- persistence ----
  const uid = () => Date.now().toString(36) + Math.random().toString(36).slice(2, 7);

  function normalize(c) {
    return Object.assign({
      id: uid(), nameJa: "", nameEn: "", companyJa: "", companyEn: "",
      titleJa: "", titleEn: "", departmentJa: "", departmentEn: "",
      qualifications: "", email: "", website: "", phone: "", phoneSub: "",
      mobile: "", fax: "", postalCode: "", addressJa: "", addressEn: "",
      tags: [], notes: "", favorite: false, createdAt: Date.now()
    }, c);
  }

  function load() {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      try { cards = JSON.parse(raw).map(normalize); return; } catch (e) { /* fall through */ }
    }
    seed();
  }

  function seed() {
    const src = window.MEISHI_SEED || [];
    cards = src.map((c, i) => normalize(Object.assign({ createdAt: Date.now() + i }, c)));
    save();
  }

  function save() { localStorage.setItem(STORAGE_KEY, JSON.stringify(cards)); }

  // ---- helpers ----
  const $ = (sel) => document.querySelector(sel);
  const esc = (s) => String(s == null ? "" : s).replace(/[&<>"']/g,
    (m) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[m]));

  function initials(c) {
    const n = (c.nameJa || c.nameEn || "?").trim();
    // 日本語: 姓の1文字目。英語: 各単語の頭文字。
    if (/[　-鿿＀-￯]/.test(n)) return n.replace(/\s/g, "").slice(0, 1);
    return n.split(/\s+/).map((w) => w[0]).slice(0, 2).join("").toUpperCase();
  }

  function colorFor(c) {
    const key = c.companyJa || c.companyEn || c.nameJa || "";
    let h = 0;
    for (let i = 0; i < key.length; i++) h = (h * 31 + key.charCodeAt(i)) >>> 0;
    return AVATAR_COLORS[h % AVATAR_COLORS.length];
  }

  function companyLabel(c) { return c.companyJa || c.companyEn || "（会社未設定）"; }

  function searchBlob(c) {
    return [c.nameJa, c.nameEn, c.companyJa, c.companyEn, c.titleJa, c.titleEn,
      c.departmentJa, c.departmentEn, c.email, c.qualifications, c.notes,
      (c.tags || []).join(" ")].join(" ").toLowerCase();
  }

  // ---- rendering ----
  function visibleCards() {
    let list = cards.slice();
    if (activeCompany !== "all") list = list.filter((c) => companyLabel(c) === activeCompany);
    if (favOnly) list = list.filter((c) => c.favorite);
    if (query) {
      const q = query.toLowerCase();
      list = list.filter((c) => searchBlob(c).includes(q));
    }
    const coll = new Intl.Collator("ja");
    list.sort((a, b) => {
      if (sortBy === "recent") return b.createdAt - a.createdAt;
      if (sortBy === "company") {
        const c = coll.compare(companyLabel(a), companyLabel(b));
        if (c !== 0) return c;
      }
      return coll.compare(a.nameJa || a.nameEn, b.nameJa || b.nameEn);
    });
    return list;
  }

  function renderChips() {
    const counts = new Map();
    cards.forEach((c) => {
      const k = companyLabel(c);
      counts.set(k, (counts.get(k) || 0) + 1);
    });
    const sorted = [...counts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0], "ja"));
    const chips = [`<button class="chip ${activeCompany === "all" ? "active" : ""}" data-company="all">すべて<span class="n">${cards.length}</span></button>`];
    sorted.forEach(([name, n]) => {
      chips.push(`<button class="chip ${activeCompany === name ? "active" : ""}" data-company="${esc(name)}">${esc(name)}<span class="n">${n}</span></button>`);
    });
    $("#companyChips").innerHTML = chips.join("");
  }

  function cardHTML(c) {
    const tags = (c.tags || []).map((t) => `<span class="tag">${esc(t)}</span>`).join("");
    return `<article class="card" data-id="${c.id}">
      <button class="fav-star ${c.favorite ? "on" : ""}" data-fav="${c.id}" title="お気に入り">${c.favorite ? "★" : "☆"}</button>
      <div class="avatar" style="background:${colorFor(c)}">${esc(initials(c))}</div>
      <div class="card-main">
        <div class="name">${esc(c.nameJa || c.nameEn)}</div>
        ${c.nameEn && c.nameJa ? `<div class="name-en">${esc(c.nameEn)}</div>` : ""}
        <div class="company">${esc(companyLabel(c))}</div>
        <div class="title">${esc(c.titleJa || c.titleEn || "")}</div>
        ${tags ? `<div class="tags">${tags}</div>` : ""}
      </div>
    </article>`;
  }

  function render() {
    renderChips();
    const list = visibleCards();
    $("#grid").innerHTML = list.map(cardHTML).join("");
    $("#count").textContent = `${list.length} 件${activeCompany !== "all" ? `（${activeCompany}）` : ""}`;
    $("#empty").classList.toggle("hidden", list.length > 0);
  }

  // ---- detail ----
  let currentId = null;

  function pair(ja, en) {
    if (!ja && !en) return "";
    return `<span class="pair">${esc(ja || en)}${ja && en ? `<span class="en">${esc(en)}</span>` : ""}</span>`;
  }

  function row(label, value) {
    return value ? `<dt>${label}</dt><dd>${value}</dd>` : "";
  }

  function openDetail(id) {
    const c = cards.find((x) => x.id === id);
    if (!c) return;
    currentId = id;
    const tel = (v) => v ? `<a href="tel:${esc(String(v).replace(/[^0-9+]/g, ""))}">${esc(v)}</a>` : "";
    const phones = [c.phone, c.phoneSub, c.mobile && `携帯: ${c.mobile}`, c.fax && `FAX: ${c.fax}`]
      .filter(Boolean).map((p) => tel(p)).join("<br>");
    const addr = pair(
      (c.postalCode ? "〒" + c.postalCode + " " : "") + (c.addressJa || ""),
      c.addressEn
    );
    $("#detailBody").innerHTML = `
      <div class="detail-head">
        <div class="avatar" style="background:${colorFor(c)}">${esc(initials(c))}</div>
        <div>
          <div class="name">${esc(c.nameJa || c.nameEn)}</div>
          ${c.nameEn && c.nameJa ? `<div class="name-en">${esc(c.nameEn)}</div>` : ""}
          <div class="company">${esc(c.companyJa || c.companyEn)}</div>
          ${c.companyEn && c.companyJa ? `<div class="company-en">${esc(c.companyEn)}</div>` : ""}
          <div class="title">${esc([c.departmentJa, c.titleJa].filter(Boolean).join(" / "))}</div>
          ${(c.titleEn || c.departmentEn) ? `<div class="title">${esc([c.departmentEn, c.titleEn].filter(Boolean).join(" / "))}</div>` : ""}
        </div>
      </div>
      <dl>
        ${row("資格", c.qualifications ? `<span class="qual">${esc(c.qualifications)}</span>` : "")}
        ${row("メール", c.email ? `<a href="mailto:${esc(c.email)}">${esc(c.email)}</a>` : "")}
        ${row("電話", phones)}
        ${row("住所", addr)}
        ${row("Web", c.website ? `<a href="${esc(c.website)}" target="_blank" rel="noopener">${esc(c.website)}</a>` : "")}
        ${row("タグ", (c.tags || []).map((t) => `<span class="tag">${esc(t)}</span>`).join(" "))}
        ${row("メモ", c.notes ? esc(c.notes).replace(/\n/g, "<br>") : "")}
      </dl>`;
    show("#detailModal");
  }

  // ---- form ----
  let editingId = null;

  function openForm(id) {
    editingId = id || null;
    const form = $("#cardForm");
    form.reset();
    $("#formTitle").textContent = id ? "名刺を編集" : "名刺を追加";
    if (id) {
      const c = cards.find((x) => x.id === id);
      Object.keys(c).forEach((k) => {
        if (form.elements[k]) {
          form.elements[k].value = k === "tags" ? (c.tags || []).join(", ") : (c[k] || "");
        }
      });
    }
    show("#formModal");
    setTimeout(() => form.elements["nameJa"].focus(), 50);
  }

  function submitForm(e) {
    e.preventDefault();
    const fd = new FormData(e.target);
    const data = Object.fromEntries(fd.entries());
    data.tags = (data.tags || "").split(",").map((s) => s.trim()).filter(Boolean);
    if (editingId) {
      const c = cards.find((x) => x.id === editingId);
      Object.assign(c, data);
    } else {
      cards.push(normalize(Object.assign({ createdAt: Date.now() }, data)));
    }
    save();
    render();
    hide("#formModal");
  }

  // ---- modals ----
  function show(sel) { $(sel).classList.remove("hidden"); }
  function hide(sel) { $(sel).classList.add("hidden"); }

  // ---- import / export ----
  function exportJSON() {
    const blob = new Blob([JSON.stringify(cards, null, 2)], { type: "application/json" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = `meishi-backup-${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    URL.revokeObjectURL(a.href);
  }

  function importJSON(file) {
    const reader = new FileReader();
    reader.onload = () => {
      try {
        const data = JSON.parse(reader.result);
        if (!Array.isArray(data)) throw new Error("配列ではありません");
        if (!confirm(`${data.length} 件を読み込みます。現在のデータは置き換えられます。よろしいですか？`)) return;
        cards = data.map(normalize);
        save();
        activeCompany = "all";
        render();
      } catch (err) {
        alert("読み込みに失敗しました: " + err.message);
      }
    };
    reader.readAsText(file);
  }

  // ---- events ----
  function bind() {
    $("#search").addEventListener("input", (e) => { query = e.target.value.trim(); render(); });
    $("#favOnly").addEventListener("change", (e) => { favOnly = e.target.checked; render(); });
    $("#sort").addEventListener("change", (e) => { sortBy = e.target.value; render(); });
    $("#addBtn").addEventListener("click", () => openForm(null));

    $("#companyChips").addEventListener("click", (e) => {
      const chip = e.target.closest(".chip");
      if (!chip) return;
      activeCompany = chip.dataset.company;
      render();
    });

    $("#grid").addEventListener("click", (e) => {
      const fav = e.target.closest("[data-fav]");
      if (fav) {
        const c = cards.find((x) => x.id === fav.dataset.fav);
        c.favorite = !c.favorite; save(); render();
        return;
      }
      const card = e.target.closest(".card");
      if (card) openDetail(card.dataset.id);
    });

    // menu
    $("#menuBtn").addEventListener("click", (e) => {
      e.stopPropagation();
      $("#menuPanel").classList.toggle("hidden");
    });
    document.addEventListener("click", () => $("#menuPanel").classList.add("hidden"));
    $("#menuPanel").addEventListener("click", (e) => e.stopPropagation());
    $("#exportBtn").addEventListener("click", () => { exportJSON(); $("#menuPanel").classList.add("hidden"); });
    $("#importBtn").addEventListener("click", () => $("#importFile").click());
    $("#importFile").addEventListener("change", (e) => { if (e.target.files[0]) importJSON(e.target.files[0]); e.target.value = ""; });
    $("#resetBtn").addEventListener("click", () => {
      if (confirm("サンプルデータに戻します。現在の変更は失われます。よろしいですか？")) {
        seed(); activeCompany = "all"; render();
      }
    });

    // detail actions
    $("#detailEdit").addEventListener("click", () => { hide("#detailModal"); openForm(currentId); });
    $("#detailDelete").addEventListener("click", () => {
      const c = cards.find((x) => x.id === currentId);
      if (c && confirm(`「${c.nameJa || c.nameEn}」を削除しますか？`)) {
        cards = cards.filter((x) => x.id !== currentId);
        save(); render(); hide("#detailModal");
      }
    });

    // form
    $("#cardForm").addEventListener("submit", submitForm);

    // close handlers
    document.querySelectorAll("[data-close]").forEach((el) =>
      el.addEventListener("click", () => { hide("#detailModal"); hide("#formModal"); }));
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") { hide("#detailModal"); hide("#formModal"); }
    });
  }

  // ---- init ----
  load();
  bind();
  render();
})();
