// src/components/Logo.tsx

import React from 'react';
import { LinkContainer } from 'react-router-bootstrap'; // Ensure react-router-bootstrap is installed
import './Logo.css';

const Logo: React.FC = () => {
  return (
    <LinkContainer to="/">
      <div className="logo-container">
        <div className="text-container">
          <div className="main-text">Kairos</div>
          <div className="sub-text">by Aethra</div>
        </div>
      </div>
    </LinkContainer>
  );
};

export default Logo;
