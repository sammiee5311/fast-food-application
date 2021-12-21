import React from 'react'

import RestaurantMenuList from '../ReastaurantMenu/RestaurantMenuList'
import Line from '../../../UI/Line'
import classess from './Restaurant.module.css'

const Restaurant = (props) => {
    return (
        <pre>
            <p>Name : {props.restaurant.name}</p>
            <p>Address : {props.restaurant.address}</p>
            <p>Phone Number : {props.restaurant.phone_number}</p>
            <p className={classess.menus}> - Menu - </p>
            <Line />
            <RestaurantMenuList menus={props.restaurant.menus}/>
        </pre>
    )
}

export default Restaurant
