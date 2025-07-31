const TERMS_URL = '/turkce-sozluk/assets/terms.json';

/* assets/js/site.js */
(async () => {
  /* ---------- helpers ---------- */
  function safeSlug(t) {
    return slugify(t, { lower: true, strict: true, locale: 'tr', remove: /[\\/]/g }) || 'unnamed';
  }

  /* ---------- DOM ---------- */
  const $search  = document.getElementById('search');
  const $list    = document.getElementById('results');
  const $random  = document.getElementById('random-word');

  /* ---------- load term list once ---------- */
  const TERMS_URL = '/turkce-sozluk/assets/terms.json';
  const terms = JSON.parse(sessionStorage.getItem('terms')) ||
                await fetch(TERMS_URL).then(r => r.json()).then(ts => {
                  sessionStorage.setItem('terms', JSON.stringify(ts));
                  return ts;
                });

  /* ---------- autocomplete ---------- */
  function filter() {
    const q = $search.value.toLowerCase().trim();
    if (!q) {
      $list.style.display = 'none';
      $search.setAttribute('aria-expanded', 'false');
      return;
    }
    const matches = terms.filter(t => t.title.toLowerCase().startsWith(q)).slice(0, 15);
    $list.innerHTML = matches.map(t => `<li role="option" data-url="${t.url}">${t.title}</li>`).join('');
    const open = !!matches.length;
    $list.style.display = open ? 'block' : 'none';
    $search.setAttribute('aria-expanded', open);
  }

  $search.addEventListener('input', filter);
  $list.addEventListener('click', ev => {
    const li = ev.target.closest('li');
    if (li) window.location.href = li.dataset.url;
  });

  /* ---------- “Enter” jumps straight to slug ---------- */
  $search.addEventListener('keydown', ev => {
    if (ev.key !== 'Enter') return;
    const raw = $search.value.trim();
    if (raw) window.location.href = `/turkce-sozluk/terim/${safeSlug(raw)}.html`;
  });

  /* ---------- random term ---------- */
  $random.addEventListener('click', () => {
    if (!terms.length) return;
    const { url } = terms[Math.floor(Math.random() * terms.length)];
    window.location.href = url;
  });
})();
