import React, {useEffect, useState, useCallback} from 'react'
import { ReactComponent as BACK } from '../assets/chevron-left.svg'
import { useParams, Link } from 'react-router-dom'

const RestaurantDetailPage = () => {
    let restaurantId = useParams().id
    let [restaurant, setRestaurant] = useState(null)
    let text = "There is not a restaurant."

    let getRestaurant = useCallback(async () => {
        let response = await fetch(`/api/restaurants/${restaurantId}/`)
        let data = await response.json()
        setRestaurant(data)
    }, [restaurantId])

    useEffect(() => {
        getRestaurant()
    }, [getRestaurant])


    if (restaurant?.name !== undefined) {
        text = `Name : ${restaurant?.name} \n Address : ${restaurant?.address} \n Phone Number : ${restaurant?.phone_number} \n Menu : ${restaurant?.menus}`
    }

    return (
        <div>
            <h2>Restaurant Detail </h2>
            <Link to="/restaurants"> <BACK /> </Link>
            <pre>
                {text}
            </pre>
        </div>
    )
}

export default RestaurantDetailPage
