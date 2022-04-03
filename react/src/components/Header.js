import React from "react";
import { Link } from "react-router-dom";

const Header = () => {
  return (
    <div>
      <h1>Fast Food Restaurant</h1>
      <Link to="/">Home</Link>
      <span> | </span>
      <Link to="/login">Login</Link>
    </div>
  );
};

export default Header;
