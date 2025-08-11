/* assets/js/site.js */
(async () => {
  /* ────────────────── helpers ────────────────── */
  function safeSlug(str) {
    return (
      slugify(str, {
        lower: true,
        strict: true,
        locale: 'tr',
        remove: /[\\/]/g,
      }) || 'unnamed'
    );
  }

  /* ────────────────── DOM refs ────────────────── */
  const $search = document.getElementById('search');
  const $list   = document.getElementById('results');
  const $random = document.getElementById('random-word');

  /* ────────────────── load term list ────────────────── */
  const TERMS_URL = '/assets/terms.json';

  let terms;
  const cached = sessionStorage.getItem('terms');

  if (cached) {
    try {
      terms = JSON.parse(cached);
    } catch {
      sessionStorage.removeItem('terms');
    }
  }

  if (!terms) {
    terms = await fetch(TERMS_URL).then(r => r.json());
    try {
      sessionStorage.setItem('terms', JSON.stringify(terms));
    } catch { /* ignore quota */ }
  }

  /* ────────────────── autocomplete ────────────────── */
  function filter() {
    if (!$search || !$list) return;

    const q = $search.value.toLowerCase().trim();

    if (!q) {
      $list.style.display = 'none';
      $search.setAttribute('aria-expanded', 'false');
      return;
    }

    const matches = terms
      .filter(t => t.title.toLowerCase().startsWith(q))
      .slice(0, 15);

    $list.innerHTML = matches
      .map(t => `<li role="option" data-url="${t.url}">${t.title}</li>`)
      .join('');

    const open = matches.length > 0;
    $list.style.display = open ? 'block' : 'none';
    $search.setAttribute('aria-expanded', open);
  }

  if ($search) $search.addEventListener('input', filter);

  /* click on a suggestion */
  if ($list) {
    $list.addEventListener('click', ev => {
      const li = ev.target.closest('li');
      if (li) window.location.href = li.dataset.url;
    });
  }

  /* Enter key → go to the best matching term's URL (NOT a constructed slug path) */
  if ($search) {
    $search.addEventListener('keydown', ev => {
      if (ev.key !== 'Enter') return;
      const raw = $search.value.trim();
      if (!raw) return;

      const rawLower = raw.toLowerCase();

      // 1) exact title match (case-insensitive)
      let hit = terms.find(t => t.title.toLowerCase() === rawLower);

      // 2) same-slug title match (handles diacritics → slug collapse)
      if (!hit) {
        const targetSlug = safeSlug(raw);
        hit = terms.find(t => safeSlug(t.title) === targetSlug);
      }

      // 3) startsWith fallback
      if (!hit) {
        hit = terms.find(t => t.title.toLowerCase().startsWith(rawLower));
      }

      if (hit) {
        window.location.href = hit.url;
      } else {
        // nothing found: close dropdown (or you could keep it open)
        if ($list) {
          $list.style.display = 'none';
          $list.innerHTML = '';
        }
        $search.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* ────────────────── random term ────────────────── */
  if ($random) {
    $random.addEventListener('click', () => {
      if (!terms.length) return;

      if ($list && $search) {
        $list.style.display = 'none';
        $search.setAttribute('aria-expanded', 'false');
        $list.innerHTML = '';
      }

      const { url } = terms[Math.floor(Math.random() * terms.length)];
      window.location.href = url;
    });
  }
})();
