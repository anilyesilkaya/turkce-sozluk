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

  let selectedIdx = 0;

  /* ────────────────── load term list ────────────────── */
  const TERMS_URL = '/assets/terms.json';

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

  function render(nodeList) {
    if (!$list) return;
    if (!nodeList || nodeList.length == 0) {
      $list.innerHTML = "";
      $list.style.display = "none";
      $search?.setAttribute("aria-expanded", "false");
      return;
    }

    $list.innerHTML = nodeList.map(t => `
      <li role="option" data-url="${t.url}">
        <a href="${t.url}">
          <span class="res-title">${t.title}</span>
          ${t._id ? `<small class="res-desc">(${t._slug}—${t._id})</small>` : ""}
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

    // Support typing term/slug/id
    const score = (t) => {
      if (t._titleFold === qFold) return 100;              // matches exact title
      if (t._slug === qSlug) return 90;                    // matches exact slug
      if (t._titleFold.startsWith(qFold)) return 80;       // starts with the title
      if (t._slug.startsWith(qSlug)) return 70;            // starts with the slug
      if (t._titleFold.includes(qFold)) return 60;         // contains title
      if (t.search && t.search.includes(qFold)) return 40; // contains normalized (no-accents) search
      if (t._id.includes(qFold)) return 20;                // contains term id
      return 0;
    };

    const matches = terms
      .map(t => ({ t, s: score(t) }))
      .filter(x => x.s > 0)
      .sort((a, b) => b.s - a.s || a.t.title.localeCompare(b.t.title, "tr"))
      .slice(0, 15)
      .map(x => x.t);

    return matches;
  }

  function selectListItem(selectedIdx) {
    const nodeList = $list.querySelectorAll('li[data-url]');

    if (!nodeList) return;

    // Remove all the highlights first
    nodeList.forEach(item => item.classList.remove('selected'));

    // Add highlight to the selected item
    nodeList[selectedIdx].classList.add('selected');

    // Ensure the selected item is visible
    nodeList[selectedIdx].scrollIntoView({block: 'nearest'}); 
  }

  // Input handler (light debounce)
  let timer;
  $search?.addEventListener("input", () => {
    clearTimeout(timer);
    timer = setTimeout(render(filter()), 60);
    selectedIdx = 0;
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

    let hit = filter()[0];
    const nodeList = $list.querySelectorAll('li');
    selectedIdx = Array.from(nodeList).findIndex(li => li.classList.contains('selected'));

    if (hit && selectedIdx === 0) {
      go(hit.url);
    } else if (hit && selectedIdx !== 0) {
      go(nodeList[selectedIdx].getAttribute("data-url"));
    } 
    else {
      render([]);
    }
  });

  // Keyboard: ArrowUp/ArrowDown selection
  $search?.addEventListener("keydown", (ev) => {
    const numElements = $list.querySelectorAll('li[data-url]').length;
    if (ev.key === "ArrowDown") {
      ev.preventDefault(); // This stops default browser behavior
      selectedIdx += 1;
    } else if (ev.key === "ArrowUp" && selectedIdx !== 0) {
      ev.preventDefault(); // This stops default browser behavior
      selectedIdx -= 1;
    } else if (ev.key === "ArrowUp" && selectedIdx === 0) {
      ev.preventDefault(); // This stops default browser behavior
    } else return;
    selectListItem((((selectedIdx-1) % numElements) + numElements) % numElements);
  });

  /* ────────────────── random term ────────────────── */
  $random?.addEventListener("click", () => {
    if (!terms.length) return;
    render([]);
    const { url } = terms[Math.floor(Math.random() * terms.length)];
    go(url);
  });
})();

// Add CSS for highlighting selected item
const style = document.createElement('style');
style.textContent = `
  #results.autocomplete li.selected {
    background-color: #f0f8ff; /* Light blue background */
  }
  
  #results.autocomplete li.selected a {
    color: #0066cc; /* Darker blue text */
    font-weight: bold;
  }
`;
document.head.appendChild(style);

