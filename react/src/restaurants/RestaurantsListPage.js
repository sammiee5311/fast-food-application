import React, {useState, useEffect} from 'react'
import ListItem from '../components/ListItem'

const RestaurantsListPage = () => {
    let [restaurants, setRestaurants] = useState([])

    let getRestaurants = async () => {
        let response = await fetch('/api/restaurants/')
        let data = await response.json()
        console.log('DATA: ', data)
        setRestaurants(data)
    }

    useEffect(() => {
        getRestaurants()
    }, [])

    return (
        <div>
            <div className="restaurants-list">
                {restaurants.map((restaurant, index) => (
                    <ListItem key={index} restaurant={restaurant} />
                ))}
            </div>
        </div>
    )
}

export default RestaurantsListPage
