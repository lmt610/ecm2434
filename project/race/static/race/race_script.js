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
