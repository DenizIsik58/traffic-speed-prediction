import React, { Component } from "react";
import {Route, Router} from "react-router-dom";
import Navbar from "./layout/header";
import {Switch} from "@mui/material";
import Map from "./layout/map.js"
import Home from "./pages/home";
import About from "./pages/about";
import Contact from "./pages/contact";
import Faq from "./pages/faq";
import Footer from './layout/footer'

export default class App extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return(<div>
            <div>
         <Navbar />
            </div>
                <div>
                <Map />
                </div>
                <div>
                    <Footer />
                </div>

                </div>
  );
    }
}
