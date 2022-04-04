import React from "react";
import { Navigate, Outlet } from "react-router-dom";
import { useSelector } from "react-redux";

const PrivateRoute = () => {
  const userSelector = useSelector((state) => state.auth.user);

  return userSelector ? <Outlet /> : <Navigate to="/login" />;
};

export default PrivateRoute;
