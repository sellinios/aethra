// src/App.tsx
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Header from './components/Header/Header';
import Footer from './components/Footer/Footer';
import HomePage from './pages/HomePage';
import AboutPage from './pages/AboutPage';
import ContactPage from './pages/ContactPage';
import Municipalities from './pages/Municipalities';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import PlaceDetail from './pages/PlaceDetail'; // Import the PlaceDetail component
import './App.css'; // Import global styles
import 'bootstrap/dist/css/bootstrap.min.css'; // Bootstrap CSS

const App: React.FC = () => {
  return (
    <div className="app-container">
      <Header /> {/* Header stays consistent on every page */}
      <main className="main-content">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/contact" element={<ContactPage />} />
          <Route path="/geography/greece/municipalities" element={<Municipalities />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          {/* Dynamic route for place details */}
          <Route
            path="/:continentSlug/:countrySlug/:regionSlug/:municipalitySlug/:placeSlug/"
            element={<PlaceDetail />}
          />
          {/* Add more routes as needed */}
        </Routes>
      </main>
      <Footer /> {/* Footer is placed after the content */}
    </div>
  );
};

export default App;
