import React, { useEffect, useState } from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import { useTranslation } from 'react-i18next';
import { Helmet } from 'react-helmet';
import './Municipalities.css';

interface Municipality {
    id: number;
    name: string;  // We'll only use the 'name' field
}

const GreekMunicipalities: React.FC = () => {
    const { t } = useTranslation();
    const [municipalities, setMunicipalities] = useState<Municipality[]>([]);
    const [error, setError] = useState<string | null>(null);

    // Fetch the municipalities from the API
    useEffect(() => {
        const fetchMunicipalities = async () => {
            try {
                // Use the environment variable for the API base URL
                const apiUrl = `${process.env.REACT_APP_API_URL}api/municipalities/`;
                console.log('API URL:', apiUrl); // Log the API URL to verify it

                const response = await fetch(apiUrl);
                const data = await response.json();

                console.log('Fetched data:', data);  // Log the fetched data
                setMunicipalities(data);  // Assuming the response is an array of municipalities
            } catch (error) {
                setError(t('error_fetching_municipalities'));
                console.error('Error fetching municipalities:', error);
            }
        };

        fetchMunicipalities();
    }, [t]);  // Include 't' in the dependency array to ensure translations are up-to-date

    return (
        <Container>
            <Helmet>
                <title>{t('municipalities_of_greece')}</title>
            </Helmet>
            <h1>{t('municipalities_of_greece')}</h1>
            {error && <p className="error-message">{error}</p>}
            <Row>
                {municipalities.map(municipality => (
                    <Col key={municipality.id} sm={12} md={6} lg={4}>
                        <div className="municipality">
                            <h5>{municipality.name}</h5>  {/* Only display the name */}
                        </div>
                    </Col>
                ))}
            </Row>
        </Container>
    );
};

export default GreekMunicipalities;
