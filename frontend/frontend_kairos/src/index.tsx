// src/index.tsx

import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import { BrowserRouter } from 'react-router-dom'; // Import BrowserRouter
import { HelmetProvider } from 'react-helmet-async'; // Import HelmetProvider
import './i18n'; // Import i18n configuration
import 'bootstrap/dist/css/bootstrap.min.css'; // Import Bootstrap CSS

ReactDOM.render(
  <React.StrictMode>
    <HelmetProvider>
      <BrowserRouter> {/* Single Router instance */}
        <App />
      </BrowserRouter>
    </HelmetProvider>
  </React.StrictMode>,
  document.getElementById('root')
);
