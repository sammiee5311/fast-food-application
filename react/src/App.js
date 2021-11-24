import './App.css'
import { BrowserRouter as Router, Route, Routes } from "react-router-dom"
import Header from './components/Header'
import Footer from './components/Footer'
import RestaurantsListPage from './restaurants/RestaurantsListPage'
import RestaurantDetailPage from './restaurants/RestaurantDetailPage'


function App() {
  return (
    <Router>
      <div className="App">
        <Header />
        <Routes>
          <Route path="/" exact element={<RestaurantsListPage />} />
          <Route path="/restaurant/:id" element={<RestaurantDetailPage />} />
        </Routes>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
