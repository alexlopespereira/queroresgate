var OpenStreetMap_Mapnik = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    });
orig = [-15.7801,-47.9292]
var alertmap = new L.Map('alertmap', {
    tap: false, // ref https://github.com/Leaflet/Leaflet/issues/7255
    layers: [OpenStreetMap_Mapnik],
    zoom: 10,
    zoomControl: true
})

var rectangle = L.rectangle([  [-15.6801,-47.9292], [-15.8801,-47.7292]]);
alertmap.addLayer(rectangle);
