import axios from 'axios'

const API_BASE = 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  }
})

export default apiClient