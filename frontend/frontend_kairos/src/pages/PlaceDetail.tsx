// src/pages/PlaceDetail.tsx
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Table, Card, Spin, Alert } from 'antd';
import moment from 'moment';
import { LineChart, Line, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface WeatherDataEntry {
  datetime: string;
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
  const { continentSlug, countrySlug, regionSlug, municipalitySlug, placeSlug } = useParams<{
    continentSlug: string;
    countrySlug: string;
    regionSlug: string;
    municipalitySlug: string;
    placeSlug: string;
  }>();

  const [placeData, setPlaceData] = useState<PlaceData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    // Construct the API URL using the dynamic parameters
    const apiUrl = `/api/${countrySlug}/${regionSlug}/${municipalitySlug}/${placeSlug}/`;

    fetch(apiUrl)
      .then((response) => {
        if (!response.ok) {
          throw new Error('Failed to fetch place details');
        }
        return response.json();
      })
      .then((data) => {
        setPlaceData(data);
        setLoading(false);
      })
      .catch((error) => {
        setError(error.message);
        setLoading(false);
      });
  }, [countrySlug, regionSlug, municipalitySlug, placeSlug]);

  if (loading) {
    return <Spin tip="Loading..." />;
  }

  if (error) {
    return <Alert message="Error" description={error} type="error" showIcon />;
  }

  if (!placeData) {
    return null;
  }

  // Prepare weather data for display
  const parameterUnits: { [key: string]: string } = {
    temperature_celsius: '°C',
    relative_humidity_percent: '%',
    wind_speed_m_s: 'm/s',
    // Add more parameters and their units as needed
  };

  const weatherColumns = [
    {
      title: 'Date & Time',
      dataIndex: 'datetime',
      key: 'datetime',
      render: (text: string) => moment(text).format('YYYY-MM-DD HH:mm'),
    },
    ...Object.keys(placeData.weather_data[0] || {})
      .filter((key) => key !== 'datetime')
      .map((key) => ({
        title: `${key
          .replace(/_/g, ' ')
          .replace(/\b\w/g, (l) => l.toUpperCase())} ${
          parameterUnits[key] ? `(${parameterUnits[key]})` : ''
        }`,
        dataIndex: key,
        key: key,
        render: (value: any) => (value !== null ? value.toString() : 'N/A'),
      })),
  ];

  const temperatureData = placeData.weather_data.map((entry) => ({
    datetime: moment(entry.datetime).format('YYYY-MM-DD HH:mm'),
    temperature: entry.temperature_celsius,
  }));

  return (
    <div style={{ padding: '20px' }}>
      <Card title={placeData.name}>
        {placeData.description && <p>{placeData.description}</p>}
        <p>
          <strong>Location:</strong> {placeData.latitude}, {placeData.longitude}
        </p>
        <p>
          <strong>Elevation:</strong> {placeData.elevation} meters
        </p>
      </Card>

      {placeData.weather_data && placeData.weather_data.length > 0 ? (
        <>
          <Card title="Weather Forecast" style={{ marginTop: '20px' }}>
            <Table
              dataSource={placeData.weather_data}
              columns={weatherColumns}
              rowKey="datetime"
              pagination={false}
            />
          </Card>

          <Card title="Temperature Over Time" style={{ marginTop: '20px' }}>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={temperatureData}>
                <XAxis dataKey="datetime" />
                <YAxis domain={['auto', 'auto']} />
                <Tooltip />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="temperature"
                  name="Temperature (°C)"
                  stroke="#8884d8"
                />
              </LineChart>
            </ResponsiveContainer>
          </Card>
        </>
      ) : (
        <Alert message="No weather data available." type="info" showIcon style={{ marginTop: '20px' }} />
      )}
    </div>
  );
};

export default PlaceDetail;
