import React, { useState } from 'react'
import Button from '../components/Button'
import { useNavigate } from 'react-router-dom'
import { api, setAuthTokens } from '../api'

export default function SignupPage({ onSignup }) {
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  // Password strength calculation
  const getPasswordStrength = (pass) => {
    let strength = 0;
    if (pass.length > 5) strength += 1;
    if (pass.length > 8) strength += 1;
    if (/[A-Z]/.test(pass)) strength += 1;
    if (/[0-9]/.test(pass)) strength += 1;
    if (/[^A-Za-z0-9]/.test(pass)) strength += 1;
    return strength;
  }

  const passwordStrength = getPasswordStrength(password);

  const getStrengthClass = () => {
    if (passwordStrength < 2) return 'weak';
    if (passwordStrength < 4) return 'medium';
    return 'strong';
  }

  const getStrengthWidth = () => {
    if (password.length === 0) return '0%';
    const percentage = Math.min(100, (passwordStrength / 5) * 100);
    return `${percentage}%`;
  }

  const navigate = useNavigate()

  const submit = async e => {
    e.preventDefault()
    setError(null)

    // Frontend validation
    if (password !== confirmPassword) {
      setError("Passwords do not match")
      return
    }

    if (password.length < 5) {
      setError("Password must be at least 5 characters")
      return
    }

    setLoading(true)
    try {
      const resp = await api.post('/api/signup/', { username, password, email })
      const { access, refresh } = resp.data
      setAuthTokens(access, refresh)
      if (onSignup) onSignup({ access, refresh })
      navigate('/')
    } catch (err) {
      setError(err.response?.data || 'Signup failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-background-shapes">
        <div className="auth-shape" style={{ top: '20%', left: '15%', width: '350px', height: '350px', background: 'radial-gradient(circle, rgba(14, 165, 233, 0.3) 0%, transparent 70%)' }}></div>
        <div className="auth-shape" style={{ bottom: '15%', right: '20%', width: '450px', height: '450px', background: 'radial-gradient(circle, rgba(168, 85, 247, 0.3) 0%, transparent 70%)', animationDelay: '-7s' }}></div>
      </div>

      <div className="auth-card" style={{ maxWidth: '500px' }}>
        <div className="auth-header">
          <h2>Create Account</h2>
          <p className="muted">Join us to visualize your data</p>
        </div>

        {error && (
          <div className="auth-error">
            {typeof error === 'string' ? error : JSON.stringify(error)}
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
              id="email"
              type="email"
              className="form-input"
              value={email}
              onChange={e => setEmail(e.target.value)}
              placeholder=" "
              required
            />
            <label htmlFor="email" className="form-label">Email Address</label>
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
            {password && (
              <div className="password-strength">
                <div
                  className={`password-strength-bar ${getStrengthClass()}`}
                  style={{ width: getStrengthWidth() }}
                ></div>
              </div>
            )}
          </div>

          <div className="form-group">
            <input
              id="confirmPassword"
              type={showPassword ? "text" : "password"}
              className="form-input"
              value={confirmPassword}
              onChange={e => setConfirmPassword(e.target.value)}
              placeholder=" "
              required
            />
            <label htmlFor="confirmPassword" className="form-label">Confirm Password</label>
          </div>

          <Button type="submit" isLoading={loading} className="w-full btn-primary" style={{ marginTop: '0.5rem', padding: '0.875rem' }}>
            Create Account
          </Button>
        </form>

        <p style={{ textAlign: 'center', marginTop: '1.5rem', color: 'var(--text-muted)' }}>
          Already have an account? <a href="/login" style={{ color: 'var(--accent)', fontWeight: 600 }}>Log in</a>
        </p>
      </div>
    </div>
  )
}
