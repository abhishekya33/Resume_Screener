import React, { useState } from 'react'
import ResumeUpload from './components/ResumeUpload'
import RankingDashboard from './components/RankingDashboard'

function App() {
  const [refreshKey, setRefreshKey] = useState(0)

  const handleUploadComplete = () => {
    setRefreshKey(prev => prev + 1)
  }

  return (
    <div style={{ 
      minHeight: '100vh', 
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      padding: '20px'
    }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <header style={{ textAlign: 'center', marginBottom: '30px' }}>
          <h1 style={{ color: 'white', fontSize: '2.5rem', margin: 0 }}>🤖 AI Resume Screener</h1>
          <p style={{ color: 'rgba(255,255,255,0.9)' }}>
            Upload resumes and job description - let AI find the best match
          </p>
        </header>
        
        <ResumeUpload onUploadComplete={handleUploadComplete} />
        <RankingDashboard key={refreshKey} />
      </div>
    </div>
  )
}

export default App