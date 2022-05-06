import React, { Fragment, useState } from "react";
import Cookies from "js-cookie";
import { Link } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
// import {v4 as uuidv4} from 'uuid'
import { useNavigate } from "react-router-dom";

import CartItem from "./Cart/CartItem";
import CartPayment from "./CartPayment";
import { cartActions } from "../../store/cart";
import BACK from "../../assets/chevron-left.svg";
import Line from "../../UI/Line";

import classes from "./CartPage.module.css";

const Cart = () => {
  const [error, setError] = useState(null);
  const [isOrderButtonClicked, setIsOrderButtonClicked] = useState(false);

  const dispatch = useDispatch();
  const cartItemsSelector = useSelector((state) => state.cart.items);
  const restaurantId = useSelector((state) => state.cart.currentRestaurantId);
  const totalPriceSelector = useSelector((state) => state.cart.totalPrice);
  const authTokensSelector = useSelector((state) => state.auth.authTokens);

  let navigate = useNavigate();

  const totalPrice = `${totalPriceSelector.toFixed(2)} $`;

  const cartItemRemoveHandler = (id) => {
    dispatch(cartActions.removeItem(id));
  };

  const cartItems = cartItemsSelector.map((item, index) => (
    <CartItem
      key={index}
      name={item.name}
      quantity={item.quantity}
      price={item.price}
      onRemove={cartItemRemoveHandler.bind(null, item.id)}
    />
  ));

  const orderConfirmHandler = async () => {
    setError(null);
    try {
      const menus = cartItemsSelector.map((item) => {
        return {
          menu: item.id,
          quantity: item.quantity,
        };
      });

      const payload = {
        restaurant: restaurantId,
        menus: menus,
      };

      const response = await fetch("/api/v0/orders/", {
        method: "POST",
        body: JSON.stringify(payload),
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": Cookies.get("csrftoken"),
          Authorization: `Bearer ${String(authTokensSelector.access)}`,
        },
      });

      response
        .json()
        .then((result) => result)
        .then((data) => {
          const result_data = JSON.stringify(data);
          if (response.status !== 201) {
            throw new Error(result_data);
          }
          dispatch(cartActions.clearCart());
          navigate(`/order/${data.id}`);
        })
        .catch((error) => {
          setError(error.message);
        });
    } catch (error) {
      setError(error.message);
    }
    setIsOrderButtonClicked(false);
  };

  const orderClickedHandler = () => {
    setError(null);
    try {
      if (cartItemsSelector.length === 0) {
        throw new Error("Order cannot be processed without items in cart.");
      }
      setIsOrderButtonClicked(true);
    } catch (error) {
      setError(error.message);
    }
  };

  const cancelOrderHandler = () => {
    setIsOrderButtonClicked(false);
  };

  const isCartEmpty = cartItems.length === 0;

  let items = <p> Cart is Empty </p>;

  if (!isCartEmpty) {
    items = (
      <Fragment>
        <Line /> {cartItems}
      </Fragment>
    );
  }

  const cartOrder = (
    <Fragment>
      <p> - Menu - </p>
      {items}
      <div className={classes.padding}>Total Price: {totalPrice}</div>
      <div className={classes.padding}>
        <button onClick={orderClickedHandler}>Order</button>
      </div>
    </Fragment>
  );

  return (
    <Fragment>
      <h2> Cart </h2>
      <Link to="/">
        <BACK />
      </Link>
      {!isOrderButtonClicked && cartOrder}
      {!error && isOrderButtonClicked && (
        <CartPayment
          onCancel={cancelOrderHandler}
          onConfrim={orderConfirmHandler}
          totalPrice={totalPrice}
        />
      )}
      <p>{error}</p>
    </Fragment>
  );
};

export default Cart;
