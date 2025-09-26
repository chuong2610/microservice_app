docker-compose up -d    
docker logs kong-deck   
docker exec -it kong-deck deck sync --kong-addr http://kong:8001 -s /kong.yml    
docker-compose run --rm kong-deck             



# Kong API Gateway

## Khởi động services
```bash
docker-compose up -d
```

## Khi sửa file kong.yml - Cách reload cấu hình

### Cách 1: Sử dụng Kong Deck (Khuyến nghị)
```bash
# Đồng bộ cấu hình từ file kong.yml
docker-compose run --rm kong-deck
```

### Cách 2: Nếu kong-deck container đang chạy
```bash
docker exec -it kong-deck deck sync --kong-addr http://kong:8001 -s /kong.yml
```

### Cách 3: Sử dụng Kong Admin API trực tiếp
```bash
# POST cấu hình mới qua Admin API
curl -X POST http://localhost:8001/config -F config=@kong.yml
```

## Kiểm tra logs và trạng thái
```bash
# Xem logs của Kong Deck
docker logs kong-deck

# Kiểm tra trạng thái containers
docker-compose ps

# Xem logs của Kong Gateway
docker logs kong-gateway
```

## Kiểm tra cấu hình hiện tại
```bash
# Xem tất cả services
curl http://localhost:8001/services

# Xem tất cả routes
curl http://localhost:8001/routes

# Xem tất cả plugins
curl http://localhost:8001/plugins
```