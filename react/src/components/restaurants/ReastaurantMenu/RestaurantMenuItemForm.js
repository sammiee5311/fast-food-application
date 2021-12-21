import React, { useRef, useState, useContext } from 'react'
import CartContext from '../../../store/cart-context'
import Input from '../../../UI/Input'


const isQuantityIsValid = (quantity) => {
    return (quantity !== 0 || quantity > 0)
}

const hasDifferentRestarauntMenu = (cartRestaurantId, inputRestaurantId) => {
    return cartRestaurantId !== '' && inputRestaurantId !== cartRestaurantId
}


const RestaurantMenuItemForm = (props) => {
    const [quantityIsValid, setQuantityIsValid] = useState(true)
    const quantityInputRef = useRef()
    const [orderIsValid, setOrderIsValid] = useState(true)
    const cartCtx = useContext(CartContext)

    const handleSubmit = (event) => {
        event.preventDefault()
        
        const inputQuantity = +(quantityInputRef.current.value)

        if (!isQuantityIsValid(inputQuantity)) {
            setQuantityIsValid(false)
            return
        }

        setQuantityIsValid(true)

        const inputRestaurantId = event.target.action.split('/')[4]
        
        if (hasDifferentRestarauntMenu(cartCtx.currentRestaurantId, inputRestaurantId)){
            setOrderIsValid(false)
            return
        }

        setOrderIsValid(true)

        props.onAddToCart(inputQuantity, inputRestaurantId)
    }

    return (
        <form onSubmit={handleSubmit}>
            <Input 
            ref={quantityInputRef}
            label="Quantity: "
            input={{
                id: "quantity",
                type: "number",
                min: '1',
                step: '1',
                defaultValue: '1'
            }}
            />
            <button type="submit">Add</button>
            {!quantityIsValid && <p>*Invalid quantity*</p>}
            {!orderIsValid && <p>*You cannot add different restuarant's menu in the cart.*</p>}
        </form>
    )
}

export default RestaurantMenuItemForm
