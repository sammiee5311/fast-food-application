import React, { useState, useEffect, Fragment } from "react";
import useFetch from "../../../hooks/useFetch";

import { useParams, Link } from "react-router-dom";
import BACK from "../../../assets/chevron-left.svg";

const FOOD_TYPES = [
  { id: 0, name: "main" },
  { id: 1, name: "side" },
  { id: 2, name: "drinks" },
];

const RestaurantMenuAddPage = (props) => {
  const restaurantId = useParams().id;
  const [menuName, setMenuName] = useState("");
  const [foodName, setFoodName] = useState("");
  const [foodType, setFoodType] = useState("");
  const [description, setDescription] = useState("");
  const [price, setPrice] = useState("");

  const { isLoading: isAddMenuLoading, sendRequest: sendAddMenuRequest } =
    useFetch();

  useEffect(() => {
    if (menuName && foodName && description && price && isAddMenuLoading) {
      sendAddMenuRequest({
        url: "/api/menus/",
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: {
          restaurant_id: restaurantId,
          menus: [
            {
              name: menuName,
              food_items: [
                {
                  name: foodName,
                  type: foodType,
                  description: description,
                },
              ],
              price: price,
            },
          ],
        },
      });
    }
  }, [
    sendAddMenuRequest,
    restaurantId,
    menuName,
    foodName,
    foodType,
    description,
    price,
    isAddMenuLoading,
  ]);

  const addMenusHandler = async (event) => {
    event.preventDefault();

    setMenuName(event.target.menuName.value);
    setFoodName(event.target.foodName.value);
    setFoodType(event.target.foodType.value);
    setDescription(event.target.description.value);
    setPrice(event.target.price.value);
  };
  return (
    <Fragment>
      <h2> Add Menu </h2>
      <Link to="/owner">
        <BACK />
      </Link>
      <form onSubmit={addMenusHandler}>
        <div>
          <label htmlFor="menuName">Menu Name : </label>
          <input
            type="text"
            id="menuName"
            name="menuName"
            placeholder="Enter Menu Name"
            required
          />
        </div>
        <div>
          <label htmlFor="foodName">Food Name : </label>
          <input
            type="text"
            id="foodName"
            name="foodName"
            placeholder="Enter Food Name"
            required
          />
        </div>
        <div>
          <label htmlFor="foodType">Food Type : </label>
          <select type="text" id="foodType" name="foodType" size="2" required>
            {FOOD_TYPES.map((type) => (
              <option key={type.id} value={type.name}>
                {type.name}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label htmlFor="description">Description : </label>
          <input
            type="text"
            id="description"
            name="description"
            placeholder="Enter Description"
            required
          />
        </div>
        <div>
          <label htmlFor="price">Price : </label>
          <input
            type="number"
            id="price"
            name="price"
            placeholder="Enter Price"
            step="0.01"
            required
          />
        </div>
        <input type="submit" />
      </form>
    </Fragment>
  );
};

export default RestaurantMenuAddPage;
