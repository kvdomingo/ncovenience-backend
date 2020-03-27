document.addEventListener("DOMContentLoaded", () => {
    $("#map").first().css("height", window.innerHeight - $(".navbar").first().innerHeight());
    $("#sideDash").first()
        .css("overflow-y", "scroll")
        .css("height", window.innerHeight - $(".navbar").first().innerHeight());

    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            data = JSON.parse(this.responseText);
        }
    };
    xhttp.open('GET', window.location.href + 'api/geo', true);
    xhttp.send();

    mapboxgl.accessToken = 'pk.eyJ1Ijoia3Zkb21pbmdvIiwiYSI6ImNrODhwbDk4MjBiNTAzbHM0enByZ21pZ3YifQ.xKWVuQAh7SnTyT-IL1rb1g';
    var map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v11',
        center: [122, 13],
        zoom: 4,
    });
    map.addControl(
        new MapboxGeocoder({
            accessToken: mapboxgl.accessToken,
            mapboxgl: mapboxgl,
        })
    );
    map.addControl(new mapboxgl.NavigationControl());

    var marker = new mapboxgl.Marker().setLngLat([122, 14]).addTo(map);

    map.on('load', function() {
        map.addSource('confirmed', {
            type: 'geojson',
            data: data,
            cluster: true,
            clusterMaxZoom: 14,
            clusterRadius: 50,
        });

        map.addLayer({
            id: 'clusters',
            type: 'circle',
            source: 'confirmed',
            filter: ['has', 'point_count'],
            paint: {
                'circle-color': [
                    'step',
                    ['get', 'point_count'],
                    '#51bbd6',
                    100,
                    '#f1f075',
                    750,
                    '#f28cb1',
                ],
                'circle-radius': [
                    'step',
                    ['get', 'point_count'],
                    20,
                    100,
                    30,
                    750,
                    40,
                ],
            },
        });

        map.addLayer({
            id: 'cluster-count',
            type: 'symbol',
            source: 'confirmed',
            filter: [
                'has',
                'point_count'
            ],
            layout: {
                'text-field': '{point_count_abbreviated}',
                'text-font': ['Roboto'],
                'text-size': 12,
            },
        });

        map.addLayer({
            id: 'unclustered-point',
            type: 'circle',
            source: 'confirmed',
            filter: ['!', ['has', 'point_count']],
            paint: {
                'circle-color': '#11b4da',
                'circle-radius': 4,
                'circle-stroke-width': 1,
                'circle-stroke-color': '#fff',
            },
        });
    });
});
