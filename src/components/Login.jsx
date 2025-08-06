import React, { useState } from 'react';
import { Eye, EyeOff } from 'lucide-react';
import './Login.css';

const Login = ({ onLogin }) => {
  const [activeTab, setActiveTab] = useState('signin');
  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState({
    login: '',
    password: ''
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (formData.login && formData.password) {
      onLogin();
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="logo">
          <div className="logo-bg">
            <span className="logo-w">W</span>
          </div>
        </div>
        
        <div className="auth-tabs">
          <button 
            className={`tab ${activeTab === 'signin' ? 'active' : ''}`}
            onClick={() => setActiveTab('signin')}
          >
            Sign in
          </button>
          <button 
            className={`tab ${activeTab === 'signup' ? 'active' : ''}`}
            onClick={() => setActiveTab('signup')}
          >
            Sign up
          </button>
        </div>

        <div onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">LOGIN</label>
            <input
              type="text"
              className="form-input"
              placeholder="Enter your login"
              value={formData.login}
              onChange={(e) => setFormData({...formData, login: e.target.value})}
            />
          </div>

          <div className="form-group">
            <label className="form-label">PASSWORD</label>
            <div style={{ position: 'relative' }}>
              <input
                type={showPassword ? "text" : "password"}
                className="form-input"
                placeholder="Enter your password"
                value={formData.password}
                onChange={(e) => setFormData({...formData, password: e.target.value})}
                style={{ paddingRight: '50px' }}
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                style={{
                  position: 'absolute',
                  right: '16px',
                  top: '50%',
                  transform: 'translateY(-50%)',
                  background: 'none',
                  border: 'none',
                  color: '#666',
                  cursor: 'pointer'
                }}
              >
                {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
              </button>
            </div>
            <div className="forgot-password">
              <a href="#">Forgot Password ?</a>
            </div>
          </div>

          <button onClick={handleSubmit} className="signin-btn">
            Sign in
          </button>
        </div>

        {/* <div className="divider">OR</div> */}
      </div>
    </div>
  );
};

export default Login;