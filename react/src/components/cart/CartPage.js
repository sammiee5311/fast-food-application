import React, { Fragment, useContext, useState } from 'react'
import Cookies from 'js-cookie'
import { Link } from 'react-router-dom'
import { ReactComponent as BACK } from '../../assets/chevron-left.svg'
import {v4 as uuidv4} from 'uuid'
import { useNavigate } from "react-router-dom"

import Line from '../../UI/Line'
import CartContext from '../../store/cart-context'
import CartItem from './CartItem'
import classes from './CartPage.module.css'

const Cart = () => {
    const cartCtx = useContext(CartContext)
    const [isSuccessOrder, setIsSuccessOrder] = useState(true)
    const [error, setError] = useState(null)

    let navigate = useNavigate()

    const totalPrice = `${cartCtx.totalPrice.toFixed(2)} $`

    const cartItemRemoveHandler = id => {
        cartCtx.removeItem(id)
    }

    const cartItems = 
        cartCtx.items.map((item, index) => 
            <CartItem 
                key={index} 
                name={item.name}
                quantity={item.quantity}
                price={item.price}
                onRemove={cartItemRemoveHandler.bind(null, item.id)}
            />
        )
    
    const orderCartItemsHandler = async() => {
        setError(null)
        setIsSuccessOrder(true)
        try {
            if (cartCtx.items.length === 0) {
                throw new Error("Order cannot be proccessed with no items in Cart.")
            }
            const restaurantID = cartCtx.currentRestaurantId
            const user = 1
            const menus = cartCtx.items.map((item) => {
                return {
                    menu: item.id,
                    quantity: item.quantity
                }
            })

            const payload = 
                {
                    "restaurant": restaurantID,
                    "user": user,
                    "menus": menus
                }

            const response = await fetch('/api/orders/', {
                method: 'POST',
                body: JSON.stringify(payload),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': Cookies.get('csrftoken')
                }
            })
        
            response.json()
            .then((result) => result)
            .then((data) => {
                const result_data = JSON.stringify(data)
                if (response.status !== 201) {
                    throw new Error(result_data)
                }
                cartCtx.clearCart()
                navigate(`/order/${data.id}`)
            }).catch(error => {
                setError(error.message)
                setIsSuccessOrder(false)
            })
                
            
        } catch (error) {
            setError(error.message)
            setIsSuccessOrder(false)
        }
    }
    
    const isCartEmpty = cartItems.length === 0
    
    let items = <p> Cart is Empty </p>

    if (!isCartEmpty) {
        items = <Fragment> <Line /> {cartItems} </Fragment>
    }

    return (
        <Fragment>
            <h2> Cart </h2>
            <Link to="/"> <BACK /> </Link>
            <p> - Menu - </p>
            {items}
            <div className={classes.padding}>
                <span>Total Price: </span>
                <span>{totalPrice}</span>
            </div>
            <div className={classes.padding}>
                <button onClick={orderCartItemsHandler}>Order</button>
                <p>{!isSuccessOrder && error.length > 0 && error}</p>
            </div>
        </Fragment>
    )
}

export default Cart