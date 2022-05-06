import React, { useEffect } from "react";

import useFetch from "../../../hooks/useFetch";

const RestaurantType = (props) => {
  const { data: types, isLoading, error, sendRequest } = useFetch();

  useEffect(() => {
    sendRequest({ url: "/api/v0/restaurantstypes/" });
  }, [sendRequest]);

  const filterType = (event) => {
    props.onFilterType(event.target.value);
  };

  return (
    <div>
      {!isLoading | !error && (
        <select
          name="type"
          size={types ? types.length : 1}
          onChange={filterType}
        >
          {types &&
            types.map((type) => (
              <option key={type.id} value={type.name}>
                {type.name}
              </option>
            ))}
        </select>
      )}
    </div>
  );
};

export default RestaurantType;
