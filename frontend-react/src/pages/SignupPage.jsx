import React, { useState } from 'react'
import Button from '../components/Button'
import { useNavigate } from 'react-router-dom'
import { api, setAuthTokens } from '../api'

export default function SignupPage({ onSignup }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [email, setEmail] = useState('')
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const submit = async e => {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      const resp = await api.post('/api/signup/', { username, password, email })
      const { access, refresh } = resp.data
      setAuthTokens(access, refresh)
      if (onSignup) onSignup({ access, refresh })
      navigate('/')
    } catch (err) {
      setError(err.response?.data || 'Signup failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h2>Welcome</h2>
        <p className="muted">Sign up to access datasets and visualizations</p>
        <form onSubmit={submit} className="form-grid">
          <label>Username</label>
          <input value={username} onChange={e => setUsername(e.target.value)} />
          <label>Password</label>
          <input type="password" value={password} onChange={e => setPassword(e.target.value)} />
          <label>Email</label>
          <input type="email" value={email} onChange={e => setEmail(e.target.value)} />
          <div />
          <Button type="submit" isLoading={loading} className="w-full">Sign up</Button>
        </form>
        <p>Already have an account? <a href="/login">Log in</a></p>
        {error && <div className="error">{JSON.stringify(error)}</div>}
      </div>
    </div>
  )
}
