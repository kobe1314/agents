package com.stock.controller;

import com.stock.service.StockDataService;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/stocks")
public class StockController {

    private final StockDataService stockService;

    public StockController(StockDataService stockService) {
        this.stockService = stockService;
    }

    @GetMapping("/quote/{symbol}")
    public Map<String, Object> getQuote(@PathVariable String symbol) {
        return stockService.getQuote(symbol.toUpperCase());
    }

    @GetMapping("/kline/{symbol}")
    public Map<String, Object> getKLines(@PathVariable String symbol) {
        return stockService.getKLines(symbol.toUpperCase());
    }

    @GetMapping("/search")
    public Map<String, Object> search(@RequestParam String q) {
        return stockService.search(q);
    }
}
