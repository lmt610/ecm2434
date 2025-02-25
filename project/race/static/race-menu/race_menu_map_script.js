document.addEventListener("DOMContentLoaded", function () {
    if (typeof races === "undefined") {
        console.error("Race data is not defined!");
        return;
    }

    // Loop through races and create maps
    races.forEach(race => {
        const mapContainer = document.getElementById(`map-${race.id}`);
        if (!mapContainer) {
            console.error(`Map container not found for race ID: ${race.id}`);
            return;
        }

        // Initialize Leaflet map
        const map = L.map(`map-${race.id}`, {zoomControl: false, dragging: false, touchZoom: false, scrollWheelZoom: false}).setView([50.736577, -3.532512], 14.5);

        // Add OpenStreetMap tiles
        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
            attribution: "&copy; OpenStreetMap contributors",
        }).addTo(map);

        // Create flag icons for start and end
        const startIcon = L.divIcon({
            html: '<i class="fa fa-flag fa-3x flag-border" style="color: #40ff40;"></i>',  // Green flag
            iconSize: [35, 37],
            iconAnchor: [0, 42],
            className: 'start-flag-icon'
        });
        const endIcon = L.divIcon({
            html: '<i class="fa fa-flag-checkered fa-3x" style="color: #4040ff;"></i>',  // Blue checkered flag
            iconSize: [35, 37],
            iconAnchor: [0, 42],
            className: 'end-flag-icon'
        });

        // Add markers with the flag icons
        const startMarker = L.marker([race.start.lat, race.start.lng], {
            icon: startIcon
        })
            .addTo(map)

        const endMarker = L.marker([race.end.lat, race.end.lng], {
            icon: endIcon
        })
            .addTo(map)

        // Fit bounds to show both markers
        const bounds = L.latLngBounds([
            [race.start.lat, race.start.lng],
            [race.end.lat, race.end.lng]
        ]);
        map.fitBounds(bounds, {padding: [50,50]});
        });
});
