import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './StatusIndicator.css'; 

/* StatusIndicator component checks the device status and displays a status indicator */

//const apiUrl = process.env.NODE_ENV === 'production' ? process.env.REACT_APP_API_URL : process.env.LOCAL_API_URL;
const StatusIndicator: React.FC = () => {
  const [isConnected, setIsConnected] = useState<boolean>(false);

  useEffect(() => {
    const checkStatus = async () => {
      try {
        const apiUrl = process.env.REACT_APP_API_URL;
        console.log('API URL:', apiUrl);
        const response = await axios.get(`https://iot-scanner-dashboard.onrender.com/api/data`);
        //const response = await axios.get(`http://localhost:5000/api/data`); Use this line if you are running the server locally

        setIsConnected(response.data.length > 0); 
      } catch (error) {
        setIsConnected(false);
        console.error('Error checking device status:', error);
      }
    };

    checkStatus();
    const interval = setInterval(checkStatus, 5000); 
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="status-indicator">
      <span className={`indicator ${isConnected ? 'connected' : 'disconnected'}`}></span>
      <span>{isConnected ? 'Device: Connected' : 'Device: Disconnected'}</span>
    </div>
  );
};

export default StatusIndicator;
