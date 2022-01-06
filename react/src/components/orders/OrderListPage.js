import React, { useEffect, Fragment } from "react";
import OrderListItem from "./Order/OrderListItem";
import useFetch from "../../hooks/useFetch";
import { Link } from "react-router-dom";
import { ReactComponent as BACK } from "../../assets/chevron-left.svg";

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

  // TODO: Need to refactor (reason: load 4 times)
  useEffect(() => {
    sendRequest({ url: "/api/orders/" });
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
