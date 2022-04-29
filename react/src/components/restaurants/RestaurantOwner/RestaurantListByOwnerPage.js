import React, { useEffect, Fragment } from "react";
import { Link } from "react-router-dom";

import RestaurantsList from "../Restaurant/RestaurantList";
import useFetch from "../../../hooks/useFetch";
import BACK from "../../../assets/chevron-left.svg";

const getProperContent = (restaurants, isLoading, error) => {
  let content = <p> No restaurant found. </p>;

  if (restaurants && restaurants.length > 0) {
    content = (
      <RestaurantsList restaurants={restaurants} url={"/owner/addmenu"} />
    );
  }

  if (error) {
    content = error;
  }

  if (isLoading) {
    content = <p>Loading...</p>;
  }

  return content;
};

const RestaurantListByOwner = () => {
  const { data: restaurants, sendRequest } = useFetch();
  const content = getProperContent(restaurants);

  useEffect(() => {
    sendRequest({ url: "/api/restaurantsbyowner/" });
  }, [sendRequest]);

  return (
    <Fragment>
      <h2> Restaurant List </h2>
      <Link to="/owner">
        <BACK />
      </Link>
      {content}
    </Fragment>
  );
};

export default RestaurantListByOwner;
