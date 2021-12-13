import React from 'react'
import { Link } from 'react-router-dom'

const OrderListItem = ({order}) => {
    return (
        <Link to={`/order/${order.id}`}>
            <h3> {order.username} - {order.created_on_str} </h3>
        </Link>
    )
}

export default OrderListItem
