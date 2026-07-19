document.addEventListener('DOMContentLoaded', () => {
    const sections = document.querySelectorAll('.section-panel');
    const navLinks = document.querySelectorAll('[data-target]');
    const navbar = document.querySelector('.site-nav');

    function activateSection(targetId) {
        sections.forEach(section => section.classList.toggle('active', section.id === targetId));
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.toggle('active', link.dataset.target === targetId);
        });
        const target = document.getElementById(targetId);
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }

    navLinks.forEach(link => {
        link.addEventListener('click', event => {
            const targetId = link.dataset.target;
            if (!targetId) return;
            event.preventDefault();
            activateSection(targetId);
            history.replaceState(null, '', `#${targetId}`);
        });
    });

    document.querySelectorAll('.filter-btn').forEach(button => {
        button.addEventListener('click', () => {
            const filter = button.dataset.filter;
            document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            document.querySelectorAll('.gallery-item').forEach(item => {
                const visible = filter === 'all' || item.classList.contains(filter);
                item.classList.toggle('is-hidden', !visible);
            });
        });
    });

    const revealObserver = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                revealObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.16 });

    document.querySelectorAll('.reveal').forEach(element => revealObserver.observe(element));

    const counterObserver = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (!entry.isIntersecting) return;
            const counter = entry.target;
            const target = Number(counter.dataset.counter);
            const duration = 1200;
            const start = performance.now();
            function tick(now) {
                const progress = Math.min((now - start) / duration, 1);
                const eased = 1 - Math.pow(1 - progress, 3);
                counter.textContent = `${Math.round(target * eased)}+`;
                if (progress < 1) requestAnimationFrame(tick);
            }
            requestAnimationFrame(tick);
            counterObserver.unobserve(counter);
        });
    }, { threshold: 0.5 });

    document.querySelectorAll('[data-counter]').forEach(counter => counterObserver.observe(counter));

    window.addEventListener('scroll', () => {
        navbar.classList.toggle('is-scrolled', window.scrollY > 20);
    }, { passive: true });

    const initial = window.location.hash.replace('#', '');
    if (initial && document.getElementById(initial)) {
        activateSection(initial);
    }
});
