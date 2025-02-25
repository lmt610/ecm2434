
let map;
let playerLocationMarker = null;

// Function to initialize the map
function initializeMap(raceData) {
    // Initialize the map with the start location
    map = L.map('map').setView([50.736577, -3.532512], 14.5);  

    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Create flag icons for start and end
    const startIcon = L.divIcon({
        html: '<i class="fa fa-flag fa-3x flag-border" style="color: #40ff40;"></i>',  // Green flag
        iconSize: [25, 37],
        iconAnchor: [0, 42],
        popupAnchor: [0, -42],  // Popup will appear above the flag
        className: 'start-flag-icon'
    });

    const endIcon = L.divIcon({
        html: '<i class="fa fa-flag-checkered fa-3x" style="color: #4040ff;"></i>',  // Blue checkered flag
        iconSize: [35, 37],
        iconAnchor: [0, 42],
        popupAnchor: [0, -42],
        className: 'end-flag-icon'
    });

    // Add markers with the flag icons
    const startMarker = L.marker([raceData.start.lat, raceData.start.lng], {
        icon: startIcon
    })
        .addTo(map)
        .bindPopup(`Start: ${raceData.start.name}`);

    const endMarker = L.marker([raceData.end.lat, raceData.end.lng], {
        icon: endIcon
    })
        .addTo(map)
        .bindPopup(`End: ${raceData.end.name}`);

    // Fit bounds to show both markers
    const bounds = L.latLngBounds([
        [raceData.start.lat, raceData.start.lng],
        [raceData.end.lat, raceData.end.lng]
    ]);
    map.fitBounds(bounds, { padding: [50, 50] });
}

// Check if raceData exists and initialize the map
if (typeof raceData !== 'undefined') {
    initializeMap(raceData);
} else {
    console.error('Race data not found');
}
