import React, { useState, useEffect, Fragment } from "react";
import RestaurantType from "./Restaurant/RestaurantType";
import useFetch from "../../hooks/useFetch";
import RestaurantsList from "./Restaurant/RestaurantList";
import { Link } from "react-router-dom";
import BACK from "../../assets/chevron-left.svg";
import classes from "./RestaurantsPage.module.css";

const getProperContent = (restaurants, restaurantType, isLoading, error) => {
  let content = <p> No restaurant found. </p>;

  if (restaurants && restaurants.length > 0) {
    content = (
      <RestaurantsList
        restaurants={restaurants}
        restaurantType={restaurantType}
        url="/restaurant"
      />
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

const RestaurantsPage = () => {
  const { data: restaurants, isLoading, error, sendRequest } = useFetch();
  const [restaurantType, setRestaurantType] = useState("");
  const content = getProperContent(
    restaurants,
    restaurantType,
    isLoading,
    error
  );

  const filterType = (filteredType) => {
    setRestaurantType(filteredType);
  };

  useEffect(() => {
    sendRequest({ url: "/api/v0/restaurants/" });
  }, [sendRequest]);

  return (
    <Fragment>
      <h2> Restaurants List </h2>
      <Link to="/">
        <BACK />
      </Link>
      <div className={classes.filter_type}>
        <RestaurantType onFilterType={filterType} />
      </div>
      {content}
    </Fragment>
  );
};

export default RestaurantsPage;
