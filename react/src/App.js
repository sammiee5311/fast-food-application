import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import RestaurantsPage from "./components/restaurants/RestaurantsPage";
import RestaurantDetailPage from "./components/restaurants/RestaurantDetailPage";
import OrderListPage from "./components/orders/OrderListPage";
import OrderDetailPage from "./components/orders/OrderDetailPage";
import CartPage from "./components/cart/CartPage";
import Home from "./components/Home";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/restaurants" exact element={<RestaurantsPage />} />
        <Route path="/restaurant/:id" element={<RestaurantDetailPage />} />
        <Route path="/orders" exact element={<OrderListPage />} />
        <Route path="/order/:id" exact element={<OrderDetailPage />} />
        <Route path="/cart" exact element={<CartPage />} />
      </Routes>
    </Router>
  );
}

export default App;
