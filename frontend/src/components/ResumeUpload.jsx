import React, { useState } from 'react'
import apiClient from '../api/client'

function ResumeUpload({ onUploadComplete }) {
  const [files, setFiles] = useState([])
  const [uploading, setUploading] = useState(false)
  const [message, setMessage] = useState('')

  const handleUpload = async () => {
    if (files.length === 0) {
      setMessage('Please select at least one resume.')
      return
    }

    setUploading(true)
    setMessage('')

    try {
      for (const file of files) {
        const formData = new FormData()
        formData.append('file', file)

        const response = await apiClient.post('/api/upload-resume', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        console.log("UPLOAD RESPONSE:", response)
      }

      setMessage(`✅ ${files.length} resume(s) uploaded successfully!`)

      setFiles([])

      const input = document.getElementById('resume-input')
      if (input) input.value = ''

      if (onUploadComplete) {
        onUploadComplete()
      }

      setTimeout(() => {
        setMessage('')
      }, 3000)

    } catch (error) {
      console.error(error)
      console.error("RESPONSE:", error.response)
      console.error("MESSAGE:", error.message)

      setMessage(
        `❌ Upload failed: ${
          error.response?.data?.detail || error.message
        }`
      )
    } finally {
      setUploading(false)
    }
  }

  return (
    <div
      style={{
        background: 'white',
        borderRadius: '12px',
        padding: '24px',
        boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
        marginBottom: '20px'
      }}
    >
      <h2 style={{ marginBottom: '16px', fontSize: '1.25rem' }}>
        📄 Upload Resume(s)
      </h2>

      <input
        id="resume-input"
        type="file"
        accept=".pdf,.docx"
        multiple
        onChange={(e) => setFiles(Array.from(e.target.files))}
        style={{
          display: 'block',
          marginBottom: '16px',
          padding: '8px',
          border: '1px solid #ddd',
          borderRadius: '4px',
          width: '100%'
        }}
      />

      {files.length > 0 && (
        <div style={{ marginBottom: '16px' }}>
          <strong>Selected Files:</strong>
          <ul>
            {files.map((file, index) => (
              <li key={index}>{file.name}</li>
            ))}
          </ul>
        </div>
      )}

      <button
        onClick={handleUpload}
        disabled={files.length === 0 || uploading}
        style={{
          background: '#667eea',
          color: 'white',
          border: 'none',
          padding: '10px 20px',
          borderRadius: '6px',
          cursor:
            files.length === 0 || uploading
              ? 'not-allowed'
              : 'pointer',
          opacity:
            files.length === 0 || uploading
              ? 0.6
              : 1
        }}
      >
        {uploading
          ? 'Uploading...'
          : `Upload ${files.length || ''} Resume${
              files.length === 1 ? '' : 's'
            }`}
      </button>

      {message && (
        <div
          style={{
            marginTop: '12px',
            padding: '10px',
            borderRadius: '4px',
            background: message.startsWith('✅')
              ? '#d4edda'
              : '#f8d7da',
            color: message.startsWith('✅')
              ? '#155724'
              : '#721c24'
          }}
        >
          {message}
        </div>
      )}
    </div>
  )
}

export default ResumeUpload