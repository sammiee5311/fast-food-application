import React, { useEffect, Fragment } from "react";
import useFetch from "../../hooks/useFetch";
import { ReactComponent as BACK } from "../../assets/chevron-left.svg";
import { useParams, Link } from "react-router-dom";
import Restaurant from "./Restaurant/Restaurant";

const getProperContent = (restaurant, isLoading, error) => {
  let content = <p> No restaurant found. </p>;

  if (restaurant) {
    content = <Restaurant restaurant={restaurant} />;
  }

  if (error) {
    content = <p>{error}</p>;
  }

  if (isLoading) {
    content = <p>Loading...</p>;
  }

  return content;
};

const RestaurantDetailPage = () => {
  const restaurantId = useParams().id;
  const { data: restaurants, isLoading, error, sendRequest } = useFetch();
  const content = getProperContent(restaurants, isLoading, error);

  useEffect(() => {
    sendRequest({
      url: `/api/restaurants/${restaurantId}/`,
    });
  }, [sendRequest, restaurantId]);

  return (
    <Fragment>
      <h2>Restaurant Detail </h2>
      <Link to="/restaurants">
        <BACK />
      </Link>
      {content}
    </Fragment>
  );
};

export default RestaurantDetailPage;
