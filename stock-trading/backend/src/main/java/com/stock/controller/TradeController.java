package com.stock.controller;

import com.stock.service.TradeService;
import com.stock.service.FavoriteService;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.math.BigDecimal;
import java.util.Map;

@RestController
@RequestMapping("/api/trade")
public class TradeController {

    private final TradeService tradeService;
    private final FavoriteService favoriteService;

    public TradeController(TradeService tradeService, FavoriteService favoriteService) {
        this.tradeService = tradeService;
        this.favoriteService = favoriteService;
    }

    @PostMapping("/order")
    public Map<String, Object> placeOrder(Authentication auth, @RequestBody Map<String, Object> body) {
        var userId = Long.valueOf(auth.getName());
        var symbol = (String) body.get("symbol");
        var type = (String) body.get("type");
        var price = new BigDecimal((String) body.get("price"));
        var qty = (Integer) body.get("quantity");
        return tradeService.placeOrder(userId, symbol, type, price, qty);
    }

    @GetMapping("/orders")
    public Object getOrders(Authentication auth) {
        var userId = Long.valueOf(auth.getName());
        return tradeService.getOrders(userId);
    }

    @GetMapping("/portfolio")
    public Object getPortfolio(Authentication auth) {
        var userId = Long.valueOf(auth.getName());
        return tradeService.getPortfolio(userId);
    }

    @PostMapping("/favorite")
    public Object addFavorite(Authentication auth, @RequestBody Map<String, String> body) {
        var userId = Long.valueOf(auth.getName());
        return favoriteService.add(userId, body.get("symbol"));
    }

    @GetMapping("/favorites")
    public Object getFavorites(Authentication auth) {
        var userId = Long.valueOf(auth.getName());
        return favoriteService.list(userId);
    }

    @DeleteMapping("/favorite/{symbol}")
    public Object removeFavorite(Authentication auth, @PathVariable String symbol) {
        var userId = Long.valueOf(auth.getName());
        favoriteService.remove(userId, symbol);
        return Map.of("success", true);
    }
}
