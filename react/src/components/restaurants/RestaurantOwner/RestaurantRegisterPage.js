import React, { Fragment, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { Link } from "react-router-dom";
import BACK from "../../../assets/chevron-left.svg";

import useFetch from "../../../hooks/useFetch";

const phoneNumberValidation = new RegExp("^[+][0-9]{11}$", "g");
const zipcodeValidation = new RegExp("^[0-9]{5}$", "g");

const isValidatedInput = (phoneNumber, zipcode) => {
  return (
    phoneNumberValidation.test(phoneNumber) && zipcodeValidation.test(zipcode)
  );
};

const RegisterRestaurant = () => {
  const navigate = useNavigate();
  const [restaurantName, setName] = useState("");
  const [restaurantType, setType] = useState("");
  const [restaurantAddress, setAddress] = useState("");
  const [restaurantZipcode, setZipcode] = useState("");
  const [restaurantPhoneNumber, setPhoneNumber] = useState("");
  const { data: types, sendRequest: sendTypeRequest } = useFetch();
  const {
    error,
    isLoading,
    sendRequest: sendResgiterRestaurantRequest,
  } = useFetch();

  useEffect(() => {
    sendTypeRequest({ url: "/api/restaurantstypes/" });

    if (
      restaurantName &&
      restaurantType &&
      restaurantAddress &&
      restaurantZipcode &&
      restaurantPhoneNumber &&
      isLoading
    ) {
      sendResgiterRestaurantRequest({
        url: "/api/restaurants/",
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: {
          name: restaurantName,
          type_name: restaurantType,
          address: restaurantAddress,
          zipcode: restaurantZipcode,
          phone_number: restaurantPhoneNumber,
        },
      });
      if (!error) {
        navigate("/");
      }
    }
  }, [
    sendTypeRequest,
    sendResgiterRestaurantRequest,
    restaurantName,
    restaurantType,
    restaurantAddress,
    restaurantZipcode,
    restaurantPhoneNumber,
    isLoading,
    navigate,
    error,
  ]);

  const registerRestaurantHandler = async (event) => {
    event.preventDefault();

    if (
      isValidatedInput(
        event.target.phoneNumber.value,
        event.target.zipcode.value
      )
    ) {
      setName(event.target.name.value);
      setType(event.target.rType.value);
      setAddress(event.target.address.value);
      setZipcode(event.target.zipcode.value);
      setPhoneNumber(event.target.phoneNumber.value);
    }
  };

  return (
    <Fragment>
      <h2> Register Restaurant </h2>
      <Link to="/owner">
        <BACK />
      </Link>
      <form onSubmit={registerRestaurantHandler}>
        <div>
          <label htmlFor="name">Restaurant Name : </label>
          <input
            type="text"
            id="name"
            name="name"
            placeholder="Enter Name"
            required
          />
        </div>
        <div>
          <label htmlFor="address">Restaurant Address :</label>
          <input
            type="text"
            id="address"
            name="address"
            placeholder="Enter Address"
            required
          />
        </div>
        <div>
          <label htmlFor="zipcode">Restaurant Zipcode : </label>
          <input
            type="number"
            id="zipcode"
            name="zipcode"
            placeholder="Enter Zipcode"
            required
          />
        </div>
        <div>
          <label htmlFor="phoneNumber">Restaurant Phone Number : </label>
          <input
            type="tel"
            id="phoneNumber"
            name="phoneNumber"
            placeholder="Enter Phone Number"
            required
          />
        </div>
        <div>
          <label htmlFor="rType">Restaurant Type : </label>
          <select
            type="text"
            id="rType"
            name="rType"
            size={types ? types.length : 1}
            required
          >
            {types &&
              types.map((type) => (
                <option key={type.id} value={type.name}>
                  {type.name}
                </option>
              ))}
          </select>
        </div>
        <input type="submit" />
      </form>
      {error && error}
    </Fragment>
  );
};

export default RegisterRestaurant;
