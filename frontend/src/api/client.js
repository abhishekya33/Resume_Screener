import axios from 'axios'

const API_BASE =
  import.meta.env.VITE_API_URL || 'http://localhost:8000'

console.log("API BASE =", API_BASE)

const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  }
})

export default apiClient