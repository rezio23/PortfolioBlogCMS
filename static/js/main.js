document.addEventListener("DOMContentLoaded", () => {
    const alerts = document.querySelectorAll(".alert");
    alerts.forEach((alert) => {
        window.setTimeout(() => {
            alert.classList.add("show");
        }, 100);
    });
});
