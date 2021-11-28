import { BrowserRouter as Router, Route, Routes } from "react-router-dom"
import RestaurantsListPage from './restaurants/RestaurantsListPage'
import RestaurantDetailPage from './restaurants/RestaurantDetailPage'
import OrderListPage from './orders/OrderListPage'
import OrderDetailPage from "./orders/OrderDetailPage"
import Home from './components/Home'


function App() {
  return (
    <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/restaurants" exact element={<RestaurantsListPage />} />
          <Route path="/restaurant/:id" element={<RestaurantDetailPage />} />
          <Route path="/orders" exact element={<OrderListPage />} />
          <Route path="/order/:id" exact element={<OrderDetailPage />} />
        </Routes>
    </Router>
  );
}

export default App;
