import axios from "axios";
import { getSessionId } from "@/lib/session-id";
const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 60000,
});

api.interceptors.request.use((config) => {
  config.headers["X-Session-Id"] = getSessionId();
  return config;
});

api.interceptors.request.use(
  (config) => {
    const token =
  localStorage.getItem("access_token") ||
  sessionStorage.getItem("access_token");;

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api;