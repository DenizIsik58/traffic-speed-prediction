import React, {Component, useEffect, useRef, useState} from "react";
import { render } from "react-dom";
import mapboxgl from "mapbox-gl";
import { Alert } from '@mui/material';
import CircularProgress from '@mui/material/CircularProgress';

mapboxgl.accessToken = "pk.eyJ1IjoidnNvbi1zb2xpdGEiLCJhIjoiY2wxNmlqcG5jMDdyMjNkcGt1N241bTV3eSJ9.R4IzYACNR4PEWDAoBlTkYw";

export function darkMode(){
    return new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/navigation-night-v1',
        center: [26, 62.3], // starting position
        zoom: 5, // starting zoom
    });
}

const Map = () => {
  const mapContainerRef = useRef(null);
    var numberOfRoads = 0;
    var debug = false;


    const map = useRef(null);
    const [lng, setLng] = useState(26);
    const [lat, setLat] = useState(62.3);
    const [zoom, setZoom] = useState(5);
    const [roadName, setRoadName] = useState(null);
    const [speed, setSpeed] = useState(null);
    const [speedLimit, setSpeedLimit] = useState(null);
    const [isDarkMode, setDarkMode] = useState(false);


  // initialize map when component mounts
  useEffect(() => {

    if (map.current) return; // initialize map only once
    map.current = new mapboxgl.Map({
    container: mapContainerRef.current,
    style: 'mapbox://styles/mapbox/navigation-day-v1',
      center: [lng, lat], // starting position
            zoom: zoom,
    });

    map.current.on('move', () => {
    setLng(map.current.getCenter().lng.toFixed(2));
    setLat(map.current.getCenter().lat.toFixed(2));
    setZoom(map.current.getZoom().toFixed(2));
    });

    map.current.on('click', () => {
          const newLng = map.current.getCenter().lng;
          const newLat = map.current.getCenter().lat;
          predict(newLng, newLat);

        });

  }, []);
     // eslint-disable-line react-hooks/exhaustive-deps


    function predict(latitude, longitude){

            console.log(latitude + " " + longitude)

            //handle the road object fetched from the coordinates
            fetch_prediction(latitude, longitude).then(function(result) {

                const closestRoad = result.roadId;
                const closestRoadSection = result.roadSectionId;
                const predition = result.predictedSpeed;
                const roadN = result.roadName
                setRoadName(roadN);

                console.log(roadName);
                console.log(result);
                console.log(result.roadName);

                //get the geodata of the entire road section
                const geodataPromise = fetch_geodata(closestRoad, closestRoadSection)

                geodataPromise.then(function(geodata) {
                    load_road_from_geojson(predition, numberOfRoads.toString(), numberOfRoads.toString(), geodata)
                    numberOfRoads++;

                })
            })
        }

function load_road_from_geojson(prediction, source_name, layer_name, multiLineString)
        {

             map.current.addSource(source_name, {
                'type': 'geojson',
                'data': {
                    'type': 'Feature',
                    'properties': {},
                    'geometry': {
                        'type': 'MultiLineString',
                        'coordinates': multiLineString
                    }
                },
            });

            const marker_source = source_name + "_marker"
            const marker_name = source_name + "_marker"
            const prediction_formatted = prediction.toFixed(0) + " km/h"
            setSpeed(prediction_formatted)
            //add markers (kilometer prediction) source



             map.current.addLayer({
                'id': layer_name,
                'type': 'line',
                'source': source_name,
                'layout': {
                    'line-join': 'round',
                    'line-cap': 'round'
                },
                'paint': {
                    'line-color': isDarkMode ? 'white' : "black",
                    'line-width': 4
                }
            });

            //add markers (kilometer prediction) text layer
            map.current.addLayer({
                'id': marker_name,
                'type': 'symbol',
                'source': marker_source,
                'layout': {
                    'icon-image': 'custom-marker',
                    // get the title name from the source's "title" property
                    'text-field': ['get', 'title'],
                    'text-font': [
                        'Open Sans Semibold',
                        'Arial Unicode MS Bold'
                    ],
                    'text-offset': [0, 1.25],
                    'text-anchor': 'top'
                },
                paint: {
                    "text-color": "black"
                }
            });

            //console.log("added road")
            //console.log(multiLineString[0][0])

            map.current.flyTo({
                zoom: 12,
                center: multiLineString[0][0]
            });
        }

        async function fetch_prediction(givenLon, givenLat)
        {
            const lon = JSON.stringify(givenLon)
            const lat = JSON.stringify(givenLat)

            if(debug)
            {
                console.log("Recieved coords:")


                console.log("Longitude:")
                console.log(lon)
                console.log("Latitude:")
                console.log(lat)
            }

            //this would be cleaner with string formatting, but I couldnt get it to work
            const apiPath = "http://localhost:8000/api/get-pred&lat=" + lat + "&lon=" + lon + "&existingRoads=''"

            const response = await fetch(apiPath)

            const road = await response.json();
            const road1 = JSON.stringify(road)

            return road;
        }


        async function fetch_coordinates(roadId)
        {
            var apiPath = "https://tie.digitraffic.fi/api/v2/metadata/forecast-sections/" + roadId;
            const response = await fetch(apiPath)
            const coords = await response.json();

            return coords;
        }

        async function fetch_geodata(roadNumber, roadSectionId)
        {
            // API call to the server
            // Get the geodata of the road section
            const currentLoc = window.location.href.replace("3000", "8000").replace("/FinMap", "")
            const apiPath = currentLoc + "api/get-geojson&roadNumber=" + roadNumber + "&roadSectionId=" + roadSectionId
            console.log(apiPath)
            const response = await fetch(apiPath)
            const geodata = await response.json();

            return geodata;
        }

        function switch_language(language)
        {
             map.current.setLayoutProperty('country-label', 'text-field', [
                "get",
                `name_${language}`
            ]);
        }

    return <div  style={{cursor: "pointer"} }><div  className="map-container" ref={mapContainerRef} style={{ width: "100%", height: "85vh" }}>
        <div className="sidebar">
Longitude: {lng} | Latitude: {lat} | Zoom: {zoom}
</div>
        <div className="roadInfo">
Road Name: { roadName } | Speed: {speed} | Speed Limit: 80 km/h
</div>
    </div></div>;
};

export default Map;
