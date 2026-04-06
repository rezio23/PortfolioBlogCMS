document.addEventListener("DOMContentLoaded", () => {
    const updateSearchPlaceholder = (root = document) => {
        const searchInput = root.querySelector("input[name='title']");
        if (searchInput) {
            searchInput.placeholder = "Search blog posts";
        }
    };

    const revealInjectedContent = (root = document) => {
        const elements = [];

        if (root instanceof Element && root.matches("[data-reveal], [data-scroll-float]")) {
            elements.push(root);
        }

        root.querySelectorAll("[data-reveal], [data-scroll-float]").forEach((element) => {
            elements.push(element);
        });

        elements.forEach((element) => {
            element.classList.add("scroll-pop", "is-visible");
            element.style.transitionDelay = element.style.transitionDelay || "0ms";
        });
    };

    const replaceSection = (selector, incomingRoot) => {
        const current = document.querySelector(selector);
        const next = incomingRoot.querySelector(selector);

        if (current && next) {
            current.replaceWith(next);
            return next;
        }

        if (current && !next) {
            current.remove();
        }

        return next || null;
    };

    const replacePagination = (incomingRoot) => {
        const current = document.querySelector(".pagination-shell");
        const next = incomingRoot.querySelector(".pagination-shell");

        if (current && next) {
            current.replaceWith(next);
            return next;
        }

        if (!current && next) {
            const postsSection = document.querySelector("#blog-posts");
            if (postsSection) {
                postsSection.insertAdjacentElement("afterend", next);
            }
            return next;
        }

        if (current && !next) {
            current.remove();
        }

        return next || null;
    };

    const replacePostCount = (incomingRoot) => {
        const selector = ".blog-page-hero__showcase .about-panel--primary .about-panel__title";
        const current = document.querySelector(selector);
        const next = incomingRoot.querySelector(selector);

        if (current && next) {
            current.textContent = next.textContent;
        }
    };

    const enhanceBlogFilters = () => {
        updateSearchPlaceholder();

        const filterForm = document.querySelector(".blog-filter__form");
        if (!filterForm || filterForm.dataset.enhanced === "true") {
            return;
        }
        filterForm.dataset.enhanced = "true";

        const submitButton = filterForm.querySelector("button[type='submit']");
        const buildUrl = (overrideUrl) => {
            if (overrideUrl) {
                return overrideUrl;
            }

            const params = new URLSearchParams(new FormData(filterForm));
            for (const [key, value] of [...params.entries()]) {
                if (!String(value).trim()) {
                    params.delete(key);
                }
            }

            const basePath = filterForm.getAttribute("action") || window.location.pathname;
            const query = params.toString();
            return query ? `${basePath}?${query}` : basePath;
        };

        const loadResults = async (overrideUrl) => {
            const requestUrl = buildUrl(overrideUrl);

            if (submitButton) {
                submitButton.disabled = true;
                submitButton.dataset.originalText = submitButton.dataset.originalText || submitButton.textContent;
                submitButton.textContent = "Applying...";
            }

            try {
                const response = await fetch(requestUrl, {
                    headers: {
                        "X-Requested-With": "XMLHttpRequest",
                    },
                });

                if (!response.ok) {
                    throw new Error(`Request failed with status ${response.status}`);
                }

                const html = await response.text();
                const parser = new DOMParser();
                const incomingDoc = parser.parseFromString(html, "text/html");

                const filtersSection = replaceSection("#blog-filters", incomingDoc);
                const postsSection = replaceSection("#blog-posts", incomingDoc);
                const paginationSection = replacePagination(incomingDoc);
                replacePostCount(incomingDoc);

                revealInjectedContent(filtersSection || document);
                revealInjectedContent(postsSection || document);
                if (paginationSection) {
                    revealInjectedContent(paginationSection);
                }

                window.history.replaceState({}, "", requestUrl);
                enhanceBlogFilters();
                enhancePagination();
            } catch (error) {
                window.location.href = requestUrl;
            } finally {
                const latestSubmitButton = document.querySelector(".blog-filter__form button[type='submit']");
                if (latestSubmitButton) {
                    latestSubmitButton.disabled = false;
                    latestSubmitButton.textContent = latestSubmitButton.dataset.originalText || "Apply Filters";
                }
            }
        };

        filterForm.addEventListener("submit", (event) => {
            event.preventDefault();
            loadResults();
        });

        ["category", "tag"].forEach((name) => {
            const field = filterForm.querySelector(`[name='${name}']`);
            if (!field) {
                return;
            }

            field.addEventListener("change", () => {
                loadResults();
            });
        });
    };

    const enhancePagination = () => {
        document.querySelectorAll(".pagination-shell a.page-link").forEach((link) => {
            if (link.dataset.enhanced === "true") {
                return;
            }
            link.dataset.enhanced = "true";

            link.addEventListener("click", async (event) => {
                event.preventDefault();
                const filterForm = document.querySelector(".blog-filter__form");
                if (!filterForm) {
                    window.location.href = link.href;
                    return;
                }

                const submitButton = filterForm.querySelector("button[type='submit']");
                if (submitButton) {
                    submitButton.disabled = true;
                }

                try {
                    const response = await fetch(link.href, {
                        headers: {
                            "X-Requested-With": "XMLHttpRequest",
                        },
                    });

                    if (!response.ok) {
                        throw new Error(`Request failed with status ${response.status}`);
                    }

                    const html = await response.text();
                    const parser = new DOMParser();
                    const incomingDoc = parser.parseFromString(html, "text/html");

                    const filtersSection = replaceSection("#blog-filters", incomingDoc);
                    const postsSection = replaceSection("#blog-posts", incomingDoc);
                    const paginationSection = replacePagination(incomingDoc);
                    replacePostCount(incomingDoc);

                    revealInjectedContent(filtersSection || document);
                    revealInjectedContent(postsSection || document);
                    if (paginationSection) {
                        revealInjectedContent(paginationSection);
                    }

                    window.history.replaceState({}, "", link.href);
                    enhanceBlogFilters();
                    enhancePagination();
                } catch (error) {
                    window.location.href = link.href;
                } finally {
                    const latestSubmitButton = document.querySelector(".blog-filter__form button[type='submit']");
                    if (latestSubmitButton) {
                        latestSubmitButton.disabled = false;
                    }
                }
            });
        });
    };

    enhanceBlogFilters();
    enhancePagination();
});
