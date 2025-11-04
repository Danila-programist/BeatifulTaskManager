import axios from "axios";

const API_URL = "/api/v1/auth";

export const loginUser = async (username, password) => {
  return axios.post(
    `${API_URL}/login`,
    { username, password },
    { withCredentials: true }
  );
};

export const registerUser = async (data) => {
  return axios.post(
    `${API_URL}/register`,
    data,
    { withCredentials: true }
  );
};
