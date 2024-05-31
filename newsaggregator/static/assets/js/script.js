'use strict';

// navbar variables
const nav = document.querySelector('.mobile-nav');
const navMenuBtn = document.querySelector('.nav-menu-btn');
const navCloseBtn = document.querySelector('.nav-close-btn');


// navToggle function
const navToggleFunc = function () { nav.classList.toggle('active'); }

navMenuBtn.addEventListener('click', navToggleFunc);
navCloseBtn.addEventListener('click', navToggleFunc);


// for star rating
let selectedRating = {};

function setRating(headlineId, rating) {
    selectedRating[headlineId] = rating;
}

function submitRating(headlineId) {

  const rating = selectedRating[headlineId];
  if (typeof rating !== 'undefined') {
    console.log(typeof(rating));
    fetch(`/rate_headline/${headlineId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ rating: rating })
    })
      .then(response => response.json())
      .then(data => {
          if (data.status === 'success') {
              const averageRatingElement = document.querySelector(`#average-rating-${headlineId}`);
              averageRatingElement.innerHTML = `(${data.average_rating}:${data.rating_count} ratings)`;
          } else {
              console.error('Error:', data);
          }
      })
      .catch(error => console.error('Error:', error));
  } else {
      alert('Please select a rating before submitting.');
  }
}