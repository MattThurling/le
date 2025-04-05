import axios from 'axios'

const secureApi = axios.create({
  baseURL: '/api/',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
    'X-Requested-With': 'XMLHttpRequest',
  }
})

secureApi.interceptors.request.use(
  (config) => {
    const el = document.getElementById('data')
    if (el?.dataset?.token) {
      config.headers['X-CSRFToken'] = el.dataset.token
    }
    return config
  },
  (error) => Promise.reject(error)
)

const publicApi = axios.create({
  baseURL: '/api/',
  headers: {
    'Content-Type': 'application/json',
  }
})

export { secureApi, publicApi }
