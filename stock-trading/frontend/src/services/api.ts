import axios from 'axios';

const api = axios.create({ baseURL: '/api' });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export default api;

export const auth = {
  login: (username: string, password: string) =>
    api.post('/auth/login', { username, password }).then(r => r.data),
  register: (username: string, password: string) =>
    api.post('/auth/register', { username, password }).then(r => r.data),
};

export const stocks = {
  quote: (symbol: string) => api.get(`/stocks/quote/${symbol}`).then(r => r.data),
  kline: (symbol: string) => api.get(`/stocks/kline/${symbol}`).then(r => r.data),
  search: (q: string) => api.get(`/stocks/search?q=${q}`).then(r => r.data),
};

export const trade = {
  order: (data: any) => api.post('/trade/order', data).then(r => r.data),
  orders: () => api.get('/trade/orders').then(r => r.data),
  portfolio: () => api.get('/trade/portfolio').then(r => r.data),
  favorites: () => api.get('/trade/favorites').then(r => r.data),
  addFavorite: (symbol: string) => api.post('/trade/favorite', { symbol }).then(r => r.data),
  removeFavorite: (symbol: string) => api.delete(`/trade/favorite/${symbol}`).then(r => r.data),
};
