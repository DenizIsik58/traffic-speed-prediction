import React, {Component, useEffect, useRef, useState} from "react";
import { render } from "react-dom";
import mapboxgl from "mapbox-gl";

mapboxgl.accessToken = "pk.eyJ1IjoidnNvbi1zb2xpdGEiLCJhIjoiY2wxNmlqcG5jMDdyMjNkcGt1N241bTV3eSJ9.R4IzYACNR4PEWDAoBlTkYw";

const Map = () => {
  const mapContainerRef = useRef(null);
    var numberOfRoads = 0;
    var debug = false;
  // initialize map when component mounts
  useEffect(() => {
    const map = new mapboxgl.Map({
      container: mapContainerRef.current,
      // See style options here: https://docs.mapbox.com/api/maps/#styles
      style: 'mapbox://styles/mapbox/light-v10',
      center: [26, 62.3], // starting position
            zoom: 5,
    });

    
    // add navigation control (the +/- zoom buttons)
    map.addControl(new mapboxgl.NavigationControl(), 'bottom-right');

    // clean up on unmount
    return () => map.remove();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

    function onMouseClick (e) {
            const mouseCoords = e.lngLat.wrap()

            const promise = fetch_prediction(mouseCoords)

            document.getElementById('footer').innerHTML = JSON.stringify(e.lngLat.wrap());

            //handle the road object fetched from the coordinates
            promise.then(function(result) {
                const closestRoad = result.roadId;
                const closestRoadSection = result.roadSectionId;
                const predition = result.predictedSpeed;

                //get the geodata of the entire road section
                const geodataPromise = fetch_geodata(closestRoad, closestRoadSection)

                geodataPromise.then(function(geodata) {
                    load_road_from_geojson(predition, numberOfRoads.toString(), numberOfRoads.toString(), geodata)
                    numberOfRoads++;

                    if(debug)
                    {
                        console.log("THE ROAD WE ARE LOOKING FOR HAS ID: " + result.toadId)
                        console.log("Coords at mouse: " + mouseCoords);
                        console.log("closestRoad: " + closestRoad)
                    }
                })
            })
        }

  function lightMode(){
    return new mapboxgl.Map({
            container: 'map',
            style: 'mapbox://styles/mapbox/dark-v10',
            center: [26, 62.3], // starting position
            zoom: 5, // starting zoom
        });
  }

function load_road_from_geojson(prediction, source_name, layer_name, multiLineString)
        {
             this.map.addSource(source_name, {
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

            //add markers (kilometer prediction) source
             this.map.addSource(marker_source, {
                'type': 'geojson',
                'data': {
                    'type': 'FeatureCollection',
                    'features': [
                    {
                        // feature for Mapbox DC
                        'type': 'Feature',
                        'geometry': {
                        'type': 'Point',
                            'coordinates': [multiLineString[0][0][0], multiLineString[0][0][1]]
                        },
                        'properties': {
                            'title': prediction_formatted
                        }
                    },
                    ]
                }
            });


             this.map.addLayer({
                'id': layer_name,
                'type': 'line',
                'source': source_name,
                'layout': {
                    'line-join': 'round',
                    'line-cap': 'round'
                },
                'paint': {
                    'line-color': 'red',
                    'line-width': 4
                }
            });

            //add markers (kilometer prediction) text layer
            this.map.addLayer({
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

            this.map.flyTo({
                zoom: 12,
                center: multiLineString[0][0]
            });
        }

        async function fetch_prediction(coords)
        {
            const lon = JSON.stringify(coords.lng)
            const lat = JSON.stringify(coords.lat)

            if(debug)
            {
                console.log("Recieved coords:")
                console.log(coords)

                console.log("Longitude:")
                console.log(lon)
                console.log("Latitude:")
                console.log(lat)
            }

            //this would be cleaner with string formatting, but I couldnt get it to work
            const apiPath = "http://localhost:8000/api/get-pred&lat=" + lat + "&lon=" + lon

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
            const apiPath = "http://localhost:8000/api/get-geojson&roadNumber=" + roadNumber + "&roadSectionId=" + roadSectionId
            const response = await fetch(apiPath)
            const geodata = await response.json();

            return geodata;
        }

        function switch_language(language)
        {
             this.map.setLayoutProperty('country-label', 'text-field', [
                "get",
                `name_${language}`
            ]);
        }


  return <div style={{cursor: "pointer"} }><div  onClick={() => onMouseClick(this)} className="map-container" ref={mapContainerRef} style={{ width: "100%", height: "85vh" }} /></div>;
};

export default Map;