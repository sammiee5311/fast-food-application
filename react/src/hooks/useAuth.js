import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { useState, useCallback } from "react";

import { authActions } from "../store/auth";

const useAuth = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const sendRequest = useCallback(
    async (requestConfig) => {
      try {
        const response = await fetch(requestConfig.url, {
          method: requestConfig.method ? requestConfig.method : "GET",
          headers: { "Content-Type": "application/json" },
          body: requestConfig.body ? JSON.stringify(requestConfig.body) : null,
        });

        if (!response.ok) {
          throw Error("Something went wrong.");
        }

        const data = await response.json();

        dispatch(authActions.setAuthTokens(data));
        dispatch(authActions.setUser({ access: data.access }));
        localStorage.setItem("authTokens", JSON.stringify(data));
      } catch (err) {
        setError(err.message);
      }
      setIsLoading(false);
      navigate("/");
    },
    [isLoading]
  );

  return {
    isLoading,
    error,
    sendRequest,
  };
};

export default useAuth;
