import React, { Fragment } from 'react'
import classes from './CartPayment.module.css'

const CartPayment = (props) => {
    return (
        <Fragment>
            <div className={classes.payment}>
                *payment api*
                <div className={classes.payment}>
                    Total Price: {props.totalPrice}
                </div>
            </div>
            <div className={classes.confirm}>
                <span><button onClick={props.onConfrim}>confirm</button></span>
                <span><button onClick={props.onCancel}>cancel</button></span>
            </div>
        </Fragment>
    )
}

export default CartPayment
