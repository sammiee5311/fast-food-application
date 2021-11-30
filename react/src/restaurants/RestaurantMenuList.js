import React from 'react'
import {v4 as uuidv4} from 'uuid'
import { useNavigate } from "react-router-dom"


const RestaurantMenuList = (props) => {
    let navigate = useNavigate()

    if (props.menus === undefined) {
        return <h2>No menu found.</h2>
    }

    const handlSubmit = (event) => {
        event.preventDefault()
        const uuid = uuidv4()
        navigate(`/orders/`) // navigate to /orders/review/ param=uuid
    }

    let menus = props.menus.map((menu, index) => (
        <div key={index}>
            <p> name: {menu.name} </p>
            <p> price: {menu.price} </p>
            <input type="number" defaultValue="0" />
            <p> ======================== </p>
        </div>
    ))

    return (
        <form onSubmit={handlSubmit}>
            ========================
            {menus}
            <div>
                <button type="submit">Order Food</button>
            </div>
        </form>
    )
}

export default RestaurantMenuList
