import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './DataTable.css';
import './customStyles.css';  // Import custom styles

const apiUrl = process.env.NODE_ENV === 'production' ? process.env.REACT_APP_API_URL : process.env.LOCAL_API_URL;

interface Measurement {
  angle: number;
  distance: number;
  intensity: number;
}

interface LaserData {
  timestamp: string;
  measurements: Measurement[];
}

const DataTable: React.FC = () => {
  const [data, setData] = useState<LaserData | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(`${apiUrl}/api/data`);
        const latestData = response.data[response.data.length - 1]; // Get the latest data entry
        setData(latestData);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 5000); // Fetch data every 5 seconds
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="container">
      <h2 className="text-center">Live Data Log</h2>
      {data ? (
        <>
          <h4 className="text-center">Timestamp: {data.timestamp}</h4>
          <div className="table-responsive">
            <table className="table table-striped table-bordered table-hover">
              <thead className="thead-dark">
                <tr>
                  <th>Angle</th>
                  <th>Distance</th>
                  <th>Intensity</th>
                </tr>
              </thead>
              <tbody>
                {data.measurements.map((measurement, idx) => (
                  <tr key={idx}>
                    <td>{measurement.angle}</td>
                    <td>{measurement.distance}</td>
                    <td>{measurement.intensity}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      ) : (
        <p className="text-center">Loading data...</p>
      )}
    </div>
  );
};

export default DataTable;
