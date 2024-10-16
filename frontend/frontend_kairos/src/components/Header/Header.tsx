import React, { useEffect, useState } from 'react';
import { Navbar, Container, Nav, NavDropdown, NavbarText } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import LanguageSwitcher from '../LanguageSwitcher';
import Logo from '../Logo';
import './Header.css'; // Optional: Additional styling for header

interface PlaceData {
  name: string;
  description: string | null;
  latitude: number;
  longitude: number;
  elevation: number;
  continent_slug: string;
  country_slug: string;
  region_slug: string;
  municipality_slug: string;
  place_slug: string;
}

const Header: React.FC = () => {
  const { t } = useTranslation();
  const [placeData, setPlaceData] = useState<PlaceData | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if ('geolocation' in navigator) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude } = position.coords;
          fetch(`/api/place/?latitude=${latitude}&longitude=${longitude}`)
            .then((response) => {
              if (!response.ok) {
                throw new Error('Network response was not ok');
              }
              return response.json();
            })
            .then((data) => {
              setPlaceData(data);
            })
            .catch((error) => {
              setError(error.toString());
            });
        },
        (error) => {
          setError(t('error_geolocation') + ': ' + error.message);
        }
      );
    } else {
      setError(t('geolocation_not_available'));
    }
  }, [t]);

  return (
    <header className="header">
      <Navbar expand="lg" className="navbar-dark bg-dark" sticky="top">
        <Container>
          {/* Logo as a clickable home link */}
          <LinkContainer to="/">
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

            {/* Display the nearest place */}
            {placeData && (
              <Navbar.Text className="nearest-place-info">
                {t('nearest_place')}:{' '}
                <Link
                  to={`/${placeData.continent_slug}/${placeData.country_slug}/${placeData.region_slug}/${placeData.municipality_slug}/${placeData.place_slug}/`}
                >
                  {placeData.name}
                </Link>
              </Navbar.Text>
            )}
            {error && (
              <Navbar.Text className="error">
                {error}
              </Navbar.Text>
            )}
          </Navbar.Collapse>
        </Container>
      </Navbar>
    </header>
  );
};

export default Header;
