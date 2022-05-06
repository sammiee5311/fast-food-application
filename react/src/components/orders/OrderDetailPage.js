import React, { useEffect, Fragment } from "react";
import useFetch from "../../hooks/useFetch";
import BACK from "../../assets/chevron-left.svg";
import { useParams, Link } from "react-router-dom";

import OrderDetailItem from "./Order/OrderDetailItem";

const getProperContent = (order, isLoading, error) => {
  let content = "";

  if (error) {
    content = <p>{error}</p>;
  }

  if (isLoading) {
    content = <p>Loading...</p>;
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
  return content;
};

const OrderDetailPage = () => {
  const orderId = useParams().id;
  const { data: order, isLoading, error, sendRequest } = useFetch();
  const content = getProperContent(order, isLoading, error);

  useEffect(() => {
    sendRequest({ url: `/api/v0/orders/${orderId}/` });
  }, [orderId, sendRequest]);

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
