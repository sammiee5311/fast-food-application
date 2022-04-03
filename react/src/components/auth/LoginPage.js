import React, { Fragment } from "react";
import classes from "./LoginPage.module.css";

const LoginPage = () => {
  return (
    <Fragment>
      <form style={classes.grid}>
        <input
          className={classes.padding}
          type="text"
          name="email"
          placeholder="Enter Email"
        />
        <input
          className={classes.padding}
          type="text"
          name="passoword"
          placeholder="Enter Password"
        />
        <input className={classes.padding} type="submit" />
      </form>
    </Fragment>
  );
};

export default LoginPage;
