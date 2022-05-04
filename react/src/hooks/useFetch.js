import { useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { useSelector } from "react-redux";

const useFetch = () => {
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const authTokensSelector = useSelector((state) => state.auth.authTokens);

  const sendRequest = useCallback(
    async (requestConfig) => {
      setIsLoading(true);
      setError(null);

      const headers = {
        ...{
          Authorization: `Bearer ${String(
            authTokensSelector ? authTokensSelector.access : ""
          )}`,
        },
        ...requestConfig.headers,
      };

      try {
        const response = await fetch(requestConfig.url, {
          method: requestConfig.method ? requestConfig.method : "GET",
          headers: headers,
          body: requestConfig.body ? JSON.stringify(requestConfig.body) : null,
        });

        if (!response.ok) {
          throw Error("Something went wrong.");
        }

        const data = await response.json();

        setData(data);
      } catch (err) {
        setError(err.message);
      }
      setIsLoading(false);
      if (requestConfig.navigate) navigate(requestConfig.navigate);
    },
    [authTokensSelector, navigate]
  );

  return {
    data,
    isLoading,
    error,
    sendRequest,
  };
};

export default useFetch;
