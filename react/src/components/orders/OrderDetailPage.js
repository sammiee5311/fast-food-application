import React, { useEffect, useState, useCallback, Fragment } from "react";
import { ReactComponent as BACK } from "../../assets/chevron-left.svg";
import { useParams, Link } from "react-router-dom";

import OrderDetailItem from "./Order/OrderDetailItem";

const OrderDetailPage = () => {
  const orderId = useParams().id;
  const [order, setOrder] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  let content = "";

  const getOrder = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    const response = await fetch(`/api/orders/${orderId}/`);
    const data = await response.json();

    if (!response.ok) {
      throw new Error("Something went wrong.");
    }

    setOrder(data);
    setIsLoading(false);
  }, [orderId]);

  useEffect(() => {
    getOrder().catch((error) => {
      setError(error.message);
      setIsLoading(false);
    });
  }, [getOrder]);

  if (error) {
    content = error;
  }

  if (isLoading) {
    content = "Loading...";
  }

  if (order) {
    content = (
      <OrderDetailItem
        username={order.username}
        time={order.created_on_str}
        menus={order.menus}
        restaurantName={order.restaurant_name}
        totalPrice={order.total_price.toFixed(2)}
        estimatedDeliveryTime={order.estimated_delivery_time}
      />
    );
  }

  return (
    <Fragment>
      <h2> Order Detail </h2>
      <Link to="/orders">
        <BACK />
      </Link>
      {content}
    </Fragment>
  );
};

export default OrderDetailPage;
