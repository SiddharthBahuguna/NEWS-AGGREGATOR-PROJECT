window.addEventListener('load', function() {
    const preloader = document.querySelector('.loader');
    const mainContentlight = document.querySelector('.light-theme');
    const mainContentdark = document.querySelector('.dark-theme');

    setTimeout(() => {
        preloader.style.display = 'none';
        mainContentlight.style.pointerEvents = 'all';
        mainContentlight.style.overflow = 'auto';
        mainContentdark.style.pointerEvents = 'all';
        mainContentdark.style.overflow = 'auto';
    }, 100);
});
