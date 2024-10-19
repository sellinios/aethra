// src/components/Menu/Menu.tsx

import React from 'react';
import { Nav } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';
import LanguageSwitcher from '../components/LanguageSwitcher'; // Corrected import path
import './Menu.css'; // Additional styling for the menu

const Menu: React.FC = () => {
  return (
    <Nav className="menu-nav">
      {/* Language Switcher Positioned Before Menu Items */}
      <div className="language-switcher-container">
        <LanguageSwitcher />
      </div>

      <LinkContainer to="/home">
        <Nav.Link>Home</Nav.Link>
      </LinkContainer>
      <LinkContainer to="/about">
        <Nav.Link>About</Nav.Link>
      </LinkContainer>
      <LinkContainer to="/services">
        <Nav.Link>Services</Nav.Link>
      </LinkContainer>
      <LinkContainer to="/contact">
        <Nav.Link>Contact</Nav.Link>
      </LinkContainer>
    </Nav>
  );
};

export default Menu;
