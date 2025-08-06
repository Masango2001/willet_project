import React, { useState } from 'react';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import Send from './components/Send';
import './App.css';

function App() {
  const [currentPage, setCurrentPage] = useState('login');

  const handleLogin = () => {
    setCurrentPage('dashboard');
  };

  const handleNavigate = (page) => {
    setCurrentPage(page);
  };

  const renderCurrentPage = () => {
    switch (currentPage) {
      case 'login':
        return <Login onLogin={handleLogin} />;
      case 'dashboard':
        return <Dashboard onNavigate={handleNavigate} />;
      case 'send':
        return <Send onNavigate={handleNavigate} />;
      default:
        return <Login onLogin={handleLogin} />;
    }
  };

  return (
    <div className="app">
      {renderCurrentPage()}
    </div>
  );
}

export default App;