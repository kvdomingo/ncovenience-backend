function parseEscapedJson(s) {
    return s.replace(/\\u[0-9a-fA-F]{4}/gi, match => {
        return String.fromCharCode(parseInt(match.replace(/\\u/g, ""), 16));
    });
}

document.addEventListener("DOMContentLoaded", () => {
    $('.count').each(function() {
        $(this).prop('Counter', 0).animate({
            Counter: $(this).text()
        }, {
            duration: 3000,
            easing: 'swing',
            step: function(now) {
                $(this).text(Math.ceil(now));
            }
        });
    });

    requestProvinces = axios.get('https://raw.githubusercontent.com/macoymejia/geojsonph/master/Province/Provinces.json')
        .then((response) => {
            provinces = response.data;
            console.log('Provinces loaded');
        })
        .catch((err) => {
            console.log('Provinces failed to load');
            console.log(err);
        });

    requestMetro = axios.get('https://raw.githubusercontent.com/macoymejia/geojsonph/master/Philippines/Luzon/Metropolitant%20Manila/MetropolitantManila.json')
        .then((response) => {
            metro = response.data;
            console.log('Metro loaded');
        })
        .catch((err) => {
            console.log('Metro failed to load');
            console.log(err);
        });

    requestCases = axios.get('/api/cases')
        .then((response) => {
            cases = response.data;
            console.log('Cases loaded');

            mapboxgl.accessToken = 'pk.eyJ1Ijoia3Zkb21pbmdvIiwiYSI6ImNrOGtiYnZ4aTAwM2EzZm8xOTdmMjU2bXQifQ.zXF6zxjKqz660if2tOcdDw';

            const map = new mapboxgl.Map({
                container: 'map',
                style: 'mapbox://styles/mapbox/streets-v11',
                center: [121, 12.5],
                zoom: 4.5,
            });

            map.addControl(
                new MapboxGeocoder({
                    accessToken: mapboxgl.accessToken,
                    mapboxgl: mapboxgl,
                })
            );

            map.addControl(new mapboxgl.NavigationControl());

            map.addControl(
                new mapboxgl.GeolocateControl({
                    positionOptions: {
                        enableHighAccuracy: true,
                    },
                    trackUserLocation: true,
                })
            );

            map.on('load', function() {
                map.addSource('cases', {
                    type: 'geojson',
                    data: cases,
                    cluster: true,
                    clusterMaxZoom: 14,
                    clusterRadius: 50,
                });

                map.addSource('provinces', {
                    type: 'geojson',
                    data: provinces,
                });

                map.addSource('metro', {
                    type: 'geojson',
                    data: metro,
                });

                map.addLayer({
                    id: 'province-fills',
                    type: 'fill',
                    source: 'provinces',
                    layout: {},
                    paint: {
                        'fill-color': '#cccccc',
                        'fill-opacity': [
                            'case',
                            ['boolean', ['feature-state', 'hover'], false],
                            1,
                            0.5
                        ],
                    },
                });

                map.addLayer({
                    id: 'province-borders',
                    type: 'line',
                    source: 'provinces',
                    layout: {},
                    paint: {
                        'line-color': '#fcfcfc',
                        'line-width': 2,
                    },
                });

                map.addLayer({
                    id: 'metro-fills',
                    type: 'fill',
                    source: 'metro',
                    layout: {},
                    paint: {
                        'fill-color': 'rgba(204, 204, 204, 0.5)',
                        'fill-opacity': [
                            'case',
                            ['boolean', ['feature-state', 'hover'], false],
                            1,
                            0.5
                        ],
                    },
                });

                map.addLayer({
                    id: 'metro-borders',
                    type: 'line',
                    source: 'metro',
                    layout: {},
                    paint: {
                        'line-color': 'rgba(252, 252, 252, 0.5)',
                        'line-width': 2,
                    },
                });

                var hoveredStateId = null;

                map.on('mousemove', 'province-fills', function(e) {
                    if (e.features.length > 0) {
                        if (hoveredStateId) {
                            map.setFeatureState(
                                { source: 'provinces', id: hoveredStateId },
                                { hover: false },
                            );
                        }
                        hoveredStateId = e.features[0].properties.ID_1;
                        map.setFeatureState(
                            { source: 'provinces', id: hoveredStateId },
                            { hover: true },
                        );
                    }
                });

                map.on('mouseleave', 'province-fills', function() {
                    if (hoveredStateId) {
                        map.setFeatureState(
                            { source: 'provinces', id: hoveredStateId },
                            { hover: false }
                        );
                    }
                    hoveredStateId = null;
                });

                map.addLayer({
                    id: 'unclustered-point',
                    type: 'circle',
                    source: 'cases',
                    filter: ['!', ['has', 'point_count']],
                    paint: {
                        'circle-color': '#11b4da',
                        'circle-radius': 5,
                        'circle-stroke-width': 1,
                        'circle-stroke-color': '#fff'
                    },
                });

                map.addLayer({
                    id: 'clusters',
                    type: 'circle',
                    source: 'cases',
                    filter: ['has', 'point_count'],
                    paint: {
                        'circle-color': [
                            'step',
                            ['get', 'point_count'],
                            '#f1f075',
                            100,
                            '#f19a75',
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
                    source: 'cases',
                    filter: ['has', 'point_count'],
                    layout: {
                        'text-field': '{point_count_abbreviated}',
                        'text-font': ['DIN Offc Pro Medium', 'Arial Unicode MS Bold'],
                        'text-size': 12,
                    },
                });

                map.on('click', 'clusters', function(e) {
                    var features = map.queryRenderedFeatures(e.point, {
                        layers: ['clusters'],
                    });
                    var clusterId = features[0].properties.cluster_id;
                    map.getSource('cases').getClusterExpansionZoom(
                        clusterId,
                        function(err, zoom) {
                            if (err) return;
                            map.easeTo({
                                center: features[0].geometry.coordinates,
                                zoom: zoom,
                            });
                        },
                    );
                });

                map.on('click', 'unclustered-point', function(e) {
                    var coordinates = e.features[0].geometry.coordinates.slice();
                    var props = e.features[0].properties;
                    new mapboxgl.Popup()
                        .setLngLat(coordinates)
                        .setHTML(`
                            Location: ${props.residence}
                        `)
                        .addTo(map);
                });

                map.on('mouseenter', 'clusters', function() {
                    map.getCanvas().style.cursor = 'pointer';
                });

                map.on('mouseleave', 'clusters', function() {
                    map.getCanvas().style.cursor = '';
                });
            });
        })
        .catch((err) => {
            console.log('Cases failed to load');
            console.log(err);
        });
});
