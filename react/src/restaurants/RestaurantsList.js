import React from 'react'
import RestaurantListItem from '../components/RestaurantListItem'

const RestaurantsList = (props) => {
    if (props.restaurants === undefined) {
        return <h2>No restaurant found.</h2>
    }

    let filteredRestaurants = props.restaurants.filter((restaruant) => {
        return restaruant.type_name === props.restaurantType
    })

    return (
        <div>
        {filteredRestaurants.map((restaurant, index) => (
            <RestaurantListItem key={index} restaurant={restaurant} />
        ))}
        </div>
    )
}

export default RestaurantsList
