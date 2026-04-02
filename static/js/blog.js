document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.querySelector("input[name='title']");
    if (searchInput) {
        searchInput.placeholder = "Search blog posts";
    }
});
