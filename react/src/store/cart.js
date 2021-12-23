import { createSlice } from "@reduxjs/toolkit";

const initialCartState = {
  items: [],
  totalPrice: 0,
  currentRestaurantId: "",
};

const cartSlice = createSlice({
  name: "cart",
  initialState: initialCartState,
  reducers: {
    addItem: (state, { payload }) => {
      const cartItemIndex = state.items.findIndex(
        (item) => item.id === payload.id
      );
      const hasCartItem = state.items[cartItemIndex];

      if (hasCartItem) {
        state.items[cartItemIndex].quantity += payload.quantity;
      } else {
        state.items.push(payload);
      }

      state.totalPrice += payload.price * payload.quantity;
      state.currentRestaurantId = payload.restaurantId;
    },

    removeItem: (state, { payload }) => {
      const cartItemIndex = state.items.findIndex(
        (item) => item.id === payload
      );
      if (state.items.length === 1) return initialCartState;

      const cartItem = state.items[cartItemIndex];

      state.items = state.items.filter((item) => item.id !== payload);
      state.totalPrice -= cartItem.price * cartItem.quantity;
    },

    clearCart: () => {
      return initialCartState;
    },
  },
});

export const cartActions = cartSlice.actions;

export default cartSlice.reducer;
