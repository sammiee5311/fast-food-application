import React, {useEffect, useState, useCallback, Fragment} from 'react'
import { ReactComponent as BACK } from '../../assets/chevron-left.svg'
import { useParams, Link } from 'react-router-dom'
import Restaurant from './Restaurant'

const RestaurantDetailPage = () => {
    const restaurantId = useParams().id
    const [restaurant, setRestaurant] = useState(null)
    const [isLoading, setIsLoading] = useState(false)
    const [error, setError] = useState(null)

    let content = "No restaurant found."

    const getRestaurantDetail = useCallback(async () => {
        setIsLoading(true)
        setError(null)
        try {
            const response = await fetch(`/api/restaurants/${restaurantId}/`)
            
            if (!response.ok) {
                throw new Error("Invalid request.")
            }

            const data = await response.json()
            setRestaurant(data)
        } catch (error) {
            setError(error)
        }
        setIsLoading(false)
    }, [restaurantId])

    useEffect(() => {
        getRestaurantDetail()
    }, [getRestaurantDetail])

    if (restaurant?.name !== undefined) {
        content = <Restaurant restaurant={restaurant}/>
    }

    if (error) {
        content = <p>{error}</p>
    }

    if (isLoading) {
        content = <p>Loading...</p>
    }

    return (
        <Fragment>
            <h2>Restaurant Detail </h2>
            <Link to="/restaurants"> <BACK /> </Link>
            {content}
        </Fragment>
    )
}

export default RestaurantDetailPage
