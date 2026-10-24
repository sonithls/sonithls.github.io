'use strict';
document.documentElement.classList.add('js');

const menu = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#navigation');
function closeMenu() {
  menu.setAttribute('aria-expanded', 'false');
  navigation.classList.remove('is-open');
}
menu.addEventListener('click', () => {
  const open = menu.getAttribute('aria-expanded') !== 'true';
  menu.setAttribute('aria-expanded', String(open));
  navigation.classList.toggle('is-open', open);
});
navigation.addEventListener('click', event => {
  if (event.target.closest('a')) closeMenu();
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') {
    closeMenu();
    menu.focus();
  }
});
document.querySelector('#current-year').textContent = new Date().getFullYear();

// Preserve links to sections of the previous single-page website.
if (document.body.classList.contains('home-page')) {
  const previousSections = {
    '#about': 'bio.html', '#research': 'research.html',
    '#publications': 'publications.html', '#news': 'media.html', '#media': 'media.html',
    '#software': 'repositories.html', '#contact': 'contact.html'
  };
  if (previousSections[location.hash]) location.replace(previousSections[location.hash]);
}

// The shared script runs on every page; search is only present on Publications.
const search = document.querySelector('#publication-search');
if (search) {
  const year = document.querySelector('#publication-year');
  const filterButtons = [...document.querySelectorAll('[data-filter]')];
  const publications = [...document.querySelectorAll('.publication')];
  const count = document.querySelector('#publication-count');
  const empty = document.querySelector('#no-results');
  let activeType = 'all';
  const normalize = value => value.normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[−–—]/g, '-');
  const searchable = new Map(publications.map(item => [item, normalize(item.textContent + ' ' + item.dataset.keywords)]));
  function filterPublications() {
    const terms = normalize(search.value).trim().split(/\s+/).filter(Boolean);
    let visible = 0;
    publications.forEach(item => {
      const matches = (activeType === 'all' || item.dataset.type === activeType)
        && (year.value === 'all' || item.dataset.year === year.value)
        && terms.every(term => searchable.get(item).includes(term));
      item.hidden = !matches;
      if (matches) visible++;
    });
    count.textContent = `${visible} of ${publications.length} entries`;
    empty.hidden = visible !== 0;
  }
  document.querySelector('.publication-controls').hidden = false;
  document.querySelector('.filter-row').hidden = false;
  document.querySelector('.publication-controls').addEventListener('submit', event => event.preventDefault());
  search.addEventListener('input', filterPublications);
  year.addEventListener('change', filterPublications);
  filterButtons.forEach(button => button.addEventListener('click', () => {
    activeType = button.dataset.filter;
    filterButtons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    filterPublications();
  }));
  document.querySelector('#reset-filters').addEventListener('click', () => {
    search.value = '';
    year.value = 'all';
    activeType = 'all';
    filterButtons.forEach(item => item.setAttribute('aria-pressed', String(item.dataset.filter === 'all')));
    filterPublications();
    search.focus();
  });
  filterPublications();
}
