import React, { useState, useRef, useEffect, useContext } from 'react'
import { AuthContext } from '../App'
import './ProfileDropdown.css'

export default function ProfileDropdown() {
    const { auth, logout } = useContext(AuthContext)
    const [isOpen, setIsOpen] = useState(false)
    const dropdownRef = useRef(null)

    // Parse JWT to get user data
    const getUserInfo = () => {
        if (!auth?.access) return { name: 'User', email: '' }
        try {
            const payload = JSON.parse(atob(auth.access.split('.')[1]))
            return {
                name: payload.username || 'User',
                email: payload.email || 'user@example.com'
            }
        } catch (e) {
            console.error('Failed to parse JWT', e)
            return { name: 'User', email: '' }
        }
    }

    const user = getUserInfo()
    const initials = user.name.charAt(0).toUpperCase()

    useEffect(() => {
        const handleClickOutside = (e) => {
            if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
                setIsOpen(false)
            }
        }
        document.addEventListener('mousedown', handleClickOutside)
        return () => document.removeEventListener('mousedown', handleClickOutside)
    }, [])

    return (
        <div className="profile-dropdown" ref={dropdownRef}>
            <button
                className="profile-trigger"
                onClick={() => setIsOpen(!isOpen)}
                title={user.email}
            >
                <div className="profile-avatar">{initials}</div>
            </button>

            {isOpen && (
                <div className="profile-menu">
                    <div className="profile-info">
                        <div className="profile-name">{user.name}</div>
                        <div className="profile-email">{user.email}</div>
                    </div>
                    <div className="profile-divider"></div>
                    <button className="profile-item" onClick={() => setIsOpen(false)}>⚙️ Settings</button>
                    <button className="profile-item" onClick={() => setIsOpen(false)}>👤 Profile</button>
                    <div className="profile-divider"></div>
                    <button className="profile-item danger" onClick={() => { setIsOpen(false); logout(); }}>
                        🚪 Logout
                    </button>
                </div>
            )}
        </div>
    )
}
