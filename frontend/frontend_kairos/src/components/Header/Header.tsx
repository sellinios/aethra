import React from 'react';
import { Navbar, Container, Nav, NavDropdown } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import LanguageSwitcher from '../LanguageSwitcher';
import Logo from '../Logo';
import './Header.css'; // Optional: Additional styling for header

const Header: React.FC = () => {
  const { t } = useTranslation();

  return (
    <header className="header">
      <Navbar expand="lg" className="navbar-dark bg-dark" sticky="top">
        <Container fluid>
          {/* Logo aligned to the left */}
          <LinkContainer to="/" className="me-auto">
            <Navbar.Brand>
              <Logo />
            </Navbar.Brand>
          </LinkContainer>

          {/* Navbar toggle for smaller screens */}
          <Navbar.Toggle aria-controls="navbar-nav" />

          {/* Navbar collapse for toggling menu items */}
          <Navbar.Collapse id="navbar-nav">
            <Nav className="ms-auto">
              {/* Navigation Links */}
              <LinkContainer to="/">
                <Nav.Link>{t('home')}</Nav.Link>
              </LinkContainer>

              <LinkContainer to="/about">
                <Nav.Link>{t('about')}</Nav.Link>
              </LinkContainer>

              <LinkContainer to="/contact">
                <Nav.Link>{t('contact')}</Nav.Link>
              </LinkContainer>

              {/* Geography Dropdown Menu */}
              <NavDropdown title={t('geography')} id="geography-dropdown">
                <LinkContainer to="/geography/greece/municipalities">
                  <NavDropdown.Item>{t('municipalities')}</NavDropdown.Item>
                </LinkContainer>
              </NavDropdown>

              <LinkContainer to="/login">
                <Nav.Link>{t('login')}</Nav.Link>
              </LinkContainer>

              <LinkContainer to="/register">
                <Nav.Link>{t('register')}</Nav.Link>
              </LinkContainer>

              {/* Language Switcher */}
              <Nav.Item>
                <LanguageSwitcher />
              </Nav.Item>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </header>
  );
};

export default Header;
