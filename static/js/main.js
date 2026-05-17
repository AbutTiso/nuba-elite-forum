// Mobile Menu Toggle
function toggleMobileMenu() {
    const menu = document.getElementById('mobile-menu');
    menu.classList.toggle('hidden');
}

// Navbar Scroll Effect
window.addEventListener('scroll', function() {
    const navbar = document.getElementById('navbar');
    const backToTop = document.getElementById('back-to-top');
    
    if (window.scrollY > 50) {
        navbar.classList.add('shadow-lg');
        navbar.classList.remove('shadow-sm');
    } else {
        navbar.classList.add('shadow-sm');
        navbar.classList.remove('shadow-lg');
    }
    
    // Back to Top visibility
    if (window.scrollY > 500) {
        backToTop.classList.remove('opacity-0', 'invisible');
        backToTop.classList.add('opacity-100', 'visible');
    } else {
        backToTop.classList.add('opacity-0', 'invisible');
        backToTop.classList.remove('opacity-100', 'visible');
    }
});

// Smooth Scroll for Anchor Links
document.querySelectorAll('a[href^=\"#\"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href === '#') return;
        e.preventDefault();
        const target = document.querySelector(href);
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Intersection Observer for Fade-in Animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -30px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe elements with data-animate attribute
document.addEventListener('DOMContentLoaded', function() {
    const animatedElements = document.querySelectorAll('[data-animate]');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.7s cubic-bezier(0.4, 0, 0.2, 1), transform 0.7s cubic-bezier(0.4, 0, 0.2, 1)';
        observer.observe(el);
    });
});

// Close mobile menu when clicking outside
document.addEventListener('click', function(e) {
    const menu = document.getElementById('mobile-menu');
    const menuBtn = e.target.closest('button[onclick=\"toggleMobileMenu()\"]');
    if (!menu.classList.contains('hidden') && !menu.contains(e.target) && !menuBtn) {
        menu.classList.add('hidden');
    }
});

console.log('Nuba Elite Forum — Platform Ready');


// Dark Mode Toggle
function toggleDarkMode() {
    document.documentElement.classList.toggle('dark');
    const isDark = document.documentElement.classList.contains('dark');
    localStorage.setItem('darkMode', isDark);
}

// Check saved preference
if (localStorage.getItem('darkMode') === 'true') {
    document.documentElement.classList.add('dark');
}

