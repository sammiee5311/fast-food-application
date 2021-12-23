import React, { Fragment } from "react";
import Line from "../../../UI/Line";

const CartItem = (props) => {
  const price = `${props.price.toFixed(2)}`;

  return (
    <Fragment>
      <p> name: {props.name} </p>
      <p> price: {price} </p>
      <p> quantity: {props.quantity} </p>
      <button onClick={props.onRemove}>remove</button>
      <Line />
    </Fragment>
  );
};

export default CartItem;
