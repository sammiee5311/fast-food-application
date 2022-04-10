import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import { useState, useCallback } from "react";

import { authActions } from "../store/auth";

const useFetch = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const sendRequest = useCallback(
    async (requestConfig) => {
      setIsLoading(true);
      setError(null);

      try {
        const response = await fetch(requestConfig.url, {
          method: requestConfig.method ? requestConfig.method : "GET",
          headers: requestConfig.headers,
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
    [dispatch, navigate]
  );

  return {
    isLoading,
    error,
    sendRequest,
  };
};

export default useFetch;
