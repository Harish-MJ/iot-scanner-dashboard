import React from 'react';
import './Footer.css';

/* Footer component displays the footer text */ 

const Footer: React.FC = () => {
  return (
    <footer className="footer mt-auto py-3 bg-dark">
      <div className="container text-center">
        <span className="text-muted"> Made by Harish </span>
      </div>
    </footer>
  );
};

export default Footer;
