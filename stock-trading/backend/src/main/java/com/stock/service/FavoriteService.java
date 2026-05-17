package com.stock.service;

import com.stock.model.FavoriteStock;
import com.stock.repository.FavoriteRepository;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.Map;

@Service
public class FavoriteService {

    private final FavoriteRepository favoriteRepo;

    public FavoriteService(FavoriteRepository favoriteRepo) {
        this.favoriteRepo = favoriteRepo;
    }

    public Map<String, Object> add(Long userId, String symbol) {
        var fav = new FavoriteStock();
        fav.setUserId(userId);
        fav.setSymbol(symbol.toUpperCase());
        favoriteRepo.save(fav);
        return Map.of("success", true);
    }

    public List<FavoriteStock> list(Long userId) {
        return favoriteRepo.findByUserId(userId);
    }

    public void remove(Long userId, String symbol) {
        favoriteRepo.deleteByUserIdAndSymbol(userId, symbol.toUpperCase());
    }
}
