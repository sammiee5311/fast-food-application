import React, { useEffect, Fragment } from "react";
import { Link } from "react-router-dom";

import OrderListItem from "./Order/OrderListItem";
import useFetch from "../../hooks/useFetch";
import BACK from "../../assets/chevron-left.svg";

const getProperContent = (orders, isLoading, error) => {
  let content = <p> No order found. </p>;

  if (orders && orders.length > 0) {
    content = (
      <div className="order-list">
        {orders.map((order, index) => (
          <OrderListItem key={index} order={order} />
        ))}
      </div>
    );
  }

  if (error) {
    content = <p>{error}</p>;
  }

  if (isLoading) {
    content = <p>Loading...</p>;
  }

  return content;
};

const OrderListPage = () => {
  const { data: orders, isLoading, error, sendRequest } = useFetch();
  const content = getProperContent(orders, isLoading, error);

  useEffect(() => {
    sendRequest({
      url: "/api/v0/orders/",
    });
  }, [sendRequest]);

  return (
    <Fragment>
      <h2> Order List </h2>
      <Link to="/">
        <BACK />
      </Link>
      {content}
    </Fragment>
  );
};

export default OrderListPage;
