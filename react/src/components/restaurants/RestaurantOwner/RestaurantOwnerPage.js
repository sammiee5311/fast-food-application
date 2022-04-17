import React from "react";

import { Link } from "react-router-dom";
import BACK from "../../../assets/chevron-left.svg";

const RestaurantOwnerPage = () => {
  return (
    <div>
      <h2> Restaurant Owner </h2>
      <Link to="/">
        <BACK />
      </Link>
      <Link to="/owner/regrestaurant">
        <h2> Register Restaurant </h2>
      </Link>
      <Link to="/owner/addmenu">
        <h2> Add menu </h2>
      </Link>
    </div>
  );
};

export default RestaurantOwnerPage;
