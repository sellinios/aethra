import React, { useEffect, useState } from 'react';
import { Spin, Alert, Typography, Table, Input, Button, Space, Popconfirm } from 'antd';
import { Helmet } from 'react-helmet-async';
import './HomePage.css';
import { useTranslation } from 'react-i18next';
import { PlusOutlined, DeleteOutlined } from '@ant-design/icons';
import { Container, Row, Col } from 'react-bootstrap'; // If using Bootstrap

import LatestArticles from '../components/LatestArticles'; // Import the LatestArticles component

const { Title } = Typography;

// Define the Breakpoint type locally
type Breakpoint = 'xs' | 'sm' | 'md' | 'lg' | 'xl' | 'xxl';

interface DailyWeather {
  date: string;
  maxTemp: number;
  minTemp: number;
  avgCloudCover: number;
  maxPrecipitation: number;
  windSpeedAvg: number;
}

interface CityWeather {
  name: string;
  weather: DailyWeather[];
}

const HomePage: React.FC = () => {
  const { t, i18n } = useTranslation();
  const [weatherData, setWeatherData] = useState<{ [key: string]: CityWeather }>({});
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [locations, setLocations] = useState<string[]>([]);
  const [newLocation, setNewLocation] = useState<string>('');

  // Load locations from localStorage on component mount
  useEffect(() => {
    const storedLocations = localStorage.getItem('myLocations');
    if (storedLocations) {
      setLocations(JSON.parse(storedLocations));
    } else {
      // Initialize with a default location, e.g., Athens
      setLocations(['Athens']);
    }
  }, []);

  // Save locations to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem('myLocations', JSON.stringify(locations));
  }, [locations]);

  // Fetch weather data whenever locations or language changes
  useEffect(() => {
    const fetchWeatherData = async () => {
      setLoading(true);
      setError(null);
      try {
        const cityWeatherData: { [key: string]: CityWeather } = {};

        // Create an array of fetch promises for all locations
        const fetchPromises = locations.map(async (city) => {
          const apiUrl = `${process.env.REACT_APP_API_URL}/${i18n.language}/api/weather/daily/${city.toLowerCase()}/`;

          const response = await fetch(apiUrl);
          console.log(`Fetching data from: ${apiUrl}`);

          if (!response.ok) {
            throw new Error(`Failed to fetch data for ${city}. Status: ${response.status}`);
          }

          const data = await response.json();
          console.log(`API response for ${city}:`, data);

          if (!data.daily_weather_data) {
            throw new Error(`Unexpected data format for ${city}`);
          }

          // Sort the data to ensure it starts from the current day
          const sortedWeatherData = data.daily_weather_data.sort(
            (a: any, b: any) => new Date(a.date).getTime() - new Date(b.date).getTime()
          );

          console.log(`Sorted weather data for ${city}:`, sortedWeatherData);

          cityWeatherData[city] = {
            name: data.place_name,
            weather: sortedWeatherData.slice(0, 4).map((day: any) => ({
              date: day.date,
              maxTemp: Math.round(day.max_temp),
              minTemp: Math.round(day.min_temp),
              avgCloudCover: day.avg_cloud_cover,
              maxPrecipitation: day.max_precipitation,
              windSpeedAvg: day.wind_speed_avg,
            })),
          };
        });

        // Await all fetch promises
        await Promise.all(fetchPromises);

        console.log(`Processed weather data for all locations:`, cityWeatherData);

        setWeatherData(cityWeatherData);
      } catch (err: any) {
        console.error('Error fetching data:', err);
        setError(err.message || 'Unknown error occurred');
      } finally {
        setLoading(false);
      }
    };

    if (locations.length > 0) {
      fetchWeatherData();
    } else {
      setWeatherData({});
      setLoading(false);
    }
  }, [locations, i18n.language]);

  // Handler to add a new location
  const handleAddLocation = () => {
    const trimmedLocation = newLocation.trim();
    if (trimmedLocation && !locations.includes(trimmedLocation)) {
      setLocations([...locations, trimmedLocation]);
      setNewLocation('');
    }
  };

  // Handler to remove a location
  const handleRemoveLocation = (city: string) => {
    setLocations(locations.filter((location) => location !== city));
  };

  if (loading) {
    return (
      <Container className="weather-container">
        <Row className="justify-content-center">
          <Spin tip={t('loading')} />
        </Row>
      </Container>
    );
  }

  if (error) {
    return (
      <Container className="weather-container">
        <Row className="justify-content-center">
          <Alert message={t('error')} description={error} type="error" showIcon />
        </Row>
      </Container>
    );
  }

  if (locations.length === 0) {
    return (
      <Container className="weather-container">
        <Row className="justify-content-center">
          <Alert message={t('noLocations')} type="info" showIcon />
        </Row>
      </Container>
    );
  }

  // Prepare day names based on the first available city's weather data
  const firstCityKey = Object.keys(weatherData)[0];
  let dayNames: string[] = [];

  if (firstCityKey && weatherData[firstCityKey].weather.length) {
    const firstCityWeather = weatherData[firstCityKey].weather;
    dayNames = firstCityWeather.map((day) => {
      const date = new Date(`${day.date}T00:00:00Z`);
      console.log(`Processing date: ${day.date} -> Parsed Date: ${date}`);
      const dayIndex = date.getDay();
      const dayNameKey = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'][dayIndex];
      const dayName = t(dayNameKey);
      console.log(`Day Index: ${dayIndex}, Day Name Key: ${dayNameKey}, Day Name: ${dayName}`);
      return dayName;
    });
  }

  // Dynamically generate columns based on day names
  const columns = [
    {
      title: t('city'),
      dataIndex: 'city',
      key: 'city',
      fixed: 'left' as const,
      width: 150,
      render: (text: string, record: any) => (
        <Space>
          {text}
          <Popconfirm
            title={t('removeLocationConfirm', { city: text })}
            onConfirm={() => handleRemoveLocation(text)}
            okText={t('yes')}
            cancelText={t('no')}
          >
            <Button type="link" icon={<DeleteOutlined />} danger />
          </Popconfirm>
        </Space>
      ),
    },
    ...dayNames.map((dayName, index) => ({
      title: dayName,
      dataIndex: `day${index}`,
      key: `day${index}`,
      width: 120,
      responsive: ['sm'] as Breakpoint[], // Use the locally defined Breakpoint type
    })),
  ];

  // Generate dataSource dynamically
  const dataSource = locations.map((cityName) => {
    const cityWeather = weatherData[cityName]?.weather || [];

    const weatherDays = cityWeather.slice(0, dayNames.length);

    const dayEntries: { [key: string]: string } = {};
    weatherDays.forEach((day, index) => {
      dayEntries[`day${index}`] = `${day.maxTemp}°C / ${day.minTemp}°C`;
    });

    return {
      key: cityName,
      city: cityName,
      ...dayEntries,
    };
  });

  console.log(`Generated columns:`, columns);
  console.log(`Generated dataSource:`, dataSource);

  return (
    <>
      <Container className="weather-container">
        <Helmet>
          <title>{t('weatherForecastTitle')}</title>
          <meta name="description" content={t('weatherForecastDescription')} />
        </Helmet>
        <Row className="justify-content-center">
          <Col xs={12}>
            <Title level={2} className="weather-title">
              {t('myLocations')}
            </Title>
          </Col>
        </Row>

        {/* Add Location Input */}
        <Row className="justify-content-center mb-3">
          <Col xs={12} md={8} lg={6}>
            <Space>
              <Input
                placeholder={t('addLocationPlaceholder')}
                value={newLocation}
                onChange={(e) => setNewLocation(e.target.value)}
                onPressEnter={handleAddLocation}
                className="w-100"
              />
              <Button type="primary" onClick={handleAddLocation} icon={<PlusOutlined />}>
                {t('add')}
              </Button>
            </Space>
          </Col>
        </Row>

        {/* Weather Table */}
        <Row>
          <Col>
            <Table
              dataSource={dataSource}
              columns={columns}
              pagination={false}
              className="weather-table"
              scroll={{ x: 'max-content' }}
              rowClassName={(record) => (record.city.toLowerCase() === 'athens' ? 'athens-row' : '')} // Assign 'athens-row' class to Athens
              bordered
              size="middle"
            />
          </Col>
        </Row>
      </Container>

      {/* Separate container for Latest Articles */}
      <Container className="articles-container mt-5">
        <LatestArticles /> {/* Importing the articles component cleanly */}
      </Container>
    </>
  );
};

export default HomePage;
