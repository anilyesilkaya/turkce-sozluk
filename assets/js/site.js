---
layout: null      /* makes Jekyll run Liquid but output raw JS */
---

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
  const TERMS_URL = '{{ "/assets/terms.json" | relative_url }}';

  let terms;
  const cached = sessionStorage.getItem('terms');

  if (cached) {
    try {
      terms = JSON.parse(cached);
    } catch {
      /* corrupted JSON – ignore */
      sessionStorage.removeItem('terms');
    }
  }

  if (!terms) {
    terms = await fetch(TERMS_URL).then(r => r.json());
    /* try to cache, but don’t break if quota is full */
    try {
      sessionStorage.setItem('terms', JSON.stringify(terms));
    } catch {
      /* silently continue without storage */
    }
  }

  /* ────────────────── autocomplete ────────────────── */
  function filter() {
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

  $search.addEventListener('input', filter);

  /* click on a suggestion */
  $list.addEventListener('click', ev => {
    const li = ev.target.closest('li');
    if (li) window.location.href = li.dataset.url;
  });

  /* Enter key → jump straight to slug */
  $search.addEventListener('keydown', ev => {
    if (ev.key !== 'Enter') return;
    const raw = $search.value.trim();
    if (raw) {
      window.location.href =
        `{{ '/terim/' | relative_url }}${safeSlug(raw)}.html`;
    }
  });

  /* ────────────────── random term ────────────────── */
  $random.addEventListener('click', () => {
    if (!terms.length) return;

    /* hide any open dropdown */
    $list.style.display = 'none';
    $search.setAttribute('aria-expanded', 'false');
    $list.innerHTML = '';

    const { url } = terms[Math.floor(Math.random() * terms.length)];
    window.location.href = url;
  });
})();
