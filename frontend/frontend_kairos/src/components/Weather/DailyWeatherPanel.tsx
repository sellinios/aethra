// src/components/Weather/DailyWeatherPanel.tsx

import React from 'react';
import { Table, Typography } from 'antd';
import moment from 'moment';
import WeatherIcon from './WeatherIcon'; // Import the updated WeatherIcon component
import './DailyWeatherPanel.css';

const { Text } = Typography;

interface WeatherDataEntry {
  datetime: string;
  temperature_celsius?: number;
  relative_humidity_percent?: number;
  wind_speed_m_s?: number;
  wind_direction?: string;
  total_precipitation_mm?: number;
}

interface DailyWeatherPanelProps {
  data: WeatherDataEntry[];
}

const DailyWeatherPanel: React.FC<DailyWeatherPanelProps> = ({ data }) => {
  // Group weather data by date
  const groupedData = groupByDate(data);

  // Define columns for the table
  const columns = [
    {
      title: 'Date',
      dataIndex: 'date',
      key: 'date',
      render: (text: string) => <Text strong>{moment(text).format('dddd D MMM')}</Text>,
    },
    {
      title: 'Night',
      dataIndex: 'night',
      key: 'night',
      render: (entry: WeatherDataEntry | null) => renderTimeSlot(entry, 'Night'),
    },
    {
      title: 'Morning',
      dataIndex: 'morning',
      key: 'morning',
      render: (entry: WeatherDataEntry | null) => renderTimeSlot(entry, 'Morning'),
    },
    {
      title: 'Afternoon',
      dataIndex: 'afternoon',
      key: 'afternoon',
      render: (entry: WeatherDataEntry | null) => renderTimeSlot(entry, 'Afternoon'),
    },
    {
      title: 'Evening',
      dataIndex: 'evening',
      key: 'evening',
      render: (entry: WeatherDataEntry | null) => renderTimeSlot(entry, 'Evening'),
    },
    {
      title: 'Temperature high/low',
      dataIndex: 'temperature',
      key: 'temperature',
      render: (_: unknown, record: any) => (
        <Text>
          {record.temperature_high !== undefined && record.temperature_low !== undefined
            ? `${record.temperature_high}° / ${record.temperature_low}°`
            : '-° / -°'}
        </Text>
      ),
    },
    {
      title: 'Wind',
      dataIndex: 'wind',
      key: 'wind',
      render: (_: unknown, record: any) => (
        <Text>
          {record.wind_speed !== undefined
            ? `${record.wind_speed} m/s ${record.wind_direction ?? ''}`
            : '- m/s'}
        </Text>
      ),
    },
    {
      title: 'Precipitation',
      dataIndex: 'precipitation',
      key: 'precipitation',
      render: (_: unknown, record: any) => (
        <Text>
          {record.precipitation !== undefined ? `${record.precipitation} mm` : '- mm'}
        </Text>
      ),
    },
  ];

  // Transform grouped data into the format needed for the table
  const tableData = Object.keys(groupedData).map((date) => {
    const dailyEntries = groupedData[date];
    const temperatures = dailyEntries.map((entry) => entry.temperature_celsius ?? null).filter((temp) => temp !== null) as number[];
    return {
      key: date,
      date,
      night: getTimeSlot('night', dailyEntries),
      morning: getTimeSlot('morning', dailyEntries),
      afternoon: getTimeSlot('afternoon', dailyEntries),
      evening: getTimeSlot('evening', dailyEntries),
      temperature_high: temperatures.length > 0 ? Math.max(...temperatures) : undefined,
      temperature_low: temperatures.length > 0 ? Math.min(...temperatures) : undefined,
      wind_speed: dailyEntries[0]?.wind_speed_m_s,
      wind_direction: dailyEntries[0]?.wind_direction,
      precipitation: dailyEntries[0]?.total_precipitation_mm,
    };
  });

  return (
    <Table
      columns={columns}
      dataSource={tableData}
      pagination={false}
      bordered
      className="daily-weather-table"
    />
  );
};

// Group the data by date
const groupByDate = (data: WeatherDataEntry[]) => {
  return data.reduce((acc: { [key: string]: WeatherDataEntry[] }, entry) => {
    const date = moment(entry.datetime).format('YYYY-MM-DD');
    if (!acc[date]) {
      acc[date] = [];
    }
    acc[date].push(entry);
    return acc;
  }, {});
};

// Render the time slot with the icon and temperature
const renderTimeSlot = (entry: WeatherDataEntry | null, label: string) => {
  if (!entry) {
    return <Text type="secondary">No data</Text>;
  }
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
      <WeatherIcon
        state={getWeatherState(entry)}
        width={32}
        height={32}
        color={getIconColor(entry)} // Pass the dynamic color here
      />
      <Text>{entry.temperature_celsius !== undefined ? `${entry.temperature_celsius}°` : '-°'}</Text>
    </div>
  );
};

// Get the time slot for a given period
const getTimeSlot = (period: string, entries: WeatherDataEntry[]): WeatherDataEntry | null => {
  const hoursMap: { [key: string]: [number, number] } = {
    morning: [6, 12],
    afternoon: [12, 18],
    evening: [18, 24],
    night: [0, 6],
  };
  const [start, end] = hoursMap[period.toLowerCase()];
  return entries.find((entry) => {
    const hour = moment(entry.datetime).hour();
    return hour >= start && hour < end;
  }) || null;
};

// Placeholder function to map weather data to state for icons
const getWeatherState = (entry: WeatherDataEntry): string => {
  if (entry.temperature_celsius === undefined) {
    return 'cloudy'; // Default state
  }
  if (entry.temperature_celsius > 25) {
    return 'sunny';
  } else if (entry.wind_speed_m_s && entry.wind_speed_m_s > 10) {
    return 'wind';
  } else if (entry.total_precipitation_mm && entry.total_precipitation_mm > 0) {
    return 'rain';
  } else {
    return 'cloudy';
  }
};

// Function to determine icon color based on weather conditions
const getIconColor = (entry: WeatherDataEntry): string => {
  if (entry.temperature_celsius === undefined) {
    return 'gray';
  }
  if (entry.temperature_celsius > 25) {
    return 'orange';
  } else if (entry.wind_speed_m_s && entry.wind_speed_m_s > 10) {
    return 'blue';
  } else if (entry.total_precipitation_mm && entry.total_precipitation_mm > 0) {
    return 'blue';
  } else {
    return 'gray';
  }
};

export default DailyWeatherPanel;
