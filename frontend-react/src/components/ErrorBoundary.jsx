import React from 'react'

export default class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }

  componentDidCatch(error, info) {
    console.error('ErrorBoundary caught', error, info)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: 12 }} className="card">
          <h4>Something went wrong</h4>
          <div style={{ color: '#ffb4b4' }}>{String(this.state.error)}</div>
        </div>
      )
    }
    return this.props.children
  }
}
