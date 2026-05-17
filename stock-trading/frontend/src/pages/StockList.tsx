import React, { useState } from 'react';
import { Card, Input, Table, Button, Tag, message } from 'antd';
import { SearchOutlined, StarOutlined, StarFilled } from '@ant-design/icons';
import { stocks, trade as tradeApi } from '../services/api';

export default function StockList() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<any[]>([]);
  const [favorites, setFavorites] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  const search = async () => {
    if (!query) return;
    setLoading(true);
    try {
      const res = await stocks.search(query);
      const matches = res?.bestMatches || [];
      setResults(matches.map((m: any) => ({
        symbol: m['1. symbol'], name: m['2. name'], region: m['4. region'],
        currency: m['8. currency'],
      })));
    } catch { message.error('搜索失败'); }
    setLoading(false);
  };

  const toggleFavorite = async (symbol: string) => {
    try {
      if (favorites.includes(symbol)) {
        await tradeApi.removeFavorite(symbol);
        setFavorites(favorites.filter(s => s !== symbol));
      } else {
        await tradeApi.addFavorite(symbol);
        setFavorites([...favorites, symbol]);
      }
    } catch { message.error('操作失败'); }
  };

  const columns = [
    { title: '', key: 'fav', width: 40, render: (_: any, r: any) => (
      <Button type="text" icon={favorites.includes(r.symbol) ? <StarFilled style={{color:'#faad14'}} /> : <StarOutlined />}
        onClick={() => toggleFavorite(r.symbol)} />
    )},
    { title: '代码', dataIndex: 'symbol', key: 'symbol', render: (v: string) => <a href={`/trade?symbol=${v}`}>{v}</a> },
    { title: '名称', dataIndex: 'name', key: 'name' },
    { title: '地区', dataIndex: 'region', key: 'region' },
    { title: '货币', dataIndex: 'currency', key: 'currency' },
  ];

  return (
    <Card title="股票搜索">
      <Input.Search placeholder="输入股票代码或名称 (如 AAPL)" value={query}
        onChange={e => setQuery(e.target.value)} onSearch={search} enterButton={<><SearchOutlined /> 搜索</>}
        size="large" style={{ marginBottom: 16 }} loading={loading} />
      <Table dataSource={results} columns={columns} rowKey="symbol" pagination={false} />
    </Card>
  );
}
