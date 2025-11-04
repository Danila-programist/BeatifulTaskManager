import axios from "axios";

const API_URL = "http://localhost:8000/api/v1";

export const getUserAnalytics = async () => {
  return axios.get(`${API_URL}/analytics`, { withCredentials: true });
};
