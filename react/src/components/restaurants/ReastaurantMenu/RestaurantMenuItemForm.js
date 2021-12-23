import React, { useRef, useState } from "react";
import { useSelector } from "react-redux";

import Input from "../../../UI/Input";

const isQuantityIsValid = (quantity) => {
  return quantity !== 0 || quantity > 0;
};

const hasDifferentRestarauntMenu = (cartRestaurantId, inputRestaurantId) => {
  return cartRestaurantId !== "" && inputRestaurantId !== cartRestaurantId;
};

const RestaurantMenuItemForm = (props) => {
  const [quantityIsValid, setQuantityIsValid] = useState(true);
  const quantityInputRef = useRef();
  const [orderIsValid, setOrderIsValid] = useState(true);
  const restaurantId = useSelector((state) => state.cart.currentRestaurantId);

  const handleSubmit = (event) => {
    event.preventDefault();

    const inputQuantity = +quantityInputRef.current.value;

    if (!isQuantityIsValid(inputQuantity)) {
      setQuantityIsValid(false);
      return;
    }

    setQuantityIsValid(true);

    const inputRestaurantId = event.target.action.split("/")[4];

    if (hasDifferentRestarauntMenu(restaurantId, inputRestaurantId)) {
      setOrderIsValid(false);
      return;
    }

    setOrderIsValid(true);

    props.onAddToCart(inputQuantity, inputRestaurantId);
  };

  return (
    <form onSubmit={handleSubmit}>
      <Input
        ref={quantityInputRef}
        label="Quantity: "
        input={{
          id: "quantity",
          type: "number",
          min: "1",
          step: "1",
          defaultValue: "1",
        }}
      />
      <button type="submit">Add</button>
      {!quantityIsValid && <p>*Invalid quantity*</p>}
      {!orderIsValid && (
        <p>*You cannot add different restuarant's menu in the cart.*</p>
      )}
    </form>
  );
};

export default RestaurantMenuItemForm;
