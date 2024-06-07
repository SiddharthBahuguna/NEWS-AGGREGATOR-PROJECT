window.addEventListener('load', function() {
    const preloader = document.getElementById('preloader');
    const mainContent = document.querySelector('.outer-align');

    setTimeout(() => {
        preloader.style.display = 'none';
        mainContent.style.display = 'flex';
    }, 100);
});
