document.addEventListener("DOMContentLoaded", () => {
    $("#map").first().css("height", window.innerHeight - $(".navbar").first().innerHeight())

    mapboxgl.accessToken = 'pk.eyJ1Ijoia3Zkb21pbmdvIiwiYSI6ImNrODhwbDk4MjBiNTAzbHM0enByZ21pZ3YifQ.xKWVuQAh7SnTyT-IL1rb1g';
    var map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v11',
        center: [122, 13],
        zoom: 4,
    });
    map.addControl(new mapboxgl.NavigationControl());

    // var map = new ol.Map({
    //     target: 'map',
    //     layers: [
    //         new ol.layer.Tile({
    //             source: new ol.source.OSM(),
    //         }),
    //     ],
    //     view: new ol.View({
    //         center: ol.proj.fromLonLat([122, 14]),
    //         zoom: 5,
    //     }),
    // });
    //
    // var marker = new ol.layer.Vector({
    //     source: new ol.source.Vector({
    //         features: [
    //             new ol.Feature({
    //                 geometry: new ol.geom.Point(ol.proj.fromLonLat([122, 14])),
    //             }),
    //         ],
    //     }),
    // });
    // map.addLayer(marker);

});
