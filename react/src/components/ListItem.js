import React from 'react'
import { Link } from 'react-router-dom'

const ListItem = ({restaurant}) => {
    return (
        <Link to={`/restaurant/${restaurant.id}`}>
            <h3> {restaurant.name} - {restaurant.address} </h3>
        </Link>
    )
}

export default ListItem
