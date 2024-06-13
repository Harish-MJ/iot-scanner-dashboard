import React, { useEffect, useState } from 'react';
import { Scatter } from 'react-chartjs-2';
import { Chart, registerables } from 'chart.js';
import axios from 'axios';
import './customStyles.css';

Chart.register(...registerables);

interface Measurement {
  angle: number;
  distance: number;
  intensity: number;
}

interface LaserData {
  timestamp: string;
  measurements: Measurement[];
}

const RealTimeVisualization: React.FC = () => {
  const [data, setData] = useState<LaserData | null>(null);
  const [chartData, setChartData] = useState({
    datasets: [
      {
        label: 'Laser Data',
        data: [],
        backgroundColor: [],
        pointRadius: 3,
        showLine: false,
      },
    ],
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:5000/data');
        const latestData = response.data[response.data.length - 1]; // Get the latest data entry
        setData(latestData);
        updateChartData(latestData);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 5000); // Fetch data every 5 seconds
    return () => clearInterval(interval);
  }, []);

  const updateChartData = (latestData: LaserData) => {
    setChartData({
      datasets: [
        {
          label: `Points color based on intensity`,
          data: latestData.measurements.map(d => ({
            x: d.angle,
            y: d.distance,
          })),
          backgroundColor: latestData.measurements.map(d => `rgba(${d.intensity * 255}, 0, 0, 1)`),
          pointRadius: 5,
          showLine: false,
        },
      ],
    });
  };

  const options = {
    scales: {
      x: {
        type: 'linear',
        position: 'bottom',
        min: -10,
        max: 360,
        title: {
          display: true,
          text: 'Angle (degrees)',
        },
      },
      y: {
        type: 'linear',
        min: 0,
        max: 1050,
        title: {
          display: true,
          text: 'Distance (mm)',
        },
      },
    },
  };

  return (
    <div className="container mt-5">
      <h2 className="text-center">Real-Time Visualization</h2>
      {data && <h4 className="text-center">Timestamp: {data.timestamp}</h4>}
      <div className="chart-container">
        <Scatter data={chartData} options={options} />
      </div>
    </div>
  );
};

export default RealTimeVisualization;
