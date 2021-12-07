import React, { Fragment, useContext } from 'react'
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
    
    const orderHandler = () => {
        if (cartCtx.items.length === 0) {
            return
        }
        cartCtx.clearCart()
        navigate('/orders/')
    }
    
    const isCartEmpty = cartItems.length === 0
    
    let text = <p> Cart is Empty </p>

    if (!isCartEmpty) {
        text = <Line />
    }

    return (
        <Fragment>
            <h2> Cart </h2>
            <Link to="/"> <BACK /> </Link>
            <p> - Menu - </p>
            {text}
            {cartItems}
            <div className={classes.padding}>
                <span>Total Price: </span>
                <span>{totalPrice}</span>
            </div>
            <div className={classes.padding}>
                <button onClick={orderHandler}>Order</button>
            </div>
        </Fragment>
    )
}

export default Cart