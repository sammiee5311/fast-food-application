import React from "react";
import { useDispatch } from "react-redux";
import { cartActions } from "../../../store/cart";
import RestaurantMenuItemForm from "./RestaurantMenuItemForm";
import Line from "../../../UI/Line";

const RestaurantMenuitem = (props) => {
  const dispatch = useDispatch();

  const price = `${props.price.toFixed(2)}`;

  const addToCartHandler = (quantity, restaurantId) => {
    dispatch(
      cartActions.addItem({
        id: props.id,
        name: props.name,
        quantity: quantity,
        price: props.price,
        restaurantId: restaurantId,
      })
    );
  };

  return (
    <div>
      <p> name: {props.name} </p>
      <p> price: {price} </p>
      <RestaurantMenuItemForm onAddToCart={addToCartHandler} />
      <Line />
    </div>
  );
};

export default RestaurantMenuitem;
