import React, { useReducer } from 'react'

import CartContext from './cart-context'

const defaultCartState = {
    items: [],
    totalPrice: 0,
    currentRestaurantId: ''
}

const cartReducer = (state, action) => {
    if (action.type === 'ADD_ITEM_TO_CART') {
        const updatedTotalPrice = state.totalPrice + action.item.price * action.item.quantity

        const cartIndex = state.items.findIndex(
            (item) => item.id === action.item.id
        )

        const cartItemIndex = state.items[cartIndex]

        let updatedItems
        
        if (cartItemIndex) {
            const updatedItem = {
                ...cartItemIndex,
                quantity: cartItemIndex.quantity + action.item.quantity
            }

            updatedItems = [...state.items]
            updatedItems[cartIndex] = updatedItem
        } else {
            updatedItems = state.items.concat(action.item) 
        }

        return {
            items: updatedItems,
            totalPrice: updatedTotalPrice,
            currentRestaurantId: action.item.restaurantId
        }

    }

    if (action.type === 'REMOVE_ITEM_FROM_CART') {
        const cartItemIndex = state.items.findIndex(
            (item) => item.id === action.id
        )

        const cartItem = state.items[cartItemIndex]
        const updatedTotalPrice = state.totalPrice - (cartItem.price * cartItem.quantity)
        
        const updatedItems = state.items.filter(
            (item) => item.id !== action.id
        )

        return {
            items: updatedItems,
            totalPrice: updatedTotalPrice,
            currentRestaurantId: action.item.restaurantId
        }

    }

    if (action.type === 'CLEAR_CART') {
        return defaultCartState
    }

    return defaultCartState
}

const CartProvider = (props) => {
    const [cartState, dispatchCartAction] = useReducer(
        cartReducer,
        defaultCartState
    )

    const addItemFromCartHandler = (item) => {
        dispatchCartAction({type: 'ADD_ITEM_TO_CART', item: item})
    }

    const removeItemFromCartHandler = (id) => {
        dispatchCartAction({type: 'REMOVE_ITEM_FROM_CART', id: id})
    }

    const clearCartHandler = () => {
        dispatchCartAction({type: 'CLEAR_CART'})
    }

    const cartContext = {
        items: cartState.items,
        totalPrice: cartState.totalPrice,
        currentRestaurantId: cartState.currentRestaurantId,
        addItem: addItemFromCartHandler,
        removeItem: removeItemFromCartHandler,
        clearCart: clearCartHandler
    }

    return (
        <CartContext.Provider value={cartContext}>
            {props.children}
        </CartContext.Provider>
    )
}

export default CartProvider
