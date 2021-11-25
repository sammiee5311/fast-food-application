import React from "react"
import { Link } from "react-router-dom"
import { ReactComponent as SEARCH } from "../assets/search.svg"

const Home = () => {
    return (
        <div>
            <h2> Home </h2>
            <SEARCH />
            <Link to="/restaurants"> <h2> Restaurants List </h2> </Link>
            <Link to="/"> <h2> Order Food </h2> </Link>
        </div>
    );
}

export default Home;