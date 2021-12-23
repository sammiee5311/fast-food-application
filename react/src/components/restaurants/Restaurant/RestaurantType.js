import React from "react";

const RestaurantType = (props) => {
  const filterType = (event) => {
    props.onFilterType(event.target.value);
  };

  return (
    <div>
      <select name="type" size="3" onChange={filterType}>
        <option value="pizza"> Pizza </option>
        <option value="hamburger"> Hamburger </option>
      </select>
    </div>
  );
};

export default RestaurantType;
