import { createSlice } from "@reduxjs/toolkit";
import jwt_decode from "jwt-decode";

const AUTH_TOKENS = localStorage.getItem("authTokens");

const initialAuthState = {
  user: AUTH_TOKENS ? jwt_decode(AUTH_TOKENS) : null,
  authTokens: AUTH_TOKENS ? JSON.parse(AUTH_TOKENS) : null,
};

const authSlice = createSlice({
  name: "auth",
  initialState: initialAuthState,
  reducers: {
    setUser: (state, { payload: { access } }) => {
      const user = jwt_decode(access);

      state.user = user;
    },
    logoutUser: (state) => {
      state.user = null;
      state.authTokens = null;

      localStorage.removeItem("authTokens");
    },
    setAuthTokens: (state, { payload }) => {
      state.authTokens = payload;
    },
  },
});

export const authActions = authSlice.actions;

export default authSlice.reducer;
