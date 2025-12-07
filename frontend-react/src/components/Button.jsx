import React from 'react'
import { Link } from 'react-router-dom'
import './Button.css'

export default function Button({
    children,
    variant = 'primary', // primary, secondary, danger, outline, ghost
    size = 'md', // sm, md, lg
    isLoading = false,
    icon = null,
    className = '',
    to = null, // If provided, renders as Link
    disabled,
    ...props
}) {
    const baseClass = 'premium-btn'
    const variantClass = `btn-${variant}`
    const sizeClass = `btn-${size}`
    const combinedClass = `${baseClass} ${variantClass} ${sizeClass} ${className}`

    const content = (
        <>
            {isLoading && <div className="btn-spinner" />}
            {!isLoading && icon && <span className="btn-icon">{icon}</span>}
            <span style={{ opacity: isLoading ? 0.7 : 1 }}>{children}</span>
        </>
    )

    if (to) {
        return (
            <Link
                to={to}
                className={combinedClass}
                aria-disabled={disabled || isLoading}
                style={disabled || isLoading ? { pointerEvents: 'none' } : {}}
                {...props}
            >
                {content}
            </Link>
        )
    }

    return (
        <button
            className={combinedClass}
            disabled={disabled || isLoading}
            {...props}
        >
            {content}
        </button>
    )
}
