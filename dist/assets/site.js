const observed = document.querySelectorAll('.reveal');
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) entry.target.classList.add('is-visible');
  });
}, { threshold: 0.14 });
observed.forEach((el) => observer.observe(el));

const process = document.querySelector('[data-process]');
if (process) {
  const update = () => {
    const rect = process.getBoundingClientRect();
    const distance = Math.max(1, rect.height - innerHeight);
    const progress = Math.max(0, Math.min(1, -rect.top / distance));
    process.style.setProperty('--process', progress.toFixed(3));
  };
  addEventListener('scroll', update, { passive: true });
  addEventListener('resize', update);
  update();
}
