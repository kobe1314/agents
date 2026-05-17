package com.stock.service;

import com.stock.model.Order;
import com.stock.model.Portfolio;
import com.stock.repository.OrderRepository;
import com.stock.repository.PortfolioRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.List;
import java.util.Map;

@Service
public class TradeService {

    private final OrderRepository orderRepo;
    private final PortfolioRepository portfolioRepo;

    public TradeService(OrderRepository orderRepo, PortfolioRepository portfolioRepo) {
        this.orderRepo = orderRepo;
        this.portfolioRepo = portfolioRepo;
    }

    @Transactional
    public Map<String, Object> placeOrder(Long userId, String symbol, String type, BigDecimal price, Integer qty) {
        var total = price.multiply(BigDecimal.valueOf(qty));

        // Check balance for BUY
        if ("BUY".equals(type)) {
            var portfolio = portfolioRepo.findByUserIdAndSymbol(userId, symbol);
            // Create order
            var order = new Order();
            order.setUserId(userId); order.setSymbol(symbol); order.setType(type);
            order.setStatus("FILLED"); order.setPrice(price);
            order.setQuantity(qty); order.setTotalAmount(total);
            orderRepo.save(order);

            // Update portfolio
            if (portfolio.isPresent()) {
                var p = portfolio.get();
                var newQty = p.getQuantity() + qty;
                var newAvg = p.getAvgPrice().multiply(BigDecimal.valueOf(p.getQuantity()))
                    .add(total).divide(BigDecimal.valueOf(newQty));
                p.setQuantity(newQty); p.setAvgPrice(newAvg);
                portfolioRepo.save(p);
            } else {
                var p = new Portfolio();
                p.setUserId(userId); p.setSymbol(symbol); p.setQuantity(qty); p.setAvgPrice(price);
                portfolioRepo.save(p);
            }
            return Map.of("success", true, "message", "买入成功", "orderId", order.getId());
        }

        // SELL
        var held = portfolioRepo.findByUserIdAndSymbol(userId, symbol);
        if (held.isEmpty() || held.get().getQuantity() < qty) {
            return Map.of("success", false, "message", "持仓不足");
        }
        var order = new Order();
        order.setUserId(userId); order.setSymbol(symbol); order.setType(type);
        order.setStatus("FILLED"); order.setPrice(price);
        order.setQuantity(qty); order.setTotalAmount(total);
        orderRepo.save(order);

        var p = held.get();
        p.setQuantity(p.getQuantity() - qty);
        portfolioRepo.save(p);
        return Map.of("success", true, "message", "卖出成功", "orderId", order.getId());
    }

    public List<Order> getOrders(Long userId) {
        return orderRepo.findByUserIdOrderByCreatedAtDesc(userId);
    }

    public List<Portfolio> getPortfolio(Long userId) {
        return portfolioRepo.findByUserId(userId);
    }
}
