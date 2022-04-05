import { useState, useCallback } from "react";
import { useSelector } from "react-redux";

const useFetch = () => {
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const authTokensSelector = useSelector((state) => state.auth.authTokens);

  const sendRequest = useCallback(async (requestConfig) => {
    setIsLoading(true);
    setError(null);

    const headers = {
      ...{
        Authorization: `Bearer ${String(authTokensSelector.access)}`,
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
  }, []);

  return {
    data,
    isLoading,
    error,
    sendRequest,
  };
};

export default useFetch;
