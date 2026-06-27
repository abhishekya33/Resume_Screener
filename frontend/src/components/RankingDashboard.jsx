import React, { useState, useEffect } from 'react'
import axios from 'axios'

const API_BASE = 'http://localhost:8000'

function RankingDashboard() {
  const [resumes, setResumes] = useState([])
  const [jobDesc, setJobDesc] = useState('')
  const [rankings, setRankings] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchResumes()
  }, [])

  const fetchResumes = async () => {
    try {
      const response = await axios.get(`${API_BASE}/api/resumes`)
      setResumes(response.data)
    } catch (error) {
      console.error('Failed to fetch resumes:', error)
    }
  }

  const handleRank = async () => {
    if (!jobDesc.trim()) {
      alert('Please enter a job description')
      return
    }
    
    if (resumes.length === 0) {
      alert('Please upload at least one resume first')
      return
    }
    
    setLoading(true)
    
    try {
      const jdResponse = await axios.post(
    `${API_BASE}/api/job-description`,
    { text: jobDesc },  // Note: { text: jobDesc } not just jobDesc
    { headers: { 'Content-Type': 'application/json' } }
      )
      
      const rankResponse = await axios.post(`${API_BASE}/api/rank`, {
        job_description_id: jdResponse.data.job_description_id,
        resume_ids: resumes.map(r => r.id)
      })
      
      setRankings(rankResponse.data.rankings)
    } catch (error) {
      console.error('Ranking failed:', error)
      alert(`Ranking failed: ${error.response?.data?.detail || error.message}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{
      background: 'white',
      borderRadius: '12px',
      padding: '24px',
      boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
    }}>
      <h2 style={{ marginBottom: '16px', fontSize: '1.25rem' }}>🎯 Job Description & Ranking</h2>
      
      <div style={{ marginBottom: '24px' }}>
        <label style={{ display: 'block', marginBottom: '8px', fontWeight: '500' }}>
          Paste Job Description:
        </label>
        <textarea
          value={jobDesc}
          onChange={(e) => setJobDesc(e.target.value)}
          rows={6}
          placeholder="Example: We are looking for a Software Engineer with experience in Python, React, and SQL..."
          style={{
            width: '100%',
            padding: '12px',
            border: '1px solid #ddd',
            borderRadius: '8px',
            fontFamily: 'monospace',
            fontSize: '14px'
          }}
        />
      </div>
      
      <div style={{ marginBottom: '16px' }}>
        <p><strong>📁 Uploaded Resumes:</strong> {resumes.length} file(s)</p>
        {resumes.map(r => <p key={r.id} style={{ fontSize: '12px', color: '#666' }}>• {r.filename}</p>)}
      </div>
      
      <button
        onClick={handleRank}
        disabled={loading || !jobDesc.trim() || resumes.length === 0}
        style={{
          background: '#764ba2',
          color: 'white',
          border: 'none',
          padding: '12px 24px',
          borderRadius: '8px',
          cursor: loading || !jobDesc.trim() || resumes.length === 0 ? 'not-allowed' : 'pointer',
          opacity: loading || !jobDesc.trim() || resumes.length === 0 ? 0.6 : 1,
          fontSize: '16px',
          fontWeight: '500'
        }}
      >
        {loading ? '🤖 Analyzing Candidates...' : '📊 Rank Candidates'}
      </button>
      
      {rankings && rankings.length > 0 && (
        <div style={{ marginTop: '32px' }}>
          <h3 style={{ marginBottom: '16px', fontSize: '1.1rem' }}>🏆 Ranked Candidates</h3>
          {rankings.map((candidate, idx) => (
            <div key={idx} style={{
              border: '1px solid #e0e0e0',
              borderRadius: '10px',
              padding: '16px',
              marginBottom: '16px'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <div>
                  <strong>#{idx + 1}: {candidate.candidate_name}</strong>
                  <div style={{ fontSize: '12px', color: '#666' }}>{candidate.filename}</div>
                </div>
                <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#667eea' }}>
                  {candidate.total_score}%
                </div>
              </div>
              <div style={{ marginTop: '8px', fontSize: '12px' }}>
                Semantic: {candidate.semantic_score}% | Keyword: {candidate.keyword_score}%
              </div>
              {candidate.extracted_skills?.length > 0 && (
                <div style={{ marginTop: '8px' }}>
                  <span style={{ fontSize: '12px', color: '#666' }}>Skills: </span>
                  {candidate.extracted_skills.slice(0, 5).map((s, i) => (
                    <span key={i} style={{ background: '#e3f2fd', padding: '2px 8px', borderRadius: '12px', fontSize: '11px', marginRight: '5px' }}>
                      {s}
                    </span>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default RankingDashboard