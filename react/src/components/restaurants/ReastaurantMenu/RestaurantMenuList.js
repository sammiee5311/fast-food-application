import React, { Fragment } from "react";
import { Link } from "react-router-dom";
import RestaurantMenuitem from "./RestaurantMenuitem";

const RestaurantMenuList = (props) => {
  if (props.menus === undefined) {
    return <h2>No menu found.</h2>;
  }

  const menus = props.menus.map((menu, index) => (
    <RestaurantMenuitem
      key={index}
      id={menu.menu_id}
      name={menu.name}
      price={menu.price}
    />
  ));

  return (
    <Fragment>
      {menus}
      <Link to="/cart/"> Cart </Link>
    </Fragment>
  );
};

export default RestaurantMenuList;
