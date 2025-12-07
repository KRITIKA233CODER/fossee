import React from 'react'
import Button from './Button'
import Badge from './Badge'
import { api, BASE_URL } from '../api'

function buildMediaUrl(csvField) {
  if (!csvField) return null
  if (csvField.startsWith('http://') || csvField.startsWith('https://')) return csvField
  if (csvField.startsWith('/')) return `${BASE_URL}${csvField}`
  return `${BASE_URL}/media/${csvField}`
}

async function downloadFile(url, filename) {
  try {
    const resp = await api.get(url, { responseType: 'blob' })
    const blob = new Blob([resp.data])
    const link = document.createElement('a')
    link.href = window.URL.createObjectURL(blob)
    link.download = filename || 'download'
    document.body.appendChild(link)
    link.click()
    link.remove()
  } catch (err) {
    console.error('Download failed', err)
    alert('Download failed: ' + (err.response?.data?.detail || err.message))
  }
}

export default function DatasetList({ datasets, onSelect }) {
  if (!datasets || datasets.length === 0) {
    return <div className="muted text-center py-8">No datasets found. Upload one to get started.</div>
  }

  return (
    <div className="dataset-list">
      {datasets.map(d => {
        const csvUrl = buildMediaUrl(d.csv_file || '')
        const reportEndpoint = `/api/datasets/${d.id}/report/`

        // Determine badges
        const badges = []
        if (d.total_rows > 10000) badges.push({ label: 'LARGE', variant: 'warning' })
        // Mock logic for other badges since backend flags might not exist yet
        const isRecent = (new Date() - new Date(d.uploaded_at)) < (24 * 60 * 60 * 1000)
        if (isRecent) badges.push({ label: 'NEW', variant: 'success' })

        return (
          <div key={d.id} className="dataset-card" onClick={() => onSelect(d)}>
            {/* Left: Icon & Info */}
            <div className="dataset-left">
              <div className="dataset-icon-wrapper">
                <span className="dataset-file-icon">📄</span>
              </div>
              <div className="dataset-info">
                <div className="dataset-name">{d.filename || `Dataset ${d.id}`}</div>
                <div className="dataset-meta">
                  {d.uploaded_at ? new Date(d.uploaded_at).toLocaleString() : 'Unknown date'} • {d.total_rows || 0} rows
                </div>
              </div>
            </div>

            {/* Middle: Tags */}
            <div className="dataset-tags">
              {badges.map((b, i) => (
                <Badge key={i} variant={b.variant}>{b.label}</Badge>
              ))}
              {/* Always show analyzed if it exists in list */}
              <Badge variant="info">ANALYZED</Badge>
            </div>

            {/* Right: Actions */}
            <div className="dataset-actions" onClick={e => e.stopPropagation()}>
              <Button size="sm" variant="outline" onClick={() => onSelect(d)}>View</Button>
              {csvUrl && (
                <Button size="sm" variant="ghost" onClick={() => downloadFile(csvUrl, d.filename || 'data.csv')}>CSV</Button>
              )}
              <Button size="sm" variant="ghost" onClick={() => downloadFile(reportEndpoint, `${d.filename || 'report'}.pdf`)}>PDF</Button>
            </div>
          </div>
        )
      })}
    </div>
  )
}
