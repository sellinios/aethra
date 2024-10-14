// src/components/Footer/Footer.tsx
import React from 'react';
import './Footer.css';  // Import any custom styling if necessary

const Footer: React.FC = () => {
  return (
    <footer className="footer bg-dark text-light py-3">
      <div className="container">
        <div className="row">
          <div className="col-md-6">
            <p>&copy; 2024 Your Website. All Rights Reserved.</p>
          </div>
          <div className="col-md-6 text-md-end">
            <ul className="list-unstyled d-inline-flex">
              <li className="ms-3">
                <a href="/about" className="text-decoration-none text-light">About Us</a>
              </li>
              <li className="ms-3">
                <a href="/contact" className="text-decoration-none text-light">Contact</a>
              </li>
              <li className="ms-3">
                <a href="/privacy" className="text-decoration-none text-light">Privacy Policy</a>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
