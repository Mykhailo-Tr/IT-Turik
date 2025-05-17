document.addEventListener('DOMContentLoaded', function () {
    // Show toasts
    document.querySelectorAll('.toast').forEach(el => {
        new bootstrap.Toast(el, { delay: 5000 }).show();
    });

    const toggleBtn = document.getElementById('theme-toggle');
    const iconSpan = document.getElementById('theme-icon');

    function setTheme(theme) {
        document.documentElement.setAttribute('data-bs-theme', theme);
        document.cookie = `theme=${theme};path=/;max-age=31536000`;
        iconSpan.textContent = theme === 'dark' ? '☀️' : '🌙';
    }

    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

    // Init theme from cookie or system preference
    let theme = getCookie('theme');
    if (!theme) {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        theme = prefersDark ? 'dark' : 'light';
        setTheme(theme);
    } else {
        document.documentElement.setAttribute('data-bs-theme', theme);
        iconSpan.textContent = theme === 'dark' ? '☀️' : '🌙';
    }

    toggleBtn.addEventListener('click', () => {
        const newTheme = document.documentElement.getAttribute('data-bs-theme') === 'dark' ? 'light' : 'dark';
        setTheme(newTheme);
    });
});