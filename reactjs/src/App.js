import React, { Component } from "react";
import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import Navbar from "./layout/header";
import Map from "./pages/map"
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
        return(
                      <Router>
            <div>
                <div>
                    <Navbar />
                </div>
                <div>
                      <Routes>
                        <Route index element={<Map />} />
                          <Route path="/finmap" element={<Map />} />
                        <Route path="/about%20us" element={<About />} />
                       <Route path="/contact%20us" element={<Contact />} />
                       <Route path="/faq" element={<Faq />} />
                      </Routes>
                </div>
                <div>
                    <Footer />
                </div>

                </div>
                    </Router>
  );
    }
}