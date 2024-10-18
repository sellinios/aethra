import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';

function NearestPlace() {
  const { t, i18n } = useTranslation();
  const [placeData, setPlaceData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchNearestPlace = async (latitude, longitude) => {
      try {
        const apiUrl = `${process.env.REACT_APP_API_URL}/${i18n.language}/api/place/?latitude=${latitude}&longitude=${longitude}`;
        console.log('Fetching nearest place from:', apiUrl);
        const response = await fetch(apiUrl);

        if (!response.ok) {
          const errorMessage = await response.text();
          throw new Error(`Error fetching data: ${response.status} ${response.statusText} - ${errorMessage}`);
        }

        const data = await response.json();
        console.log('Place Data:', data);
        setPlaceData(data);
      } catch (err) {
        console.error('Error fetching nearest place:', err);
        setError(t('error_fetching_nearest_place'));
      }
    };

    if ('geolocation' in navigator) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude } = position.coords;
          fetchNearestPlace(latitude, longitude);
        },
        (geoError) => {
          console.error('Geolocation error:', geoError);
          if (geoError.code === geoError.PERMISSION_DENIED) {
            setError(t('geolocation_permission_denied'));
          } else {
            setError(`${t('error_getting_geolocation')}: ${geoError.message}`);
          }
        }
      );
    } else {
      setError(t('geolocation_not_available'));
    }
  }, [i18n.language, t]);

  if (error) {
    return <div>{t('error')}: {error}</div>;
  }

  if (!placeData) {
    return <div>{t('loading')}</div>;
  }

  const placeUrl = `/${placeData.continent_slug}/${placeData.country_slug}/${placeData.region_slug}/${placeData.municipality_slug}/${placeData.place_slug}/`;
  console.log('Generated URL:', placeUrl);

  return (
    <div>
      <h2>{t('nearest_place')}: {placeData.name}</h2>
      {placeData.description && <p>{placeData.description}</p>}
      <p>
        {t('location')}: {placeData.latitude}, {placeData.longitude}
      </p>
      <p>{t('elevation')}: {placeData.elevation}</p>
      {/* Link to the place detail page */}
      <a href={placeUrl}>
        {t('view_details')}
      </a>
    </div>
  );
}

export default NearestPlace;
