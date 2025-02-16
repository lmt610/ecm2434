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
    let elapsed = Math.floor((Date.now() - startTime) / 1000);

    // Send time to the backend before reloading
    fetch('/update-race-time/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({ time_taken: elapsed })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Time submitted:", data);
        location.reload(); // Reload page after successful submission
    })
    .catch(error => {
        console.error("Error:", error);
        location.reload(); // Still reload even if an error occurs
    });
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
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;

    //let user see lat and lon
    x.innerHTML = "Latitude: " + lat + "<br> Longitude: " + lon;

    sendLocation(lat, lon);
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

//Send location to Django Backend
function getCSRFToken() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    return csrfToken;
}

function sendLocation(lat, lon) {
    fetch('/calculate-distance/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(), //Include CSRF token
        },
        body: JSON.stringify({latitude: lat, longitude: lon})
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "within range") {
            alert("You are within range!")
        } else {
            alert("You are out of the range.")
        }
    })
    .catch(error => console.error("Error:", error));
}

function createRace(title, startId, endId) {
    fetch('/create-race/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({
            title: title,
            start_id: startId,
            end_id: endId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            console.log("Race created with ID:", data.race_id);
            localStorage.setItem("currentRaceId", data.race_id);
        } else {
            console.error("Error creating race:", data.message);
        }
    })
    .catch(error => console.error("Error:", error));
}

function updateRaceTime(startTime, endTime) {
    const raceId = localStorage.getItem("currentRaceId"); //get stored race ID

    if (!raceId) {
        console.error("No active race found.");
        return;
    }

    fetch('/update-race-time/', {
        method: 'POST',
        headers: {
            'Content-Type': 'applciation/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({
            race_id:raceId,
            start_time: new Date(startTime).toISOString(),
            end_time:new Date(endTime).toISOString()
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
        location.reload(); //reload after updating
    })
    .catch(error => console.error("Error:", error));
}

getLocation();