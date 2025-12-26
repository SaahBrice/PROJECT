/**
 * FDTM Platform - Main JavaScript
 * Alpine.js is loaded via CDN, this file is for custom functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize any custom components
    initScrollAnimations();
    initProgressBars();
});

/**
 * Scroll-triggered animations using Intersection Observer
 */
function initScrollAnimations() {
    const animatedElements = document.querySelectorAll('[data-animate]');
    
    if (animatedElements.length === 0) return;
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in-up');
                entry.target.style.opacity = '1';
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        observer.observe(el);
    });
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
                    }, 200);
                }
                
                observer.unobserve(bar);
            }
        });
    }, { threshold: 0.5 });
    
    progressBars.forEach(bar => {
        const fill = bar.querySelector('.progress-bar-fill');
        if (fill) {
            fill.style.width = '0%';
        }
        observer.observe(bar);
    });
}

/**
 * Animated counter for impact numbers
 */
function animateCounter(element, target, duration = 2000) {
    let start = 0;
    const increment = target / (duration / 16);
    
    function updateCounter() {
        start += increment;
        if (start < target) {
            element.textContent = Math.floor(start).toLocaleString();
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = target.toLocaleString();
        }
    }
    
    updateCounter();
}

/**
 * Format currency for donations
 */
function formatCurrency(amount, currency = 'EUR') {
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: currency
    }).format(amount);
}

/**
 * Smooth scroll to element
 */
function scrollToElement(selector) {
    const element = document.querySelector(selector);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Expose functions globally for use in templates
window.FDTM = {
    animateCounter,
    formatCurrency,
    scrollToElement
};
