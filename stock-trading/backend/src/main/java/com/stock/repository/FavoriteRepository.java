package com.stock.repository;
import com.stock.model.FavoriteStock;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;
public interface FavoriteRepository extends JpaRepository<FavoriteStock, Long> {
    List<FavoriteStock> findByUserId(Long userId);
    void deleteByUserIdAndSymbol(Long userId, String symbol);
}
