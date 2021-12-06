import React, { Fragment } from 'react'
import RestaurantListItem from './RestaurantListItem'

const RestaurantsList = (props) => {
    if (props.restaurants === undefined) {
        return <h2>No restaurant found.</h2>
    }

    let filteredRestaurants = props.restaurants.filter((restaruant) => {
        return restaruant.type_name === props.restaurantType
    })

    return (
        <Fragment>
        {filteredRestaurants.map((restaurant, index) => (
            <RestaurantListItem key={index} restaurant={restaurant} />
        ))}
        </Fragment>
    )
}

export default RestaurantsList
