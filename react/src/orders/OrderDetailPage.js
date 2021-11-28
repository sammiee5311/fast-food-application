import React, {useEffect, useState, useCallback} from 'react'
import { ReactComponent as BACK } from '../assets/chevron-left.svg'
import { useParams, Link } from 'react-router-dom'

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

    let menus = order?.menus.map((menu, index) => (
        <li key={index}>
            <p> name: {menu.name} </p>
            <p> price: {menu.price} </p>
        </li>
    ))

    if (order?.username !== undefined) {
        text = `Order From : ${order?.username} \n At : ${order?.created_on_str} \n Total Price : ${order?.total_price}`
    }

    return (
        <div>
            <h2> Order Detail </h2>
            <Link to="/orders"> <BACK /> </Link>
            <pre>
                {text}
                <p> - Menu - </p>
                {menus}
            </pre>
        </div>
    )
}

export default OrderDetailPage
