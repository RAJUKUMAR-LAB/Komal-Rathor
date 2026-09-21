/**
 * KOMAL RATHOR - PORTFOLIO & INTERACTIVE RESUME JAVASCRIPT
 */

document.addEventListener('DOMContentLoaded', () => {
  initThemeToggle();
  initDynamicRoleText();
  initMobileMenu();
  initSkillsFilter();
  initCopyToClipboard();
  initContactForm();
  initPrintButton();
  initScrollSpy();
});

/* ==========================================================
   1. THEME TOGGLE (Dark / Light Mode)
   ========================================================== */
function initThemeToggle() {
  const themeToggleBtn = document.getElementById('theme-toggle-btn');
  const htmlRoot = document.documentElement;

  // Retrieve saved theme or default to 'dark'
  const savedTheme = localStorage.getItem('kr_theme') || 'dark';
  htmlRoot.setAttribute('data-theme', savedTheme);

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
      const currentTheme = htmlRoot.getAttribute('data-theme');
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

      htmlRoot.setAttribute('data-theme', newTheme);
      localStorage.setItem('kr_theme', newTheme);
      showToast(`Switched to ${newTheme.toUpperCase()} mode 🌓`);
    });
  }
}

/* ==========================================================
   2. DYNAMIC ROTATING / TYPING ROLE TEXT
   ========================================================== */
function initDynamicRoleText() {
  const roleElement = document.getElementById('dynamic-role');
  if (!roleElement) return;

  const roles = [
    'an Aspiring Web Developer',
    'a Frontend & React Developer',
    'a Python & C Programmer',
    'a B.Tech Scholar (2024–27)',
    'a Next.js Enthusiast'
  ];

  let roleIndex = 0;
  let charIndex = 0;
  let isDeleting = false;
  let typingSpeed = 100;

  function type() {
    const currentRole = roles[roleIndex];

    if (isDeleting) {
      roleElement.textContent = currentRole.substring(0, charIndex - 1);
      charIndex--;
      typingSpeed = 50;
    } else {
      roleElement.textContent = currentRole.substring(0, charIndex + 1);
      charIndex++;
      typingSpeed = 100;
    }

    if (!isDeleting && charIndex === currentRole.length) {
      typingSpeed = 2000; // Pause at end of text
      isDeleting = true;
    } else if (isDeleting && charIndex === 0) {
      isDeleting = false;
      roleIndex = (roleIndex + 1) % roles.length;
      typingSpeed = 500; // Pause before typing new word
    }

    setTimeout(type, typingSpeed);
  }

  type();
}

/* ==========================================================
   3. MOBILE MENU TOGGLE
   ========================================================== */
function initMobileMenu() {
  const toggleBtn = document.getElementById('mobile-menu-toggle');
  const navLinks = document.getElementById('nav-links');

  if (!toggleBtn || !navLinks) return;

  toggleBtn.addEventListener('click', () => {
    const isOpen = navLinks.classList.toggle('active');
    toggleBtn.classList.toggle('active', isOpen);
    toggleBtn.setAttribute('aria-expanded', isOpen);
  });

  // Close menu when clicking on any link or button
  navLinks.querySelectorAll('a, button').forEach(link => {
    link.addEventListener('click', () => {
      navLinks.classList.remove('active');
      toggleBtn.classList.remove('active');
      toggleBtn.setAttribute('aria-expanded', 'false');
    });
  });

  // Close when clicking outside
  document.addEventListener('click', (e) => {
    if (!toggleBtn.contains(e.target) && !navLinks.contains(e.target)) {
      navLinks.classList.remove('active');
      toggleBtn.classList.remove('active');
      toggleBtn.setAttribute('aria-expanded', 'false');
    }
  });
}

/* ==========================================================
   4. SKILLS FILTER TABS
   ========================================================== */
function initSkillsFilter() {
  const filterBtns = document.querySelectorAll('.skills-filter .filter-btn');
  const skillCards = document.querySelectorAll('.skills-grid .skill-card');

  if (!filterBtns.length || !skillCards.length) return;

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => {
        b.classList.remove('active');
        b.setAttribute('aria-selected', 'false');
      });
      btn.classList.add('active');
      btn.setAttribute('aria-selected', 'true');

      const filterValue = btn.getAttribute('data-filter');

      skillCards.forEach(card => {
        const category = card.getAttribute('data-category');
        if (filterValue === 'all' || category === filterValue) {
          card.style.display = 'flex';
          setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
          }, 10);
        } else {
          card.style.opacity = '0';
          card.style.transform = 'translateY(10px)';
          setTimeout(() => {
            card.style.display = 'none';
          }, 200);
        }
      });
    });
  });
}

/* ==========================================================
   5. COPY TO CLIPBOARD
   ========================================================== */
function initCopyToClipboard() {
  const copyBtns = document.querySelectorAll('.copy-btn');

  copyBtns.forEach(btn => {
    btn.addEventListener('click', async () => {
      const textToCopy = btn.getAttribute('data-copy');
      if (!textToCopy) return;

      try {
        await navigator.clipboard.writeText(textToCopy);
        showToast(`Copied "${textToCopy}" to clipboard! 📋`);

        // Quick visual feedback on the button
        const originalHtml = btn.innerHTML;
        btn.innerHTML = `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#10b981" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>`;
        setTimeout(() => {
          btn.innerHTML = originalHtml;
        }, 2000);
      } catch (err) {
        showToast(`Error copying: ${textToCopy}`);
      }
    });
  });
}

/* ==========================================================
   6. CONTACT FORM HANDLER
   ========================================================== */
function initContactForm() {
  const form = document.getElementById('contact-form');
  if (!form) return;

  let isSubmitting = false;

  form.addEventListener('submit', (e) => {
    e.preventDefault();

    if (isSubmitting) return;

    const name = document.getElementById('sender-name').value.trim();
    const email = document.getElementById('sender-email').value.trim();
    const subject = document.getElementById('sender-subject').value.trim() || 'Website Inquiry for Komal Rathor';
    const message = document.getElementById('sender-message').value.trim();

    if (!name || !email || !message) {
      showToast('Please complete all required fields ⚠️');
      return;
    }

    // Email format validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      showToast('Please enter a valid email address ⚠️');
      return;
    }

    // Sanitize message strings
    const cleanName = name.replace(/[<>]/g, '');
    const cleanSubject = subject.replace(/[<>]/g, '');
    const cleanMessage = message.replace(/[<>]/g, '');

    const mailtoUrl = `mailto:komalrathorebgs@gmail.com?subject=${encodeURIComponent(cleanSubject)}&body=${encodeURIComponent(
      `Hello Komal,\n\nMy name is ${cleanName} (${email}).\n\nMessage:\n${cleanMessage}\n\nSent from your portfolio website (komalrathor.in).`
    )}`;

    isSubmitting = true;
    const submitBtn = form.querySelector('button[type="submit"]');
    if (submitBtn) submitBtn.disabled = true;

    showToast('Opening your email client... 🚀');
    window.location.href = mailtoUrl;

    form.reset();

    setTimeout(() => {
      isSubmitting = false;
      if (submitBtn) submitBtn.disabled = false;
    }, 3000);
  });
}

/* ==========================================================
   7. PRINT BUTTON
   ========================================================== */
function initPrintButton() {
  const printBtn = document.getElementById('print-resume-btn');
  if (printBtn) {
    printBtn.addEventListener('click', () => {
      window.print();
    });
  }
}

/* ==========================================================
   8. SCROLL SPY FOR NAVIGATION
   ========================================================== */
function initScrollSpy() {
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-links .nav-link');

  if (!sections.length || !navLinks.length) return;

  window.addEventListener('scroll', () => {
    let currentId = '';
    const scrollPosition = window.pageYOffset + 120;

    sections.forEach(sec => {
      const sectionTop = sec.offsetTop;
      const sectionHeight = sec.offsetHeight;
      if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
        currentId = sec.getAttribute('id');
      }
    });

    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === `#${currentId}`) {
        link.classList.add('active');
      }
    });
  }, { passive: true });
}

/* ==========================================================
   9. TOAST NOTIFICATION UTILITY
   ========================================================== */
function showToast(message) {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.innerHTML = `
    <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 14 14"/></svg>
    <span>${message}</span>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.animation = 'fadeOut 0.3s ease-out forwards';
    setTimeout(() => {
      toast.remove();
    }, 300);
  }, 3500);
}
