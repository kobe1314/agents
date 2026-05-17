import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { Card, Input, Button, message, Tabs } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import { auth as authApi } from '../services/api';
import { login } from '../store';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const dispatch = useDispatch();

  const handleLogin = async () => {
    setLoading(true);
    try {
      const res = await authApi.login(username, password);
      if (res.success) {
        dispatch(login(res));
        message.success('登录成功');
      } else {
        message.error(res.message);
      }
    } catch { message.error('登录失败'); }
    setLoading(false);
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', background: '#f0f2f5' }}>
      <Card title="📈 股票交易系统" style={{ width: 380 }}>
        <Input prefix={<UserOutlined />} placeholder="用户名" value={username}
          onChange={e => setUsername(e.target.value)} style={{ marginBottom: 12 }} />
        <Input.Password prefix={<LockOutlined />} placeholder="密码" value={password}
          onChange={e => setPassword(e.target.value)} style={{ marginBottom: 16 }}
          onPressEnter={handleLogin} />
        <Button type="primary" block loading={loading} onClick={handleLogin}>登录</Button>
      </Card>
    </div>
  );
}
