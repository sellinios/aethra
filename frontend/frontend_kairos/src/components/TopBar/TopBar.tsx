// src/components/TopBar/TopBar.tsx
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import './TopBar.css'; // Import the CSS file

interface PlaceData {
  name: string;
  description: string | null;
  latitude: number;
  longitude: number;
  elevation: number;
  url?: string;
}

const TopBar: React.FC = () => {
  const [placeData, setPlaceData] = useState<PlaceData | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if ('geolocation' in navigator) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude } = position.coords;
          fetch(`/api/place/?latitude=${latitude}&longitude=${longitude}`)
            .then((response) => {
              if (!response.ok) {
                throw new Error('Network response was not ok');
              }
              const nearestPlaceUrl = response.headers.get('Nearest-Place-URL');
              return response.json().then((data) => ({ data, nearestPlaceUrl }));
            })
            .then(({ data, nearestPlaceUrl }) => {
              setPlaceData({ ...data, url: nearestPlaceUrl });
            })
            .catch((error) => {
              setError(error.toString());
            });
        },
        (error) => {
          setError('Error getting geolocation: ' + error.message);
        }
      );
    } else {
      setError('Geolocation is not available in this browser.');
    }
  }, []);

  return (
    <div className="top-bar">
      {placeData && (
        <div className="nearest-place-info">
          Nearest Place: <Link to={placeData.url || '#'}>{placeData.name}</Link>
        </div>
      )}
      {error && <div className="error">{error}</div>}
    </div>
  );
};

export default TopBar;
