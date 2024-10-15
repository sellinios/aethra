import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Table, Card, Spin, Alert } from 'antd';
import moment from 'moment';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import './PlaceDetail.css'; // Import the CSS file

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
  const {
    continentSlug,
    countrySlug,
    regionSlug,
    municipalitySlug,
    placeSlug,
  } = useParams<{
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
    return (
      <Alert message="Error" description={error} type="error" showIcon />
    );
  }

  if (!placeData) {
    return null;
  }

  const parameterUnits: { [key: string]: string } = {
    temperature_celsius: '°C',
    relative_humidity_percent: '%',
    wind_speed_m_s: 'm/s',
    wind_direction: '',
    wind_beaufort_scale: '',
    total_precipitation_mm: 'mm',
    pressure_hPa: 'hPa',
    storm_probability_percent: '%',
    total_cloud_cover_percent: '%',
  };

  const parameterNames: { [key: string]: string } = {
    temperature_celsius: 'Temperature',
    relative_humidity_percent: 'Humidity',
    wind_speed_m_s: 'Wind Speed',
    wind_direction: 'Wind Direction',
    wind_beaufort_scale: 'Wind (Beaufort)',
    total_precipitation_mm: 'Precipitation',
    pressure_hPa: 'Pressure',
    storm_probability_percent: 'Storm Probability',
    total_cloud_cover_percent: 'Cloud Cover',
  };

  const weatherColumns = [
    {
      title: 'Date & Time',
      dataIndex: 'datetime',
      key: 'datetime',
      render: (text: string) => moment(text).format('YYYY-MM-DD HH:mm'),
    },
    {
      title: `${parameterNames.temperature_celsius} (${parameterUnits.temperature_celsius})`,
      dataIndex: 'temperature_celsius',
      key: 'temperature_celsius',
      render: (value: number) =>
        value !== null && value !== undefined ? `${value}°C` : 'N/A',
    },
    {
      title: `${parameterNames.relative_humidity_percent} (${parameterUnits.relative_humidity_percent})`,
      dataIndex: 'relative_humidity_percent',
      key: 'relative_humidity_percent',
      render: (value: number) =>
        value !== null && value !== undefined ? `${value}%` : 'N/A',
    },
    {
      title: `${parameterNames.wind_speed_m_s} (${parameterUnits.wind_speed_m_s})`,
      dataIndex: 'wind_speed_m_s',
      key: 'wind_speed_m_s',
      render: (value: number) =>
        value !== null && value !== undefined ? `${value} m/s` : 'N/A',
    },
    {
      title: `${parameterNames.wind_direction}`,
      dataIndex: 'wind_direction',
      key: 'wind_direction',
      render: (value: string) => (value ? value : 'N/A'),
    },
    {
      title: `${parameterNames.wind_beaufort_scale}`,
      dataIndex: 'wind_beaufort_scale',
      key: 'wind_beaufort_scale',
      render: (value: number) =>
        value !== null && value !== undefined ? `F${value}` : 'N/A',
    },
    {
      title: `${parameterNames.total_precipitation_mm} (${parameterUnits.total_precipitation_mm})`,
      dataIndex: 'total_precipitation_mm',
      key: 'total_precipitation_mm',
      render: (value: number) =>
        value !== null && value !== undefined ? `${value} mm` : 'N/A',
    },
    {
      title: `${parameterNames.storm_probability_percent} (${parameterUnits.storm_probability_percent})`,
      dataIndex: 'storm_probability_percent',
      key: 'storm_probability_percent',
      render: (value: number) =>
        value !== null && value !== undefined ? `${value}%` : 'N/A',
    },
    {
      title: `${parameterNames.total_cloud_cover_percent} (${parameterUnits.total_cloud_cover_percent})`,
      dataIndex: 'total_cloud_cover_percent',
      key: 'total_cloud_cover_percent',
      render: (value: number) =>
        value !== null && value !== undefined ? `${value}%` : 'N/A',
    },
    {
      title: `${parameterNames.pressure_hPa} (${parameterUnits.pressure_hPa})`,
      dataIndex: 'pressure_hPa',
      key: 'pressure_hPa',
      render: (value: number) =>
        value !== null && value !== undefined ? `${value} hPa` : 'N/A',
    },
    // Add more columns as needed
  ];

  const temperatureData = placeData.weather_data.map((entry) => ({
    datetime: moment(entry.datetime).format('YYYY-MM-DD HH:mm'),
    temperature: entry.temperature_celsius,
  }));

  return (
    <div className="place-detail-container">
      <Card title={placeData.name} className="place-detail-card">
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
          <Card title="Weather Forecast" className="weather-forecast-card">
            <Table
              dataSource={placeData.weather_data}
              columns={weatherColumns}
              rowKey="datetime"
              pagination={false}
              scroll={{ x: true }}
            />
          </Card>

          <Card title="Temperature Over Time" className="temperature-chart-card">
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
        <Alert
          message="No weather data available."
          type="info"
          showIcon
          className="alert-info"
        />
      )}
    </div>
  );
};

export default PlaceDetail;
