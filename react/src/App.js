import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import PrivateRoute from "./utils/PrivateRoute";

import Header from "./components/Header";
import RestaurantsPage from "./components/restaurants/RestaurantsPage";
import RegisterRestaurantPage from "./components/restaurants/Register/RegisterRestaurantPage";
import RestaurantDetailPage from "./components/restaurants/RestaurantDetailPage";
import OrderListPage from "./components/orders/OrderListPage";
import OrderDetailPage from "./components/orders/OrderDetailPage";
import CartPage from "./components/cart/CartPage";
import Home from "./components/Home";
import LoginPage from "./components/auth/LoginPage";

function App() {
  return (
    <Router>
      <Header />
      <Routes>
        <Route exact path="/" element={<PrivateRoute />}>
          <Route exact path="/" element={<Home />} />
          <Route path="/restaurant/:id" element={<RestaurantDetailPage />} />
          <Route path="/orders" element={<OrderListPage />} />
          <Route path="/order/:id" element={<OrderDetailPage />} />
          <Route path="/cart" element={<CartPage />} />
        </Route>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/restaurants" element={<RestaurantsPage />} />
        <Route path="/regrestaurant" element={<RegisterRestaurantPage />} />
      </Routes>
    </Router>
  );
}

export default App;
