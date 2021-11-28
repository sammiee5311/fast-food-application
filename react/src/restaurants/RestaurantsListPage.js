import React, {useState, useEffect} from 'react'
import RestaurantListItem from '../components/RestaurantListItem'
import { Link } from 'react-router-dom'
import { ReactComponent as BACK } from '../assets/chevron-left.svg'

const RestaurantsListPage = () => {
    let [restaurants, setRestaurants] = useState([])

    let getRestaurants = async () => {
        let response = await fetch('/api/restaurants/')
        let data = await response.json()
        setRestaurants(data)
    }

    useEffect(() => {
        getRestaurants()
    }, [])

    return (
        <div>
            <h2> Restaurants List </h2>
            <Link to="/"> <BACK /> </Link>
            <div className="restaurants-list">
                {restaurants.map((restaurant, index) => (
                    <RestaurantListItem key={index} restaurant={restaurant} />
                ))}
            </div>
        </div>
    )
}

export default RestaurantsListPage
