import React, {Component, useEffect, useRef, useState} from "react";
import { render } from "react-dom";
import mapboxgl from "mapbox-gl";

mapboxgl.accessToken = "pk.eyJ1IjoidnNvbi1zb2xpdGEiLCJhIjoiY2wxNmlqcG5jMDdyMjNkcGt1N241bTV3eSJ9.R4IzYACNR4PEWDAoBlTkYw";

const Map = () => {
  const mapContainerRef = useRef(null);

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

  return <div className="map-container" ref={mapContainerRef} style={{ width: "100%", height: "85vh" }} />;
};

export default Map;