const themeToggle = document.querySelector('#theme-toggle');
const body = document.querySelector('body');
const header = document.querySelector('.header');
const tables = document.querySelectorAll('table');
const cardBodies = document.querySelectorAll('.card-body');
const cardFooters = document.querySelectorAll('.card-footer')
const listItems = document.querySelectorAll('.list-group-item');
const cardHeaders = document.querySelectorAll('.card-header');

let currentThemeMode = localStorage.getItem('themeMode') || 'light';
applyThemeMode(currentThemeMode);

themeToggle.addEventListener('click', function() {
const currentThemeMode = localStorage.getItem('themeMode') || 'light';
  let newThemeMode = currentThemeMode === 'light' ? 'dark' : 'light';
  localStorage.setItem('themeMode', newThemeMode);
  applyThemeMode(newThemeMode);
  currentThemeMode = newThemeMode;
});

function applyThemeMode(themeMode) {
  body.classList.toggle('body-bg-dark', themeMode === 'dark');
  body.classList.toggle('text-white', themeMode === 'dark');
  header.classList.toggle('header-dark', themeMode === 'dark');
  header.classList.toggle('text-white', themeMode === 'dark');
  
  tables.forEach(item => {
    item.classList.toggle('bg-dark', themeMode === 'dark');
    item.style.borderColor = themeMode === 'dark' ? 'var(--light)' : 'var(--dark)';
  });
  cardBodies.forEach(item => {
    item.classList.toggle('bg-dark', themeMode === 'dark');
    item.classList.toggle('text-white', themeMode === 'dark');
    item.style.borderColor = themeMode === 'dark' ? 'var(--light)' : 'var(--dark)';
  });
  cardHeaders.forEach(item => {
    item.classList.toggle('bg-dark', themeMode === 'dark');
    item.classList.toggle('text-white', themeMode === 'dark');
    item.style.borderColor = themeMode === 'dark' ? 'var(--light)' : 'var(--dark)';
  });
  listItems.forEach(item => {
    item.classList.toggle('bg-dark', themeMode === 'dark');
    item.classList.toggle('text-white', themeMode === 'dark');
    item.style.borderColor = themeMode === 'dark' ? 'var(--light)' : 'var(--dark)';
  });
  cardFooters.forEach(item => {
    item.classList.toggle('bg-dark', themeMode === 'dark');
    item.classList.toggle('text-white', themeMode === 'dark');
    item.style.borderColor = themeMode === 'dark' ? 'var(--light)' : 'var(--dark)';
  });
}