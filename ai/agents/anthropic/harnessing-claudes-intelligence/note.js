function revealHash() {
  const id = decodeURIComponent(location.hash.slice(1));
  const target = document.getElementById(id);
  if (!target) return;
  const disclosure = target.closest('details');
  if (disclosure) { disclosure.open = true; requestAnimationFrame(() => target.scrollIntoView()); }
}
window.addEventListener('hashchange', revealHash);
revealHash();
