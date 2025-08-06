import React, { useState } from 'react';
import { ArrowUpRight, ArrowDownLeft } from 'lucide-react';
import './Dashboard.css';

const Dashboard = ({ onNavigate }) => {
  const [balance] = useState(0.00756);
  const [usdBalance] = useState(2847.52);
  
  const transactions = [
    { id: 1, type: 'Sent', address: '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa', amount: -0.001, status: 'sent' }
  ];

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1 className="dashboard-title">Bitcoin Wallet</h1>
        <div className="header-subtitle">Secure • Fast • Reliable</div>
      </header>

      <div className="balance-card">
        <div className="balance-title">Total Balance</div>
        <div className="balance-amount">{balance.toFixed(5)} BTC</div>
        <div className="balance-usd">${usdBalance.toLocaleString()}</div>
        <div className="balance-change">+2.5% today</div>
      </div>

      <div className="actions-grid">
        <button className="action-btn send-btn" onClick={() => onNavigate('send')}>
          <div className="action-icon-wrapper send-icon">
            <ArrowUpRight className="action-icon" />
          </div>
          <span className="action-text">Send</span>
        </button>
        
        <button className="action-btn receive-btn">
          <div className="action-icon-wrapper receive-icon">
            <ArrowDownLeft className="action-icon" />
          </div>
          <span className="action-text">Receive</span>
        </button>
      </div>

      <div className="transactions-section">
        <h2 className="section-title">Recent Transactions</h2>
        <div className="transactions-list">
          {transactions.map((tx) => (
            <div key={tx.id} className="transaction-item">
              <div className={`transaction-icon ${tx.status}`}>
                {tx.status === 'sent' ? <ArrowUpRight size={20} /> : <ArrowDownLeft size={20} />}
              </div>
              <div className="transaction-details">
                <div className="transaction-type">{tx.type}</div>
                <div className="transaction-address">{tx.address.substring(0, 20)}...</div>
                <div className="transaction-time">2 hours ago</div>
              </div>
              <div className={`transaction-amount ${tx.status}`}>
                {tx.amount > 0 ? '+' : ''}{Math.abs(tx.amount)} BTC
                <div className="transaction-usd">
                  ${(Math.abs(tx.amount) * 37700).toFixed(2)}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
