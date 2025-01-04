// index.js
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css'; // must exist
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import 'bootstrap/dist/css/bootstrap.min.css';      // The CSS
import 'bootstrap/dist/js/bootstrap.bundle.min.js'; // The JS for toggling
// or your Bootswatch link in public/index.html

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>
);
