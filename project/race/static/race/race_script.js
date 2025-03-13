// Simple Timer Function
let startTime;
let isRunActive = false;

let showUserLocationOnMap = false;
let currentPosition = null;
if(navigator.geolocation){       
	// variables to allow older geolocation data if it is more accurate
	navigator.geolocation.watchPosition(updatePosition, showError);
} else {
    alert("Geolocation is not supported by this browser.")
}


function startRace() {
    startTime = Date.now();
    isRunActive = true;
    timerId = setInterval(updateTimer, 1000);
}

function updateTimer() {
    let elapsed = Math.floor((Date.now() - startTime) / 1000);
    document.getElementById("timer").textContent = elapsed + " seconds";

    if (!isRunActive) {
        clearInterval(timerId);
        return;
    }
}

function resetRace() {
    isRunActive = false
    let start_time = new Date(startTime).toISOString();
    let end_time = Date.now()
    end_time = new Date(end_time).toISOString();
    // Send time to the backend before reloading
    fetch('/race/update-race-time/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({ race_id: raceID, start_time: start_time, end_time: end_time})
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

// update the current position if the new position is more accurate
// or if the old position is older than 5 seconds
function updatePosition(position) {
	if(currentPosition==null){
		currentPosition=position;
		return;
	}
	const currentTime = Date.now();
    const acc = position.coords.accuracy;
	if(!currentPosition.coords.accuracy || 
		acc<currentPosition.coords.accuracy ||
		currentTime - currentPosition.timestamp > 50000
	){
		currentPosition = position;
	}
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

function checkStartLocation(position) {
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;
    return fetch('/race/calculate-distance/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(), //Include CSRF token
        },
        body: JSON.stringify({latitude: lat, longitude: lon, targetLatitude: raceData.start.lat, targetLongitude: raceData.start.lng})
    })
    .then(response => response.json())
    .then(data => {
        return data.status === "within range";
    })
    .catch(error => {
        console.error("Error:", error);
        return false;
    });
}

function checkEndLocation(position) {
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;
    return fetch('/race/calculate-distance/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(), //Include CSRF token
        },
        body: JSON.stringify({latitude: lat, longitude: lon, targetLatitude: raceData.end.lat, targetLongitude: raceData.end.lng})
    })
    .then(response => response.json())
    .then(data => {
        return data.status === "within range";
    })
    .catch(error => {
        console.error("Error:", error);
        return false;
    });
}

function toggleShowUserOnMap(){
    if (typeof map !== 'undefined' && map !== null) {
        showUserLocationOnMap = !showUserLocationOnMap;
		if (playerLocationMarker != null){
            map.removeLayer(playerLocationMarker);
        }
		bounds = L.latLngBounds(
			[raceData.start.lat, raceData.start.lng],
            [raceData.end.lat, raceData.end.lng]
		);
		if(showUserLocationOnMap){
			const lat = currentPosition.coords.latitude;
			const long = currentPosition.coords.longitude;
			const acc = currentPosition.coords.accuracy;
			playerLocationMarker = L.circle([lat, long], {
				color: 'red',      
				fillColor: 'red',   
				fillOpacity: 0.5,    
				radius: acc       
			}).addTo(map);
			bounds.extend([lat,long]);
		}
        // fit the user location and race points on the map view
        map.fitBounds(bounds, { padding: [50, 50] });
    } else {
        console.error("Map not initialized yet");
    }
}

async function startTimeTrial() {
    if(!navigator.geolocation){
		alert("Geolocation is not supported by this browser.");
		return;
	}

	isAtStartLocation = await checkStartLocation(currentPosition);
	if (isAtStartLocation) {
		const timeTrialDiv = document.getElementById('activeTimeTrialView');
		timeTrialDiv.classList.add('visible');
		startRace();
	} else {
		alert("You are not at the start point");
	}
}

async function endTimeTrial() {
    if(!navigator.geolocation){
		alert("Geolocation is not supported by this browser.");
		return;
	}

	isAtEndLocation = await checkEndLocation(currentPosition);
	if (isAtEndLocation) {
		resetRace();
		document.getElementById('activeTimeTrialView').classList.remove('visible');
	} else {
		alert("You are not at the end point");
	}
}

async function startExePLORE() {
    if(!navigator.geolocation){
		alert("Geolocation is not supported by this browser.");
		return;
	}

	isAtStartLocation = await checkStartLocation(currentPosition);
	if (isAtStartLocation) {
		const timeTrialDiv = document.getElementById('activeExePLOREView');
		timeTrialDiv.classList.add('visible');
	} else {
		alert("You are not at the start point");
    }
}

async function endExePLORE() {
    if(!navigator.geolocation){
		alert("Geolocation is not supported by this browser.");
		return;
	}

	isAtEndLocation = await checkEndLocation(currentPosition);
	if (isAtEndLocation) {
		addExePlorePoints();
		document.getElementById("pointsNotif").classList.add("visible");
		setTimeout(() => {
			document.getElementById("pointsNotif").classList.remove('visible');
		}, 2000);
		setTimeout(() => {
			document.getElementById('activeExePLOREView').classList.remove('visible');
			document.querySelectorAll("#activeExePLOREView button").forEach(button => {
				button.disabled = false;
			});
		}, 3000);
	} else {
		alert("You are not at the end point");
	}
}

function addExePlorePoints() {
    return fetch('/race/add-exeplore-points/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(), //Include CSRF token
        },
        body: JSON.stringify({start_latitude: raceData.start.lat, start_longitude: raceData.start.lng, end_latitude: raceData.end.lat, end_longitude: raceData.end.lng, user: loggedInUser})
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("pointsNotif").textContent = "You just earned " + data.points + " points!";
        return data.points > 0;
    })
    .catch(error => {
        console.error("Error:", error);
        return false;
    });
}
