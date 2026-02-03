import React, { useState } from 'react'
import Button from '../components/Button'
import { useNavigate } from 'react-router-dom'
import { api, setAuthTokens } from '../api'

export default function LoginPage({ onLogin }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const submit = async e => {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      const resp = await api.post('/api/auth/login/', { username, password })
      const { access, refresh } = resp.data
      setAuthTokens(access, refresh)
      if (onLogin) onLogin({ access, refresh })
      navigate('/')
    } catch (err) {
      setError(err.response?.data || 'Login failed. Please check your credentials.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-background-shapes">
        <div className="auth-shape" style={{ top: '10%', left: '10%', width: '300px', height: '300px', background: 'radial-gradient(circle, rgba(56, 189, 248, 0.4) 0%, transparent 70%)' }}></div>
        <div className="auth-shape" style={{ bottom: '10%', right: '10%', width: '400px', height: '400px', background: 'radial-gradient(circle, rgba(139, 92, 246, 0.4) 0%, transparent 70%)', animationDelay: '-5s' }}></div>
      </div>
      
      <div className="auth-card">
        <div className="auth-header">
          <h2>Welcome Back</h2>
          <p className="muted">Sign in to continue your journey</p>
        </div>
        
        {error && (
          <div className="auth-error">
            {typeof error === 'string' ? error : 'Invalid username or password'}
          </div>
        )}

        <form onSubmit={submit}>
          <div className="form-group">
            <input 
              id="username"
              className="form-input" 
              value={username} 
              onChange={e => setUsername(e.target.value)} 
              placeholder=" "
              required
            />
            <label htmlFor="username" className="form-label">Username</label>
          </div>
          
          <div className="form-group">
            <input 
              id="password"
              type={showPassword ? "text" : "password"} 
              className="form-input" 
              value={password} 
              onChange={e => setPassword(e.target.value)} 
              placeholder=" "
              required
            />
            <label htmlFor="password" className="form-label">Password</label>
            <button 
              type="button" 
              className="password-toggle"
              onClick={() => setShowPassword(!showPassword)}
            >
              {showPassword ? (
                <svg width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                </svg>
              ) : (
                <svg width="20" height="20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              )}
            </button>
          </div>
          
          <Button type="submit" isLoading={loading} className="w-full btn-primary" style={{ marginTop: '1rem', padding: '0.875rem' }}>
            Sign in
          </Button>
        </form>
        
        <p style={{ textAlign: 'center', marginTop: '1.5rem', color: 'var(--text-muted)' }}>
          Don't have an account? <a href="/signup" style={{ color: 'var(--accent)', fontWeight: 600 }}>Sign up</a>
        </p>
      </div>
    </div>
  )
}
