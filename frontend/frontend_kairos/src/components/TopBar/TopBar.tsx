import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { Container, Row, Col } from 'react-bootstrap';
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
  municipality_slug: string;  // Use this to show municipality
  place_slug: string;
}

const TopBar: React.FC = () => {
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
    <div className="top-bar">
      <Container fluid>
        <Row className="align-items-center">
          <Col md={12} className="text-center">
            {placeData && (
              <div className="nearest-place-info">
                {t('nearest_municipality')}: {' '}
                <Link
                  to={`/${placeData.continent_slug}/${placeData.country_slug}/${placeData.region_slug}/${placeData.municipality_slug}/`}
                  className="nearest-place-link"
                >
                  {placeData.municipality_slug} {/* Display municipality instead of place */}
                </Link>
              </div>
            )}
            {error && <div className="error">{error}</div>}
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default TopBar;
