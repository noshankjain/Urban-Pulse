// Initialize Map (Centered on London)
const map = L.map('map').setView([51.505, -0.09], 13);

// Add Dark Mode Map Tiles
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; OpenStreetMap contributors &copy; CARTO'
}).addTo(map);

// Function to get color based on AQI
function getAqiColor(aqi) {
    if (aqi > 150) return '#ff0000'; // Red (Hazardous)
    if (aqi > 100) return '#ff9900'; // Orange (Unhealthy)
    return '#00cc00';                // Green (Good)
}

// Fetch data from our FastAPI backend
async function fetchData() {
    try {
        const response = await fetch('http://127.0.0.1:8000/api/v1/latest');
        const data = await response.json();

        // Clear existing markers (optional optimization omitted for simplicity)
        
        data.forEach(point => {
            L.circleMarker([point.latitude, point.longitude], {
                radius: 10,
                fillColor: getAqiColor(point.aqi),
                color: "#000",
                weight: 1,
                opacity: 1,
                fillOpacity: 0.8
            })
            .bindPopup(`
                <b>Sensor:</b> ${point.sensor_id}<br>
                <b>AQI:</b> ${point.aqi}<br>
                <b>Temp:</b> ${point.temperature}°C
            `)
            .addTo(map);
        });
        console.log("Updated map with " + data.length + " points");
    } catch (error) {
        console.error("Error fetching data:", error);
    }
}

// Auto-refresh every 5 seconds
setInterval(fetchData, 5000);
fetchData(); // Initial load