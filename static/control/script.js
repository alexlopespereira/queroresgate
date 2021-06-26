first_location = true
var OpenStreetMap_Mapnik = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
	maxZoom: 19,
	attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
});
orig = [-16.7801,-47.9292]
var map = new L.Map('map', {
    tap: false, // ref https://github.com/Leaflet/Leaflet/issues/7255
    layers: [OpenStreetMap_Mapnik],
    zoom: 10,
    zoomControl: true
})

function onLocationFound(e) {
    if (first_location) {
        marker = new L.marker(e.latlng).addTo(map);
        marker.bindPopup("Informar aqui ").openPopup();
        $('#latlong').val(e.latlng.lat + "," + e.latlng.lng);
        first_location = false
    }
}

map.on('locationfound', onLocationFound);

function onMapClick(e) {
    if (marker !== null) {
        map.removeLayer(marker);
    }
    marker = new L.marker([e.latlng.lat,e.latlng.lng]).addTo(map);
    marker.bindPopup("Informar aqui ").openPopup();
    $('#latlong').val(e.latlng.lat + "," + e.latlng.lng);
    }

map.on('click', onMapClick);