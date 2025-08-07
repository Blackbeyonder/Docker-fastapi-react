import apiService from "./apiService";

const SimuladorService = {
  getUbicaciones: () => apiService.get(`/api/v1/ubicaciones/operador`),
  postGuardarUbicaciones: (data) => apiService.post(`/api/v1/save_ubication/operador`, data)
  
  //   getUserById: (id) => apiService.get(`/users/${id}`),
//   createUser: (userData) => apiService.post("/users", userData),
//   updateUser: (id, userData) => apiService.put(`/users/${id}`, userData),
//   deleteUser: (id) => apiService.delete(`/users/${id}`),
};

export default SimuladorService;
