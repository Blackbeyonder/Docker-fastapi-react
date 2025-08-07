import axios from "axios";

// Base URL de la API
const API_URL = import.meta.env.VITE_API_URL; // Cambia esto por tu URL real

// Configurar instancia de Axios
const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Interceptores (Opcional: Para manejar errores o agregar tokens)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("Error en la API:", error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Funciones genéricas para consumir la API
const apiService = {
  get: (url, params = {}) => api.get(url, { params }),
  post: (url, data) => api.post(url, data),
  put: (url, data) => api.put(url, data),
  patch: (url, data) => api.patch(url, data),
  delete: (url) => api.delete(url),
};

export default apiService;
