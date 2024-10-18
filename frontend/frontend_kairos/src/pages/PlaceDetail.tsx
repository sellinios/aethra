// src/pages/PlaceDetail.tsx

import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { Spin, Alert, Typography } from 'antd';
import DailyWeatherPanel from '../components/Weather/DailyWeatherPanel';
import './PlaceDetail.css';

const { Title } = Typography;

interface WeatherDataEntry {
  datetime: string;
  night?: string;
  morning?: string;
  afternoon?: string;
  evening?: string;
  temperature_high?: number;
  temperature_low?: number;
  precipitation?: number;
  wind_speed?: number;
  wind_direction?: string;
}

interface WeatherData {
  place_name: string;
  weather_data: WeatherDataEntry[];
}

interface PlaceData {
  name: string;
  description: string | null;
  latitude: number;
  longitude: number;
  elevation: number;
  municipality_name: string;
}

const PlaceDetail: React.FC = () => {
  const { t, i18n } = useTranslation();
  const { placeSlug } = useParams<{ placeSlug: string }>();

  const [placeData, setPlaceData] = useState<PlaceData | null>(null);
  const [weatherData, setWeatherData] = useState<WeatherData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchPlaceAndWeatherData = async () => {
      const language = i18n.language;
      const placeApiUrl = `${process.env.REACT_APP_API_URL}/${language}/api/place/attica/municipality-of-vyronas/${placeSlug}/`;
      const weatherApiUrl = `${process.env.REACT_APP_API_URL}/${language}/api/weather/${placeSlug}/`;

      try {
        const [placeResponse, weatherResponse] = await Promise.all([
          fetch(placeApiUrl),
          fetch(weatherApiUrl),
        ]);

        if (!placeResponse.ok) {
          const errorMessage = await placeResponse.text();
          throw new Error(`Failed to fetch place details: ${placeResponse.status} ${placeResponse.statusText} - ${errorMessage}`);
        }

        if (!weatherResponse.ok) {
          const errorMessage = await weatherResponse.text();
          throw new Error(`Failed to fetch weather details: ${weatherResponse.status} ${weatherResponse.statusText} - ${errorMessage}`);
        }

        const placeData: PlaceData = await placeResponse.json();
        const weatherData: WeatherData = await weatherResponse.json();

        setPlaceData(placeData);
        setWeatherData(weatherData);
      } catch (error: any) {
        console.error('Error fetching data:', error);
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };

    fetchPlaceAndWeatherData();
  }, [placeSlug, i18n.language]);

  if (loading) {
    return <Spin tip={t('loading')} />;
  }

  if (error) {
    return <Alert message={t('error')} description={error} type="error" showIcon />;
  }

  if (!placeData || !weatherData) {
    return null;
  }

  return (
    <div className="place-detail-container">
      <Title level={2}>{placeData.name}</Title>
      <p>{placeData.description ? placeData.description : t('no_description')}</p>
      <p>{t('location')}: {placeData.latitude}, {placeData.longitude}</p>
      <p>{t('elevation')}: {placeData.elevation} m</p>
      <p>{t('municipality')}: {placeData.municipality_name}</p>

      {/* Render daily weather panel */}
      <DailyWeatherPanel data={weatherData.weather_data} />
    </div>
  );
};

export default PlaceDetail;
