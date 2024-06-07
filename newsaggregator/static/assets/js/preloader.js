window.addEventListener('load', function() {
    const preloader = document.getElementById('preloader');
    const mainContent = document.querySelector('.outer-align');

    // Add a delay before hiding the preloader
    setTimeout(() => {
        preloader.style.display = 'none';
        mainContent.style.display = 'flex';
    }, 100); // Adjust the delay time (in milliseconds) as needed
});
