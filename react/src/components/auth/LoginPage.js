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
        url: "/api/token/",
        method: "POST",
        body: {
          email: email,
          password: password,
        },
      });
    }
  }, [email, password]);

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
