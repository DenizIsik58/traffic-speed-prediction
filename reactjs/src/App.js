import React, { Component } from "react";
import {Route, Router} from "react-router-dom";
import Navbar from "./layout/header";
import {Switch} from "@mui/material";
import Home from "./pages/home";
import About from "./pages/about_us";
import Contact from "./pages/contact_us";
import Faq from "./pages/faq";

export default class App extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return(
      <Navbar />
  );
    }
}
