
var OpenStreetMap_Mapnik = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
	maxZoom: 19,
	attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
});
orig = [-15.7801,-47.9292]
var map = new L.Map('map', {
    tap: false, // ref https://github.com/Leaflet/Leaflet/issues/7255
    layers: [OpenStreetMap_Mapnik],
    center: orig,
    zoom: 10,
    zoomControl: true
});

// add location control to global name space for testing only
// on a production site, omit the "lc = "!
lc = L.control.locate({
    strings: {
        title: "Onde me vacinei "
    }
}).addTo(map);

// var marker = L.marker(orig).addTo(map);
// var popup = marker.bindPopup('<b>Me vacinei!</b><br />aqui.');

function onMapClick(e) {
    if (marker !== null) {
        map.removeLayer(marker);
    }
    marker = new L.marker([e.latlng.lat,e.latlng.lng]).addTo(map);
    marker.bindPopup("Me vacinei aqui ");
    $('#latlong').val(e.latlng.lat + "," + e.latlng.lng);
    }

map.on('click', onMapClick);