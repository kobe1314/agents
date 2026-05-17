import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Card, Row, Col, Input, InputNumber, Button, Table, Tabs, message, Statistic } from 'antd';
import { trade as tradeApi, stocks as stocksApi } from '../services/api';

export default function Trade() {
  const [searchParams] = useSearchParams();
  const [symbol, setSymbol] = useState(searchParams.get('symbol') || 'AAPL');
  const [price, setPrice] = useState(100);
  const [qty, setQty] = useState(1);
  const [orders, setOrders] = useState<any[]>([]);
  const [portfolio, setPortfolio] = useState<any[]>([]);
  const [quote, setQuote] = useState<any>(null);

  useEffect(() => {
    tradeApi.orders().then(setOrders);
    tradeApi.portfolio().then(setPortfolio);
  }, []);

  const refreshQuote = async () => {
    try {
      const res = await stocksApi.quote(symbol);
      setQuote(res);
    } catch { /* ignore */ }
  };

  const handleTrade = async (type: string) => {
    try {
      const res = await tradeApi.order({ symbol, type, price: price.toString(), quantity: qty });
      if (res.success) {
        message.success(`${type === 'BUY' ? '买入' : '卖出'}成功`);
        tradeApi.orders().then(setOrders);
        tradeApi.portfolio().then(setPortfolio);
      } else {
        message.error(res.message);
      }
    } catch { message.error('交易失败'); }
  };

  return (
    <Row gutter={24}>
      <Col span={12}>
        <Card title="交易" style={{ marginBottom: 16 }}>
          <div style={{ marginBottom: 12 }}>
            <span style={{ marginRight: 8 }}>股票代码:</span>
            <Input.Search value={symbol} onChange={(e: React.ChangeEvent<HTMLInputElement>) => setSymbol(e.target.value.toUpperCase())}
              onSearch={refreshQuote} enterButton="查询" style={{ width: 240 }} />
          </div>
          {quote && (
            <div style={{ marginBottom: 16, padding: 12, background: '#f5f5f5', borderRadius: 8 }}>
              <Statistic title={symbol} value={190.45} precision={2} prefix="$"
                valueStyle={{ color: '#3f8600' }} />
            </div>
          )}
          <div style={{ marginBottom: 12 }}>
            <span style={{ marginRight: 8 }}>价格:</span>
            <InputNumber value={price} onChange={v => setPrice(v || 0)} min={0.01}
              step={0.01} prefix="$" style={{ width: 160 }} />
          </div>
          <div style={{ marginBottom: 16 }}>
            <span style={{ marginRight: 8 }}>数量:</span>
            <InputNumber value={qty} onChange={v => setQty(v || 1)} min={1} max={10000}
              style={{ width: 160 }} />
          </div>
          <div style={{ marginBottom: 12, color: '#888' }}>
            预估金额: ${(price * qty).toFixed(2)}
          </div>
          <Button type="primary" danger style={{ marginRight: 12 }}
            onClick={() => handleTrade('SELL')}>卖出</Button>
          <Button type="primary" style={{ background: '#52c41a', borderColor: '#52c41a' }}
            onClick={() => handleTrade('BUY')}>买入</Button>
        </Card>
      </Col>
      <Col span={12}>
        <Card title="持仓" style={{ marginBottom: 16 }}>
          <Table dataSource={portfolio} columns={[
            { title: '股票', dataIndex: 'symbol' },
            { title: '数量', dataIndex: 'quantity' },
            { title: '均价', dataIndex: 'avgPrice', render: (v: string) => `$${parseFloat(v || '0').toFixed(2)}` },
          ]} rowKey="id" pagination={false} size="small" />
        </Card>
        <Card title="订单历史">
          <Table dataSource={orders} columns={[
            { title: '时间', dataIndex: 'createdAt', render: (v: string) => new Date(v).toLocaleString() },
            { title: '股票', dataIndex: 'symbol' },
            { title: '类型', dataIndex: 'type', render: (v: string) => v === 'BUY' ? '买入' : '卖出' },
            { title: '数量', dataIndex: 'quantity' },
            { title: '金额', dataIndex: 'totalAmount', render: (v: string) => `$${parseFloat(v || '0').toFixed(2)}` },
          ]} rowKey="id" pagination={false} size="small" />
        </Card>
      </Col>
    </Row>
  );
}
