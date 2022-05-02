import React, {useEffect, useRef, useState} from "react";
import mapboxgl from "mapbox-gl";
import 'bootstrap/dist/css/bootstrap.min.css';
import {Alert} from "reactstrap";


mapboxgl.accessToken = process.env.REACT_APP_MAPBOX_SECRET_KEY;

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
    const [showSuccess, setShowSuccess] = useState(false);
    const [showWarning, setShowWarning] = useState(false);
    const [showError, setShowError] = useState(false);

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

    map.current.on('click', (e) => {
          const newLng = JSON.stringify(e.lngLat.wrap().lng);
          const newLat = JSON.stringify(e.lngLat.wrap().lat);
          predict(newLng, newLat);
        });

  }, []);
     // eslint-disable-line react-hooks/exhaustive-deps

    function clearTimer() {
        setTimeout(() => {
      // After 3 seconds set the showSuccess value to false
      setShowSuccess(false)
        setShowWarning(false)
        setShowError(false)
    }, 3000)
    }

    function predict(latitude, longitude){

            //handle the road object fetched from the coordinates
            fetch_prediction(latitude, longitude).then(function(result) {

                const closestRoad = result.roadId;
                const closestRoadSection = result.roadSectionId;
                const predition = result.predictedSpeed;
                const roadN = result.roadName
                setRoadName(roadN);

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

            map.current.flyTo({
                zoom: 12,
                center: multiLineString[0][0]
            });
        }

        async function fetch_prediction(givenLon, givenLat)
        {

            if(debug)
            {
                console.log("Recieved coords:")

            }

            //this would be cleaner with string formatting, but I couldnt get it to work
            const apiPath = (process.env.NODE_ENV === "production" ? process.env.REACT_APP_BACKEND_PRODUCTION_URL : process.env.REACT_APP_BACKEND_DEVELOPMENT_URL) + "/api/get-pred&lat=" + givenLat + "&lon=" + givenLon + "&existingRoads=''"
            const response = await fetch(apiPath)
            if (response.status === 400) {
                setShowWarning(true)
                clearTimer()
                return
            }else if (response.status === 226) {
                setShowWarning(true)
                clearTimer()
                return
            }else if (response.status === 500) {
                setShowError(true)
                clearTimer()
                return
            }else if (response.status === 200) {
                setShowSuccess(true)
                clearTimer()
            }

            return await response.json();
        }

        async function fetch_geodata(roadNumber, roadSectionId)
        {
            // API call to the server
            // Get the geodata of the road section
            const apiPath = (process.env.NODE_ENV === "production" ? process.env.REACT_APP_BACKEND_PRODUCTION_URL : process.env.REACT_APP_BACKEND_DEVELOPMENT_URL) + "/api/get-geojson&roadNumber=" + roadNumber + "&roadSectionId=" + roadSectionId
            const response = await fetch(apiPath)
            return await response.json();
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
        {showSuccess ? (<div  className="alerts">
             <Alert show={showSuccess}  color="success">
                Successful road lookup!
            </Alert>
    </div>): showWarning ? (<div  className="alerts">
             <Alert show={showSuccess}  color="warning">
                The model is currently being trained or hasn't been trained yet. Please be patient!
            </Alert>
    </div>) : showError ? (<div  className="alerts">
             <Alert show={showSuccess}  color="danger">
                An exception occurred during lookup. The road might be under maintenance
            </Alert>
    </div>) : <div></div>}

        <div className="roadInfo">
Road Name: { roadName } | Speed: {speed} | Speed Limit: N/A
</div>
    </div></div>;
};

export default Map;
