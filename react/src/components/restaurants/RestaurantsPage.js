import React, { useState, useEffect, useCallback, Fragment } from "react";
import RestaurantType from "./Restaurant/RestaurantType";
import RestaurantsList from "./Restaurant/RestaurantList";
import { Link } from "react-router-dom";
import { ReactComponent as BACK } from "../../assets/chevron-left.svg";
import classes from "./RestaurantsPage.module.css";

const RestaurantsPage = () => {
  const [restaurants, setRestaurants] = useState([]);
  const [restaurantType, setRestaurantType] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  let content = <p> No restaurant found. </p>;

  const filterType = (filteredType) => {
    setRestaurantType(filteredType);
  };

  const getRestaurantList = useCallback(async () => {
    const response = await fetch("/api/restaurants/");

    if (!response.ok) {
      throw new Error("Somthing went wrong.");
    }

    const data = await response.json();
    setRestaurants(data);
    setIsLoading(false);
  }, []);

  useEffect(() => {
    getRestaurantList().catch((error) => {
      setError(error.message);
      setIsLoading(false);
    });
  }, [getRestaurantList]);

  if (restaurants.length > 0) {
    content = (
      <RestaurantsList
        restaurants={restaurants}
        restaurantType={restaurantType}
      />
    );
  }

  if (error) {
    content = error;
  }

  if (isLoading) {
    content = <p>Loading...</p>;
  }

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
