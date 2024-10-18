// src/pages/PlaceDetail.tsx

import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { Card, Spin, Alert, Table, Typography } from 'antd';
import moment from 'moment';
import WeatherIcon from '../components/Weather/WeatherIcon';
import CurrentConditions from '../components/Weather/CurrentConditions';
import './PlaceDetail.css';

const { Title, Text } = Typography;

interface WeatherDataEntry {
  datetime: string;
  temperature_celsius?: number;
  relative_humidity_percent?: number;
  wind_speed_m_s?: number;
  wind_direction?: string;
  wind_beaufort_scale?: number;
  total_precipitation_mm?: number;
  storm_probability_percent?: number;
  total_cloud_cover_percent?: number;
  pressure_hPa?: number;
  weather_condition?: string;
  [key: string]: any;
}

interface PlaceData {
  name: string;
  description: string | null;
  latitude: number;
  longitude: number;
  elevation: number;
  weather_data: WeatherDataEntry[];
}

const PlaceDetail: React.FC = () => {
  const { t, i18n } = useTranslation();
  const { placeSlug } = useParams<{ placeSlug: string }>();

  const [placeData, setPlaceData] = useState<PlaceData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchPlaceData = async () => {
      const apiUrl = `${process.env.REACT_APP_API_URL}/api/${i18n.language}/place/${placeSlug}/`;
      console.log('Fetching place data from:', apiUrl);

      try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
          const errorMessage = await response.text();
          throw new Error(
            `Failed to fetch place details: ${response.status} ${response.statusText} - ${errorMessage}`
          );
        }
        const data: PlaceData = await response.json();
        setPlaceData(data);
      } catch (error: any) {
        console.error('Error fetching place details:', error);
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };
    fetchPlaceData();
  }, [placeSlug, i18n.language]);

  if (loading) {
    return <Spin tip={t('loading')} />;
  }

  if (error) {
    return <Alert message={t('error')} description={error} type="error" showIcon />;
  }

  if (!placeData) {
    return null;
  }

  // ... Rest of your component code remains the same ...

  return (
    <div className="place-detail-container">
      {/* ... Existing JSX code ... */}
    </div>
  );
};

export default PlaceDetail;
