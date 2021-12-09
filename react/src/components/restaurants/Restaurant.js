import React from 'react'
import RestaurantMenuList from './RestaurantMenuList'
import Line from '../../UI/Line'

const Restaurant = (props) => {
    let content = `Name : ${props.restaurant.name} \n Address : ${props.restaurant.address} \n Phone Number : ${props.restaurant.phone_number}`
    return (
        <pre>
            {content}
            <p> - Menu - </p>
            <Line />
            <RestaurantMenuList menus={props.restaurant.menus}/>
        </pre>
    )
}

export default Restaurant
