import React, { useEffect } from "react";
import { Link } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import useAuth from "../hooks/useAuth";

import { authActions } from "../store/auth";

const Header = () => {
  const dispatch = useDispatch();
  const userSelector = useSelector((state) => state.auth.user);
  const { isLoading, error, sendRequest } = useAuth();
  const TIME = 1000 * 60 * 3;
  const authTokensSelector = useSelector((state) => state.auth.authTokens);

  const onLogoutClicked = () => {
    dispatch(authActions.logoutUser());
  };

  const refreshTokens = () => {
    sendRequest({
      url: "/api/token/refresh/",
      method: "POST",
      body: {
        refresh: authTokensSelector.refresh,
      },
    });
    if (error) {
      dispatch(authActions.logoutUser());
    }
  };

  useEffect(() => {
    if (isLoading) {
      refreshTokens();
    }

    const interval = setInterval(() => {
      refreshTokens();
    }, TIME);

    return () => clearInterval(interval);
  }, [isLoading, authTokensSelector]);

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
