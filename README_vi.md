# Xiaozhi ESP32 Server - Phiên bản Tiếng Việt

Dự án này là phiên bản **hoàn chỉnh** được việt hóa từ [xiaozhi-esp32-server](https://github.com/xinnan-tech/xiaozhi-esp32-server), bao gồm đầy đủ 3 component chính:

- 🐍 **xiaozhi-server**: Backend Python (WebSocket, AI, TTS/ASR)
- ☕ **manager-api**: Java Spring Boot API quản lý
- 💻 **manager-web**: Vue.js Dashboard quản trị

## 🌟 Tính năng chính

### Xiaozhi Server (Backend Python)
*   **Giao tiếp thời gian thực WebSocket** với thiết bị ESP32
*   **Tích hợp AI đa nền tảng**: OpenAI, Gemini, Coze, Doubao, Qwen, v.v.
*   **Nhận dạng giọng nói (ASR)**: FunASR, Whisper, Vosk, Sherpa-onnx, Aliyun, Baidu, Tencent
*   **Tổng hợp giọng nói (TTS)**: Edge TTS, Azure, Aliyun, Fish Speech, GPT-SoVITS
*   **Hỗ trợ MCP (Model Context Protocol)**: Mở rộng khả năng AI
*   **Quản lý bộ nhớ hội thoại**: Mem0, Dify
*   **Nhận dạng giọng nói (Voiceprint)**
*   **Tích hợp Home Assistant**

### Manager API (Java Backend)
*   Quản lý người dùng, thiết bị, cấu hình
*   API RESTful đầy đủ
*   Xác thực JWT
*   Quản lý OTA firmware

### Manager Web (Vue.js Dashboard)
*   Giao diện quản trị trực quan
*   Quản lý thiết bị ESP32
*   Cấu hình AI models
*   Thống kê và giám sát

## 📦 Cấu trúc dự án

```
xiaozhi-server-full/
├── main/
│   ├── xiaozhi-server/        # Backend Python
│   ├── manager-api/           # Java Spring Boot API
│   ├── manager-web/           # Vue.js Dashboard
│   └── manager-mobile/        # Mobile App (Uniapp)
├── docs/                      # Tài liệu chi tiết
├── Dockerfile                 # Docker cho toàn bộ hệ thống
└── README.md                  # File này
```

## 🚀 Hướng dẫn triển khai nhanh

### 1. Chỉ chạy xiaozhi-server (Backend Python)

**Yêu cầu**:
- Python 3.10
- FFmpeg

**Cài đặt**:
```bash
cd main/xiaozhi-server
pip install -r requirements.txt
python app.py
```

**Cổng mặc định**:
- WebSocket: `8011`
- HTTP/OTA: `8012`

### 2. Chạy toàn bộ hệ thống (Full Stack)

Xem hướng dẫn chi tiết trong thư mục `docs/`:
- [Deployment.md](docs/Deployment.md) - Chỉ chạy server Python
- [Deployment_all.md](docs/Deployment_all.md) - Chạy cả 3 component

### 3. Chạy bằng Docker

```bash
# Build image
docker build -t xiaozhi-full .

# Chạy container
docker run -d \
  -p 8011:8011 \
  -p 8012:8012 \
  -p 8080:8080 \
  -p 8081:8081 \
  --name xiaozhi \
  xiaozhi-full
```

## 🖥️ Yêu cầu phần cứng

### Chế độ Cloud API (Khuyến nghị)
- **CPU**: 1-2 vCPU
- **RAM**: 2-4GB
- **Thiết bị hỗ trợ**: Raspberry Pi 4, VPS, PC thường

### Chế độ Local AI (Offline)
- **CPU**: 4+ cores
- **RAM**: 8GB+ (khuyến nghị 16GB)
- **GPU**: NVIDIA GPU với CUDA (tùy chọn nhưng khuyến nghị)

**Lưu ý**: Raspberry Pi 4 8GB chạy tốt ở chế độ Cloud API, nhưng hạn chế với AI cục bộ.

## 📚 Tài liệu

Tất cả tài liệu đã được dịch sang tiếng Việt trong thư mục `docs/`:

- **FAQ.md** - Câu hỏi thường gặp
- **firmware-build.md** - Hướng dẫn build firmware ESP32
- **homeassistant-integration.md** - Tích hợp Home Assistant
- **mcp-endpoint-integration.md** - Tích hợp MCP
- **performance_tester.md** - Công cụ đo hiệu năng

## 🔧 Cấu hình

File cấu hình chính: `main/xiaozhi-server/data/.config.yaml`

Tham khảo:
- `config.yaml` - Mẫu cấu hình đầy đủ
- `config_from_api.yaml` - Cấu hình kết nối API quản lý

## 🤝 Đóng góp

Dự án được việt hóa và tùy chỉnh từ:
- **Dự án gốc**: [xinnan-tech/xiaozhi-esp32-server](https://github.com/xinnan-tech/xiaozhi-esp32-server)
- **Biên dịch**: Bản việt hóa hoàn chỉnh với 900+ file được dịch

## 📝 Giấy phép

Dự án sử dụng giấy phép MIT (theo dự án gốc)

## ⚠️ Lưu ý quan trọng

1. **Bảo mật**: Không để lộ `auth_key` và API keys
2. **Production**: Cần thêm HTTPS, rate limiting, và firewall
3. **API Keys**: Đăng ký API key của các nhà cung cấp (OpenAI, Gemini, v.v.)

## 🔗 Liên kết

- [Dự án gốc](https://github.com/xinnan-tech/xiaozhi-esp32-server)
- [Dự án phần cứng ESP32](https://github.com/78/xiaozhi-esp32)
- [Giao thức giao tiếp](https://ccnphfhqs21z.feishu.cn/wiki/M0XiwldO9iJwHikpXD5cEx71nKh)

---

**Cập nhật**: 2025-11-21

Nếu gặp vấn đề, vui lòng tham khảo FAQ hoặc mở issue.
