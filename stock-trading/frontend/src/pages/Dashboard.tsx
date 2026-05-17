import React, { useEffect, useState } from 'react';
import { Card, Row, Col, Statistic, Table, Button } from 'antd';
import { ArrowUpOutlined, ArrowDownOutlined } from '@ant-design/icons';
import { trade as tradeApi } from '../services/api';

export default function Dashboard() {
  const [portfolio, setPortfolio] = useState<any[]>([]);
  const [orders, setOrders] = useState<any[]>([]);

  useEffect(() => {
    tradeApi.portfolio().then(setPortfolio);
    tradeApi.orders().then(setOrders);
  }, []);

  const totalValue = portfolio.reduce((s, p) => s + p.quantity * 100, 0);
  const totalProfit = 1250.80;

  const columns = [
    { title: '股票', dataIndex: 'symbol', key: 'symbol' },
    { title: '持仓', dataIndex: 'quantity', key: 'quantity' },
    { title: '均价', dataIndex: 'avgPrice', key: 'avgPrice', render: (v: string) => `$${parseFloat(v).toFixed(2)}` },
    { title: '市值', key: 'marketValue', render: (_: any, r: any) => `$${(r.quantity * 100).toFixed(2)}` },
  ];

  return (
    <div>
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}><Card><Statistic title="总资产" value={totalValue} precision={2} prefix="$" /></Card></Col>
        <Col span={6}><Card><Statistic title="日盈亏" value={totalProfit} precision={2} prefix="$"
          valueStyle={{ color: totalProfit >= 0 ? '#3f8600' : '#cf1322' }}
          suffix={totalProfit >= 0 ? <ArrowUpOutlined /> : <ArrowDownOutlined />} /></Card></Col>
        <Col span={6}><Card><Statistic title="持仓数" value={portfolio.length} /></Card></Col>
        <Col span={6}><Card><Statistic title="收益率" value={2.35} suffix="%" precision={2}
          valueStyle={{ color: '#3f8600' }} /></Card></Col>
      </Row>
      <Card title="我的持仓" style={{ marginBottom: 24 }}>
        <Table dataSource={portfolio} columns={columns} rowKey="id" pagination={false} />
      </Card>
      <Card title="最近交易">
        <Table dataSource={orders.slice(0, 10)} columns={[
          { title: '时间', dataIndex: 'createdAt', key: 'createdAt', render: (v: string) => new Date(v).toLocaleString() },
          { title: '股票', dataIndex: 'symbol', key: 'symbol' },
          { title: '类型', dataIndex: 'type', key: 'type', render: (v: string) => v === 'BUY' ? '买入' : '卖出' },
          { title: '数量', dataIndex: 'quantity', key: 'quantity' },
          { title: '金额', dataIndex: 'totalAmount', key: 'totalAmount', render: (v: string) => `$${parseFloat(v).toFixed(2)}` },
        ]} rowKey="id" pagination={false} />
      </Card>
    </div>
  );
}
