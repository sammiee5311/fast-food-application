import React, { Fragment, useEffect, useState } from "react";

import useAuth from "../../hooks/useAuth";

import classes from "./LoginPage.module.css";

const LoginPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const { sendRequest } = useAuth();

  const authLoginHandler = async (event) => {
    event.preventDefault();

    setEmail(event.target.email.value);
    setPassword(event.target.password.value);
  };

  useEffect(() => {
    if (email && password) {
      sendRequest({
        url: "/api/v0/token/",
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: {
          email: email,
          password: password,
        },
      });
    }
  }, [email, password, sendRequest]);

  return (
    <Fragment>
      <h2> Login </h2>
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
