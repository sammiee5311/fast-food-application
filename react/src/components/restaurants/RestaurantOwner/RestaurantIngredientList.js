import React from "react";

const RestaurantIngredientList = ({ ingredient, quantity }) => {
  return (
    <div>
      <label htmlFor={ingredient}>{ingredient} : </label>
      <input
        type="number"
        defaultValue={quantity}
        id={ingredient}
        name={ingredient}
        min="0"
        required
      ></input>
    </div>
  );
};

export default RestaurantIngredientList;
