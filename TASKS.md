# 📋 FOSSEE Dashboard: Phase-by-Phase Implementation Tasks

## 🎯 Quick Reference
- **Total Phases**: 6
- **Total Tasks**: 68
- **Estimated Duration**: 4-5 weeks
- **Priority Order**: Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6

---

# 🔴 PHASE 1: Professional Alignment & Layout Fixes (WEEK 1)
**Objective**: Fix critical alignment issues and establish proper layout structure
**Estimated Time**: 3-4 days

## Task 1.1: Fix Container Max-Width Issue
**Problem**: All content centered, wasting sidebar space
**Status**: ⏳ TODO

- [ ] **1.1.1** Open `src/styles.css`
- [ ] **1.1.2** Find `.container` class definition
- [ ] **1.1.3** Change from:
  ```css
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
  }
  ```
  To:
  ```css
  .container {
    width: 100%;
    padding: 0 1.5rem;
    margin: 0;
  }
  ```
- [ ] **1.1.4** Test: Content should now align to left, not center

**Files to Modify**: `src/styles.css`

---

## Task 1.2: Fix Main Content Area Expansion
**Problem**: Right column doesn't expand to fill available space
**Status**: ⏳ TODO

- [ ] **1.2.1** Open `src/styles.css`, find `.main-content`
- [ ] **1.2.2** Ensure it has:
  ```css
  .main-content {
    padding: 2rem;
    background-color: transparent;
    width: 100%;
    overflow-x: hidden;
  }
  ```
- [ ] **1.2.3** Verify `.dashboard-layout` has:
  ```css
  .dashboard-layout {
    display: grid;
    grid-template-columns: var(--sidebar-width) 1fr;
    min-height: calc(100vh - var(--nav-height));
    width: 100%;
  }
  ```
- [ ] **1.2.4** Test: Main content should expand fully next to sidebar

**Files to Modify**: `src/styles.css`

---

## Task 1.3: Fix Hamburger Icon Alignment
**Problem**: Sidebar toggle floating right, not properly positioned
**Status**: ⏳ TODO

- [ ] **1.3.1** Open `src/styles.css`, find `.sidebar-top`
- [ ] **1.3.2** Change from:
  ```css
  .sidebar-top { display:flex; justify-content:flex-end }
  ```
  To:
  ```css
  .sidebar-top {
    display: flex;
    justify-content: flex-start;
    align-items: center;
    padding-bottom: 1rem;
    margin-bottom: 0.5rem;
    border-bottom: 1px solid var(--border);
  }
  ```
- [ ] **1.3.3** Update `.sidebar-toggle`:
  ```css
  .sidebar-toggle {
    background: none;
    border: none;
    color: var(--text-muted);
    font-size: 1.2rem;
    cursor: pointer;
    padding: 0.5rem;
    border-radius: 10px;
    transition: all 200ms ease;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  ```
- [ ] **1.3.4** Test: Hamburger should be on left, properly sized

**Files to Modify**: `src/styles.css`

---

## Task 1.4: Update Header Layout
**Problem**: Header content not properly aligned with available space
**Status**: ⏳ TODO

- [ ] **1.4.1** Open `src/styles.css`, find `.navbar-content`
- [ ] **1.4.2** Update to:
  ```css
  .navbar-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    padding: 1rem 2rem;
    gap: 2rem;
  }
  ```
- [ ] **1.4.3** Update `.nav-brand`:
  ```css
  .nav-brand {
    flex: 0 0 auto;
    font-weight: 600;
    font-size: 1.1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  ```
- [ ] **1.4.4** Add `.nav-center`:
  ```css
  .nav-center {
    flex: 1;
    display: flex;
    justify-content: center;
  }
  ```
- [ ] **1.4.5** Update `.user-menu`:
  ```css
  .user-menu {
    flex: 0 0 auto;
    display: flex;
    align-items: center;
    gap: 1rem;
  }
  ```
- [ ] **1.4.6** Test: Logo left, center space, user menu right

**Files to Modify**: `src/styles.css`, `src/components/Header.jsx`

---

## Task 1.5: Create ProfileDropdown Component
**Problem**: No user profile interaction available
**Status**: ⏳ TODO

- [ ] **1.5.1** Create `src/components/ProfileDropdown.jsx`:
  ```jsx
  import React, { useState, useRef, useEffect } from 'react'
  import { useContext } from 'react'
  import { AuthContext } from '../App'
  
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
      document.addEventListener('click', handleClickOutside)
      return () => document.removeEventListener('click', handleClickOutside)
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
            <button className="profile-item">⚙️ Settings</button>
            <button className="profile-item">👤 Profile</button>
            <div className="profile-divider"></div>
            <button className="profile-item danger" onClick={logout}>
              🚪 Logout
            </button>
          </div>
        )}
      </div>
    )
  }
  ```

- [ ] **1.5.2** Create `src/components/ProfileDropdown.css`:
  ```css
  .profile-dropdown {
    position: relative;
  }
  
  .profile-trigger {
    background: none;
    border: none;
    cursor: pointer;
    padding: 0.25rem;
    border-radius: 50%;
    transition: all 200ms ease;
  }
  
  .profile-trigger:hover {
    background: rgba(167, 139, 250, 0.1);
  }
  
  .profile-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--accent) 0%, #d8b4fe 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 600;
    font-size: 0.875rem;
  }
  
  .profile-menu {
    position: absolute;
    top: 100%;
    right: 0;
    width: 240px;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 0.75rem 0;
    margin-top: 0.5rem;
    box-shadow: var(--clay-shadow);
    z-index: 1000;
    animation: slideDown 200ms ease-out;
  }
  
  @keyframes slideDown {
    from {
      opacity: 0;
      transform: translateY(-8px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  .profile-info {
    padding: 0.75rem 1rem;
  }
  
  .profile-name {
    font-weight: 600;
    color: var(--text);
    font-size: 0.875rem;
  }
  
  .profile-email {
    color: var(--text-muted);
    font-size: 0.75rem;
    margin-top: 0.25rem;
    word-break: break-all;
  }
  
  .profile-divider {
    height: 1px;
    background: var(--border);
    margin: 0.5rem 0;
  }
  
  .profile-item {
    width: 100%;
    text-align: left;
    background: none;
    border: none;
    padding: 0.65rem 1rem;
    color: var(--text-muted);
    cursor: pointer;
    transition: all 150ms ease;
    font-size: 0.875rem;
  }
  
  .profile-item:hover {
    background: rgba(167, 139, 250, 0.08);
    color: var(--accent);
  }
  
  .profile-item.danger:hover {
    background: rgba(239, 68, 68, 0.1);
    color: #f87171;
  }
  ```

- [ ] **1.5.3** Update `src/components/Header.jsx` to import and use ProfileDropdown:
  ```jsx
  import ProfileDropdown from './ProfileDropdown'
  
  // In user-menu section, replace Button logout with:
  <ProfileDropdown />
  ```

**Files to Create**: `src/components/ProfileDropdown.jsx`, `src/components/ProfileDropdown.css`
**Files to Modify**: `src/components/Header.jsx`

---

## Task 1.6: Fix Stats Grid Alignment
**Problem**: Stats cards centered and not properly distributed
**Status**: ⏳ TODO

- [ ] **1.6.1** Open `src/styles.css`, find `.stats-grid`
- [ ] **1.6.2** Update to:
  ```css
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
    width: 100%;
  }
  ```
- [ ] **1.6.3** Update `.stat-card`:
  ```css
  .stat-card {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 140px;
  }
  ```
- [ ] **1.6.4** Test: Stats should be in 3-column grid, left-aligned

**Files to Modify**: `src/styles.css`

---

## Task 1.7: Fix Dataset Grid Layout
**Problem**: Dataset list not utilizing available space
**Status**: ⏳ TODO

- [ ] **1.7.1** Open `src/styles.css`, find `.dataset-grid` section
- [ ] **1.7.2** Update to:
  ```css
  .dataset-list.dataset-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1.5rem;
    width: 100%;
  }
  ```
- [ ] **1.7.3** Update `.dataset-card`:
  ```css
  .dataset-card {
    aspect-ratio: 1 / 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 1rem;
    border-radius: 16px;
    background: var(--card);
    border: 1px solid var(--border);
    cursor: pointer;
    transition: all 220ms cubic-bezier(0.34, 1.56, 0.64, 1);
    box-shadow: var(--clay-shadow-sm);
  }
  ```
- [ ] **1.7.4** Test: Grid should adapt to screen width

**Files to Modify**: `src/styles.css`

---

## Task 1.8: Test & Validate Phase 1
**Status**: ⏳ TODO

- [ ] **1.8.1** Desktop (1920x1080): All content left-aligned, sidebar on left, content fills space
- [ ] **1.8.2** Tablet (768px): Sidebar collapses, content expands
- [ ] **1.8.3** Mobile (375px): Single column layout, hamburger functional
- [ ] **1.8.4** Profile dropdown: Shows/hides on click, displays user info
- [ ] **1.8.5** No horizontal scroll: All content fits within viewport

---

# 🟡 PHASE 2: Animations & Interactions (WEEK 2)
**Objective**: Add GSAP animations for professional interactions
**Estimated Time**: 3-4 days
**Dependency**: Phase 1 complete

## Task 2.1: Create GSAP Animation Utilities
**Status**: ⏳ TODO

- [ ] **2.1.1** Create `src/utils/gsapAnimations.js`:
  ```js
  import gsap from 'gsap'
  
  export const animateEntrance = (element, config = {}) => {
    const defaults = { duration: 0.6, delay: 0, stagger: 0 }
    gsap.fromTo(element, 
      { opacity: 0, y: 20 },
      { ...defaults, opacity: 1, y: 0, ease: 'back.out', ...config }
    )
  }
  
  export const animateHover = (element, config = {}) => {
    const defaults = { duration: 0.3 }
    element.addEventListener('mouseenter', () => {
      gsap.to(element, { y: -8, ...defaults, ...config, ease: 'power2.out' })
    })
    element.addEventListener('mouseleave', () => {
      gsap.to(element, { y: 0, ...defaults, ...config, ease: 'power2.out' })
    })
  }
  
  export const animateClick = (element) => {
    gsap.to(element, {
      scale: 0.95,
      duration: 0.1,
      yoyo: true,
      repeat: 1,
      ease: 'power2.inOut'
    })
  }
  
  export const staggerCards = (container, selector) => {
    const cards = container.querySelectorAll(selector)
    gsap.fromTo(cards,
      { opacity: 0, y: 20 },
      { opacity: 1, y: 0, duration: 0.5, stagger: 0.1, ease: 'back.out' }
    )
  }
  ```

- [ ] **2.1.2** Create `src/hooks/useGsapAnimation.js`:
  ```js
  import { useEffect, useRef } from 'react'
  import * as animUtils from '../utils/gsapAnimations'
  
  export const useGsapEntrance = (config) => {
    const ref = useRef(null)
    useEffect(() => {
      if (ref.current) {
        animUtils.animateEntrance(ref.current, config)
      }
    }, [])
    return ref
  }
  
  export const useGsapHover = (config) => {
    const ref = useRef(null)
    useEffect(() => {
      if (ref.current) {
        animUtils.animateHover(ref.current, config)
      }
    }, [])
    return ref
  }
  ```

**Files to Create**: `src/utils/gsapAnimations.js`, `src/hooks/useGsapAnimation.js`

---

## Task 2.2: Animate Dashboard Page Load
**Status**: ⏳ TODO

- [ ] **2.2.1** Update `src/pages/DashboardPage.jsx`:
  ```jsx
  import { useGsapEntrance } from '../hooks/useGsapAnimation'
  import { staggerCards } from '../utils/gsapAnimations'
  
  export default function DashboardPage() {
    // ... existing code
    const statsRef = useGsapEntrance({ stagger: 0.1 })
    const cardsRef = useRef(null)
    
    useEffect(() => {
      if (cardsRef.current) {
        staggerCards(cardsRef.current, '.dataset-card')
      }
    }, [datasets])
    
    return (
      // ... JSX with ref={statsRef} on stats-grid and ref={cardsRef} on cards container
    )
  }
  ```

**Files to Modify**: `src/pages/DashboardPage.jsx`

---

## Task 2.3: Add Hover Animations to Cards
**Status**: ⏳ TODO

- [ ] **2.3.1** Update `src/styles.css`:
  ```css
  .card {
    transition: all 240ms cubic-bezier(0.34, 1.56, 0.64, 1);
  }
  
  .card:hover {
    transform: translateY(-8px);
    box-shadow: var(--clay-shadow);
  }
  
  .dataset-card:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: var(--clay-shadow);
  }
  ```

**Files to Modify**: `src/styles.css`

---

## Task 2.4: Animate Profile Dropdown
**Status**: ⏳ TODO

- [ ] **2.4.1** Update `src/components/ProfileDropdown.jsx`:
  ```jsx
  import gsap from 'gsap'
  
  useEffect(() => {
    if (isOpen && dropdownRef.current?.querySelector('.profile-menu')) {
      const menu = dropdownRef.current.querySelector('.profile-menu')
      gsap.fromTo(menu,
        { opacity: 0, y: -10 },
        { opacity: 1, y: 0, duration: 0.2, ease: 'power2.out' }
      )
    }
  }, [isOpen])
  ```

**Files to Modify**: `src/components/ProfileDropdown.jsx`

---

## Task 2.5: Add Button Click Animations
**Status**: ⏳ TODO

- [ ] **2.5.1** Update `src/components/Button.jsx`:
  ```jsx
  import { animateClick } from '../utils/gsapAnimations'
  
  const handleClick = (e) => {
    if (buttonRef.current) animateClick(buttonRef.current)
    if (onClick) onClick(e)
  }
  ```

**Files to Modify**: `src/components/Button.jsx`

---

## Task 2.6: Add CSS Animation Keyframes
**Status**: ⏳ TODO

- [ ] **2.6.1** Create `src/styles/animations.css`:
  ```css
  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }
  
  @keyframes slideUp {
    from { 
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
  }
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  ```

- [ ] **2.6.2** Import in main `src/styles.css`:
  ```css
  @import './styles/animations.css';
  ```

**Files to Create**: `src/styles/animations.css`
**Files to Modify**: `src/styles.css`

---

## Task 2.7: Test & Validate Phase 2
**Status**: ⏳ TODO

- [ ] **2.7.1** Page loads: Stats cards stagger in
- [ ] **2.7.2** Hover effects: Cards lift smoothly
- [ ] **2.7.3** Profile dropdown: Slides down with animation
- [ ] **2.7.4** Button clicks: Instant scale feedback
- [ ] **2.7.5** 60 FPS: All animations smooth, no jank

---

# 🟢 PHASE 3: Component Refinement (WEEK 2-3)
**Objective**: Update and create new components with professional styling
**Estimated Time**: 3-4 days
**Dependency**: Phase 1 & 2 complete

## Task 3.1: Create MetricCard Component
**Status**: ⏳ TODO

- [ ] **3.1.1** Create `src/components/MetricCard.jsx`:
  ```jsx
  import React, { useEffect, useRef } from 'react'
  import gsap from 'gsap'
  
  export default function MetricCard({
    title,
    value,
    unit = '',
    trend,
    trendPercent = 0,
    icon,
    color = 'blue'
  }) {
    const valueRef = useRef(null)
    
    useEffect(() => {
      if (valueRef.current) {
        gsap.fromTo(valueRef.current,
          { textContent: 0 },
          {
            textContent: typeof value === 'number' ? value : 0,
            duration: 1,
            ease: 'power2.out',
            snap: { textContent: 1 },
            onUpdate() {
              valueRef.current.textContent = Math.ceil(
                gsap.getProperty(valueRef.current, 'textContent')
              )
            }
          }
        )
      }
    }, [value])
    
    return (
      <div className={`metric-card metric-${color}`}>
        <div className="metric-header">
          <span className="metric-title">{title}</span>
          {icon && <span className="metric-icon">{icon}</span>}
        </div>
        <div className="metric-content">
          <div className="metric-value" ref={valueRef}>{value}</div>
          {unit && <span className="metric-unit">{unit}</span>}
        </div>
        {trend && (
          <div className={`metric-trend trend-${trend}`}>
            {trend === 'up' ? '↑' : trend === 'down' ? '↓' : '→'}
            {trendPercent}%
          </div>
        )}
      </div>
    )
  }
  ```

- [ ] **3.1.2** Create `src/components/MetricCard.css`:
  ```css
  .metric-card {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 1.5rem;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    min-height: 140px;
    transition: all 240ms cubic-bezier(0.34, 1.56, 0.64, 1);
    box-shadow: var(--clay-shadow-sm);
  }
  
  .metric-card:hover {
    transform: translateY(-8px);
    box-shadow: var(--clay-shadow);
    border-color: var(--accent);
  }
  
  .metric-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .metric-title {
    font-size: 0.875rem;
    color: var(--text-muted);
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  
  .metric-icon {
    font-size: 1.5rem;
  }
  
  .metric-content {
    display: flex;
    align-items: baseline;
    gap: 0.5rem;
  }
  
  .metric-value {
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--text);
  }
  
  .metric-unit {
    font-size: 0.875rem;
    color: var(--text-muted);
  }
  
  .metric-trend {
    font-size: 0.875rem;
    font-weight: 600;
  }
  
  .trend-up { color: #10b981; }
  .trend-down { color: #ef4444; }
  .trend-neutral { color: var(--text-muted); }
  ```

**Files to Create**: `src/components/MetricCard.jsx`, `src/components/MetricCard.css`

---

## Task 3.2: Update DatasetCard Component
**Status**: ⏳ TODO

- [ ] **3.2.1** Update `src/components/DatasetCard.jsx` (new file):
  ```jsx
  import React from 'react'
  import Badge from './Badge'
  import Button from './Button'
  
  export default function DatasetCard({ dataset, onSelect, onDelete }) {
    return (
      <div className="dataset-card" onClick={() => onSelect?.(dataset)}>
        <div className="dataset-card-icon">📄</div>
        <div className="dataset-card-name">{dataset.filename || `Dataset ${dataset.id}`}</div>
        <div className="dataset-card-meta">{dataset.total_rows} rows</div>
        <div className="dataset-card-badges">
          <Badge variant="success">ANALYZED</Badge>
        </div>
        <div className="dataset-card-actions" onClick={(e) => e.stopPropagation()}>
          <Button size="sm" variant="outline" onClick={() => onSelect?.(dataset)}>
            View
          </Button>
        </div>
      </div>
    )
  }
  ```

- [ ] **3.2.2** Create `src/components/DatasetCard.css`:
  ```css
  .dataset-card {
    aspect-ratio: 1 / 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
    padding: 1rem;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    cursor: pointer;
    transition: all 220ms cubic-bezier(0.34, 1.56, 0.64, 1);
    box-shadow: var(--clay-shadow-sm);
    text-align: center;
    position: relative;
  }
  
  .dataset-card:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: var(--clay-shadow);
    border-color: var(--accent);
  }
  
  .dataset-card-icon {
    font-size: 2.5rem;
  }
  
  .dataset-card-name {
    font-weight: 600;
    color: var(--text);
    font-size: 0.875rem;
    line-height: 1.3;
    word-break: break-word;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
  
  .dataset-card-meta {
    font-size: 0.75rem;
    color: var(--text-muted);
  }
  
  .dataset-card-badges {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    justify-content: center;
    width: 100%;
  }
  
  .dataset-card-actions {
    width: 100%;
    opacity: 0;
    transform: translateY(8px);
    transition: all 200ms ease;
  }
  
  .dataset-card:hover .dataset-card-actions {
    opacity: 1;
    transform: translateY(0);
  }
  ```

**Files to Create**: `src/components/DatasetCard.jsx`, `src/components/DatasetCard.css`

---

## Task 3.3: Create EmptyState Component
**Status**: ⏳ TODO

- [ ] **3.3.1** Create `src/components/EmptyState.jsx`:
  ```jsx
  import React from 'react'
  import Button from './Button'
  
  export default function EmptyState({ icon, title, description, action }) {
    return (
      <div className="empty-state">
        <div className="empty-state-icon">{icon}</div>
        <h3 className="empty-state-title">{title}</h3>
        <p className="empty-state-description">{description}</p>
        {action && (
          <Button variant="primary" onClick={action.onClick}>
            {action.label}
          </Button>
        )}
      </div>
    )
  }
  ```

- [ ] **3.3.2** Create `src/components/EmptyState.css`:
  ```css
  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    padding: 3rem 2rem;
    text-align: center;
    min-height: 300px;
  }
  
  .empty-state-icon {
    font-size: 4rem;
    opacity: 0.5;
  }
  
  .empty-state-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text);
    margin: 0;
  }
  
  .empty-state-description {
    font-size: 0.875rem;
    color: var(--text-muted);
    margin: 0;
    max-width: 400px;
  }
  ```

**Files to Create**: `src/components/EmptyState.jsx`, `src/components/EmptyState.css`

---

## Task 3.4: Update Button Component Styling
**Status**: ⏳ TODO

- [ ] **3.4.1** Update `src/components/Button.css`:
  ```css
  .btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 0.65rem 1.25rem;
    border-radius: 12px;
    border: none;
    font-weight: 600;
    font-size: 0.875rem;
    cursor: pointer;
    transition: all 220ms cubic-bezier(0.34, 1.56, 0.64, 1);
    will-change: transform, box-shadow, background;
  }
  
  .btn-primary {
    background: linear-gradient(135deg, var(--accent) 0%, #d8b4fe 100%);
    color: white;
    box-shadow: var(--clay-shadow-sm);
  }
  
  .btn-primary:hover {
    box-shadow: var(--clay-shadow);
    transform: translateY(-2px);
  }
  
  .btn-primary:active {
    transform: scale(0.95);
  }
  
  .btn-outline {
    background: transparent;
    border: 2px solid var(--border);
    color: var(--text);
  }
  
  .btn-outline:hover {
    border-color: var(--accent);
    background: rgba(167, 139, 250, 0.05);
  }
  ```

**Files to Modify**: `src/components/Button.css`

---

## Task 3.5: Update Card Component
**Status**: ⏳ TODO

- [ ] **3.5.1** Update `src/components/Card.jsx`:
  ```jsx
  import React from 'react'
  import './Card.css'
  
  export default function Card({ title, children, className = '', ...props }) {
    return (
      <div className={`card ${className}`} {...props}>
        {title && <h2 className="card-title">{title}</h2>}
        <div className="card-content">
          {children}
        </div>
      </div>
    )
  }
  ```

- [ ] **3.5.2** Create `src/components/Card.css`:
  ```css
  .card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem;
    transition: all 240ms cubic-bezier(0.34, 1.56, 0.64, 1);
    box-shadow: var(--clay-shadow-sm);
  }
  
  .card:hover {
    transform: translateY(-2px);
    box-shadow: var(--clay-shadow);
  }
  
  .card-title {
    font-size: 1.125rem;
    font-weight: 600;
    color: var(--text);
    margin: 0 0 1rem 0;
  }
  
  .card-content {
    color: var(--text);
  }
  ```

**Files to Create**: `src/components/Card.css`
**Files to Modify**: `src/components/Card.jsx`

---

## Task 3.6: Test & Validate Phase 3
**Status**: ⏳ TODO

- [ ] **3.6.1** MetricCard: Shows animated counters
- [ ] **3.6.2** DatasetCard: Displays in square grid
- [ ] **3.6.3** EmptyState: Shows when no data
- [ ] **3.6.4** All components: Hover effects work
- [ ] **3.6.5** Styling: Consistent across all components

---

# 🔵 PHASE 4: Dashboard Enhancement (WEEK 3)
**Objective**: Upgrade dashboard UI with enhanced stats and better data presentation
**Estimated Time**: 2-3 days
**Dependency**: Phase 1-3 complete

## Task 4.1: Update Stats Section
**Status**: ⏳ TODO

- [ ] **4.1.1** Modify `src/pages/DashboardPage.jsx` stats section:
  ```jsx
  import MetricCard from '../components/MetricCard'
  
  <div className="stats-grid">
    <MetricCard
      title="Total Datasets"
      value={datasets.length}
      unit="files"
      trend="up"
      trendPercent={12}
      icon="📁"
      color="blue"
    />
    <MetricCard
      title="Processing"
      value={0}
      unit="active"
      icon="⚙️"
      color="orange"
    />
    <MetricCard
      title="Storage Used"
      value={124}
      unit="MB"
      trend="down"
      trendPercent={-5}
      icon="💾"
      color="purple"
    />
  </div>
  ```

**Files to Modify**: `src/pages/DashboardPage.jsx`

---

## Task 4.2: Implement Dataset Grid View
**Status**: ⏳ TODO

- [ ] **4.2.1** Update `src/components/DatasetList.jsx`:
  ```jsx
  import DatasetCard from './DatasetCard'
  
  return (
    <div className="dataset-list dataset-grid">
      {datasets.map(d => (
        <DatasetCard
          key={d.id}
          dataset={d}
          onSelect={onSelect}
        />
      ))}
    </div>
  )
  ```

- [ ] **4.2.2** Ensure grid CSS is applied (from Phase 1)
- [ ] **4.2.3** Test: Grid responsive at different breakpoints

**Files to Modify**: `src/components/DatasetList.jsx`

---

## Task 4.3: Add Empty State Handling
**Status**: ⏳ TODO

- [ ] **4.3.1** Update `src/pages/DashboardPage.jsx`:
  ```jsx
  import EmptyState from '../components/EmptyState'
  
  {datasets.length === 0 ? (
    <Card>
      <EmptyState
        icon="📁"
        title="No datasets yet"
        description="Start by uploading your first dataset to begin analysis"
        action={{ label: '+ Upload Dataset', onClick: () => navigate('/upload') }}
      />
    </Card>
  ) : (
    // existing dataset list
  )}
  ```

**Files to Modify**: `src/pages/DashboardPage.jsx`, `src/components/DatasetList.jsx`

---

## Task 4.4: Enhance Analytics Panel
**Status**: ⏳ TODO

- [ ] **4.4.1** Update `src/components/ChartsPanel.jsx`:
  - Add clay card styling
  - Add loading skeleton
  - Add animations on chart load

- [ ] **4.4.2** Test: Charts display with animations

**Files to Modify**: `src/components/ChartsPanel.jsx`

---

## Task 4.5: Test & Validate Phase 4
**Status**: ⏳ TODO

- [ ] **4.5.1** Stats: Show with animated counters
- [ ] **4.5.2** Grid: Displays 3 columns, square cards
- [ ] **4.5.3** Empty state: Shows when no datasets
- [ ] **4.5.4** All responsive: Mobile → Desktop

---

# 🟣 PHASE 5: Advanced Features (WEEK 4)
**Objective**: Add advanced interactions and user features
**Estimated Time**: 3-4 days
**Dependency**: Phase 1-4 complete

## Task 5.1: Create Search/Filter UI
**Status**: ⏳ TODO

- [ ] **5.1.1** Create `src/components/SearchBar.jsx`
- [ ] **5.1.2** Create `src/components/FilterPanel.jsx`
- [ ] **5.1.3** Implement search logic
- [ ] **5.1.4** Test: Search/filter functionality

---

## Task 5.2: Create Toast Notification System
**Status**: ⏳ TODO

- [ ] **5.2.1** Create `src/components/Toast.jsx`
- [ ] **5.2.2** Create `src/hooks/useToast.js`
- [ ] **5.2.3** Implement toast animations
- [ ] **5.2.4** Test: Notifications appear/disappear

---

## Task 5.3: Add Keyboard Navigation
**Status**: ⏳ TODO

- [ ] **5.3.1** Update components for tab navigation
- [ ] **5.3.2** Add escape key handling
- [ ] **5.3.3** Test: All components keyboard accessible

---

## Task 5.4: Test & Validate Phase 5
**Status**: ⏳ TODO

- [ ] **5.4.1** Search: Works as expected
- [ ] **5.4.2** Toasts: Display and auto-dismiss
- [ ] **5.4.3** Keyboard: All interactive elements accessible

---

# ⭐ PHASE 6: Polish & Optimization (WEEK 4-5)
**Objective**: Final polish, testing, and performance optimization
**Estimated Time**: 3-5 days
**Dependency**: Phase 1-5 complete

## Task 6.1: Performance Optimization
**Status**: ⏳ TODO

- [ ] **6.1.1** Run Lighthouse audit
- [ ] **6.1.2** Optimize images
- [ ] **6.1.3** Code splitting by route
- [ ] **6.1.4** Minify CSS/JS
- [ ] **6.1.5** Target: 90+ Lighthouse score

---

## Task 6.2: Accessibility Audit
**Status**: ⏳ TODO

- [ ] **6.2.1** WCAG 2.1 AA compliance check
- [ ] **6.2.2** Screen reader testing
- [ ] **6.2.3** Color contrast verification
- [ ] **6.2.4** ARIA labels update
- [ ] **6.2.5** Test with axe DevTools

---

## Task 6.3: Cross-Browser Testing
**Status**: ⏳ TODO

- [ ] **6.3.1** Chrome/Edge latest
- [ ] **6.3.2** Firefox latest
- [ ] **6.3.3** Safari latest
- [ ] **6.3.4** Mobile browsers (iOS Safari, Chrome Mobile)

---

## Task 6.4: Dark/Light Mode Verification
**Status**: ⏳ TODO

- [ ] **6.4.1** Test all components in dark mode
- [ ] **6.4.2** Test all components in light mode
- [ ] **6.4.3** Verify color contrast in both themes
- [ ] **6.4.4** Test theme persistence

---

## Task 6.5: Final QA & Documentation
**Status**: ⏳ TODO

- [ ] **6.5.1** Document component APIs
- [ ] **6.5.2** Create style guide
- [ ] **6.5.3** Record demo video
- [ ] **6.5.4** User acceptance testing
- [ ] **6.5.5** Launch!

---

## 📊 Quick Task Reference

### Phase 1 Tasks: 8 tasks (Alignment)
- 1.1: Fix centering
- 1.2: Expand main content
- 1.3: Align hamburger
- 1.4: Header layout
- 1.5: Profile dropdown
- 1.6: Stats grid
- 1.7: Dataset grid
- 1.8: Test & validate

### Phase 2 Tasks: 7 tasks (Animations)
- 2.1: GSAP utilities
- 2.2: Dashboard animations
- 2.3: Card hover
- 2.4: Profile dropdown animation
- 2.5: Button animations
- 2.6: CSS keyframes
- 2.7: Test & validate

### Phase 3 Tasks: 6 tasks (Components)
- 3.1: MetricCard
- 3.2: DatasetCard
- 3.3: EmptyState
- 3.4: Button styling
- 3.5: Card component
- 3.6: Test & validate

### Phase 4 Tasks: 5 tasks (Dashboard)
- 4.1: Stats section
- 4.2: Dataset grid
- 4.3: Empty state
- 4.4: Analytics
- 4.5: Test & validate

### Phase 5 Tasks: 4 tasks (Advanced)
- 5.1: Search/filter
- 5.2: Toast notifications
- 5.3: Keyboard navigation
- 5.4: Test & validate

### Phase 6 Tasks: 5 tasks (Polish)
- 6.1: Performance
- 6.2: Accessibility
- 6.3: Cross-browser
- 6.4: Theme verification
- 6.5: Final QA

**Total: 35 tasks across 6 phases**

---

## 🚀 Getting Started

**To begin Phase 1:**
1. Open this file
2. Start with Task 1.1
3. Check off items as completed
4. Move to next task only when previous is validated
5. Refer to IMPLEMENTATION_PLAN.md for architecture details

**Track Progress:**
- Update status: ⏳ TODO → ⏸️ IN_PROGRESS → ✅ DONE
- Note any blockers or questions
- Link to commits/PRs for reference

---

**Last Updated**: February 1, 2026 | **Version**: 1.0
