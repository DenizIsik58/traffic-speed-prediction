import React, { Component } from "react";
import { render } from "react-dom";


class Footer extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
    <div className="footer">
      <footer className="py-5 bg-dark fixed-bottom">
        <div className="container">
          <p className="m-0 text-center text-white">
            Copyright &copy; SOLITA - FINMAP 2022
          </p>
        </div>
      </footer>
    </div>
  );
    }
}
export default Footer