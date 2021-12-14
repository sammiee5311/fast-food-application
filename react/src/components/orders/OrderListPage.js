import React, {useState, useEffect, Fragment} from 'react'
import OrderListItem from './Order/OrderListItem'
import { Link } from 'react-router-dom'
import { ReactComponent as BACK } from '../../assets/chevron-left.svg'

const OrderListPage = () => {
    const [orders, setOrders] = useState([])
    const [isLoading, setIsLoading] = useState(false)
    const [error, setError] = useState(null)

    let content = <p> No order found. </p>

    const getOrders = async () => {
        setIsLoading(true)
        setError(null)
        const response = await fetch("/api/orders/")

        if (!response.ok) {
            throw Error("Something went wrong.")
        }
        const data = await response.json()
        setIsLoading(false)
        setOrders(data)
    }

    useEffect(() => {
        getOrders().catch(error => {
            setError(error.message)
            setIsLoading(false)
        })
    }, [])

    if (orders.length > 0) {
        content = 
        <div className="order-list">
            {orders.map((order, index) => (
                <OrderListItem key={index} order={order} />
            ))}
        </div>
    }

    if (error) {
        content = <p>{error}</p>
    }

    if (isLoading) {
        content = <p>Loading...</p>
    }

    return (
        <Fragment>
            <h2> Order List </h2>
            <Link to="/"> <BACK /> </Link>
            {content}
        </Fragment>
    )
}

export default OrderListPage
