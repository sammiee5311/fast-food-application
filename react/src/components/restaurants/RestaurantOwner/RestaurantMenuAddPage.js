import React, { Fragment } from "react";

import { Link } from "react-router-dom";
import BACK from "../../../assets/chevron-left.svg";

const RestaurantMenuAddPage = () => {
  return (
    <Fragment>
      <h2> Add Menu </h2>
      <Link to="/owner">
        <BACK />
      </Link>
    </Fragment>
  );
};

export default RestaurantMenuAddPage;
