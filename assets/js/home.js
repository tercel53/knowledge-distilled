const names = { ai: 'AI Engineering', software: 'Software', frontiers: 'Frontiers' };
for (const control of document.querySelectorAll('[data-category]')) {
  control.addEventListener('click', () => {
    const category = control.dataset.category;
    document.querySelector('#topics-ai').hidden = category !== 'ai';
    document.querySelector('#topics-empty').hidden = category === 'ai';
    document.querySelector('#category-label').textContent = names[category];
    document.querySelector('#empty-title').textContent = names[category];
    for (const link of document.querySelectorAll('.site-nav [data-category]')) {
      if (link.dataset.category === category) link.setAttribute('aria-current', 'true');
      else link.removeAttribute('aria-current');
    }
  });
}
