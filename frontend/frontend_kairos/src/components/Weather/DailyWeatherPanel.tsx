// src/components/Weather/DailyWeatherPanel.tsx

import React from 'react';
import { Table, Typography } from 'antd';
import moment from 'moment';
import WeatherIcon from './WeatherIcon';
import { useTranslation } from 'react-i18next';
import { Helmet } from 'react-helmet-async';
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
  const { t } = useTranslation();
  const groupedData = groupByDate(data);

  // Define translations outside the renderTimeSlot function
  const noDataText = t('noData');
  const timeSlots = {
    night: t('night'),
    morning: t('morning'),
    afternoon: t('afternoon'),
    evening: t('evening'),
  };

  const columns = [
    {
      title: t('date'),
      dataIndex: 'date',
      key: 'date',
      render: (text: string) => <Text strong>{moment(text).format('dddd D MMM')}</Text>,
    },
    {
      title: timeSlots.night,
      dataIndex: 'night',
      key: 'night',
      render: (entry: WeatherDataEntry | null) => renderTimeSlot(entry, timeSlots.night, noDataText),
    },
    {
      title: timeSlots.morning,
      dataIndex: 'morning',
      key: 'morning',
      render: (entry: WeatherDataEntry | null) => renderTimeSlot(entry, timeSlots.morning, noDataText),
    },
    {
      title: timeSlots.afternoon,
      dataIndex: 'afternoon',
      key: 'afternoon',
      render: (entry: WeatherDataEntry | null) => renderTimeSlot(entry, timeSlots.afternoon, noDataText),
    },
    {
      title: timeSlots.evening,
      dataIndex: 'evening',
      key: 'evening',
      render: (entry: WeatherDataEntry | null) => renderTimeSlot(entry, timeSlots.evening, noDataText),
    },
    {
      title: t('temperatureHighLow'),
      dataIndex: 'temperature',
      key: 'temperature',
      render: (_: unknown, record: any) => (
        <Text>
          {record.temperature_high !== undefined && record.temperature_low !== undefined
            ? `${Math.round(record.temperature_high)}° / ${Math.round(record.temperature_low)}°`
            : '-° / -°'}
        </Text>
      ),
    },
    {
      title: t('precipitation'),
      dataIndex: 'precipitation',
      key: 'precipitation',
      render: (_: unknown, record: any) => (
        <Text>
          {record.precipitation !== undefined ? `${record.precipitation} mm` : '- mm'}
        </Text>
      ),
    },
    {
      title: t('wind'),
      dataIndex: 'wind',
      key: 'wind',
      render: (_: unknown, record: any) => (
        <Text>
          {record.wind_direction ? `${record.wind_direction} ` : ''}{record.wind_speed !== undefined
            ? `${record.wind_speed.toFixed(1)} m/s`
            : '- m/s'}
        </Text>
      ),
    },
  ];

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
    <>
      <Helmet>
        <title>{t('weatherForecastTitle')}</title>
        <meta name="description" content={t('weatherForecastDescription')} />
      </Helmet>
      <div className="container my-4">
        <div className="table-responsive">
          <Table
            columns={columns}
            dataSource={tableData}
            pagination={false}
            bordered
            className="daily-weather-table"
          />
        </div>
      </div>
    </>
  );
};

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

const renderTimeSlot = (entry: WeatherDataEntry | null, label: string, noDataText: string) => {
  if (!entry) {
    return <Text type="secondary">{label}: {noDataText}</Text>;
  }

  return (
    <div className="d-flex align-items-center gap-2">
      <WeatherIcon
        state={getWeatherState(entry)}
        width={32}
        height={32}
        color="black" // Keeping icons black as requested
      />
      <Text>{entry.temperature_celsius !== undefined ? `${Math.round(entry.temperature_celsius)}°` : '-°'}</Text>
    </div>
  );
};

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

const getWeatherState = (entry: WeatherDataEntry): string => {
  if (entry.temperature_celsius === undefined) {
    return 'cloudy';
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

export default DailyWeatherPanel;
