// src/pages/MunicipalityDetail.tsx

import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { Card, Spin, Alert, Typography } from 'antd';
import './MunicipalityDetail.css';

const { Title, Text } = Typography;

interface MunicipalityData {
  name: string;
  description: string | null;
  latitude: number;
  longitude: number;
  elevation: number;
  [key: string]: any;
}

const MunicipalityDetail: React.FC = () => {
  const { t } = useTranslation();
  const { continentSlug, countrySlug, regionSlug, municipalitySlug } = useParams<{
    continentSlug: string;
    countrySlug: string;
    regionSlug: string;
    municipalitySlug: string;
  }>();

  const [municipalityData, setMunicipalityData] = useState<MunicipalityData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const apiUrl = `/api/${countrySlug}/${regionSlug}/${municipalitySlug}/`; // Fetch municipality details

    fetch(apiUrl)
      .then((response) => {
        if (!response.ok) {
          throw new Error('Failed to fetch municipality details');
        }
        return response.json();
      })
      .then((data) => {
        setMunicipalityData(data);
        setLoading(false);
      })
      .catch((error) => {
        setError(error.message);
        setLoading(false);
      });
  }, [countrySlug, regionSlug, municipalitySlug]);

  if (loading) {
    return <Spin tip={t('loading')} />;
  }

  if (error) {
    return <Alert message={t('error')} description={error} type="error" showIcon />;
  }

  if (!municipalityData) {
    return null;
  }

  return (
    <div className="municipality-detail-container">
      <Card className="municipality-detail-card">
        <Title level={2}>{t('municipality_details')}: {municipalityData.name}</Title>
        {municipalityData.description && <Text>{municipalityData.description}</Text>}
        <br />
        <Text>
          <strong>{t('location')}:</strong> {municipalityData.latitude}, {municipalityData.longitude}
        </Text>
        <br />
        <Text>
          <strong>{t('elevation')}:</strong> {municipalityData.elevation} meters
        </Text>
      </Card>
    </div>
  );
};

export default MunicipalityDetail;