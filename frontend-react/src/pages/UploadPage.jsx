import React, { useState, useRef } from 'react'
import { api } from '../api'
import { useNavigate } from 'react-router-dom'
import Button from '../components/Button'
import Card from '../components/Card'

export default function UploadPage() {
  const [file, setFile] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [dragActive, setDragActive] = useState(false)
  const [uploadStep, setUploadStep] = useState(0) // 0: idle, 1: uploading, 2: processing, 3: done
  const navigate = useNavigate()
  const inputRef = useRef(null)

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      validateAndSetFile(e.dataTransfer.files[0])
    }
  }

  const handleChange = (e) => {
    e.preventDefault()
    if (e.target.files && e.target.files[0]) {
      validateAndSetFile(e.target.files[0])
    }
  }

  const validateAndSetFile = (selectedFile) => {
    if (selectedFile.type !== 'text/csv' && !selectedFile.name.endsWith('.csv')) {
      alert('Please upload a CSV file.')
      return
    }
    setFile(selectedFile)
    setUploadStep(0)
  }

  const onButtonClick = () => {
    inputRef.current.click()
  }

  const submit = async () => {
    if (!file) return

    const fd = new FormData()
    fd.append('file', file)

    try {
      setUploading(true)
      setUploadStep(1) // Uploading

      // Simulate progress steps for UX
      setTimeout(() => setUploadStep(2), 1000) // Processing

      const resp = await api.post('/api/datasets/upload/', fd, { headers: { 'Content-Type': 'multipart/form-data' } })

      setUploadStep(3) // Done

      if (resp && resp.data && resp.data.id) {
        localStorage.setItem('last_uploaded_id', resp.data.id)
        setTimeout(() => navigate('/'), 1000)
      }
    } catch (err) {
      console.error(err)
      alert('Upload error: ' + (err.response?.data?.detail || err.message))
      setUploadStep(0)
    } finally {
      setUploading(false)
    }
  }

  const steps = [
    { label: 'CSV uploaded', status: uploadStep >= 1 ? 'completed' : 'pending' },
    { label: 'Validating & cleaning data', status: uploadStep >= 2 ? 'completed' : 'pending' },
    { label: 'Generating analytics', status: uploadStep >= 2 ? 'completed' : 'pending' },
    { label: 'Saving dataset', status: uploadStep >= 3 ? 'completed' : 'pending' },
    { label: 'Done 🎉', status: uploadStep >= 3 ? 'completed' : 'pending' },
  ]

  return (
    <div className="upload-page-container">
      <Card title="Upload Dataset">
        <div className="upload-card-content">
          <form onSubmit={(e) => e.preventDefault()} onDragEnter={handleDrag}>
            <input
              ref={inputRef}
              type="file"
              className="file-input-hidden"
              accept=".csv"
              onChange={handleChange}
            />

            <div
              className={`upload-dropzone ${dragActive ? 'active' : ''}`}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
              onClick={onButtonClick}
            >
              <svg className="upload-icon-large" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>

              <div className="drop-text">
                {file ? file.name : 'Drop your CSV here or click to browse'}
              </div>
              <div className="drop-subtext">
                {file ? `${(file.size / 1024).toFixed(1)} KB` : 'CSV formats, up to 50MB'}
              </div>

              {!file && (
                <Button variant="outline" type="button" onClick={(e) => { e.stopPropagation(); onButtonClick(); }}>
                  Browse File
                </Button>
              )}
            </div>

            {file && (
              <div className="upload-actions">
                <Button
                  variant="primary"
                  onClick={submit}
                  disabled={uploading}
                  isLoading={uploading}
                  size="lg"
                  style={{ width: '100%' }}
                >
                  {uploading ? 'Processing...' : 'Upload Dataset'}
                </Button>
              </div>
            )}
          </form>

          {(uploading || uploadStep > 0) && (
            <div className="upload-status-timeline">
              {steps.map((step, idx) => (
                <div key={idx} className={`timeline-step ${step.status}`}>
                  <div className="step-icon">
                    {step.status === 'completed' ? '✓' : (idx + 1)}
                  </div>
                  <span>{step.label}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </Card>
    </div>
  )
}
