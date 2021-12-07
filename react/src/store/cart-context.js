import React from 'react'

const CartContext = React.createContext({
    items: [],
    totalPrice: 0,
    currentRestaurantId: '',
    addItem: (item) => {},
    removeItem: (id) => {},
    clearCart: () => {}
})

export default CartContext
