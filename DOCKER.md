# HƯỚNG DẪN SỬ DỤNG DOCKER

## Giới thiệu

Dự án cung cấp nhiều cách triển khai Docker:

1. **Dockerfile-server**: Chỉ chạy backend Python (xiaozhi-server)
2. **Dockerfile-web**: Chạy cả API Manager (Java) + Web Dashboard (Vue.js)
3. **docker-compose.yml**: Chạy toàn bộ hệ thống (khuyến nghị)

## Cách 1: Chỉ chạy Xiaozhi Server (Backend Python)

### Build image
```bash
docker build -f Dockerfile-server -t xiaozhi-server:latest .
```

### Chạy container
```bash
docker run -d \
  -p 8011:8011 \
  -p 8012:8012 \
  -v $(pwd)/main/xiaozhi-server/data:/opt/xiaozhi-esp32-server/data \
  -v $(pwd)/main/xiaozhi-server/tmp:/opt/xiaozhi-esp32-server/tmp \
  --name xiaozhi-server \
  xiaozhi-server:latest
```

### Kiểm tra logs
```bash
docker logs -f xiaozhi-server
```

## Cách 2: Chạy toàn bộ hệ thống (Docker Compose)

### Khởi động tất cả services
```bash
docker-compose up -d
```

### Xem logs
```bash
# Tất cả services
docker-compose logs -f

# Chỉ xem xiaozhi-server
docker-compose logs -f xiaozhi-server

# Chỉ xem web dashboard
docker-compose logs -f xiaozhi-web
```

### Dừng tất cả
```bash
docker-compose down
```

### Dừng và xóa volumes
```bash
docker-compose down -v
```

## Cách 3: Build riêng từng service

### Build Xiaozhi Server
```bash
docker build -f Dockerfile-server -t xiaozhi-server .
```

### Build Web Dashboard + API
```bash
docker build -f Dockerfile-web -t xiaozhi-web .
```

## Ports và Services

Sau khi chạy xong, bạn có thể truy cập:

- **WebSocket Server**: `ws://localhost:8011/xiaozhi/v1/`
- **HTTP/OTA API**: `http://localhost:8012/xiaozhi/ota/`
- **Web Dashboard**: `http://localhost:8002/`
- **Manager API**: `http://localhost:8002/api/`

## Cấu hình

### File cấu hình
Đặt file cấu hình tại: `main/xiaozhi-server/data/.config.yaml`

**Lưu ý**: File này phải được tạo trước khi chạy container.

### Volume mapping
- `data/`: Chứa cấu hình và database
- `tmp/`: Chứa file tạm (logs, audio cache)

## Môi trường sản phẩm (Production)

### Khuyến nghị bổ sung
1. **Reverse Proxy**: Sử dụng Nginx/Traefik ở phía trước
2. **HTTPS**: Thêm SSL certificate
3. **Database**: Sử dụng PostgreSQL/MySQL ngoài (không dùng SQLite)
4. **Monitoring**: Thêm Prometheus + Grafana
5. **Backup**: Tự động backup thư mục `data/`

### Ví dụ với Nginx reverse proxy
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /xiaozhi/ {
        proxy_pass http://localhost:8011;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }

    location / {
        proxy_pass http://localhost:8002;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Troubleshooting

### Container không khởi động
```bash
# Xem logs
docker logs xiaozhi-server

# Kiểm tra status
docker ps -a
```

### Port đã được sử dụng
Thay đổi port mapping trong `docker-compose.yml` hoặc lệnh `docker run`

### Lỗi thiếu dependencies
```bash
# Rebuild image
docker-compose build --no-cache
```

### Reset toàn bộ
```bash
docker-compose down -v
docker system prune -a
docker-compose up -d --build
```

## Cập nhật

### Cập nhật code mới
```bash
git pull
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## Giám sát tài nguyên

```bash
# Xem resource usage
docker stats

# Xem logs realtime
docker-compose logs -f --tail=100
```
