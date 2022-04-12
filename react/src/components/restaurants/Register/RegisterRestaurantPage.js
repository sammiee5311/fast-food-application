import React, { Fragment, useEffect, useState } from "react";

import useFetch from "../../../hooks/useFetch";

const RegisterRestaurant = () => {
  const [restaurantName, setName] = useState("");
  const [restaurantType, setType] = useState("");
  const [restaurantAddress, setAddress] = useState("");
  const [restaurantZipcode, setZipcode] = useState("");
  const [restaurantPhoneNumber, setPhoneNumber] = useState("");
  const { data: types, sendRequest } = useFetch();

  useEffect(() => {
    sendRequest({ url: "/api/restauratnstypes/" });
  }, [sendRequest]);

  const authLoginHandler = async (event) => {
    event.preventDefault();

    setName(event.target.name.value);
    setType(event.target.rType.value);
    setAddress(event.target.address.value);
    setZipcode(event.target.zipcode.value);
    setPhoneNumber(event.target.phoneNumber.value);
  };

  return (
    <Fragment>
      <form onSubmit={authLoginHandler}>
        <div>
          <label htmlFor="name">Restaurant Name : </label>
          <input type="text" id="name" name="name" placeholder="Enter Name" />
        </div>
        <div>
          <label htmlFor="address">Restaurant Address :</label>
          <input
            type="text"
            id="address"
            name="address"
            placeholder="Enter Address"
          />
        </div>
        <div>
          <label htmlFor="zipcode">Restaurant Zipcode : </label>
          <input
            type="number"
            id="zipcode"
            name="zipcode"
            placeholder="Enter Zipcode"
          />
        </div>
        <div>
          <label htmlFor="phoneNumber">Restaurant Phone Number : </label>
          <input
            type="tel"
            id="phoneNumber"
            name="phoneNumber"
            placeholder="Enter Phone Number"
          />
        </div>
        <div>
          <label htmlFor="rType">Restaurant Type : </label>
          <select
            type="text"
            id="rType"
            name="rType"
            size={types ? types.length : 1}
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
    </Fragment>
  );
};

export default RegisterRestaurant;
