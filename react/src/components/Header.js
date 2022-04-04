import React from "react";
import { Link } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";

import { authActions } from "../store/auth";

const Header = () => {
  const dispatch = useDispatch();
  const userSelector = useSelector((state) => state.auth.user);

  const onLogoutClicked = () => {
    dispatch(authActions.logoutUser());
  };

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
