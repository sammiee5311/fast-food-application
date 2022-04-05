import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";

import { authActions } from "../store/auth";

const Header = () => {
  const dispatch = useDispatch();
  const userSelector = useSelector((state) => state.auth.user);
  const TIME = 1000 * 60 * 3;

  const [isLoading, setIsLoading] = useState(true);

  const authTokensSelector = useSelector((state) => state.auth.authTokens);

  const fetchTokens = async (endpoint, payload) => {
    const response = await fetch(`${endpoint}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (response.status !== 200) {
      throw Error("Something went wrong.");
    }

    const data = await response.json();

    dispatch(authActions.setAuthTokens(data));
    dispatch(authActions.setUser({ access: data.access }));
    localStorage.setItem("authTokens", JSON.stringify(data));
  };

  const onLogoutClicked = () => {
    dispatch(authActions.logoutUser());
  };

  const updateToken = async () => {
    try {
      await fetchTokens("/api/token/refresh/", {
        refresh: authTokensSelector.refresh,
      });
    } catch {
      dispatch(authActions.logoutUser());
    }

    if (isLoading) setIsLoading(false);
  };

  useEffect(() => {
    if (isLoading) {
      updateToken();
    }

    const interval = setInterval(() => {
      if (authTokensSelector) {
        updateToken();
      }
    }, TIME);

    return () => clearInterval(interval);
  }, [authTokensSelector, isLoading]);

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
