import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { Layout, Menu } from 'antd';
import { useNavigate } from 'react-router-dom';
import { RootState } from './store';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import StockList from './pages/StockList';
import Trade from './pages/Trade';

const { Header, Content } = Layout;

function App() {
  const token = useSelector((s: RootState) => s.auth.token);
  const navigate = useNavigate();

  if (!token) return <Login />;

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ display: 'flex', alignItems: 'center' }}>
        <div style={{ color: '#fff', fontSize: 18, fontWeight: 'bold', marginRight: 40 }}>📈 股票交易</div>
        <Menu theme="dark" mode="horizontal"
          items={[
            { key: '/dashboard', label: '仪表盘' },
            { key: '/stocks', label: '股票' },
            { key: '/trade', label: '交易' },
          ]}
          onClick={({ key }) => navigate(key)}
          style={{ flex: 1 }}
        />
      </Header>
      <Content style={{ padding: 24 }}>
        <Routes>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/stocks" element={<StockList />} />
          <Route path="/trade" element={<Trade />} />
          <Route path="*" element={<Navigate to="/dashboard" />} />
        </Routes>
      </Content>
    </Layout>
  );
}

export default App;
