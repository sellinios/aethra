import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Header from './components/Header/Header';
import HomePage from './pages/HomePage';
import AboutPage from './pages/AboutPage';
import ContactPage from './pages/ContactPage';
import Municipalities from './pages/Municipalities';  // Corrected from GreekMunicipalities
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import './App.css';  // Make sure you're importing global styles
import 'bootstrap/dist/css/bootstrap.min.css';  // Bootstrap

const App: React.FC = () => {
  return (
    <>
      <Header /> {/* Header stays consistent on every page */}
      <main className="content"> {/* Main content container */}
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/contact" element={<ContactPage />} />
          <Route path="/geography/greece/municipalities" element={<Municipalities />} /> {/* Corrected route */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          {/* Add more routes as needed */}
        </Routes>
      </main>
      <footer className="footer"> {/* Optional footer if needed */}
        <p>&copy; 2024 Your Website. All Rights Reserved.</p>
      </footer>
    </>
  );
};

export default App;
