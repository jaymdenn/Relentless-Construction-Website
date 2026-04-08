// Relentless Construction - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {

    // Mobile Menu Toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const nav = document.querySelector('.nav');

    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', function() {
            this.classList.toggle('active');
            nav.classList.toggle('active');
        });
    }

    // Close mobile menu when clicking a link
    const navLinks = document.querySelectorAll('.nav-list a');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            mobileMenuBtn.classList.remove('active');
            nav.classList.remove('active');
        });
    });

    // FAQ Accordion
    const faqItems = document.querySelectorAll('.faq-item');

    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');

        question.addEventListener('click', () => {
            // Close other open items
            faqItems.forEach(otherItem => {
                if (otherItem !== item && otherItem.classList.contains('active')) {
                    otherItem.classList.remove('active');
                }
            });

            // Toggle current item
            item.classList.toggle('active');
        });
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const headerOffset = 80;
                const elementPosition = target.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Header scroll effect
    const header = document.querySelector('.header');
    let lastScroll = 0;

    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;

        if (currentScroll > 100) {
            header.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.2)';
        } else {
            header.style.boxShadow = 'none';
        }

        lastScroll = currentScroll;
    });

    // Form submission handling
    const contactForm = document.getElementById('contact-form');

    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();

            // Get form data
            const formData = new FormData(this);
            const name = formData.get('name');
            const email = formData.get('email');
            const message = formData.get('message');

            // Basic validation
            if (!name || !email || !message) {
                alert('Please fill in all fields.');
                return;
            }

            // Email validation
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                alert('Please enter a valid email address.');
                return;
            }

            // Show success message (in a real implementation, you would send this to a server)
            alert('Thank you for your message! We will get back to you soon.');
            this.reset();
        });
    }

    // Intersection Observer for animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe elements for animation
    const animateElements = document.querySelectorAll(
        '.service-card, .testimonial-card, .process-step, .area-card, .stat-box'
    );

    animateElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(el);
    });

    // Add animation class styles
    const style = document.createElement('style');
    style.textContent = `
        .animate-in {
            opacity: 1 !important;
            transform: translateY(0) !important;
        }
    `;
    document.head.appendChild(style);

    // Stagger animations for grid items
    const staggerElements = (selector, delay = 100) => {
        const elements = document.querySelectorAll(selector);
        elements.forEach((el, index) => {
            el.style.transitionDelay = `${index * delay}ms`;
        });
    };

    staggerElements('.service-card', 100);
    staggerElements('.testimonial-card', 100);
    staggerElements('.process-step', 150);

});

// Preload hero image
window.addEventListener('load', function() {
    const heroImg = new Image();
    heroImg.src = 'assets/images/hero-bg.webp';
});

// Form Popup Functions
function openFormPopup() {
    const popup = document.getElementById('form-popup');
    if (popup) {
        popup.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

function closeFormPopup(event) {
    const popup = document.getElementById('form-popup');
    if (popup) {
        if (!event || event.target === popup) {
            popup.classList.remove('active');
            document.body.style.overflow = '';
        }
    }
}

// Close popup on Escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeFormPopup();
        closeLightbox();
    }
});

// ============================================
// Portfolio Gallery Filter & Lightbox
// ============================================

// Gallery Filter
document.addEventListener('DOMContentLoaded', function() {
    const filterBtns = document.querySelectorAll('.filter-btn');
    const galleryItems = document.querySelectorAll('.gallery-item');

    if (filterBtns.length > 0) {
        filterBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                // Update active button
                filterBtns.forEach(b => b.classList.remove('active'));
                this.classList.add('active');

                const filter = this.dataset.filter;

                // Filter items
                galleryItems.forEach(item => {
                    if (filter === 'all' || item.dataset.category === filter) {
                        item.classList.remove('hidden');
                    } else {
                        item.classList.add('hidden');
                    }
                });
            });
        });

        // Click to open lightbox
        galleryItems.forEach((item, index) => {
            item.addEventListener('click', function() {
                openLightbox(this.querySelector('img').src, this.dataset.category);
            });
        });
    }
});

// Lightbox Variables
let currentLightboxItems = [];
let currentLightboxIndex = 0;

// Open Lightbox
function openLightbox(imgSrc, category) {
    const lightbox = document.getElementById('gallery-lightbox');
    const lightboxImg = document.getElementById('lightbox-image');
    const lightboxCaption = document.getElementById('lightbox-caption');

    if (lightbox && lightboxImg) {
        // Get all visible gallery items for navigation
        const visibleItems = document.querySelectorAll('.gallery-item:not(.hidden)');
        currentLightboxItems = Array.from(visibleItems).map(item => ({
            src: item.querySelector('img').src,
            category: item.dataset.category
        }));

        // Find current index
        currentLightboxIndex = currentLightboxItems.findIndex(item => item.src === imgSrc);

        lightboxImg.src = imgSrc;
        lightboxCaption.textContent = category.charAt(0).toUpperCase() + category.slice(1) + ' Project';
        lightbox.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

// Close Lightbox
function closeLightbox() {
    const lightbox = document.getElementById('gallery-lightbox');
    if (lightbox) {
        lightbox.classList.remove('active');
        document.body.style.overflow = '';
    }
}

// Navigate Lightbox
function navigateLightbox(direction) {
    if (currentLightboxItems.length === 0) return;

    currentLightboxIndex += direction;

    // Loop around
    if (currentLightboxIndex < 0) {
        currentLightboxIndex = currentLightboxItems.length - 1;
    } else if (currentLightboxIndex >= currentLightboxItems.length) {
        currentLightboxIndex = 0;
    }

    const item = currentLightboxItems[currentLightboxIndex];
    const lightboxImg = document.getElementById('lightbox-image');
    const lightboxCaption = document.getElementById('lightbox-caption');

    if (lightboxImg && item) {
        lightboxImg.src = item.src;
        lightboxCaption.textContent = item.category.charAt(0).toUpperCase() + item.category.slice(1) + ' Project';
    }
}

// Keyboard navigation for lightbox
document.addEventListener('keydown', function(e) {
    const lightbox = document.getElementById('gallery-lightbox');
    if (lightbox && lightbox.classList.contains('active')) {
        if (e.key === 'ArrowLeft') {
            navigateLightbox(-1);
        } else if (e.key === 'ArrowRight') {
            navigateLightbox(1);
        }
    }
});

// Close lightbox on background click
document.addEventListener('click', function(e) {
    const lightbox = document.getElementById('gallery-lightbox');
    if (lightbox && e.target === lightbox) {
        closeLightbox();
    }
});
