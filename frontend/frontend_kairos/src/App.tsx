// src/App.tsx
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import TopBar from './components/TopBar/TopBar';
import Header from './components/Header/Header';
import Footer from './components/Footer/Footer';
import HomePage from './pages/HomePage';
import AboutPage from './pages/AboutPage';
import ContactPage from './pages/ContactPage';
import Municipalities from './pages/Municipalities';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import MunicipalityDetail from './pages/MunicipalityDetail';
import PlaceDetail from './pages/PlaceDetail';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';

const App: React.FC = () => {
  return (
    <div className="app-container">
      <TopBar />
      <Header />
      <main className="main-content">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/contact" element={<ContactPage />} />
          <Route path="/geography/greece/municipalities" element={<Municipalities />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          {/* Place the PlaceDetail route above MunicipalityDetail */}
          <Route
            path="/:continentSlug/:countrySlug/:regionSlug/:municipalitySlug/:placeSlug/"
            element={<PlaceDetail />}
          />

          {/* Route for Municipality Details */}
          <Route
            path="/:continentSlug/:countrySlug/:regionSlug/:municipalitySlug/"
            element={<MunicipalityDetail />}
          />
        </Routes>
      </main>
      <Footer />
    </div>
  );
};

export default App;
