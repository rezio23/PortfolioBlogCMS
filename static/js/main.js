document.addEventListener("DOMContentLoaded", () => {
    const root = document.documentElement;
    const body = document.body;
    const alerts = document.querySelectorAll(".alert");
    const themeToggle = document.querySelector("[data-theme-toggle]");
    const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

    const setTheme = (theme) => {
        root.setAttribute("data-theme", theme);
        root.style.colorScheme = theme;

        try {
            localStorage.setItem("theme", theme);
        } catch (error) {
            // Ignore storage failures and keep the active theme for the current page.
        }

        if (themeToggle) {
            const icon = themeToggle.querySelector(".theme-toggle-btn__icon i");
            const label = themeToggle.querySelector(".theme-toggle-btn__label");
            const isDark = theme === "dark";

            themeToggle.setAttribute("aria-pressed", String(isDark));
            themeToggle.setAttribute("aria-label", isDark ? "Switch to light mode" : "Switch to dark mode");

            if (icon) {
                icon.className = isDark ? "fa-solid fa-sun" : "fa-solid fa-moon";
            }

            if (label) {
                label.textContent = isDark ? "Light" : "Dark";
            }
        }
    };

    const currentTheme = root.getAttribute("data-theme") === "dark" ? "dark" : "light";
    setTheme(currentTheme);

    if (themeToggle && themeToggle.dataset.themeBound !== "true") {
        themeToggle.dataset.themeBound = "true";
        themeToggle.addEventListener("click", () => {
            const nextTheme = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
            setTheme(nextTheme);
        });
    }

    alerts.forEach((alert) => {
        window.setTimeout(() => {
            alert.classList.add("show");
        }, 100);
    });

    const motionClassGroups = [
        {
            selector: "main .hero-showcase, main .about-hero, main .auth-login__showcase, main .portfolio-roadmap__shell, main .portfolio-hero",
            className: "portfolio-motion-surface",
        },
        {
            selector: "main .card, main .feature-card, main .hero-stat, main .about-panel, main .about-story-card, main .about-note-card, main .about-principle, main .about-journey__step, main .about-cta, main .auth-login__card, main .auth-login__pillar, main .skills-card, main .skills-hero__stat, main .portfolio-roadmap__card, main .hero-phone, main .hero-floating-card",
            className: "portfolio-hover-card",
        },
        {
            selector: "main .skills-list__item, main .hero-phone__list-item",
            className: "portfolio-hover-list",
        },
        {
            selector: "main .btn, main .site-action-btn, main .hero-btn, main .auth-social-btn, main .page-link",
            className: "portfolio-hover-button",
            exclude: [".btn-close"],
        },
        {
            selector: "main .hero-phone__chip, main .skills-hero__summary-item, main .hero-copy__eyebrow, main .about-hero__eyebrow, main .about-section__eyebrow, main .auth-login__eyebrow, main .auth-login__kicker, main .skills-card__eyebrow, main .portfolio-roadmap__eyebrow, main .portfolio-roadmap__year, main .about-journey__number",
            className: "portfolio-hover-chip",
        },
    ];

    const applyMotionClass = ({ selector, className, exclude = [] }) => {
        document.querySelectorAll(selector).forEach((element) => {
            if (exclude.some((pattern) => element.matches(pattern))) {
                return;
            }

            element.classList.add(className);
        });
    };

    motionClassGroups.forEach(applyMotionClass);

    const autoRevealGroups = [
        {
            selector: "main .hero-showcase, main .about-hero, main .auth-login__showcase, main .portfolio-roadmap__shell, main .portfolio-hero, main :is(.hero-copy, .hero-device-wrap, .about-section-heading, .auth-login__card, .skills-hero__panel, .portfolio-roadmap__heading, .portfolio-hero__content, .portfolio-hero__media, .about-cta), main .container > :is(.d-flex, h1, .card)",
            mode: "reveal",
            step: 90,
            depth: 12,
            baseDelay: 0,
        },
        {
            selector: "main .row > [class*='col-'] > :is(.card, .feature-card, .about-story-card, .about-note-card, .about-principle, .about-journey__step, .about-panel, .skills-card, .skills-hero__stat)",
            mode: "reveal",
            step: 80,
            depth: 14,
            baseDelay: 70,
        },
        {
            selector: "main :is(.hero-copy__actions > *, .hero-copy__stats > *, .hero-floating-card, .hero-phone, .hero-phone__grid > *, .hero-phone__list > *, .hero-phone__chips > *, .about-showcase > *, .about-mini-grid > *, .about-stack > *, .about-cta__actions > *, .auth-login__social-grid > *, .d-flex.gap-2 > *, .d-flex.flex-wrap.gap-3 > *, .skills-hero__summary > *, .skills-list > *, .pagination .page-item)",
            mode: "float",
            step: 70,
            depth: 10,
            baseDelay: 110,
        },
    ];

    const registerAutoReveal = ({ selector, mode = "reveal", step = 70, depth = 10, baseDelay = 0 }) => {
        document.querySelectorAll(selector).forEach((element, index) => {
            if (element.hasAttribute("data-reveal") || element.hasAttribute("data-scroll-float")) {
                return;
            }

            const delay = baseDelay + ((index % 6) * step);
            const elementDepth = depth + ((index % 3) * 2);

            if (mode === "float") {
                element.setAttribute("data-scroll-float", "");
            } else {
                element.setAttribute("data-reveal", "");
            }

            element.dataset.revealDelay = String(delay);
            element.dataset.floatDepth = String(elementDepth);
        });
    };

    autoRevealGroups.forEach(registerAutoReveal);

    const animatedElements = Array.from(
        new Set(document.querySelectorAll("[data-reveal], [data-scroll-float]"))
    );

    if (!animatedElements.length) {
        return;
    }

    animatedElements.forEach((element) => {
        element.classList.add("scroll-pop");
    });

    body.classList.add("motion-enabled");

    if (prefersReducedMotion.matches) {
        animatedElements.forEach((element) => {
            element.classList.add("is-visible");
        });
        return;
    }

    const revealObserver = "IntersectionObserver" in window
        ? new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("is-visible");
                    revealObserver.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.14,
            rootMargin: "0px 0px -10% 0px",
        })
        : null;

    animatedElements.forEach((element, index) => {
        const delay = Number(element.dataset.revealDelay || ((index % 5) * 70));
        const depth = Number(element.dataset.floatDepth || 10);
        const travel = Math.max(0.8, Math.min(1.7, depth / 10));

        element.style.transitionDelay = `${delay}ms`;
        element.style.setProperty("--float-enter-distance", `${travel.toFixed(2)}rem`);

        if (revealObserver) {
            revealObserver.observe(element);
        } else {
            element.classList.add("is-visible");
        }
    });
});
