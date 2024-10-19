import React from 'react';
import './WeatherPanel.css';

interface WeatherDataEntry {
  datetime: string;
  temperature_celsius: number;
  relative_humidity_percent: number;
  wind_speed_m_s: number;
  total_precipitation_mm: number;
}

interface WeatherPanelProps {
  weatherData: {
    [city: string]: WeatherDataEntry[];
  };
}

const WeatherPanel: React.FC<WeatherPanelProps> = ({ weatherData }) => {
  return (
    <div className="weather-panel">
      <table className="forecast-table">
        <thead>
          <tr>
            <th>City</th>
            <th>Date</th>
            <th>Temperature (°C)</th>
            <th>Humidity (%)</th>
            <th>Wind Speed (m/s)</th>
            <th>Precipitation (mm)</th>
          </tr>
        </thead>
        <tbody>
          {Object.keys(weatherData).map((city) =>
            weatherData[city].map((entry, index) => (
              <tr key={`${city}-${index}`}>
                <td>{city}</td>
                <td>{new Date(entry.datetime).toLocaleDateString()}</td>
                <td>{entry.temperature_celsius}°C</td>
                <td>{entry.relative_humidity_percent}%</td>
                <td>{entry.wind_speed_m_s} m/s</td>
                <td>{entry.total_precipitation_mm} mm</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
};

export default WeatherPanel;
