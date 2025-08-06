import React, { useState } from 'react';
import { ArrowLeft, Copy, Check } from 'lucide-react';

const ReceivePage = ({ onBack }) => {
  const [address] = useState('bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh');
  const [copied, setCopied] = useState(false);

  const copyAddress = () => {
    navigator.clipboard.writeText(address);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="centered-container" style={{
      background: 'linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #1e40af 100%)'
    }}>
      <div className="px-6 py-8 centered-content">
        {/* Header */}
        <div className="flex items-center mb-8">
          <button
            onClick={onBack}
            className="p-2 text-white hover:bg-gray-800 rounded-lg transition-all duration-200"
          >
            <ArrowLeft size={24} />
          </button>
          <h1 className="text-white text-xl font-bold ml-4">Receive Bitcoin</h1>
        </div>

        <div className="space-y-6">
          {/* QR Code Placeholder */}
          <div className="bg-gray-800 p-8 rounded-xl text-center">
            <div className="w-48 h-48 bg-white mx-auto rounded-lg flex items-center justify-center mb-4">
              <div className="text-4xl">📱</div>
            </div>
            <p className="text-gray-400">QR Code for your Bitcoin address</p>
          </div>

          {/* Address */}
          <div className="bg-gray-800 p-6 rounded-xl">
            <label className="block text-gray-400 text-sm mb-3">YOUR BITCOIN ADDRESS</label>
            <div className="flex items-center gap-3">
              <input
                type="text"
                value={address}
                readOnly
                className="flex-1 bg-gray-700 text-white px-4 py-3 rounded-lg font-mono text-sm"
              />
              <button
                onClick={copyAddress}
                className="p-3 bg-gradient-to-r from-cyan-500 to-blue-500 text-white rounded-lg hover:from-cyan-600 hover:to-blue-600 transition-all duration-200"
              >
                {copied ? <Check size={20} /> : <Copy size={20} />}
              </button>
            </div>
          </div>

          {/* Instructions */}
          <div className="bg-gray-800 p-6 rounded-xl">
            <h3 className="text-white font-semibold mb-3">How to receive Bitcoin:</h3>
            <div className="space-y-2 text-gray-300">
              <p>1. Share this address with the sender</p>
              <p>2. Or let them scan the QR code</p>
              <p>3. Wait for the transaction to be confirmed</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ReceivePage;