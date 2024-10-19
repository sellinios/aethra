import React from 'react';
import { List, Card, Typography } from 'antd';

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

interface WeatherPanelProps {
  weatherData: {
    [key: string]: CityWeather;
  };
}

// Format the date to a more readable format
const formatDate = (dateStr: string) => {
  const date = new Date(dateStr);
  return new Intl.DateTimeFormat('en-GB', { month: 'short', day: 'numeric', year: 'numeric' }).format(date);
};

const WeatherPanel: React.FC<WeatherPanelProps> = ({ weatherData }) => {
  return (
    <div>
      {Object.keys(weatherData).map((cityName) => {
        const cityWeather = weatherData[cityName];
        return (
          <Card key={cityName} title={cityWeather.name}>
            <List
              grid={{ gutter: 16, column: 4 }}
              dataSource={cityWeather.weather}
              renderItem={(day) => (
                <List.Item>
                  <Card>
                    <Title level={4}>{formatDate(day.date)}</Title>
                    <p>Max Temp: {day.maxTemp.toFixed(1)}°C</p>
                    <p>Min Temp: {day.minTemp.toFixed(1)}°C</p>
                    <p>Avg Cloud Cover: {day.avgCloudCover.toFixed(1)}%</p>
                    <p>Max Precipitation: {day.maxPrecipitation.toFixed(1)}mm</p>
                    <p>Wind Speed: {day.windSpeedAvg.toFixed(1)} km/h</p>
                    {(day.avgCloudCover > 50 || day.maxPrecipitation > 0) && (
                      <p>Warning: Potential bad weather!</p>
                    )}
                  </Card>
                </List.Item>
              )}
            />
          </Card>
        );
      })}
    </div>
  );
};

export default WeatherPanel;
