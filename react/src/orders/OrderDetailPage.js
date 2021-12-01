import React, {useEffect, useState, useCallback, Fragment} from 'react'
import { ReactComponent as BACK } from '../assets/chevron-left.svg'
import { useParams, Link } from 'react-router-dom'

import OrderMenuList from './OrderMenuList'

const OrderDetailPage = () => {
    let orderId = useParams().id
    let [order, setOrder] = useState(null)
    let text = "Invalid request."

    let getOrder = useCallback(async () => {
        let response = await fetch(`/api/orders/${orderId}/`)
        let data = await response.json()
        setOrder(data)
    }, [orderId])

    useEffect(() => {
        getOrder()
    }, [getOrder])

    if (order?.username !== undefined) {
        text = `Order From : ${order?.username} \n At : ${order?.created_on_str} \n Total Price : ${order?.total_price}`
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
