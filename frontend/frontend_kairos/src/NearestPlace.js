import React, { useEffect, useState } from 'react';

function NearestPlace() {
  const [placeData, setPlaceData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Check if geolocation is available
    if ('geolocation' in navigator) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude } = position.coords;

          // Use the environment variable for the API base URL
          const apiUrl = `${process.env.REACT_APP_API_URL}/api/place/?latitude=${latitude}&longitude=${longitude}`;

          // Fetch the nearest place from your API
          fetch(apiUrl)
            .then((response) => {
              if (!response.ok) {
                throw new Error('Network response was not ok');
              }
              // Access the custom header
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

  if (error) {
    return <div>Error: {error}</div>;
  }

  if (!placeData) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>Nearest Place: {placeData.name}</h1>
      {placeData.description && <p>{placeData.description}</p>}
      <p>
        Location: {placeData.latitude}, {placeData.longitude}
      </p>
      <p>Elevation: {placeData.elevation}</p>
      <a href={placeData.url}>View Details</a>
    </div>
  );
}

export default NearestPlace;
