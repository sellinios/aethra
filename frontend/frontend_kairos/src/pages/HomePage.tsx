import React, { useEffect, useState } from 'react';
import { Spin, Alert, Typography } from 'antd';
import WeatherPanel from '../components/Weather/WeatherPanel';

const { Title } = Typography;

interface City {
  name: string;
  apiUrl: string;
}

const cities: City[] = [
  { name: 'Athens', apiUrl: 'https://kairos.gr/en/api/weather/athens/' },
  // Add more cities as needed
];

const HomePage: React.FC = () => {
  const [weatherData, setWeatherData] = useState<{ [key: string]: any }>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCityWeather = async (city: City) => {
      try {
        const response = await fetch(city.apiUrl);
        if (!response.ok) {
          throw new Error(`Failed to fetch weather for ${city.name}`);
        }
        const data = await response.json();
        return { name: city.name, data: data.weather_data };
      } catch (error) {
        console.error(`Error fetching weather for ${city.name}:`, error);
        throw error;
      }
    };

    const fetchAllWeather = async () => {
      try {
        const results = await Promise.all(cities.map(fetchCityWeather));
        const cityWeatherData = results.reduce<{ [key: string]: any }>((acc, city) => {
          acc[city.name] = city.data;
          return acc;
        }, {});
        setWeatherData(cityWeatherData);
      } catch (error) {
        if (error instanceof Error) {
          setError(error.message);
        } else {
          setError('An unknown error occurred');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchAllWeather();
  }, []);

  if (loading) {
    return <Spin tip="Loading weather data..." />;
  }

  if (error) {
    return <Alert message="Error" description={error} type="error" showIcon />;
  }

  return (
    <div>
      <Title level={2}>City Weather Forecast</Title>
      <WeatherPanel weatherData={weatherData} />
    </div>
  );
};

export default HomePage;
