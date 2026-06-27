import React, { useState } from 'react'
import axios from 'axios'

const API_BASE = 'http://localhost:8000'

function ResumeUpload({ onUploadComplete }) {
  const [file, setFile] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [message, setMessage] = useState('')

  const handleUpload = async () => {
    if (!file) {
      setMessage('Please select a file')
      return
    }
    
    setUploading(true)
    setMessage('')
    
    const formData = new FormData()
    formData.append('file', file)
    
    try {
      const response = await axios.post(`${API_BASE}/api/upload-resume`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      
      setMessage(`✅ ${response.data.filename} uploaded successfully!`)
      setFile(null)
      
      const fileInput = document.getElementById('resume-input')
      if (fileInput) fileInput.value = ''
      
      if (onUploadComplete) onUploadComplete()
      
      setTimeout(() => setMessage(''), 3000)
    } catch (error) {
      console.error('Upload failed:', error)
      setMessage(`❌ Upload failed: ${error.response?.data?.detail || error.message}`)
    } finally {
      setUploading(false)
    }
  }

  return (
    <div style={{
      background: 'white',
      borderRadius: '12px',
      padding: '24px',
      boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
      marginBottom: '20px'
    }}>
      <h2 style={{ marginBottom: '16px', fontSize: '1.25rem' }}>📄 Upload Resume</h2>
      
      <input
        id="resume-input"
        type="file"
        accept=".pdf,.docx"
        onChange={(e) => setFile(e.target.files[0])}
        style={{
          display: 'block',
          marginBottom: '16px',
          padding: '8px',
          border: '1px solid #ddd',
          borderRadius: '4px',
          width: '100%'
        }}
      />
      
      <button
        onClick={handleUpload}
        disabled={!file || uploading}
        style={{
          background: '#667eea',
          color: 'white',
          border: 'none',
          padding: '10px 20px',
          borderRadius: '6px',
          cursor: !file || uploading ? 'not-allowed' : 'pointer',
          opacity: !file || uploading ? 0.6 : 1
        }}
      >
        {uploading ? 'Uploading...' : 'Upload Resume'}
      </button>
      
      {message && (
        <div style={{
          marginTop: '12px',
          padding: '10px',
          borderRadius: '4px',
          background: message.startsWith('✅') ? '#d4edda' : '#f8d7da',
          color: message.startsWith('✅') ? '#155724' : '#721c24'
        }}>
          {message}
        </div>
      )}
    </div>
  )
}

export default ResumeUpload