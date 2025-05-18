document.addEventListener('click', function (e) {
    const navCollapse = document.getElementById('navbarSupportedContent');
    const isClickInside = navCollapse.contains(e.target) || e.target.classList.contains('navbar-toggler');
    if (!isClickInside && navCollapse.classList.contains('show')) {
        const bsCollapse = bootstrap.Collapse.getInstance(navCollapse);
        bsCollapse.hide();
    }
});