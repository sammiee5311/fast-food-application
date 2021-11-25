import React from 'react';
import ReactDOM from 'react-dom';
import Header from './components/Header'
import Footer from './components/Footer'
import App from './App';
import './App.css'

const routing = (
    <React.StrictMode>
      <div className="App">
        <Header />
          <App />
        <Footer />
      </div>
    </React.StrictMode>
);

ReactDOM.render(routing, document.getElementById('root'));
