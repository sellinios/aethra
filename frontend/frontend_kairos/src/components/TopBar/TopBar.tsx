// src/components/TopBar/TopBar.tsx

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { Container, Row, Col, Alert, Button, Spinner } from 'react-bootstrap';
import { FaMapMarkerAlt } from 'react-icons/fa'; // Optional: Importing an icon
import './TopBar.css';

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
  municipality_name: string;
  place_slug: string;
}

const TopBar: React.FC = () => {
  const { t, i18n } = useTranslation();
  const [placeData, setPlaceData] = useState<PlaceData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Retrieve stored location data from localStorage
    const storedLocation = localStorage.getItem('placeData');
    if (storedLocation) {
      setPlaceData(JSON.parse(storedLocation));
    }
  }, []);

  const handleLocationRequest = () => {
    setLoading(true);
    setError(null);

    if ('geolocation' in navigator) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude } = position.coords;

          const apiUrl = `${process.env.REACT_APP_API_URL}/${i18n.language}/api/place/?latitude=${latitude}&longitude=${longitude}`;

          fetch(apiUrl, {
            headers: {
              'Accept-Language': i18n.language,
            },
          })
            .then((response) => {
              if (!response.ok) {
                throw new Error('Network response was not ok');
              }
              return response.json();
            })
            .then((data) => {
              // Save fetched data to localStorage
              localStorage.setItem('placeData', JSON.stringify(data));
              setPlaceData(data);
              setLoading(false);
            })
            .catch(() => {
              setError(t('error_fetching_place_data'));
              setLoading(false);
            });
        },
        (geoError) => {
          setError(`${t('error_geolocation')}: ${geoError.message}`);
          setLoading(false);
        }
      );
    } else {
      setError(t('geolocation_not_available'));
      setLoading(false);
    }
  };

  return (
    <div className="top-bar">
      <Container fluid className="px-0">
        <Row className="justify-content-center">
          <Col md={12} className="text-center">
            {loading ? (
              <Alert variant="secondary" className="loading-alert mb-0 rounded-0">
                <Spinner
                  as="span"
                  animation="border"
                  size="sm"
                  role="status"
                  aria-hidden="true"
                  className="me-2"
                />
                {t('loading')}...
              </Alert>
            ) : error ? (
              <Alert variant="danger" className="top-bar-alert mb-0 rounded-0">
                {error}
              </Alert>
            ) : placeData ? (
              <Alert variant="info" className="top-bar-alert mb-0 rounded-0">
                {t('nearest_place')}: {' '}
                <Link
                  to={`/${placeData.continent_slug}/${placeData.country_slug}/${placeData.region_slug}/${placeData.municipality_slug}/${placeData.place_slug}/`}
                  className="nearest-place-link"
                >
                  {placeData.name}
                </Link>
              </Alert>
            ) : (
              <div>
                <Button onClick={handleLocationRequest} variant="primary" className="find-nearest-btn">
                  {/* Optional: Add an icon */}
                  <FaMapMarkerAlt className="me-2" />
                  {t('find_nearest_place')}
                </Button>
              </div>
            )}
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default TopBar;
