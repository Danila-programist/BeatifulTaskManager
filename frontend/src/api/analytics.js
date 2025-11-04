import axios from "axios";

const API_URL = "api/v1";

export const getUserAnalytics = async () => {
  return axios.get(`${API_URL}/analytics`, { withCredentials: true });
};
