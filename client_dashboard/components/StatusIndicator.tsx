import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './StatusIndicator.css'; 

const StatusIndicator: React.FC = () => {
  const [isConnected, setIsConnected] = useState<boolean>(false);

  useEffect(() => {
    const checkStatus = async () => {
      try {
        const response = await axios.get('http://localhost:5000/data');
        setIsConnected(response.data.length > 0); 
      } catch (error) {
        setIsConnected(false);
        console.error('Error checking device status:', error);
      }
    };

    checkStatus();
    const interval = setInterval(checkStatus, 5000); // Check status every 5 seconds
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
