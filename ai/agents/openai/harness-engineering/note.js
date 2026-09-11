const navLinks = [...document.querySelectorAll('.reading-toc a')];
const sections = navLinks.map(link => document.querySelector(link.getAttribute('href'))).filter(Boolean);
let scheduled = false;
function updateCurrent() {
  scheduled = false;
  let current = sections[0];
  for (const section of sections) if (section.getBoundingClientRect().top <= 140) current = section;
  navLinks.forEach(link => {
    if (link.getAttribute('href') === `#${current.id}`) link.setAttribute('aria-current','location');
    else link.removeAttribute('aria-current');
  });
}
addEventListener('scroll', () => { if (!scheduled) { scheduled = true; requestAnimationFrame(updateCurrent); } }, { passive: true });
const mobile = matchMedia('(max-width:800px)');
function setToc() { document.querySelector('.reading-toc details').open = !mobile.matches; }
mobile.addEventListener('change',setToc);setToc();updateCurrent();

// Reveal reference sections before navigating to a chapter, including direct URLs.
function revealReference(hash) {
  if (!hash || hash === '#') return;
  const target = document.getElementById(decodeURIComponent(hash.slice(1)));
  if (!target) return;
  for (let parent = target.parentElement; parent; parent = parent.parentElement) {
    if (parent.tagName === 'DETAILS') parent.open = true;
  }
  return target;
}
document.addEventListener('click', event => {
  const link = event.target.closest('a[href^="#"]');
  if (link) revealReference(link.getAttribute('href'));
});
addEventListener('hashchange', () => revealReference(location.hash));
const initialTarget = revealReference(location.hash);
if (initialTarget) requestAnimationFrame(() => initialTarget.scrollIntoView());
