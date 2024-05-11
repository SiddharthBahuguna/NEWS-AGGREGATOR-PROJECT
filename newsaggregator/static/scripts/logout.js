function logout() {
    // Perform logout action here
    // For demonstration purposes, let's just hide the logout button and show the login dropdown again
    document.getElementById("logoutButton").style.display = "none";
    document.getElementById("loginDropdown").style.display = "block";
}

document.getElementById("loginForm").addEventListener("submit", function(event) {
    // Prevent the form from submitting and refreshing the page
    event.preventDefault();
    // Perform login action here
    // For demonstration purposes, let's just hide the login dropdown and show the logout button
    document.getElementById("loginDropdown").style.display = "none";
    document.getElementById("logoutButton").style.display = "block";
});