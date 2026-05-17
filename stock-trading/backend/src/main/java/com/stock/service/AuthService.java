package com.stock.service;

import com.stock.model.User;
import com.stock.repository.UserRepository;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.Map;

@Service
public class AuthService {

    private final UserRepository userRepo;
    private final JwtService jwtService;
    private final BCryptPasswordEncoder encoder;

    public AuthService(UserRepository userRepo, JwtService jwtService, BCryptPasswordEncoder encoder) {
        this.userRepo = userRepo;
        this.jwtService = jwtService;
        this.encoder = encoder;
    }

    public Map<String, Object> register(String username, String password, String nickname) {
        if (userRepo.findByUsername(username).isPresent()) {
            return Map.of("success", false, "message", "用户名已存在");
        }
        var user = new User();
        user.setUsername(username);
        user.setPassword(encoder.encode(password));
        user.setNickname(nickname != null ? nickname : username);
        userRepo.save(user);
        var token = jwtService.generateToken(user.getId(), username);
        return Map.of("success", true, "token", token, "user", Map.of("id", user.getId(), "username", username, "nickname", user.getNickname()));
    }

    public Map<String, Object> login(String username, String password) {
        var userOpt = userRepo.findByUsername(username);
        if (userOpt.isEmpty() || !encoder.matches(password, userOpt.get().getPassword())) {
            return Map.of("success", false, "message", "用户名或密码错误");
        }
        var user = userOpt.get();
        var token = jwtService.generateToken(user.getId(), username);
        return Map.of("success", true, "token", token, "user", Map.of("id", user.getId(), "username", username, "nickname", user.getNickname()));
    }
}
