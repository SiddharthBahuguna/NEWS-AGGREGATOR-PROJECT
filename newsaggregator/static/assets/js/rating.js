function setRating(recordId, rating) {
    document.querySelectorAll(`input[name="rate-${recordId}"]`).forEach(input => {
        input.checked = input.value == rating;
    });
}

function submitRating(recordId) {
    const rating = document.querySelector(`input[name="rate-${recordId}"]:checked`).value;

    fetch(`/rate_headline/${recordId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ rating: rating })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            document.getElementById(`average-rating-${recordId}`).innerHTML = `(${data.average_rating})`;
            const submitBtn = document.getElementById(`submit-btn-${recordId}`);
            submitBtn.innerHTML = 'Rated';
            submitBtn.style.backgroundColor = 'green';
            submitBtn.style.borderColor = 'green';
        } else {
            alert('Failed to submit rating');
        }
    });
}

// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}