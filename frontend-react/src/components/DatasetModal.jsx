import React from 'react'
import Button from './Button'
import ChartsPanel from './ChartsPanel'
import DataTable from './DataTable'
import { api, BASE_URL } from '../api'

export default function DatasetModal({ dataset, onClose }) {
  if (!dataset) return null

  const downloadReport = () => {
    const url = `/api/datasets/${dataset.id}/report/`
    api.get(url, { responseType: 'blob' })
      .then(r => {
        const blob = new Blob([r.data])
        const link = document.createElement('a')
        link.href = window.URL.createObjectURL(blob)
        link.download = `${dataset.filename || dataset.id}.pdf`
        document.body.appendChild(link)
        link.click()
        link.remove()
      })
      .catch(e => alert('Download failed'))
  }

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-card" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <div>
            <h3 style={{ margin: 0 }}>{dataset.filename || dataset.id}</h3>
            <div className="muted">Uploaded: {dataset.uploaded_at ? new Date(dataset.uploaded_at).toLocaleString() : 'unknown'}</div>
          </div>
          <div>
            <Button variant="ghost" onClick={downloadReport}>Download PDF</Button>
            <Button variant="secondary" onClick={onClose} style={{ marginLeft: 8 }}>Close</Button>
          </div>
        </div>
        <div className="modal-body">
          <div className="modal-left">
            <ChartsPanel dataset={dataset} />
          </div>
          <div className="modal-right">
            <DataTable datasetId={dataset.id} />
          </div>
        </div>
      </div>
    </div>
  )
}
