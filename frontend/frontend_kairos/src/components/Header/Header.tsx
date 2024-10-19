// src/components/Header/Header.tsx

import React from 'react';
import { Navbar, Container } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';
import Logo from '../Logo';
import Menu from '../Menu'; // Ensure Menu is properly imported
import './Header.css'; // Additional styling for the header

const Header: React.FC = () => {
  return (
    <header className="header">
      <Navbar expand="lg" bg="dark" variant="dark" className="navbar-custom">
        <Container fluid className="d-flex align-items-center justify-content-between">
          {/* Logo positioned on the left */}
          <LinkContainer to="/">
            <Navbar.Brand className="d-flex align-items-center">
              <Logo />
            </Navbar.Brand>
          </LinkContainer>

          {/* Toggle Button for Mobile View */}
          <Navbar.Toggle aria-controls="basic-navbar-nav" />

          {/* Menu Component positioned on the right */}
          <Navbar.Collapse id="basic-navbar-nav">
            <div className="menu-container d-flex align-items-center">
              <Menu />
            </div>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </header>
  );
};

export default Header;
