// src/pages/Municipalities.tsx
import React, { useEffect, useState } from 'react';
import { Container, Row, Col, Spinner } from 'react-bootstrap';
import { useTranslation } from 'react-i18next';
import { Helmet } from 'react-helmet';
import './Municipalities.css';

interface Municipality {
  id: number;
  name: string;
}

const Municipalities: React.FC = () => {
  const { t, i18n } = useTranslation();
  const [municipalities, setMunicipalities] = useState<Municipality[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchMunicipalities = async () => {
      try {
        // Correct API URL with language prefix before 'api/'
        const apiUrl = `${process.env.REACT_APP_API_URL}/${i18n.language}/api/municipalities/`;
        console.log('API URL:', apiUrl); // Log the API URL for debugging

        const response = await fetch(apiUrl, {
          headers: {
            'Accept-Language': i18n.language, // Set the Accept-Language header to the current language
          },
        });

        if (!response.ok) {
          const errorMessage = await response.text();
          throw new Error(`HTTP error! Status: ${response.status} - ${errorMessage}`);
        }

        const data = await response.json();
        console.log('Fetched data:', data); // Log the fetched data for debugging
        setMunicipalities(data);
      } catch (error: any) {
        console.error('Error fetching municipalities:', error);
        setError(t('error_fetching_municipalities'));
      } finally {
        setLoading(false);
      }
    };

    fetchMunicipalities();
  }, [i18n.language, t]); // Refetch data when the language changes

  return (
    <Container>
      <Helmet>
        <title>{t('municipalities_of_greece')}</title>
      </Helmet>
      <h1>{t('municipalities_of_greece')}</h1>
      {loading && <Spinner animation="border" />}
      {error && <p className="error-message">{error}</p>}
      {municipalities.length === 0 && !loading && <p>{t('no_municipalities_found')}</p>}
      <Row>
        {municipalities.map((municipality) => (
          <Col key={municipality.id} sm={12} md={6} lg={4}>
            <div className="municipality">
              <h5>{municipality.name}</h5>
            </div>
          </Col>
        ))}
      </Row>
    </Container>
  );
};

export default Municipalities;