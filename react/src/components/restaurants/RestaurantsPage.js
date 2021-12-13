import React, {useState, useEffect, useCallback, Fragment} from 'react'
import RestaurantType from './Restaurant/RestaurantType'
import RestaurantsList from './Restaurant/RestaurantList'
import { Link } from 'react-router-dom'
import { ReactComponent as BACK } from '../../assets/chevron-left.svg'
import classes from './RestaurantsPage.module.css'


const RestaurantsPage = () => {
    const [restaurants, setRestaurants] = useState([])
    const [restaurantType, setRestaurantType] = useState('')
    
    const filterType = (filteredType) => {
        setRestaurantType(filteredType)
    }

    const getRestaurantList = useCallback(async () => {
        const response = await fetch('/api/restaurants/')
        const data = await response.json()
        setRestaurants(data)
    }, [])

    useEffect(() => {
        getRestaurantList()
    }, [getRestaurantList])

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
