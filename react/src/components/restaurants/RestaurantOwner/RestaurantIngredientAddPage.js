import React, { useEffect, Fragment, useState } from "react";
import { Link, useParams } from "react-router-dom";

import RestaurantIngredientList from "./RestaurantIngredientList";

import useFetch from "../../../hooks/useFetch";
import BACK from "../../../assets/chevron-left.svg";

const getProperContent = (restaurantData, isLoading, error) => {
  let content = <p> Something weng wrong. </p>;

  if (restaurantData && restaurantData.recipes !== null) {
    content = Object.entries(restaurantData.recipes.ingredients).map(
      ([ingredient, quantity]) => (
        <RestaurantIngredientList
          key={ingredient}
          ingredient={ingredient}
          quantity={quantity}
        />
      )
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

const RestaurantIngredientAddPage = () => {
  const [ingredients, setIngredients] = useState({});
  const { data: restaurantData, isLoading, error, sendRequest } = useFetch();
  const {
    data: ingredientResponse,
    isLoading: isIngredientLoading,
    error: ingredientError,
    sendRequest: sendIngredientRequest,
  } = useFetch();

  const restaurantId = useParams().id;

  const content = getProperContent(restaurantData, isLoading, error);

  const onIngredientSubmit = (event) => {
    event.preventDefault();

    const newIngredients = {};

    for (const [ingredient, quantity] of Object.entries(
      restaurantData.recipes.ingredients
    )) {
      const newIngredientQuantity = event.target[ingredient].value - quantity;

      if (newIngredientQuantity === 0) continue;

      newIngredients[ingredient] = newIngredientQuantity;
    }

    setIngredients(newIngredients);
  };

  useEffect(() => {
    if (isLoading) {
      sendRequest({
        url: "/api/v1/recipes/",
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: { restaurantId: restaurantId },
      });
    }

    if (isIngredientLoading && Object.keys(ingredients).length > 0) {
      sendIngredientRequest({
        url: "/api/v1/ingredients/",
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: {
          restaurantId: restaurantId,
          restaurantIngredients: ingredients,
        },
        navigate: "/owner/",
      });
    }
  }, [
    sendRequest,
    sendIngredientRequest,
    isLoading,
    ingredients,
    restaurantId,
    ingredientError,
    isIngredientLoading,
  ]);

  return (
    <Fragment>
      <h2> Restaurant Ingredients </h2>
      <Link to="/owner">
        <BACK />
      </Link>
      <form onSubmit={onIngredientSubmit}>
        {content}
        {!error && <input type="submit" />}
      </form>
    </Fragment>
  );
};

export default RestaurantIngredientAddPage;
