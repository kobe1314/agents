package com.stock.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.math.BigDecimal;
import java.util.Map;

@Service
public class StockDataService {

    @Value("${app.stock.alpha-vantage-key}")
    private String apiKey;

    private final RestTemplate rest = new RestTemplate();

    // Alpha Vantage: 实时行情
    public Map<String, Object> getQuote(String symbol) {
        String url = "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=" 
            + symbol + "&apikey=" + apiKey;
        try {
            return rest.getForObject(url, Map.class);
        } catch (Exception e) {
            // 降级到 Yahoo Finance
            return getQuoteYahoo(symbol);
        }
    }

    // Yahoo Finance: 实时行情（备用）
    private Map<String, Object> getQuoteYahoo(String symbol) {
        String url = "https://query1.finance.yahoo.com/v8/finance/chart/" 
            + symbol + "?range=1d&interval=1m";
        try {
            return rest.getForObject(url, Map.class);
        } catch (Exception e) {
            return Map.of("error", "行情数据暂时不可用");
        }
    }

    // K 线数据
    public Map<String, Object> getKLines(String symbol) {
        String url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" 
            + symbol + "&apikey=" + apiKey;
        try {
            return rest.getForObject(url, Map.class);
        } catch (Exception e) {
            return Map.of("error", "K线数据暂时不可用");
        }
    }

    // 搜索股票
    public Map<String, Object> search(String keyword) {
        String url = "https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=" 
            + keyword + "&apikey=" + apiKey;
        try {
            return rest.getForObject(url, Map.class);
        } catch (Exception e) {
            return Map.of("error", "搜索暂时不可用");
        }
    }
}
