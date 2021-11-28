import React from 'react'
import { Link } from 'react-router-dom'

const RestaurantListItem = ({restaurant}) => {
    return (
        <Link to={`/restaurant/${restaurant.id}`}>
            <h3> {restaurant.name} - {restaurant.address} </h3>
        </Link>
    )
}

export default RestaurantListItem
