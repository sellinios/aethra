import React, { useEffect, useState } from 'react';
import { Spin, Alert, Typography, Table } from 'antd';
import './HomePage.css'; // Import the custom CSS

const { Title } = Typography;

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
  const [weatherData, setWeatherData] = useState<{ [key: string]: CityWeather }>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchWeatherData = async () => {
      try {
        const cityWeatherData: { [key: string]: CityWeather } = {};
        const apiUrl = `${process.env.REACT_APP_API_URL}/en/api/weather/daily/athens/`; // API for Athens

        const response = await fetch(apiUrl);
        console.log(`Fetching data from: ${apiUrl}`);

        if (!response.ok) {
          throw new Error(`Failed to fetch data for Athens. Status: ${response.status}`);
        }

        const data = await response.json();
        console.log(`API response for Athens:`, data);

        if (!data.daily_weather_data) {
          throw new Error(`Unexpected data format for Athens`);
        }

        cityWeatherData['Athens'] = {
          name: data.place_name,
          weather: data.daily_weather_data.slice(0, 4).map((day: any) => ({
            date: day.date,
            maxTemp: Math.round(day.max_temp),  // Round temperature
            minTemp: Math.round(day.min_temp),  // Round temperature
            avgCloudCover: day.avg_cloud_cover,
            maxPrecipitation: day.max_precipitation,
            windSpeedAvg: day.wind_speed_avg,
          })),
        };

        setWeatherData(cityWeatherData);
      } catch (err: any) {
        console.error('Error fetching data:', err);
        setError(err.message || 'Unknown error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchWeatherData();
  }, []); // Fetch data only once

  if (loading) {
    return <Spin tip="Loading weather data..." />;
  }

  if (error) {
    return <Alert message="Error" description={error} type="error" showIcon />;
  }

  const columns = [
    {
      title: 'City',
      dataIndex: 'city',
      key: 'city',
    },
    {
      title: 'Saturday',
      dataIndex: 'saturday',
      key: 'saturday',
    },
    {
      title: 'Sunday',
      dataIndex: 'sunday',
      key: 'sunday',
    },
    {
      title: 'Monday',
      dataIndex: 'monday',
      key: 'monday',
    },
    {
      title: 'Tuesday',
      dataIndex: 'tuesday',
      key: 'tuesday',
    },
  ];

  const dataSource = Object.keys(weatherData).map((cityName) => {
    const cityWeather = weatherData[cityName].weather;

    return {
      key: cityName,
      city: weatherData[cityName].name,
      saturday: `${cityWeather[0].maxTemp}°C / ${cityWeather[0].minTemp}°C`,
      sunday: `${cityWeather[1].maxTemp}°C / ${cityWeather[1].minTemp}°C`,
      monday: `${cityWeather[2].maxTemp}°C / ${cityWeather[2].minTemp}°C`,
      tuesday: `${cityWeather[3].maxTemp}°C / ${cityWeather[3].minTemp}°C`,
    };
  });

  return (
    <div className="weather-container">
      <Title level={2} className="weather-title">City Weather Forecast (4 days)</Title>
      <Table
        dataSource={dataSource}
        columns={columns}
        pagination={false}
        className="weather-table"
        scroll={{ x: true }} // Enable horizontal scrolling on small screens
      />
    </div>
  );
};

export default HomePage;
