window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(feature, latlng) {
                let color = feature.properties.color || "blue";
                let iconUrl = "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-" + color + ".png";
                let icon = L.icon({
                    iconUrl: iconUrl,
                    shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png",
                    iconSize: [25, 41],
                    iconAnchor: [12, 41],
                    popupAnchor: [1, -34],
                    shadowSize: [41, 41]
                });
                return L.marker(latlng, {
                    icon: icon
                });
            }

            ,
        function1: function(feature, layer) {
            if (feature.properties && feature.properties.popup) {
                layer.bindPopup(feature.properties.popup);
            }
        }

    }
});