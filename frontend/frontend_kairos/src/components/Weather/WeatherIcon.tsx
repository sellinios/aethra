// src/components/WeatherIcon.tsx

import React from 'react';
import {
  RseClearDay,
  RseClearNight,
  RseCloudy,
  RseFog,
  RseHail,
  RsePartlyCloudyDay,
  RsePartlyCloudyNight,
  RseRain,
  RseRainSnow,
  RseRainSnowShowersDay,
  RseRainSnowShowersNight,
  RseShowersDay,
  RseShowersNight,
  RseSleet,
  RseSnow,
  RseSnowShowersDay,
  RseSnowShowersNight,
  RseThunder,
  RseThunderRain,
  RseThunderShowersDay,
  RseThunderShowersNight,
  RseWind,
} from 'react-skycons-extended';

interface WeatherIconProps {
  state?: string; // Made optional to handle undefined values
  width: number;
  height: number;
  color?: string; // Added 'color' prop as optional
  className?: string;
}

const WeatherIcon: React.FC<WeatherIconProps> = ({
  state = 'cloudy', // Default state if undefined
  width,
  height,
  color = 'black', // Default color if not provided
  className = '',
}) => {
  const getIconComponent = (state: string): React.FC<any> => {
    switch (state.toLowerCase()) {
      case 'sunny':
        return RseClearDay;
      case 'clear-night':
        return RseClearNight;
      case 'cloudy':
        return RseCloudy;
      case 'fog':
        return RseFog;
      case 'hail':
        return RseHail;
      case 'partlycloudy':
      case 'partly-cloudy':
      case 'partlycloudy-day':
        return RsePartlyCloudyDay;
      case 'partlycloudy-night':
      case 'partly-cloudy-night':
        return RsePartlyCloudyNight;
      case 'rain':
        return RseRain;
      case 'rainsnow':
        return RseRainSnow;
      case 'rainsnowshowersday':
        return RseRainSnowShowersDay;
      case 'rainsnowshowersnight':
        return RseRainSnowShowersNight;
      case 'showersday':
        return RseShowersDay;
      case 'showersnight':
        return RseShowersNight;
      case 'sleet':
        return RseSleet;
      case 'snow':
        return RseSnow;
      case 'snowshowersday':
        return RseSnowShowersDay;
      case 'snowshowersnight':
        return RseSnowShowersNight;
      case 'thunder':
        return RseThunder;
      case 'thunderrain':
        return RseThunderRain;
      case 'thundershowersday':
        return RseThunderShowersDay;
      case 'thundershowersnight':
        return RseThunderShowersNight;
      case 'wind':
        return RseWind;
      default:
        return RseCloudy; // Default icon if state doesn't match any case
    }
  };

  const IconComponent = getIconComponent(state);

  return (
    <div className={`weather-icon ${className}`}>
      <IconComponent
        color={color} // Use the color prop here
        width={width}
        height={height}
        animate={true} // Optional: Animate the icon if supported
      />
    </div>
  );
};

export default WeatherIcon;