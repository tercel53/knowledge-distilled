const links = [...document.querySelectorAll('.reading-toc a[href^="#"]')];
const sections = links.map(link => document.querySelector(link.getAttribute('href'))).filter(Boolean);
let queued = false;
function markCurrent() {
  queued = false;
  let current = sections[0];
  for (const section of sections) if (section.getBoundingClientRect().top <= 140) current = section;
  links.forEach(link => link.toggleAttribute('aria-current', link.hash === `#${current.id}`));
}
addEventListener('scroll', () => {
  if (!queued) { queued = true; requestAnimationFrame(markCurrent); }
}, {passive: true});
markCurrent();
