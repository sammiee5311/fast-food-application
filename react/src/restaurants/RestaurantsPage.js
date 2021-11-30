import React, {useState, useEffect} from 'react'
import RestaurantType from './RestaurantType'
import RestaurantsList from './RestaurantsList'
import { Link } from 'react-router-dom'
import { ReactComponent as BACK } from '../assets/chevron-left.svg'
import './RestaurantsPage.css'


const RestaurantsPage = () => {
    let [restaurants, setRestaurants] = useState([])
    let [restaurantType, setRestaurantType] = useState('pizza')
    
    const filterType = (filteredType) => {
        setRestaurantType(filteredType)
    }

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
            <div className="filter-type">
            <RestaurantType onFilterType={filterType}/>
            </div>
            <RestaurantsList restaurants={restaurants} restaurantType={restaurantType}/>
        </div>
    )
}

export default RestaurantsPage
