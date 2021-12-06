import React, {useState, useEffect, Fragment} from 'react'
import RestaurantType from './RestaurantType'
import RestaurantsList from './RestaurantsList'
import { Link } from 'react-router-dom'
import { ReactComponent as BACK } from '../../assets/chevron-left.svg'
import classes from './RestaurantsPage.module.css'


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
        <Fragment>
            <h2> Restaurants List </h2>
            <Link to="/"> <BACK /> </Link>
            <div className={classes.filter_type}>
            <RestaurantType onFilterType={filterType}/>
            </div>
            <RestaurantsList restaurants={restaurants} restaurantType={restaurantType}/>
        </Fragment>
    )
}

export default RestaurantsPage
