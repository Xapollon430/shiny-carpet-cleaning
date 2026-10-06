const observed = document.querySelectorAll('.reveal');
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) entry.target.classList.add('is-visible');
  });
}, { threshold: 0.12 });
observed.forEach((element) => observer.observe(element));

const header = document.querySelector('[data-site-header]');
const menuToggle = document.querySelector('.menu-toggle');
const company = document.querySelector('.nav-company');
const companyTrigger = document.querySelector('.company-trigger');

const updateHeader = () => {
  header?.classList.toggle('is-scrolled', window.scrollY > 24);
};
updateHeader();
window.addEventListener('scroll', updateHeader, { passive: true });

menuToggle?.addEventListener('click', () => {
  const open = !header.classList.contains('menu-open');
  header.classList.toggle('menu-open', open);
  menuToggle.setAttribute('aria-expanded', String(open));
});

companyTrigger?.addEventListener('click', () => {
  const open = !company.classList.contains('is-open');
  company.classList.toggle('is-open', open);
  companyTrigger.setAttribute('aria-expanded', String(open));
});

document.addEventListener('click', (event) => {
  if (company && !company.contains(event.target)) {
    company.classList.remove('is-open');
    companyTrigger?.setAttribute('aria-expanded', 'false');
  }
});

document.addEventListener('keydown', (event) => {
  if (event.key !== 'Escape') return;
  company?.classList.remove('is-open');
  companyTrigger?.setAttribute('aria-expanded', 'false');
  header?.classList.remove('menu-open');
  menuToggle?.setAttribute('aria-expanded', 'false');
});

document.querySelectorAll('.primary-nav a').forEach((link) => {
  link.addEventListener('click', () => {
    header?.classList.remove('menu-open');
    menuToggle?.setAttribute('aria-expanded', 'false');
  });
});

document.querySelectorAll('.service-card').forEach((card) => {
  card.addEventListener('click', () => {
    const flipped = !card.classList.contains('is-flipped');
    card.classList.toggle('is-flipped', flipped);
    card.setAttribute('aria-pressed', String(flipped));
  });
});

const heroCleaner = document.querySelector('.hero-cleaner');
const heroReviews = document.querySelector('.hero-reviews');
const heroReviewProof = heroReviews?.querySelector('.review-proof');
const heroBubbles = [...document.querySelectorAll('.hero-bubble')];
if (heroCleaner && heroReviews && heroReviewProof) {
  const liftTransitionMs = 320;
  const clearancePx = 10;
  const bubbleClearancePx = 6;
  let trackingFrame = 0;
  let passDurationMs = 5200;

  const stopReviewTracking = () => {
    if (trackingFrame) cancelAnimationFrame(trackingFrame);
    trackingFrame = 0;
    heroReviews.classList.remove('is-cleaner-near');
  };

  const trackCleanerPosition = () => {
    const cleanerRect = heroCleaner.getBoundingClientRect();
    const proofRect = heroReviewProof.getBoundingClientRect();
    const sceneRect = heroCleaner.closest('.hero-cleaning-scene')?.getBoundingClientRect();
    const sceneWidth = sceneRect?.width || window.innerWidth;
    const approachDistance = (sceneWidth / passDurationMs) * liftTransitionMs + clearancePx;
    const hasApproached = cleanerRect.left <= proofRect.right + approachDistance;
    const hasNotCleared = cleanerRect.right >= proofRect.left - clearancePx;

    heroReviews.classList.toggle('is-cleaner-near', hasApproached && hasNotCleared);
    heroBubbles.forEach((bubble) => {
      if (bubble.classList.contains('is-released')) return;
      const bubbleLeft = (sceneRect?.left || 0) + bubble.offsetLeft;
      if (cleanerRect.right <= bubbleLeft - bubbleClearancePx) bubble.classList.add('is-released');
    });
    trackingFrame = requestAnimationFrame(trackCleanerPosition);
  };

  heroCleaner.addEventListener('animationstart', (event) => {
    if (event.animationName !== 'hero-cleaner-pass') return;
    stopReviewTracking();
    heroBubbles.forEach((bubble) => bubble.classList.remove('is-released'));
    const passAnimation = heroCleaner.getAnimations().find((animation) => animation.animationName === 'hero-cleaner-pass');
    const measuredDuration = Number(passAnimation?.effect.getTiming().duration);
    if (Number.isFinite(measuredDuration) && measuredDuration > 0) passDurationMs = measuredDuration;
    trackCleanerPosition();
  });

  heroCleaner.addEventListener('animationend', (event) => {
    if (event.animationName === 'hero-cleaner-pass') stopReviewTracking();
  });
}

const serviceMapElement = document.querySelector('#service-map');
if (serviceMapElement && window.L) {
  const usesCoarsePointer = window.matchMedia('(hover: none) and (pointer: coarse)').matches;
  const serviceMap = L.map(serviceMapElement, {
    dragging: !usesCoarsePointer,
    scrollWheelZoom: false,
    zoomControl: false,
    tap: !usesCoarsePointer,
    touchZoom: true
  }).setView([38.895, -77.10], 9);
  serviceMap.attributionControl.setPrefix(false);
  L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}', {
    maxZoom: 19,
    attribution: 'Tiles &copy; Esri &mdash; Source: Esri, HERE, Garmin, USGS, and the GIS User Community'
  }).addTo(serviceMap);
  L.control.zoom({ position: 'topright' }).addTo(serviceMap);
  const serviceAreas = [
    ['Washington, DC',38.9072,-77.0369],['Springfield, VA',38.7893,-77.1872],['Alexandria, VA',38.8048,-77.0469],
    ['Arlington, VA',38.8816,-77.0910],['Fairfax, VA',38.8462,-77.3064],['Falls Church, VA',38.8823,-77.1711],
    ['Annandale, VA',38.8304,-77.1964],['Ashburn, VA',39.0438,-77.4874],['Aldie, VA',38.9757,-77.6416],
    ['Bristow, VA',38.7226,-77.5361],['Centreville, VA',38.8404,-77.4289],['Chantilly, VA',38.8943,-77.4311],
    ['Dumfries, VA',38.5676,-77.3280],['Gainesville, VA',38.7957,-77.6139],['Leesburg, VA',39.1157,-77.5636],
    ['Manassas, VA',38.7509,-77.4753],['Stafford, VA',38.4221,-77.4083],['Warrenton, VA',38.7135,-77.7953],
    ['Accokeek, MD',38.6676,-77.0283],['Bethesda, MD',38.9847,-77.0947],['Bowie, MD',39.0068,-76.7791],
    ['Columbia, MD',39.2037,-76.8610],['Gaithersburg, MD',39.1434,-77.2014],['Germantown, MD',39.1732,-77.2717],
    ['Glen Burnie, MD',39.1626,-76.6247],['Indian Head, MD',38.6001,-77.1622],['Laurel, MD',39.0993,-76.8483],
    ['Potomac, MD',39.0182,-77.2086],['Silver Spring, MD',38.9907,-77.0261],['Upper Marlboro, MD',38.8159,-76.7497],
    ['Waldorf, MD',38.6246,-76.9391]
  ];
  const pinIcon = L.divIcon({ className: 'service-pin', html: '<span></span>', iconSize: [24,24], iconAnchor: [12,12] });
  const bounds = [];
  serviceAreas.forEach(([name,lat,lng]) => {
    const locationSlug = name.toLowerCase().replace(/,/g, '').replace(/\s+/g, '-');
    const popup = `<a class="map-popup-link" href="/locations/${locationSlug}/"><strong>${name}</strong><span>View city guide ↗</span></a>`;
    L.marker([lat,lng], { icon: pinIcon }).addTo(serviceMap).bindPopup(popup);
    bounds.push([lat,lng]);
  });
  serviceMap.setView([38.90, -77.12], 10);

  if (usesCoarsePointer) {
    const mapShell = serviceMapElement.closest('.map-shell');
    let hintTimer;
    const hideGestureHint = () => mapShell?.classList.remove('is-gesture-hint');
    serviceMapElement.addEventListener('touchstart', (event) => {
      window.clearTimeout(hintTimer);
      if (event.touches.length > 1) {
        hideGestureHint();
        return;
      }
      mapShell?.classList.add('is-gesture-hint');
      hintTimer = window.setTimeout(hideGestureHint, 1200);
    }, { passive: true });
    serviceMapElement.addEventListener('touchend', () => {
      hintTimer = window.setTimeout(hideGestureHint, 700);
    }, { passive: true });
  }
}

const galleryDialog = document.querySelector('.gallery-lightbox');
const galleryButtons = [...document.querySelectorAll('[data-gallery-src]')];
let galleryIndex = 0;
const showGalleryImage = (index) => {
  if (!galleryDialog || !galleryButtons.length) return;
  galleryIndex = (index + galleryButtons.length) % galleryButtons.length;
  const button = galleryButtons[galleryIndex];
  const image = galleryDialog.querySelector('img');
  image.src = button.dataset.gallerySrc;
  image.alt = button.querySelector('img')?.alt || 'Expanded cleaning project';
};
galleryButtons.forEach((button,index) => button.addEventListener('click', () => {
  showGalleryImage(index);
  galleryDialog.showModal();
}));
galleryDialog?.querySelector('.lightbox-close')?.addEventListener('click', () => galleryDialog.close());
galleryDialog?.querySelector('.lightbox-prev')?.addEventListener('click', () => showGalleryImage(galleryIndex - 1));
galleryDialog?.querySelector('.lightbox-next')?.addEventListener('click', () => showGalleryImage(galleryIndex + 1));
galleryDialog?.addEventListener('click', (event) => { if (event.target === galleryDialog) galleryDialog.close(); });
document.addEventListener('keydown', (event) => {
  if (!galleryDialog?.open) return;
  if (event.key === 'ArrowLeft') showGalleryImage(galleryIndex - 1);
  if (event.key === 'ArrowRight') showGalleryImage(galleryIndex + 1);
});

const careerForm = document.querySelector('[data-career-form]');
const resumeInput = careerForm?.querySelector('input[type="file"]');
resumeInput?.addEventListener('change', () => {
  const target = careerForm.querySelector('[data-file-name]');
  if (target) target.textContent = resumeInput.files?.[0]?.name || 'Choose a file';
});

const connectNetlifyForm = (form, successMessage) => {
  if (!form) return;
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const status = form.querySelector('[data-form-status]');
    const button = form.querySelector('[type="submit"]');
    const buttonLabel = button?.innerHTML;
    if (status) status.textContent = 'Sending…';
    if (button) {
      button.disabled = true;
      button.setAttribute('aria-busy', 'true');
    }

    try {
      const data = new FormData(form);
      const request = { method: 'POST', body: data };
      if (form.enctype !== 'multipart/form-data') {
        const encoded = new URLSearchParams();
        data.forEach((value, key) => encoded.append(key, String(value)));
        request.body = encoded.toString();
        request.headers = { 'Content-Type': 'application/x-www-form-urlencoded' };
      }
      const response = await fetch(form.action || '/', request);
      if (!response.ok) throw new Error(`Submission failed with ${response.status}`);
      form.reset();
      const fileName = form.querySelector('[data-file-name]');
      if (fileName) fileName.textContent = 'Choose a file';
      if (status) status.textContent = successMessage;
    } catch (error) {
      console.error(error);
      if (status) status.textContent = 'We could not send this right now. Please call (703) 975-9099.';
    } finally {
      if (button) {
        button.disabled = false;
        button.removeAttribute('aria-busy');
        if (buttonLabel) button.innerHTML = buttonLabel;
      }
    }
  });
};

connectNetlifyForm(careerForm, 'Thanks — your application was sent to the Shiny team.');

const blogGrid = document.querySelector('[data-blog-grid]');
if (blogGrid) {
  const blogCards = [...blogGrid.querySelectorAll('[data-blog-card]')];
  const filterButtons = [...document.querySelectorAll('[data-blog-filter]')];
  const sortButtons = [...document.querySelectorAll('[data-blog-sort]')];
  const filterSelect = document.querySelector('[data-blog-filter-select]');
  const sortSelect = document.querySelector('[data-blog-sort-select]');
  let activeFilter = 'all';
  let activeSort = 'newest';

  const renderBlogs = () => {
    const direction = activeSort === 'oldest' ? 1 : -1;
    [...blogCards]
      .sort((a,b) => a.dataset.date.localeCompare(b.dataset.date) * direction)
      .forEach((card) => {
        card.hidden = activeFilter !== 'all' && card.dataset.category !== activeFilter;
        blogGrid.appendChild(card);
      });
    filterButtons.forEach((button) => {
      const active = button.dataset.blogFilter === activeFilter;
      button.classList.toggle('is-active', active);
      button.setAttribute('aria-pressed', String(active));
    });
    sortButtons.forEach((button) => {
      const active = button.dataset.blogSort === activeSort;
      button.classList.toggle('is-active', active);
      button.setAttribute('aria-pressed', String(active));
    });
    if (filterSelect) filterSelect.value = activeFilter;
    if (sortSelect) sortSelect.value = activeSort;
  };

  filterButtons.forEach((button) => button.addEventListener('click', () => {
    activeFilter = button.dataset.blogFilter;
    renderBlogs();
  }));
  sortButtons.forEach((button) => button.addEventListener('click', () => {
    activeSort = button.dataset.blogSort;
    renderBlogs();
  }));
  filterSelect?.addEventListener('change', () => { activeFilter = filterSelect.value; renderBlogs(); });
  sortSelect?.addEventListener('change', () => { activeSort = sortSelect.value; renderBlogs(); });
  renderBlogs();
}

const estimateForm = document.querySelector('[data-estimate-form]');
connectNetlifyForm(estimateForm, 'Thanks — your quote request was sent to the Shiny team.');

const contactForm = document.querySelector('[data-contact-form]');
connectNetlifyForm(contactForm, 'Thanks — your message was sent to the Shiny team.');
