window.addEventListener('load', function() {
    const preloader = document.querySelector('.loader');
    const mainContentlight = document.querySelector('.main-body');

    setTimeout(() => {
        preloader.style.display = 'none';
        mainContentlight.style.pointerEvents = 'all';
        mainContentlight.style.overflow = 'auto';
    }, 100);
});
