import React, { Fragment } from "react";
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";

import { authActions } from "../../store/auth";

import classes from "./LoginPage.module.css";

const LoginPage = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const authLoginHandler = async (event) => {
    event.preventDefault();

    const email = event.target.email.value;
    const password = event.target.password.value;

    const response = await fetch("/api/token/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: email,
        password: password,
      }),
    });

    if (response.status !== 200) {
      throw Error("Something went wrong.");
    }

    const data = await response.json();

    dispatch(authActions.setAuthTokens(data));
    dispatch(authActions.setUser({ access: data.access }));
    localStorage.setItem("authTokens", JSON.stringify(data));
    navigate("/");
  };

  return (
    <Fragment>
      <form className={classes.grid} onSubmit={authLoginHandler}>
        <input
          className={classes.padding}
          type="email"
          name="email"
          placeholder="Enter Email"
        />
        <input
          className={classes.padding}
          type="password"
          name="password"
          placeholder="Enter Password"
        />
        <input className={classes.padding} type="submit" />
      </form>
    </Fragment>
  );
};

export default LoginPage;
