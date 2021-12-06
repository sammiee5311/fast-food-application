import React, { useRef, useState } from 'react'
// import {v4 as uuidv4} from 'uuid'
// import { useNavigate } from "react-router-dom"

import Input from '../../../UI/Input'

const RestaurantMenuItemForm = (props) => {
    const [amountIsValid, setAmountIsValid] = useState(false)
    const amountInputRef = useRef()

    // let navigate = useNavigate()

    const handleSubmit = (event) => {
        event.preventDefault()
        
        const inputAmount = amountInputRef.current.value
        const inputAmountNumber = +inputAmount
        // const uuid = uuidv4()

        if (inputAmountNumber === 0 || inputAmountNumber < 0) {
            setAmountIsValid(true)
            return
        }

        setAmountIsValid(false)

        // navigate(`/orders/`) // navigate to /orders/review/ param=uuid
    }

    return (
        <form onSubmit={handleSubmit}>
            <Input 
            ref={amountInputRef}
            label="Amount: "
            input={{
                id: "amount",
                type: "number",
                min: '0',
                step: '1',
                defaultValue: '0'
            }}
            />
            <button type="submit">Add</button>
            {amountIsValid && <p>Invalid amount</p>}
        </form>
    )
}

export default RestaurantMenuItemForm
