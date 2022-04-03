import React from "react";
import ReactDOM from "react-dom";
import { Provider } from "react-redux";

import Footer from "./components/Footer";
import App from "./App";

import store from "./store";

import "./App.css";

const routing = (
  <Provider store={store}>
    <React.StrictMode>
      <div className="App">
        <App />
        <Footer />
      </div>
    </React.StrictMode>
  </Provider>
);

ReactDOM.render(routing, document.getElementById("root"));
