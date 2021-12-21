import React from 'react'

import OrderMenuList from '../OrderMenu/OrderMenuList'
import classses from './OrderDetailItem.module.css'

const OrderDetailItem = (props) => {
    let EDT = "Calculating EDT..."

    if (props.estimatedDeliveryTime) {
        const hours = (props.estimatedDeliveryTime / 60).toFixed(0)
        const minutes = props.estimatedDeliveryTime % 60 
        EDT =  `${hours} hours ${minutes} minutes`
    }

    return (
        <pre>
            <p>Order From : {props.username}</p>
            <p>Time : {props.time}</p>
            <p>At : {props.restaurantName}</p>
            <p>Total Price : {props.totalPrice}</p>
            <p>EDT : {EDT}</p>
            <p className={classses.menus}> - Menu - </p>
            <OrderMenuList menus={props.menus}/>
        </pre>
    )
}

export default OrderDetailItem
