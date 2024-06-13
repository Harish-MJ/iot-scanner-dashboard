import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import DataTable from '/components/DataTable';
import RealTimeVisualization from '/components/RealTimeVisualization';
import StatusIndicator from '/components/StatusIndicator';

const App: React.FC = () => {
  return (
    <Router>
      <div className="App">
        <StatusIndicator />
        <div className="container">
          <h1 className="mt-5 text-center">Lumoview Scanner Dashboard</h1>
          <div className="text-center mb-4">
            <Link to="/data-log" className="btn btn-primary mx-2">Data Log</Link>
            <Link to="/real-time-visualization" className="btn btn-secondary mx-2">Real-Time Visualization</Link>
          </div>
          <Routes>
            <Route path="/data-log" element={<DataTable />} />
            <Route path="/real-time-visualization" element={<RealTimeVisualization />} />
            <Route path="/" element={<DataTable />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
};

export default App;
