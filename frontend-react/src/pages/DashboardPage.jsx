import React, { useEffect, useState, useContext } from 'react'
import Button from '../components/Button'
import Card from '../components/Card'
import Badge from '../components/Badge'
import { api } from '../api'
import DatasetList from '../components/DatasetList'
import DatasetModal from '../components/DatasetModal'
import ChartsPanel from '../components/ChartsPanel'
import { Link } from 'react-router-dom'
import { AuthContext } from '../App'

export default function DashboardPage() {
  const [datasets, setDatasets] = useState([])
  const [selected, setSelected] = useState(null)
  const [showModal, setShowModal] = useState(false)
  const [activeTab, setActiveTab] = useState('datasets') // 'datasets' or 'analytics'
  const [analyticsDatasetId, setAnalyticsDatasetId] = useState('')
  // Sidebar collapsed state (icons only)
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)

  useEffect(() => {
    fetchDatasets()
  }, [])

  useEffect(() => {
    if (datasets.length > 0 && !analyticsDatasetId) {
      setAnalyticsDatasetId(datasets[0].id)
    }
  }, [datasets, analyticsDatasetId])

  async function fetchDatasets() {
    try {
      const resp = await api.get('/api/datasets/')
      const data = resp.data && resp.data.results ? resp.data.results : resp.data
      const arr = Array.isArray(data) ? data : []
      setDatasets(arr)

      const last = localStorage.getItem('last_uploaded_id')
      if (last) {
        const found = arr.find(x => String(x.id) === String(last))
        if (found) {
          setSelected(found)
          setShowModal(true)
          localStorage.removeItem('last_uploaded_id')
        }
      }
    } catch (err) {
      console.error(err)
    }
  }

  const analyticsDataset = datasets.find(d => String(d.id) === String(analyticsDatasetId))

  return (
    <div className="dashboard-layout mobile-stack">
      {/* Sidebar (collapsible: click ☰ to expand labels) */}
      <aside className={`sidebar ${sidebarCollapsed ? 'collapsed' : ''}`}>
        <div className="sidebar-top">
          <button className="sidebar-toggle" aria-label="Toggle sidebar" onClick={() => setSidebarCollapsed(s => !s)}>☰</button>
        </div>

        <nav className="sidebar-nav">
          <div
            className={`sidebar-item ${activeTab === 'datasets' ? 'active' : ''} `}
            onClick={() => setActiveTab('datasets')}
            style={{ cursor: 'pointer' }}
            title="Datasets"
          >
            <span className="sidebar-icon" aria-hidden>📚</span>
            <span className="sidebar-label">Datasets</span>
          </div>

          <Link to="/upload" className="sidebar-item" title="Upload New">
            <span className="sidebar-icon" aria-hidden>⬆️</span>
            <span className="sidebar-label">Upload New</span>
          </Link>

          <div
            className={`sidebar-item ${activeTab === 'analytics' ? 'active' : ''} `}
            onClick={() => setActiveTab('analytics')}
            style={{ cursor: 'pointer' }}
            title="Analytics"
          >
            <span className="sidebar-icon" aria-hidden>📊</span>
            <span className="sidebar-label">Analytics</span>
          </div>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        <div className="container">

          {activeTab === 'datasets' ? (
            <>
              {/* Stats Row */}
              <div className="stats-grid">
                <Card className="stat-card">
                  <h3>Total Datasets</h3>
                  <div className="stat-value">{datasets.length}</div>
                </Card>
                <Card className="stat-card">
                  <h3>Processing</h3>
                  <div className="stat-value">0</div>
                </Card>
                <Card className="stat-card">
                  <h3>Storage Used</h3>
                  <div className="stat-value">124 MB</div>
                </Card>
              </div>

              {/* Content Area */}
              <Card>
                <div className="flex items-center justify-between" style={{ marginBottom: '1.5rem' }}>
                  <h2 className="section-title" style={{ margin: 0 }}>Recent Datasets</h2>
                  <Button to="/upload" variant="primary">
                    + Upload
                  </Button>
                </div>

                <DatasetList
                  datasets={datasets}
                  onSelect={(d) => { setSelected(d); setShowModal(true) }}
                />
              </Card>
            </>
          ) : (
            <>
              {/* Analytics View */}
              <div className="analytics-header">
                <h2 className="section-title" style={{ margin: 0 }}>Analytics Overview</h2>
                <div className="analytics-controls">
                  <select
                    className="dataset-select"
                    value={analyticsDatasetId}
                    onChange={(e) => setAnalyticsDatasetId(e.target.value)}
                  >
                    {datasets.map(d => (
                      <option key={d.id} value={d.id}>{d.filename || `Dataset ${d.id}`}</option>
                    ))}
                  </select>
                  <Button variant="outline" size="sm" onClick={fetchDatasets}>
                    Refresh
                  </Button>
                </div>
              </div>

              {analyticsDataset ? (
                <ChartsPanel dataset={analyticsDataset} />
              ) : (
                <div className="muted">No datasets available. Please upload one first.</div>
              )}
            </>
          )}

        </div>

        {/* Modal */}
        {showModal && selected && (
          <DatasetModal dataset={selected} onClose={() => setShowModal(false)} />
        )}
      </main>
    </div>
  )
}
