import axios from 'axios'

// Vite exposes environment variables via import.meta.env
// Use `VITE_API_URL` when running the dev server or fallback to localhost
export const BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

const api = axios.create({
  baseURL: BASE_URL,
})

let isRefreshing = false
let failedQueue = []

const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) prom.reject(error)
    else prom.resolve(token)
  })
  failedQueue = []
}

api.interceptors.request.use(config => {
  const access = localStorage.getItem('access')
  if (access) config.headers['Authorization'] = `Bearer ${access}`
  return config
})

api.interceptors.response.use(
  res => res,
  err => {
    const originalRequest = err.config
    if (err.response && err.response.status === 401 && !originalRequest._retry) {
      const refresh = localStorage.getItem('refresh')
      if (!refresh) {
        return Promise.reject(err)
      }

      if (isRefreshing) {
        return new Promise(function (resolve, reject) {
          failedQueue.push({ resolve, reject })
        })
          .then(token => {
            originalRequest.headers['Authorization'] = 'Bearer ' + token
            return api(originalRequest)
          })
          .catch(e => Promise.reject(e))
      }

      originalRequest._retry = true
      isRefreshing = true

      return new Promise(function (resolve, reject) {
        axios.post(`${BASE_URL}/api/auth/refresh/`, { refresh })
          .then(({ data }) => {
            const newAccess = data.access
            localStorage.setItem('access', newAccess)
            api.defaults.headers.common['Authorization'] = 'Bearer ' + newAccess
            processQueue(null, newAccess)
            resolve(api(originalRequest))
          })
          .catch(err => {
            processQueue(err, null)
            reject(err)
          })
          .finally(() => { isRefreshing = false })
      })
    }

    return Promise.reject(err)
  }
)

export function setAuthTokens(access, refresh) {
  localStorage.setItem('access', access)
  localStorage.setItem('refresh', refresh)
}
export function clearAuthTokens() {
  localStorage.removeItem('access')
  localStorage.removeItem('refresh')
}
export function getAccess() {
  return localStorage.getItem('access')
}

export { api }
