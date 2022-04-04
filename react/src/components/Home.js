import React from "react";
import { Link } from "react-router-dom";

import SEARCH from "../assets/search.svg";

const Home = () => {
  return (
    <div>
      <h2> Home </h2>
      <SEARCH />
      <Link to="/restaurants">
        <h2> Order Food </h2>
      </Link>
      <Link to="/orders">
        <h2> Order List </h2>
      </Link>
      <Link to="/cart">
        <h2> Cart </h2>
      </Link>
    </div>
  );
};

export default Home;
