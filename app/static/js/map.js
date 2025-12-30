// static/js/map.js
document.addEventListener("DOMContentLoaded", () => {
    const map = L.map("map").setView([20, 0], 2); // Default global view

    // Add base tile layer
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 18,
    }).addTo(map);

    // Fetch and add overlays
    async function addDataOverlays() {
        // Example: Fetch weather for a location
        const weatherResponse = await fetch("/weather/London");
        const weatherData = await weatherResponse.json();

        L.marker([weatherData.coord.lat, weatherData.coord.lon])
            .addTo(map)
            .bindPopup(
                `<b>Weather in ${weatherData.name}</b><br>Temperature: ${weatherData.main.temp}°K`
            );

        // Example: Fetch air pollution
        const pollutionResponse = await fetch(
            "/pollution/place?name=New Delhi"
        );
        const pollutionData = await pollutionResponse.json();

        L.circle([pollutionData.coordinates.latitude, pollutionData.coordinates.longitude], {
            color: "red",
            radius: 10000,
        })
            .addTo(map)
            .bindPopup(
                `<b>Pollution Data</b><br>AQI: ${pollutionData.pollution.aqi}`
            );
    }

    addDataOverlays();
});
