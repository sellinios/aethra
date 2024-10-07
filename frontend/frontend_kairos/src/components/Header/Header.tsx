// src/components/Header/Header.tsx
import React from 'react';
import { Navbar, Container, Nav, NavDropdown } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';
import { useTranslation } from 'react-i18next';
import LanguageSwitcher from '../LanguageSwitcher';
import Logo from '../Logo';
import './Header.css';

const Header: React.FC = () => {
  const { t } = useTranslation();

  return (
    <header className="header">
      <Navbar expand="lg" className="navbar-dark bg-dark" sticky="top">
        <Container>
          {/* Wrap Navbar.Brand with LinkContainer to make it a navigational link */}
          <LinkContainer to="/">
            <Navbar.Brand className="navbar-brand">
              <Logo />
            </Navbar.Brand>
          </LinkContainer>

          <Navbar.Toggle aria-controls="navbar-nav" />
          <Navbar.Collapse id="navbar-nav">
            <Nav className="ms-auto">
              {/* Wrap each Nav.Link with LinkContainer */}
              <LinkContainer to="/">
                <Nav.Link>{t('home')}</Nav.Link>
              </LinkContainer>
              <LinkContainer to="/about">
                <Nav.Link>{t('about')}</Nav.Link>
              </LinkContainer>
              <LinkContainer to="/contact">
                <Nav.Link>{t('contact')}</Nav.Link>
              </LinkContainer>
              <NavDropdown title={t('geography')} id="geography-dropdown">
                <LinkContainer to="/geography/greece/municipalities">
                  <NavDropdown.Item>{t('municipalities')}</NavDropdown.Item>
                </LinkContainer>
                {/* Add more dropdown items as needed */}
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
