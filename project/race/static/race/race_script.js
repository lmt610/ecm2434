// Simple Timer Function
let startTime;
function startRace() {
    startTime = Date.now();
    setInterval(updateTimer, 1000);
}

function updateTimer() {
    let elapsed = Math.floor((Date.now() - startTime) / 1000);
    document.getElementById("timer").textContent = elapsed + " seconds";
}

function resetRace() {
    location.reload();
}

// Placeholder for Dynamic Map
function initMap() {
    console.log("Map Initialized"); // Replace with Google Maps or Leaflet.js
}


//tracking user location
const x = document.getElementById("locationDisplay");
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        x.innerHTML = "Geolocation is not supported by this browser.";
    }
}

function showPosition(position) {
    x.innerHTML = "Latitude: " + position.coords.latitude +
    "<br>Longitude: " + position.coords.longitude;
}

function showError(error) {
    switch(error.code) {
      case error.PERMISSION_DENIED:
        x.innerHTML = "User denied the request for Geolocation."
        break;
      case error.POSITION_UNAVAILABLE:
        x.innerHTML = "Location information is unavailable."
        break;
      case error.TIMEOUT:
        x.innerHTML = "The request to get user location timed out."
        break;
      case error.UNKNOWN_ERROR:
        x.innerHTML = "An unknown error occurred."
        break;
    }
} 