import React, { useContext } from 'react'
import RestaurantMenuItemForm from './RestaurantMenuItemForm'
import CartContext from '../../../store/cart-context'
import Line from '../../../UI/Line'

const RestaurantMenuitem = (props) => {
    const cartCtx = useContext(CartContext)

    const price = `${props.price.toFixed(2)}`

    const addToCartHandler = (quantity, restaurantId) => {
        cartCtx.addItem({
            id: props.id,
            name: props.name,
            quantity: quantity,
            price: props.price,
            restaurantId: restaurantId
        })
    }

    return (
        <div>
            <p> name: {props.name} </p>
            <p> price: {price} </p>
            <RestaurantMenuItemForm onAddToCart={addToCartHandler}/>
            <Line />
        </div>
    )
}

export default RestaurantMenuitem
