import React, { useEffect } from "react";
import { Link } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import useAuth from "../hooks/useAuth";

import { authActions } from "../store/auth";

const Header = () => {
  const dispatch = useDispatch();
  const userSelector = useSelector((state) => state.auth.user);
  const { error, sendRequest } = useAuth();
  const TIME = 1000 * 60 * 60;
  const authTokensSelector = useSelector((state) => state.auth.authTokens);

  const onLogoutClicked = () => {
    dispatch(authActions.logoutUser());
  };

  useEffect(() => {
    const interval = setInterval(() => {
      sendRequest({
        url: "/api/token/refresh/",
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: {
          refresh: authTokensSelector.refresh,
        },
      });
      if (error) {
        dispatch(authActions.logoutUser());
      }
    }, TIME);

    return () => clearInterval(interval);
  }, [sendRequest, error, authTokensSelector, dispatch]);

  return (
    <div>
      <h1>Fast Food Restaurant</h1>
      <Link to="/">Home</Link>
      <span> | </span>
      {userSelector ? (
        <Link to="/login" onClick={onLogoutClicked}>
          Logout
        </Link>
      ) : (
        <Link to="/login">Login</Link>
      )}
      {userSelector && <p>Hello, {userSelector.username}</p>}
    </div>
  );
};

export default Header;
