import React, { useEffect, useState } from 'react';
import axios from 'axios';
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

    const fetchMunicipalities = () => {
        const apiUrl = `${process.env.REACT_APP_BACKEND_URL}/api/municipalities/`; // Your actual API URL
        console.log(`Fetching municipalities from ${apiUrl}`);
        axios.get<Municipality[]>(apiUrl)
            .then(response => {
                setMunicipalities(response.data);
            })
            .catch(error => {
                setError(t('error_fetching_municipalities'));
                console.error('There was an error fetching the municipalities!', error);
                if (error.response) {
                    console.error('Error data:', error.response.data);
                    console.error('Error status:', error.response.status);
                    console.error('Error headers:', error.response.headers);
                }
            });
    };

    useEffect(() => {
        fetchMunicipalities();
    }, []);

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
