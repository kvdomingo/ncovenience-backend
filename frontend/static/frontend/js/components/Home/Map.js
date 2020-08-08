import React from "react";
import {
    MDBCard as Card,
    MDBCardHeader as CardHeader,
    MDBCardBody as CardBody,
} from "mdbreact";
import PropTypes from 'prop-types';
import mapboxgl from "mapbox-gl";
import MapboxGeocoder from "@mapbox/mapbox-gl-geocoder";
import "@mapbox/mapbox-gl-geocoder/dist/mapbox-gl-geocoder.css";
import "./Map.css";
import Loading from "../Loading";


export default class Map extends React.Component {
    static propTypes = {
        mapboxApiToken: PropTypes.string.isRequired,
    }

    constructor(props) {
        super(props);
        this.state = {
            lng: 121,
            lat: 12.5,
            zoom: 4.5,
            provinces: [],
            cases: [],
        }
        mapboxgl.accessToken = this.props.mapboxApiToken;
    }

    getProvinces = () => {
        fetch("https://raw.githubusercontent.com/macoymejia/geojsonph/master/Province/Provinces.json")
            .then(res => res.json())
            .then(provinces => this.setState({ provinces }))
            .catch(err => console.log(`Provinces failed to load: ${err}`));
    }

    getCases = () => {
        fetch("/api/cases")
            .then(res => res.json())
            .then(cases => {
                this.setState({ cases });

                this.map = new mapboxgl.Map({
                    container: this.mapContainer,
                    style: "mapbox://styles/mapbox/streets-v11",
                    center: [this.state.lng, this.state.lat],
                    zoom: this.state.zoom,
                });

                this.map.addControl(
                    new MapboxGeocoder({
                        accessToken: mapboxgl.accessToken,
                        mapboxgl: mapboxgl,
                    })
                );

                this.map.addControl(new mapboxgl.NavigationControl());

                this.map.addControl(
                    new mapboxgl.GeolocateControl({
                        positionOptions: { enableHighAccuracy: true },
                        trackUserLocation: true,
                    })
                );

                this.map.on("move", () => {
                    this.setState({
                        lng: this.map.getCenter().lng.toFixed(4),
                        lat: this.map.getCenter().lat.toFixed(4),
                        zoom: this.map.getZoom().toFixed(2),
                    });
                });

                this.map.on("load", () => {
                    this.map.addSource("cases", {
                        type: "geojson",
                        data: this.state.cases,
                        cluster: true,
                        clusterMaxZoom: 14,
                        clusterRadius: 50,
                    });

                    this.map.addSource("provinces", {
                        type: "geojson",
                        data: this.state.provinces,
                    });

                    let hoveredStateId = null;

                    this.map.on('mousemove', 'province-fills', e => {
                        if (e.features.length > 0) {
                            if (hoveredStateId) {
                                this.map.setFeatureState(
                                    { source: 'provinces', id: hoveredStateId },
                                    { hover: false },
                                );
                            }
                            hoveredStateId = e.features[0].properties.ID_1;
                            this.map.setFeatureState(
                                { source: 'provinces', id: hoveredStateId },
                                { hover: true },
                            );
                        }
                    });

                    this.map.on('mouseleave', 'province-fills', () => {
                        if (hoveredStateId) {
                            this.map.setFeatureState(
                                { source: 'provinces', id: hoveredStateId },
                                { hover: false }
                            );
                        }
                        hoveredStateId = null;
                    });

                    this.map.addLayer({
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

                    this.map.addLayer({
                        id: 'province-borders',
                        type: 'line',
                        source: 'provinces',
                        layout: {},
                        paint: {
                            'line-color': '#fcfcfc',
                            'line-width': 2,
                        },
                    });

                    this.map.addLayer({
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

                    this.map.addLayer({
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

                    this.map.addLayer({
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

                    this.map.on('click', 'clusters', e => {
                        let features = this.map.queryRenderedFeatures(e.point, {
                            layers: ['clusters'],
                        });
                        let clusterId = features[0].properties.cluster_id;
                        this.map.getSource('cases').getClusterExpansionZoom(
                            clusterId,
                            (err, zoom) => {
                                if (err) return;
                                this.map.easeTo({
                                    center: features[0].geometry.coordinates,
                                    zoom: zoom,
                                });
                            },
                        );
                    });

                    this.map.on('click', 'unclustered-point', e => {
                        let coordinates = e.features[0].geometry.coordinates.slice();
                        let props = e.features[0].properties;
                        new mapboxgl.Popup()
                            .setLngLat(coordinates)
                            .setHTML(`
                            Location: ${props.residence}
                        `)
                            .addTo(this.map);
                    });

                    this.map.on('mouseenter', 'clusters', () => {
                        this.map.getCanvas().style.cursor = 'pointer';
                    });

                    this.map.on('mouseleave', 'clusters', () => {
                        this.map.getCanvas().style.cursor = '';
                    });
                });
            })
            .catch(err => console.log(`Cases failed to load: ${err}`));
    }

    componentDidMount() {
        this.getProvinces();
        this.getCases();
    }

    render() {
        return (
            <div className='map-container mb-5'>
                <Card className='mb-3 m-5'>
                    <CardHeader className='text-muted text-left text-uppercase'>Cases Map</CardHeader>
                    <CardBody className='p-0'>
                        <div className='map' ref={el => this.mapContainer = el} />
                    </CardBody>
                </Card>
            </div>
        );
    }
}