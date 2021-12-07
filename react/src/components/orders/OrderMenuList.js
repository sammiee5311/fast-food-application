import React from 'react'
import Line from '../../UI/Line'

const OrderMenuList = (props) => {

    if (props.menus === undefined) {
        return <h2>No menu found.</h2>
    }

    let menus = props.menus.map((menu, index) => (
        <div key={index}>
            <p> name: {menu.name} </p>
            <p> price: {menu.price} </p>
            <p> quantity: {menu.quantity} </p>
            <Line />
        </div>
    ))

    return (
        <div>
            <Line />
            {menus}
        </div>
    )
}

export default OrderMenuList
