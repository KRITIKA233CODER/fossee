import React, { useContext, useState, useEffect, useRef } from 'react'
import gsap from 'gsap'
import Button from './Button'
import ProfileDropdown from './ProfileDropdown'
import { Link, useLocation } from 'react-router-dom'
import { AuthContext } from '../App'
import { useTheme } from '../context/ThemeContext'

export default function Header() {
  const { auth, logout } = useContext(AuthContext)
  const { theme, toggleTheme } = useTheme()
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const location = useLocation()
  const brandRef = useRef(null)
  const foseeRef = useRef(null)

  useEffect(() => {
    // Animate brand on initial load
    if (brandRef.current) {
      gsap.fromTo(brandRef.current,
        { opacity: 0, x: -30 },
        { opacity: 1, x: 0, duration: 0.8, ease: 'back.out' }
      )
    }
  }, [])

  useEffect(() => {
    // Add hover animation to FOSEE text
    if (foseeRef.current) {
      foseeRef.current.addEventListener('mouseenter', () => {
        gsap.to(foseeRef.current, {
          color: 'var(--accent)',
          duration: 0.3,
          ease: 'power2.out'
        })
      })
      foseeRef.current.addEventListener('mouseleave', () => {
        gsap.to(foseeRef.current, {
          color: 'inherit',
          duration: 0.3,
          ease: 'power2.out'
        })
      })
    }
  }, [])

  if (!auth?.access) return null

  const isActive = (path) => location.pathname === path ? 'nav-link active' : 'nav-link'

  return (
    <header className="navbar">
      <div className="container navbar-content">
        <Link to="/" className="nav-brand" ref={brandRef}>
          <span ref={foseeRef}>FOSSEE</span> Dashboard
        </Link>

        {/* Mobile Menu Button (hidden on dashboard since sidebar has links) */}
        {location.pathname !== '/' && (
          <button
            className="mobile-menu-btn"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            ☰
          </button>
        )}

        {/* Navigation Links (hidden on dashboard since sidebar provides them) */}
        {location.pathname !== '/' && (
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
        )}

        {/* User Actions */}
        <div className="user-menu">
          <Button variant="ghost" size="sm" onClick={toggleTheme} style={{ fontSize: '1.2rem', padding: '0.25rem 0.5rem' }}>
            {theme === 'dark' ? '☀️' : '🌙'}
          </Button>
          <ProfileDropdown />
        </div>
      </div>
    </header>
  )
}
