import React, { useContext, useState } from 'react'
import Button from './Button'
import { Link, useLocation } from 'react-router-dom'
import { AuthContext } from '../App'
import { useTheme } from '../context/ThemeContext'

export default function Header() {
  const { auth, logout } = useContext(AuthContext)
  const { theme, toggleTheme } = useTheme()
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const location = useLocation()

  if (!auth?.access) return null

  const isActive = (path) => location.pathname === path ? 'nav-link active' : 'nav-link'

  return (
    <header className="navbar">
      <div className="container navbar-content">
        <Link to="/" className="nav-brand">
          <span>FOSEE</span> Dashboard
        </Link>

        {/* Mobile Menu Button */}
        <button
          className="mobile-menu-btn"
          onClick={() => setIsMenuOpen(!isMenuOpen)}
        >
          ☰
        </button>

        {/* Navigation Links */}
        <nav className={`nav-links ${isMenuOpen ? 'open' : ''}`}>
          <Link to="/" className={isActive('/')} onClick={() => setIsMenuOpen(false)}>
            Dashboard
          </Link>
          <Link to="/upload" className={isActive('/upload')} onClick={() => setIsMenuOpen(false)}>
            Upload
          </Link>
          <Link to="/analytics" className={isActive('/analytics')} onClick={() => setIsMenuOpen(false)}>
            Analytics
          </Link>
        </nav>

        {/* User Actions */}
        <div className="user-menu">
          <Button variant="ghost" size="sm" onClick={toggleTheme} style={{ fontSize: '1.2rem', padding: '0.25rem 0.5rem' }}>
            {theme === 'dark' ? '☀️' : '🌙'}
          </Button>
          <div className="avatar">
            U
          </div>
          <Button variant="ghost" onClick={logout}>
            Logout
          </Button>
        </div>
      </div>
    </header>
  )
}
