import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'https://qotd-api-5zh9.onrender.com/api/v1', // Замените на URL вашего бэкенда
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

export default apiClient;
