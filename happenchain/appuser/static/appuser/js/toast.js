document.addEventListener("DOMContentLoaded", () => {
    const toasts = document.querySelectorAll(".toast");

    toasts.forEach((toast, index) => {
        setTimeout(() => {
            toast.style.animation = "fadeOut 0.4s ease forwards";
            setTimeout(() => toast.remove(), 400);
        }, 3500 + index * 300);
    });
});
