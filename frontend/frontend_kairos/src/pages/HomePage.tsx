import React, { useEffect, useState } from 'react';
import { Spin, Alert, Typography, Table } from 'antd';
import { Helmet } from 'react-helmet-async'; // Import Helmet for SEO
import './HomePage.css'; // Import the custom CSS
import { useTranslation } from 'react-i18next';

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
  const { t } = useTranslation();
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

        // Sort the data to ensure it starts from the current day
        const sortedWeatherData = data.daily_weather_data.sort(
          (a: any, b: any) => new Date(a.date).getTime() - new Date(b.date).getTime()
        );

        console.log(`Sorted weather data:`, sortedWeatherData);

        cityWeatherData['Athens'] = {
          name: data.place_name,
          weather: sortedWeatherData.slice(0, 4).map((day: any) => ({
            date: day.date,
            maxTemp: Math.round(day.max_temp), // Round temperature
            minTemp: Math.round(day.min_temp), // Round temperature
            avgCloudCover: day.avg_cloud_cover,
            maxPrecipitation: day.max_precipitation,
            windSpeedAvg: day.wind_speed_avg,
          })),
        };

        console.log(`Processed weather data for Athens:`, cityWeatherData);

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
    return <Spin tip={t('loading')} />;
  }

  if (error) {
    return <Alert message={t('error')} description={error} type="error" showIcon />;
  }

  // Check if there is at least one city with weather data
  const firstCityKey = Object.keys(weatherData)[0];
  if (!firstCityKey || !weatherData[firstCityKey].weather.length) {
    return <Alert message={t('error')} description={t('noData')} type="warning" showIcon />;
  }

  // Extract day names from the first city's weather data
  const firstCityWeather = weatherData[firstCityKey].weather;
  const dayNames = firstCityWeather.map((day) => {
    const date = new Date(`${day.date}T00:00:00Z`); // Ensures UTC parsing
    console.log(`Processing date: ${day.date} -> Parsed Date: ${date}`);
    const dayIndex = date.getDay(); // 0: Sunday, 1: Monday, ..., 6: Saturday
    const dayNameKey = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'][dayIndex];
    const dayName = t(dayNameKey);
    console.log(`Day Index: ${dayIndex}, Day Name Key: ${dayNameKey}, Day Name: ${dayName}`);
    return dayName;
  });

  // Dynamically generate columns based on day names
  const columns = [
    {
      title: t('city'),
      dataIndex: 'city',
      key: 'city',
    },
    ...dayNames.map((dayName, index) => ({
      title: dayName,
      dataIndex: `day${index}`,
      key: `day${index}`,
    })),
  ];

  // Generate dataSource dynamically
  const dataSource = Object.keys(weatherData).map((cityName) => {
    const cityWeather = weatherData[cityName].weather;

    // Ensure that the number of days matches the columns
    const weatherDays = cityWeather.slice(0, dayNames.length);

    const dayEntries: { [key: string]: string } = {};
    weatherDays.forEach((day, index) => {
      dayEntries[`day${index}`] = `${day.maxTemp}°C / ${day.minTemp}°C`;
    });

    return {
      key: cityName,
      city: weatherData[cityName].name,
      ...dayEntries,
    };
  });

  console.log(`Generated columns:`, columns);
  console.log(`Generated dataSource:`, dataSource);

  return (
    <div className="weather-container">
      <Helmet>
        <title>{t('weatherForecastTitle')}</title>
        <meta name="description" content={t('weatherForecastDescription')} />
      </Helmet>
      <Title level={2} className="weather-title">
        {t('cityWeatherForecast', { days: dayNames.length })}
      </Title>
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
