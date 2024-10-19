// src/pages/HomePage.tsx
import React, { useEffect, useState } from 'react';
import { Container } from 'react-bootstrap';

const HomePage: React.FC = () => {
  // State to store the planet count
  const [planetCount, setPlanetCount] = useState<number | null>(null);

  // Fetch the planet count from the API
  useEffect(() => {
    const fetchPlanetCount = async () => {
      try {
        const response = await fetch(`${process.env.REACT_APP_API_URL}api/planet-count/`);
        const data = await response.json();
        setPlanetCount(data.planet_count);  // Assuming the response has the key 'planet_count'
      } catch (error) {
        console.error('Error fetching planet count:', error);
      }
    };

    fetchPlanetCount();
  }, []);

  return (
    <Container className="mt-5">
      <h1>Welcome to Aethra</h1>
      <p>This is the home page.</p>

      {/* Show a loading message or the planet count */}
      {planetCount === null ? (
        <p>Loading planet count...</p>
      ) : (
        <p>There are {planetCount} planets in the database.</p>
      )}
    </Container>
  );
};

export default HomePage;
