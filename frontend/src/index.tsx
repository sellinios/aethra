// src/index.tsx
import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import { BrowserRouter } from 'react-router-dom';
import './i18n'; // Import the i18n configuration
import 'bootstrap/dist/css/bootstrap.min.css'; // Import Bootstrap CSS

ReactDOM.render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>,
  document.getElementById('root')
);
