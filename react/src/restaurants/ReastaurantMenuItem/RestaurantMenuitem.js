import React from 'react'
import RestaurantMenuItemForm from './RestaurantMenuItemForm'

const RestaurantMenuitem = (props) => {
    const price = `${props.price.toFixed(2)}`

    return (
        <div>
            <p> name: {props.name} </p>
            <p> price: {price} </p>
            <RestaurantMenuItemForm />
            <p> ======================== </p>
        </div>
    )
}

export default RestaurantMenuitem
