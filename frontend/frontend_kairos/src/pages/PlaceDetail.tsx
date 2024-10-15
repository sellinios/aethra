import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Card, Spin, Alert, Table, Typography } from 'antd';
import moment from 'moment';
import WeatherIcon from '../components/Weather/WeatherIcon'; // Ensure the correct path
import './PlaceDetail.css';

const { Title, Text } = Typography;

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
  weather_condition?: string;
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
    return <Alert message="Error" description={error} type="error" showIcon />;
  }

  if (!placeData) {
    return null;
  }

  // Helper function to map weather conditions to icon states
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

  // Define time periods
  const timePeriods = [
    { name: 'Night', startHour: 0, endHour: 6 },
    { name: 'Morning', startHour: 6, endHour: 12 },
    { name: 'Afternoon', startHour: 12, endHour: 18 },
    { name: 'Evening', startHour: 18, endHour: 24 },
  ];

  // Process weather data
  const now = moment();

  // Next 7 days data
  const next7DaysData = placeData.weather_data.filter((entry) => {
    const entryTime = moment(entry.datetime);
    return entryTime.isSameOrAfter(now) && entryTime.isBefore(now.clone().add(7, 'days'));
  });

  // Group data by date and time period
  interface PeriodData {
    timePeriod: string;
    iconState: string;
    temperatureHigh?: number;
    temperatureLow?: number;
    precipitation?: number;
    windSpeed?: number;
    condition: string;
  }

  interface DayData {
    key: string;
    date: string;
    periods: { [key: string]: PeriodData };
    hourlyData: WeatherDataEntry[];
  }

  const dayDataArray: DayData[] = [];

  // Group data by date
  const dailyDataMap = new Map<string, WeatherDataEntry[]>();

  next7DaysData.forEach((entry) => {
    const date = moment(entry.datetime).format('YYYY-MM-DD');
    if (!dailyDataMap.has(date)) {
      dailyDataMap.set(date, []);
    }
    dailyDataMap.get(date)!.push(entry);
  });

  dailyDataMap.forEach((entries, date) => {
    const periodsData: { [key: string]: PeriodData } = {};

    timePeriods.forEach((period) => {
      const periodEntries = entries.filter((entry) => {
        const hour = moment(entry.datetime).hour();
        return hour >= period.startHour && hour < period.endHour;
      });

      if (periodEntries.length > 0) {
        const temperatures = periodEntries
          .map((e) => e.temperature_celsius)
          .filter((t) => t !== undefined) as number[];
        const precipitations = periodEntries
          .map((e) => e.total_precipitation_mm)
          .filter((p) => p !== undefined) as number[];
        const windSpeeds = periodEntries
          .map((e) => e.wind_speed_m_s)
          .filter((w) => w !== undefined) as number[];

        const temperatureHigh = temperatures.length ? Math.max(...temperatures) : undefined;
        const temperatureLow = temperatures.length ? Math.min(...temperatures) : undefined;
        const precipitation = precipitations.length
          ? precipitations.reduce((a, b) => a + b, 0)
          : undefined;
        const windSpeed = windSpeeds.length
          ? windSpeeds.reduce((a, b) => a + b, 0) / windSpeeds.length
          : undefined;

        // Determine the most frequent condition
        const conditionCounts: { [key: string]: number } = {};
        periodEntries.forEach((e) => {
          const condition = e.weather_condition || 'Cloudy';
          conditionCounts[condition] = (conditionCounts[condition] || 0) + 1;
        });
        const condition = Object.keys(conditionCounts).reduce((a, b) =>
          conditionCounts[a] > conditionCounts[b] ? a : b,
        );

        const isDayTime = period.startHour >= 6 && period.startHour < 18;
        const iconState = mapConditionToIconState(condition, isDayTime);

        periodsData[period.name] = {
          timePeriod: period.name,
          iconState,
          temperatureHigh,
          temperatureLow,
          precipitation,
          windSpeed,
          condition,
        };
      }
    });

    dayDataArray.push({
      key: date,
      date,
      periods: periodsData,
      hourlyData: entries, // For expandable rows
    });
  });

  // Define table columns
  const columns = [
    {
      title: 'Date',
      dataIndex: 'date',
      key: 'date',
      render: (date: string) => moment(date).format('dddd, MMM D'),
      fixed: 'left' as 'left',
      width: 150,
    },
    ...timePeriods.map((period) => ({
      title: period.name,
      dataIndex: ['periods', period.name],
      key: period.name,
      render: (data: PeriodData) => {
        if (!data) return null;
        return (
          <div style={{ textAlign: 'center' }}>
            <WeatherIcon
              state={data.iconState}
              width={30}
              height={30}
              color="black"
            />
            <br />
            <Text>
              {data.temperatureHigh !== undefined && data.temperatureLow !== undefined
                ? `${data.temperatureLow}°C / ${data.temperatureHigh}°C`
                : 'N/A'}
            </Text>
            <br />
            <Text>
              {data.precipitation !== undefined
                ? `Precip: ${data.precipitation.toFixed(1)} mm`
                : 'Precip: N/A'}
            </Text>
            <br />
            <Text>
              {data.windSpeed !== undefined
                ? `Wind: ${data.windSpeed.toFixed(1)} m/s`
                : 'Wind: N/A'}
            </Text>
          </div>
        );
      },
    })),
  ];

  // Expandable row render for hourly data
  const expandedRowRender = (record: DayData) => {
    const hourlyColumns = [
      {
        title: 'Time',
        dataIndex: 'datetime',
        key: 'datetime',
        render: (datetime: string) => moment(datetime).format('HH:mm'),
      },
      {
        title: 'Condition',
        dataIndex: 'weather_condition',
        key: 'weather_condition',
        render: (condition: string, entry: WeatherDataEntry) => {
          const entryTime = moment(entry.datetime);
          const isDayTime = entryTime.hour() >= 6 && entryTime.hour() < 18;
          return (
            <div style={{ textAlign: 'center' }}>
              <WeatherIcon
                state={mapConditionToIconState(condition, isDayTime)}
                width={30}
                height={30}
                color="black"
              />
              <br />
              <Text>{condition}</Text>
            </div>
          );
        },
      },
      {
        title: 'Temp (°C)',
        dataIndex: 'temperature_celsius',
        key: 'temperature_celsius',
        render: (temp: number) => `${temp}°C`,
      },
      {
        title: 'Precip (mm)',
        dataIndex: 'total_precipitation_mm',
        key: 'total_precipitation_mm',
        render: (precip: number) => `${precip.toFixed(1)} mm`,
      },
      {
        title: 'Wind (m/s)',
        dataIndex: 'wind_speed_m_s',
        key: 'wind_speed_m_s',
        render: (wind: number) => `${wind.toFixed(1)} m/s`,
      },
    ];

    return (
      <Table
        columns={hourlyColumns}
        dataSource={record.hourlyData}
        pagination={false}
        rowKey="datetime"
        size="small"
      />
    );
  };

  return (
    <div className="place-detail-container">
      <Card className="place-detail-card">
        <Title level={2}>{placeData.name}</Title>
        {placeData.description && <Text>{placeData.description}</Text>}
        <br />
        <Text>
          <strong>Location:</strong> {placeData.latitude}, {placeData.longitude}
        </Text>
        <br />
        <Text>
          <strong>Elevation:</strong> {placeData.elevation} meters
        </Text>
      </Card>

      <Card title="7-Day Forecast" className="daily-forecast-card">
        <Table
          columns={columns}
          dataSource={dayDataArray}
          expandable={{ expandedRowRender }}
          scroll={{ x: true }}
          pagination={false}
        />
      </Card>
    </div>
  );
};

export default PlaceDetail;
