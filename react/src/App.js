import { BrowserRouter as Router, Route, Routes } from "react-router-dom"
import RestaurantsListPage from './restaurants/RestaurantsListPage'
import RestaurantDetailPage from './restaurants/RestaurantDetailPage'
import Home from './components/Home'


function App() {
  return (
    <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/restaurants" exact element={<RestaurantsListPage />} />
          <Route path="/restaurant/:id" element={<RestaurantDetailPage />} />
        </Routes>
    </Router>
  );
}

export default App;
