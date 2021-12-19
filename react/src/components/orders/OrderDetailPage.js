import React, {useEffect, useState, useCallback, Fragment} from 'react'
import { ReactComponent as BACK } from '../../assets/chevron-left.svg'
import { useParams, Link } from 'react-router-dom'

import OrderMenuList from './OrderMenu/OrderMenuList'

const OrderDetailPage = () => {
    const orderId = useParams().id
    const [order, setOrder] = useState(null)
    let text = "Invalid request."

    const getOrder = useCallback(async () => {
        const response = await fetch(`/api/orders/${orderId}/`)
        const data = await response.json()
        setOrder(data)
    }, [orderId])

    useEffect(() => {
        getOrder()
    }, [getOrder])

    if (order?.username !== undefined) {
        text = `Order From : ${order.username} \n Time : ${order.created_on_str} \n At : ${order.restaurant_name} \n Total Price : ${order.total_price.toFixed(2)} $`
        if (order?.estimated_delivery_time) {
            const EDT = order.estimated_delivery_time
            const hours = (EDT / 60).toFixed(0)
            const minutes = EDT % 60 
            text = text.concat(`\n EDT: ${hours} hours ${minutes} minutes`)
        } else {
            text = text.concat(`\n Calculating EDT...`)
        }
    }


    return (
        <Fragment>
            <h2> Order Detail </h2>
            <Link to="/orders"> <BACK /> </Link>
            <pre>
                {text}
                <p> - Menu - </p>
                <OrderMenuList menus={order?.menus}/>
            </pre>
        </Fragment>
    )
}

export default OrderDetailPage
