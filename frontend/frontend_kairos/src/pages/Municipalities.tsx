import React, { useEffect, useState } from 'react';
import { Container, Row, Col, Spinner } from 'react-bootstrap';
import { useTranslation } from 'react-i18next';
import { Helmet } from 'react-helmet';
import './Municipalities.css';

interface Municipality {
    id: number;
    name: string;
}

const GreekMunicipalities: React.FC = () => {
    const { t } = useTranslation();
    const [municipalities, setMunicipalities] = useState<Municipality[]>([]);
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState<boolean>(true);

    useEffect(() => {
        const fetchMunicipalities = async () => {
            try {
                const apiUrl = `${process.env.REACT_APP_API_URL}api/municipalities/`;
                console.log('API URL:', apiUrl);

                const response = await fetch(apiUrl);
                if (!response.ok) {
                    const errorMessage = await response.text();
                    throw new Error(`HTTP error! Status: ${response.status} - ${errorMessage}`);
                }

                const data = await response.json();
                console.log('Fetched data:', data); // Log the fetched data
                setMunicipalities(data);
            } catch (error) {
                console.error('Error fetching municipalities:', error);
                setError(t('error_fetching_municipalities'));
            } finally {
                setLoading(false);
            }
        };

        fetchMunicipalities();
    }, [t]);

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
                {municipalities.map(municipality => (
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

export default GreekMunicipalities;
