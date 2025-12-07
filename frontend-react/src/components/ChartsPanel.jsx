import React, { useEffect, useState } from 'react'
import { Bar, Scatter, Line } from 'react-chartjs-2'
import { api } from '../api'
import Card from './Card'
import { generateInsights } from '../utils/analyticsUtils'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
  Title,
} from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, BarElement, PointElement, LineElement, Tooltip, Legend, Title)

export default function ChartsPanel({ dataset }) {
  const [summary, setSummary] = useState(null)
  const [renderError, setRenderError] = useState(null)
  const [scatterRows, setScatterRows] = useState([])

  useEffect(() => {
    if (!dataset) return
    fetchSummary()
  }, [dataset])

  useEffect(() => {
    if (!dataset) return
    api.get(`/api/datasets/${dataset.id}/table/?page=1&page_size=200`)
      .then(r => setScatterRows(r.data.rows || []))
      .catch(() => setScatterRows([]))
  }, [dataset])

  async function fetchSummary() {
    try {
      const resp = await api.get(`/api/datasets/${dataset.id}/summary/`)
      setSummary(resp.data)
    } catch (err) {
      console.error(err)
      setRenderError(err)
    }
  }

  if (!summary) return <div className="muted">Loading analytics...</div>

  // --- Data Prep ---

  // 1. Metrics
  const metrics = [
    { label: 'Avg Flowrate', value: summary.stats?.flowrate?.mean?.toFixed(2) || '-', unit: 'L/min' },
    { label: 'Avg Pressure', value: summary.stats?.pressure?.mean?.toFixed(2) || '-', unit: 'bar' },
    { label: 'Avg Temp', value: summary.stats?.temperature?.mean?.toFixed(2) || '-', unit: '°C' },
    { label: 'Total Rows', value: dataset.total_rows || '-', unit: '' },
  ]

  // 2. Type Distribution
  const typeLabels = Object.keys(summary.type_distribution || {})
  const typeCounts = Object.values(summary.type_distribution || {}).map(v => Number(v) || 0)
  const barData = {
    labels: typeLabels,
    datasets: [{
      label: 'Count',
      data: typeCounts,
      backgroundColor: 'rgba(56, 189, 248, 0.6)',
      borderRadius: 4,
    }]
  }

  // 3. Scatter (Flow vs Temp)
  const scatterPoints = (scatterRows && scatterRows.length > 0)
    ? scatterRows.map(r => ({ x: parseFloat(r.temperature), y: parseFloat(r.flowrate) }))
      .filter(p => Number.isFinite(p.x) && Number.isFinite(p.y))
    : []

  const scatterData = {
    datasets: [{
      label: 'Flowrate vs Temperature',
      data: scatterPoints,
      backgroundColor: 'rgba(244, 63, 94, 0.6)',
    }]
  }

  // 4. Histograms
  const histograms = summary.histograms || {}
  const makeHistBar = (hist, color) => {
    if (!hist || !hist.bins) return null
    const labels = hist.bins.slice(0, -1).map((b, i) => `${Number(b).toFixed(1)}`)
    return {
      labels,
      datasets: [{
        label: 'Frequency',
        data: hist.counts,
        backgroundColor: color,
        borderRadius: 4,
      }]
    }
  }
  const flowHist = makeHistBar(histograms.flowrate, 'rgba(16, 185, 129, 0.6)')

  // 5. Insights
  const insights = generateInsights(summary, dataset)

  // 6. Top Values
  const topValues = summary.top_values || {}

  // Chart Options
  const commonOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: 'rgba(15, 23, 42, 0.9)',
        titleColor: '#f8fafc',
        bodyColor: '#cbd5e1',
        padding: 10,
        cornerRadius: 8,
      }
    },
    scales: {
      x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
      y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } }
    }
  }

  if (renderError) return <Card>Error loading charts: {String(renderError)}</Card>

  return (
    <div className="charts-panel">
      {/* Metrics Row */}
      <div className="metrics-grid">
        {metrics.map((m, i) => (
          <Card key={i} className="metric-card">
            <div className="metric-label">{m.label}</div>
            <div className="metric-value">{m.value}</div>
            <div className="metric-unit muted">{m.unit}</div>
          </Card>
        ))}
      </div>

      {/* Main Charts Grid */}
      <div className="charts-grid-layout">
        <Card title="Equipment Type Distribution">
          <div className="chart-container">
            <Bar data={barData} options={commonOptions} />
          </div>
        </Card>

        <Card title="Flowrate Distribution">
          <div className="chart-container">
            {flowHist ? <Bar data={flowHist} options={commonOptions} /> : <div className="muted">No data</div>}
          </div>
        </Card>

        <Card title="Flowrate vs Temperature">
          <div className="chart-container">
            <Scatter data={scatterData} options={commonOptions} />
          </div>
        </Card>
      </div>

      {/* Insights & Top Values */}
      <div className="insights-grid">
        <Card title="Automated Insights">
          <ul style={{ paddingLeft: '1.2rem', margin: 0 }}>
            {insights.map((insight, idx) => (
              <li key={idx} style={{ marginBottom: '0.5rem', color: 'var(--text-muted)' }}>
                {insight}
              </li>
            ))}
          </ul>
        </Card>

        <Card title="Top Flow Rates">
          <div className="top-values-list">
            {(() => {
              const fv = topValues.flowrate
              const list = Array.isArray(fv) ? fv : (fv && fv.top ? fv.top : [])
              return list.slice(0, 5).map((item, idx) => (
                <div key={idx} className="flex justify-between items-center" style={{ padding: '0.5rem 0', borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                  <span className="text-muted">{item['equipment name'] || item.equipment_name || 'Unknown'}</span>
                  <span style={{ fontWeight: 600, color: 'var(--accent)' }}>{item.flowrate || item.value}</span>
                </div>
              ))
            })()}
          </div>
        </Card>
      </div>
    </div>
  )
}
