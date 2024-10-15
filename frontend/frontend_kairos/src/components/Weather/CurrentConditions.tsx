// src/components/Weather/CurrentConditions.tsx

import React from 'react';
import { Card, Typography } from 'antd';
import WeatherIcon from './WeatherIcon'; // Ensure the correct path
import moment from 'moment';

const { Title, Text } = Typography;

interface WeatherDataEntry {
  datetime: string;
  temperature_celsius?: number;
  relative_humidity_percent?: number;
  wind_speed_m_s?: number;
  weather_condition?: string;
  // Add other relevant fields if necessary
}

interface CurrentConditionsProps {
  currentData: WeatherDataEntry;
}

const CurrentConditions: React.FC<CurrentConditionsProps> = ({ currentData }) => {
  const {
    datetime,
    temperature_celsius,
    relative_humidity_percent,
    wind_speed_m_s,
    weather_condition,
  } = currentData;

  // Determine if it's daytime based on the hour
  const hour = moment(datetime).hour();
  const isDayTime = hour >= 6 && hour < 18;

  // Function to map weather condition to icon state
  const mapConditionToIconState = (condition: string, isDayTime: boolean) => {
    const normalizedCondition = condition.toLowerCase();

    if (normalizedCondition.includes('clear')) {
      return isDayTime ? 'sunny' : 'clear-night';
    } else if (normalizedCondition.includes('partly cloudy')) {
      return isDayTime ? 'partlycloudy' : 'partlycloudy-night';
    } else if (normalizedCondition.includes('cloudy')) {
      return 'cloudy';
    } else if (normalizedCondition.includes('rain')) {
      return 'rain';
    } else if (normalizedCondition.includes('snow')) {
      return 'snow';
    } else if (normalizedCondition.includes('sleet')) {
      return 'sleet';
    } else if (normalizedCondition.includes('wind')) {
      return 'wind';
    } else if (normalizedCondition.includes('fog')) {
      return 'fog';
    } else if (normalizedCondition.includes('thunder')) {
      return 'thunder';
    } else {
      return 'cloudy'; // Default icon
    }
  };

  const iconState = mapConditionToIconState(weather_condition || 'cloudy', isDayTime);

  return (
    <Card title="Current Conditions" className="current-conditions-card">
      <div style={{ display: 'flex', alignItems: 'center' }}>
        <WeatherIcon state={iconState} width={50} height={50} color="black" />
        <div style={{ marginLeft: '20px' }}>
          <Title level={4}>{moment(datetime).format('LLLL')}</Title>
          <Text>Temperature: {temperature_celsius !== undefined ? `${temperature_celsius}°C` : 'N/A'}</Text>
          <br />
          <Text>Humidity: {relative_humidity_percent !== undefined ? `${relative_humidity_percent}%` : 'N/A'}</Text>
          <br />
          <Text>Wind Speed: {wind_speed_m_s !== undefined ? `${wind_speed_m_s} m/s` : 'N/A'}</Text>
          <br />
          <Text>Condition: {weather_condition || 'N/A'}</Text>
        </div>
      </div>
    </Card>
  );
};

export default CurrentConditions;
