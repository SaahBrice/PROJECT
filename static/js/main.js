/**
 * FDTM Platform - Premium Animations & Effects
 * Parallax, counters, scroll animations, and more
 */

document.addEventListener('DOMContentLoaded', function () {
    initScrollAnimations();
    initProgressBars();
    initParallax();
    initCounters();
    initTimeline();
    initSmoothReveal();
});

/**
 * Parallax scrolling effect
 */
function initParallax() {
    const parallaxElements = document.querySelectorAll('[data-parallax]');
    if (parallaxElements.length === 0) return;

    let ticking = false;

    function updateParallax() {
        const scrollY = window.pageYOffset;

        parallaxElements.forEach(el => {
            const speed = parseFloat(el.dataset.parallax) || 0.5;
            const rect = el.getBoundingClientRect();
            const yPos = -(scrollY * speed);
            el.style.transform = `translate3d(0, ${yPos}px, 0)`;
        });

        ticking = false;
    }

    window.addEventListener('scroll', () => {
        if (!ticking) {
            requestAnimationFrame(updateParallax);
            ticking = true;
        }
    });
}

/**
 * Scroll-triggered animations using Intersection Observer
 */
function initScrollAnimations() {
    const animatedElements = document.querySelectorAll('[data-animate]');
    if (animatedElements.length === 0) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                const delay = entry.target.dataset.delay || index * 100;
                setTimeout(() => {
                    entry.target.classList.add('animate-fade-in-up');
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, delay);
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -80px 0px'
    });

    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(40px)';
        el.style.transition = 'all 0.8s cubic-bezier(0.4, 0, 0.2, 1)';
        observer.observe(el);
    });
}

/**
 * Smooth reveal for sections
 */
function initSmoothReveal() {
    const sections = document.querySelectorAll('[data-reveal]');
    if (sections.length === 0) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.15 });

    sections.forEach(section => observer.observe(section));
}

/**
 * Animate progress bars when they come into view
 */
function initProgressBars() {
    const progressBars = document.querySelectorAll('[data-progress]');
    if (progressBars.length === 0) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const bar = entry.target;
                const progress = bar.dataset.progress || 0;
                const fill = bar.querySelector('.progress-bar-fill');

                if (fill) {
                    setTimeout(() => {
                        fill.style.width = progress + '%';
                    }, 300);
                }
                observer.unobserve(bar);
            }
        });
    }, { threshold: 0.5 });

    progressBars.forEach(bar => {
        const fill = bar.querySelector('.progress-bar-fill');
        if (fill) fill.style.width = '0%';
        observer.observe(bar);
    });
}

/**
 * Animated counters for impact numbers
 */
function initCounters() {
    const counters = document.querySelectorAll('[data-counter]');
    if (counters.length === 0) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                const target = parseInt(el.dataset.counter) || 0;
                const suffix = el.dataset.suffix || '';
                animateCounter(el, target, 2000, suffix);
                observer.unobserve(el);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(counter => observer.observe(counter));
}

function animateCounter(element, target, duration = 2000, suffix = '') {
    let start = 0;
    const startTime = performance.now();

    function easeOutQuart(t) {
        return 1 - Math.pow(1 - t, 4);
    }

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const easedProgress = easeOutQuart(progress);
        const current = Math.floor(easedProgress * target);

        element.textContent = current.toLocaleString() + suffix;

        if (progress < 1) {
            requestAnimationFrame(update);
        } else {
            element.textContent = target.toLocaleString() + suffix;
        }
    }

    requestAnimationFrame(update);
}

/**
 * Timeline animation
 */
function initTimeline() {
    const timelineItems = document.querySelectorAll('.timeline-item');
    if (timelineItems.length === 0) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('timeline-visible');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.3 });

    timelineItems.forEach(item => observer.observe(item));
}

/**
 * Magnetic hover effect for buttons
 */
function initMagneticButtons() {
    const buttons = document.querySelectorAll('[data-magnetic]');

    buttons.forEach(button => {
        button.addEventListener('mousemove', (e) => {
            const rect = button.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;

            button.style.transform = `translate(${x * 0.15}px, ${y * 0.15}px)`;
        });

        button.addEventListener('mouseleave', () => {
            button.style.transform = 'translate(0, 0)';
        });
    });
}

// Smooth scroll
function scrollToElement(selector) {
    const element = document.querySelector(selector);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

// Format currency
function formatCurrency(amount, currency = 'EUR') {
    return new Intl.NumberFormat('fr-FR', { style: 'currency', currency }).format(amount);
}

// Expose functions globally
window.FDTM = { animateCounter, formatCurrency, scrollToElement };
