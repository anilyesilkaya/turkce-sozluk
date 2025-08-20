---
layout: null      /* Let Jekyll process Liquid, output raw JS */
---

/* assets/js/site.js */
(async () => {
  /* ────────────────── helpers ────────────────── */

  // Turkish-insensitive folding (for comparisons)
  const foldTR = (s = "") => s
    .toLowerCase()
    .normalize("NFD").replace(/\p{Diacritic}/gu, "")
    .replace(/ı/g, "i").replace(/ş/g, "s").replace(/ç/g, "c")
    .replace(/ğ/g, "g").replace(/ö/g, "o").replace(/ü/g, "u");

  // Slug generator using slugify (CDN included in default.html)
  const makeSlug = (s = "") =>
    (slugify(s, { lower: true, strict: true, locale: "tr", remove: /[\\/]/g }) || "unnamed");

  // Extract numeric ID from URLs like "...--12792.html" or "...-12792.html"
  const extractId = (url = "") => {
    const m = url.match(/[-]{1,2}(\d+)\.html?$/);
    return m ? m[1] : "";
  };

  // Safe navigate
  const go = (href) => { if (href) window.location.assign(href); };

  /* ────────────────── DOM refs ────────────────── */
  const $search = document.getElementById("search");
  const $list   = document.getElementById("results");
  const $random = document.getElementById("random-word");

  /* ────────────────── load term list ────────────────── */
  const TERMS_URL = '{{ "/assets/terms.json" | relative_url }}';

  let terms;
  try {
    const cached = sessionStorage.getItem("terms");
    if (cached) terms = JSON.parse(cached);
  } catch { /* ignore */ }

  if (!terms) {
    terms = await fetch(TERMS_URL, { cache: "force-cache" }).then(r => r.json());
    try { sessionStorage.setItem("terms", JSON.stringify(terms)); } catch { /* quota */ }
  }

  // Enrich for fast matching
  terms = (terms || []).map(t => ({
    ...t,
    _titleFold: foldTR(t.title),
    _slug: makeSlug(t.title),
    _id: extractId(t.url)
  }));

  /* ────────────────── autocomplete ────────────────── */

  function render(items) {
    if (!$list) return;
    if (!items.length) {
      $list.innerHTML = "";
      $list.style.display = "none";
      $search?.setAttribute("aria-expanded", "false");
      return;
    }

    $list.innerHTML = items.map(t => `
      <li role="option" data-url="${t.url}">
        <a href="${t.url}">
          <span class="res-title">${t.title}</span>
          ${t._id ? `<small class="res-desc">${t._slug}</small>` : ""}
        </a>
      </li>
    `).join("");

    $list.style.display = "block";
    $search?.setAttribute("aria-expanded", "true");
  }

  function filter() {
    if (!$search || !$list) return;

    const raw = ($search.value || "").trim();
    const qFold = foldTR(raw);
    const qSlug = makeSlug(raw);

    if (!qFold) {
      render([]);
      return;
    }

    // Support typing "slug--id" or "slug-id"
    const m = raw.match(/^(.+?)[-]{1,2}(\d+)$/);
    const typedSlugPart = m ? makeSlug(m[1]) : null;
    const typedIdPart   = m ? m[2] : null;

    const score = (t) => {
      if (t._titleFold === qFold) return 100;                 // exact title
      if (t._slug === qSlug)     return 90;                   // exact slug

      if (typedSlugPart) {                                    // slug-id pattern
        const slugOk = t._slug.startsWith(typedSlugPart);
        const idOk   = typedIdPart ? t._id.startsWith(typedIdPart) : false;
        if (slugOk && idOk) return 85;
        if (slugOk)         return 80;
      }

      if (t._titleFold.startsWith(qFold)) return 70;          // prefix title
      if (t._slug.startsWith(qSlug))     return 65;           // prefix slug

      if (t._titleFold.includes(qFold)) return 50;            // contains title
      if (t.search && t.search.includes(qFold)) return 45;    // contains normalized search (from terms.json)

      return 0;
    };

    const matches = terms
      .map(t => ({ t, s: score(t) }))
      .filter(x => x.s > 0)
      .sort((a, b) => b.s - a.s || a.t.title.localeCompare(b.t.title, "tr"))
      .slice(0, 15)
      .map(x => x.t);

    render(matches);
  }

  // Input handler (light debounce)
  let timer;
  $search?.addEventListener("input", () => {
    clearTimeout(timer);
    timer = setTimeout(filter, 60);
  });

  // Click on a suggestion
  $list?.addEventListener("click", (ev) => {
    const li = ev.target.closest("li[data-url]");
    if (li) go(li.dataset.url);
  });

  // Keyboard: Enter → best match; `/` focuses; Esc clears
  document.addEventListener("keydown", (e) => {
    if (!$search) return;
    if (e.key === "/" && document.activeElement !== $search) {
      e.preventDefault();
      $search.focus();
    } else if (e.key === "Escape" && document.activeElement === $search) {
      $search.value = "";
      render([]);
      $search.blur();
    }
  });

  $search?.addEventListener("keydown", (ev) => {
    if (ev.key !== "Enter") return;
    const raw = ($search.value || "").trim();
    if (!raw) return;

    const rawFold = foldTR(raw);
    const rawSlug = makeSlug(raw);
    const m = raw.match(/^(.+?)[-]{1,2}(\d+)$/);

    let hit =
      terms.find(t => t._titleFold === rawFold) ||
      terms.find(t => t._slug === rawSlug) ||
      (m && terms.find(t => t._slug.startsWith(makeSlug(m[1])) && t._id.startsWith(m[2]))) ||
      terms.find(t => t._titleFold.startsWith(rawFold)) ||
      terms.find(t => t._slug.startsWith(rawSlug));

    if (hit) {
      go(hit.url);
    } else {
      render([]);
    }
  });

  /* ────────────────── random term ────────────────── */
  $random?.addEventListener("click", () => {
    if (!terms.length) return;
    render([]);
    const { url } = terms[Math.floor(Math.random() * terms.length)];
    go(url);
  });
})();
