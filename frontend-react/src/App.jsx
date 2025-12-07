import React, { useState, useEffect } from 'react'
import { Routes, Route, Link, Navigate, useNavigate } from 'react-router-dom'
import LoginPage from './pages/LoginPage'
import UploadPage from './pages/UploadPage'
import SignupPage from './pages/SignupPage'
import DashboardPage from './pages/DashboardPage'
import { api, setAuthTokens, clearAuthTokens, getAccess } from './api'
import Header from './components/Header'
import { ThemeProvider } from './context/ThemeContext'

export const AuthContext = React.createContext()

function ProtectedRoute({ children }) {
  const token = getAccess()
  if (!token) return <Navigate to="/login" />
  return children
}

export default function App() {
  const [auth, setAuth] = useState({ access: null, refresh: null })
  const navigate = useNavigate()

  useEffect(() => {
    // load tokens from localStorage
    const access = localStorage.getItem('access')
    const refresh = localStorage.getItem('refresh')
    if (access) setAuth({ access, refresh })
  }, [])

  const login = ({ access, refresh }) => {
    setAuth({ access, refresh })
    setAuthTokens(access, refresh)
    navigate('/')
  }

  const logout = () => {
    setAuth({ access: null, refresh: null })
    clearAuthTokens()
    navigate('/login')
  }

  return (
    <ThemeProvider>
      <AuthContext.Provider value={{ auth, login, logout }}>
        <div className="app-root">
          <div className="aurora-bg" />
          <div className="app-content">
            <Header />
            <main className="container">
              <Routes>
                <Route path="/login" element={<LoginPage onLogin={login} />} />
                <Route path="/signup" element={<SignupPage onSignup={login} />} />
                <Route path="/upload" element={<ProtectedRoute><UploadPage /></ProtectedRoute>} />
                <Route path="/" element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
              </Routes>
            </main>
          </div>
        </div>
      </AuthContext.Provider>
    </ThemeProvider>
  )
}
