import React, { useState } from 'react';
import { Send, ArrowLeft, QrCode, Scan } from 'lucide-react';
import './Send.css';

const SendBitcoin = ({ onNavigate }) => {
  const [recipient, setRecipient] = useState('');
  const [amount, setAmount] = useState('');
  const [fee, setFee] = useState('standard');
  const [isLoading, setIsLoading] = useState(false);
  
  const feeOptions = {
    slow: { name: 'Slow', time: '60+ min', cost: '0.00001' },
    standard: { name: 'Standard', time: '10-30 min', cost: '0.00003' },
    fast: { name: 'Fast', time: '2-10 min', cost: '0.00005' }
  };

  const handleSend = async (e) => {
    e.preventDefault();
    if (recipient && amount) {
      setIsLoading(true);
      // Simulation d'envoi
      setTimeout(() => {
        alert(`Sending ${amount} BTC to ${recipient}`);
        setIsLoading(false);
        onNavigate('dashboard');
      }, 2000);
    }
  };

  const calculateUsdAmount = () => {
    return amount ? (parseFloat(amount) * 37700).toFixed(2) : '0.00';
  };

  return (
    <div className="send-container">
      <div className="send-header">
        <button className="back-btn" onClick={() => onNavigate('dashboard')}>
          <ArrowLeft size={20} />
        </button>
        <h1 className="send-title">Send Bitcoin</h1>
        <div></div>
      </div>

      <div className="send-form">
        <div className="recipient-section">
          <label className="form-label">Recipient Address</label>
          <div className="input-with-actions">
            <input
              type="text"
              className="form-input recipient-input"
              placeholder="Enter Bitcoin address or scan QR code"
              value={recipient}
              onChange={(e) => setRecipient(e.target.value)}
            />
            <div className="input-actions">
              <button type="button" className="action-icon-btn">
                <QrCode size={18} />
              </button>
              <button type="button" className="action-icon-btn">
                <Scan size={18} />
              </button>
            </div>
          </div>
        </div>

        <div className="amount-section">
          <label className="form-label">Amount</label>
          <div className="amount-input-wrapper">
            <input
              type="number"
              step="0.00000001"
              className="form-input amount-input"
              placeholder="0.00000000"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
            />
            <div className="amount-currency">BTC</div>
          </div>
          <div className="amount-usd">≈ ${calculateUsdAmount()}</div>
          
          <div className="quick-amounts">
            <button type="button" onClick={() => setAmount('0.001')}>0.001 BTC</button>
            <button type="button" onClick={() => setAmount('0.005')}>0.005 BTC</button>
            <button type="button" onClick={() => setAmount('0.01')}>0.01 BTC</button>
            <button type="button" onClick={() => setAmount('0.1')}>0.1 BTC</button>
          </div>
        </div>

        <div className="fee-section">
          <label className="form-label">Network Fee</label>
          <div className="fee-options">
            {Object.entries(feeOptions).map(([key, option]) => (
              <div
                key={key}
                className={`fee-option ${fee === key ? 'active' : ''}`}
                onClick={() => setFee(key)}
              >
                <div className="fee-info">
                  <div className="fee-name">{option.name}</div>
                  <div className="fee-time">{option.time}</div>
                </div>
                <div className="fee-cost">{option.cost} BTC</div>
              </div>
            ))}
          </div>
        </div>

        <div className="transaction-summary">
          <div className="summary-row">
            <span>Amount</span>
            <span>{amount || '0.00000000'} BTC</span>
          </div>
          <div className="summary-row">
            <span>Network Fee</span>
            <span>{feeOptions[fee].cost} BTC</span>
          </div>
          <div className="summary-row total">
            <span>Total</span>
            <span>{amount ? (parseFloat(amount) + parseFloat(feeOptions[fee].cost)).toFixed(8) : feeOptions[fee].cost} BTC</span>
          </div>
        </div>

        <button 
          onClick={handleSend}
          className={`send-btn ${isLoading ? 'loading' : ''}`}
          disabled={!recipient || !amount || isLoading}
        >
          {isLoading ? (
            <>
              <div className="spinner"></div>
              Sending...
            </>
          ) : (
            <>
              <Send size={20} />
              Send Bitcoin
            </>
          )}
        </button>
      </div>
    </div>
  );
};

export default SendBitcoin;