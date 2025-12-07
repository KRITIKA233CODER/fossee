import React, { useEffect, useState } from 'react'
import Button from './Button'
import { api } from '../api'

export default function DataTable({ datasetId }) {
  const [rows, setRows] = useState([])
  const [page, setPage] = useState(1)
  const [total, setTotal] = useState(0)

  useEffect(() => {
    if (!datasetId) return
    fetchPage(1)
  }, [datasetId])

  async function fetchPage(p) {
    try {
      const resp = await api.get(`/api/datasets/${datasetId}/table/?page=${p}&page_size=50`)
      const data = resp.data || {}
      setRows(Array.isArray(data.rows) ? data.rows : [])
      setTotal(typeof data.total === 'number' ? data.total : 0)
      setPage(p)
    } catch (err) {
      console.error(err)
      setRows([])
      setTotal(0)
    }
  }

  return (
    <div style={{ marginTop: 12 }}>
      <h4>Rows (showing page {page})</h4>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th style={{ border: '1px solid #ddd' }}>Equipment Name</th>
            <th style={{ border: '1px solid #ddd' }}>Type</th>
            <th style={{ border: '1px solid #ddd' }}>Flowrate</th>
            <th style={{ border: '1px solid #ddd' }}>Pressure</th>
            <th style={{ border: '1px solid #ddd' }}>Temperature</th>
          </tr>
        </thead>
        <tbody>
          {(rows || []).map((r, idx) => (
            <tr key={idx}>
              <td style={{ border: '1px solid #ddd' }}>{r['equipment name'] || r['Equipment Name'] || r.equipment_name || ''}</td>
              <td style={{ border: '1px solid #ddd' }}>{r.type}</td>
              <td style={{ border: '1px solid #ddd' }}>{r.flowrate}</td>
              <td style={{ border: '1px solid #ddd' }}>{r.pressure}</td>
              <td style={{ border: '1px solid #ddd' }}>{r.temperature}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <div style={{ marginTop: 8 }}>
        <Button size="sm" variant="secondary" onClick={() => fetchPage(Math.max(1, page - 1))} disabled={page === 1}>Prev</Button>
        <Button size="sm" variant="secondary" onClick={() => fetchPage(page + 1)} style={{ marginLeft: 8 }}>Next</Button>
        <span style={{ marginLeft: 12 }}>Total: {total}</span>
      </div>
    </div>
  )
}
