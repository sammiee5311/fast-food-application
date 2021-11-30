import React from 'react'

const OrderMenuList = (props) => {

    if (props.menus === undefined) {
        return <h2>No menu found.</h2>
    }

    let menus = props.menus.map((menu, index) => (
        <div key={index}>
            <p> name: {menu.name} </p>
            <p> price: {menu.price} </p>
            <p> quantity: {menu.quantity} </p>
            <p> ======================== </p>
        </div>
    ))

    return (
        <div>
            ========================
            {menus}
        </div>
    )
}

export default OrderMenuList
