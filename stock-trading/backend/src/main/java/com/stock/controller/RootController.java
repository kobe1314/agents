package com.stock.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import java.util.Map;

@RestController
public class RootController {

    @GetMapping("/")
    public Map<String, Object> root() {
        return Map.of(
            "service", "Stock Trading System",
            "version", "1.0.0",
            "status", "running",
            "endpoints", Map.of(
                "auth", "/api/auth/login|register",
                "stocks", "/api/stocks/quote|kline|search",
                "trade", "/api/trade/order|orders|portfolio|favorite"
            )
        );
    }
}
