import React, { Fragment } from 'react'
import RestaurantMenuitem from './ReastaurantMenuItem/RestaurantMenuitem'


const RestaurantMenuList = (props) => {

    if (props.menus === undefined) {
        return <h2>No menu found.</h2>
    }

    let menus = props.menus.map((menu, index) => (
        <RestaurantMenuitem key={index} id={index} name={menu.name} price={menu.price}/>
    ))

    return (
        <Fragment>
            {menus}
        </Fragment>
    )
}

export default RestaurantMenuList
