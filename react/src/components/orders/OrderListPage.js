import React, {useState, useEffect, Fragment} from 'react'
import OrderListItem from './OrderListItem'
import { Link } from 'react-router-dom'
import { ReactComponent as BACK } from '../../assets/chevron-left.svg'

const OrderListPage = () => {
    let [orders, setOrders] = useState([])

    let getOrders = async () => {
        let response = await fetch("/api/orders/")
        let data = await response.json()
        setOrders(data)
    }

    useEffect(() => {
        getOrders()
    }, [])

    return (
        <Fragment>
            <h2> Order List </h2>
            <Link to="/"> <BACK /> </Link>
            <div className="order-list">
                {orders.map((order, index) => (
                    <OrderListItem key={index} order={order} />
                ))}
            </div>
        </Fragment>
    )
}

export default OrderListPage
