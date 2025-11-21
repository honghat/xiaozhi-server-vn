# Xiaozhi Server (Phiên bản Tiếng Việt)

Dự án này là backend server dành cho thiết bị **xiaozhi-esp32**, được chuyển đổi và việt hóa từ dự án gốc [xiaozhi-esp32-server](https://github.com/xinnan-tech/xiaozhi-esp32-server). Nó cung cấp các dịch vụ điều khiển, giao tiếp thời gian thực và tích hợp AI cho thiết bị phần cứng ESP32.

## 🌟 Chức năng chính

*   **Giao tiếp thời gian thực**: Sử dụng **WebSocket** để giao tiếp hai chiều với thiết bị ESP32 (âm thanh, lệnh điều khiển).
*   **Giao thức MCP (Model Context Protocol)**: Hỗ trợ kết nối và mở rộng khả năng của mô hình AI thông qua giao thức MCP.
*   **Cập nhật OTA**: Cung cấp máy chủ HTTP đơn giản để phục vụ việc cập nhật firmware từ xa (OTA) cho thiết bị.
*   **Xử lý âm thanh**: Tích hợp sẵn các công cụ xử lý âm thanh (yêu cầu FFmpeg) để hỗ trợ nhận dạng giọng nói (ASR) và tổng hợp giọng nói (TTS).
*   **Quản lý cấu hình**: Hệ thống quản lý cấu hình linh hoạt, hỗ trợ đọc từ file cục bộ hoặc từ API quản lý tập trung.
*   **Bảo mật**: Cơ chế xác thực qua `auth_key` cho các kết nối WebSocket và API.

## 🛠 Yêu cầu hệ thống

*   **Hệ điều hành**: Windows, macOS, hoặc Linux (Ubuntu, Debian, Raspberry Pi OS).
*   **Python**: Phiên bản 3.10 (khuyến nghị).
*   **FFmpeg**: Bắt buộc phải cài đặt để xử lý âm thanh.

### 🖥️ Hiệu năng phần cứng (Tham khảo)

Dự án có thể chạy tốt trên **Raspberry Pi 4 (8GB RAM)**, tuy nhiên hiệu năng sẽ phụ thuộc vào chế độ bạn sử dụng:

1.  **Chế độ Cloud API (Khuyên dùng cho Pi 4)**:
    *   Sử dụng các dịch vụ như OpenAI, Gemini, Azure TTS...
    *   **Hiệu năng**: Rất mượt mà. Pi 4 xử lý tốt việc chuyển tiếp WebSocket và âm thanh.
    *   **Tài nguyên**: Chỉ tốn khoảng 1-2GB RAM.

2.  **Chế độ Local (Chạy Offline)**:
    *   **ASR (Nhận dạng giọng nói)**:
        *   *Vosk/Sherpa-onnx (Mô hình nhỏ)*: Chạy ổn định.
        *   *FunASR (Mô hình lớn)*: Có thể bị trễ (delay) 1-3 giây, gây ảnh hưởng trải nghiệm hội thoại.
    *   **LLM (Mô hình ngôn ngữ)**: Không khuyến nghị chạy LLM cục bộ trên Pi 4 vì tốc độ sẽ rất chậm.

## 🚀 Hướng dẫn cài đặt và chạy

### Cách 1: Chạy trực tiếp (Local)

1.  **Cài đặt FFmpeg**:
    Đảm bảo bạn đã cài đặt FFmpeg và có thể gọi lệnh `ffmpeg -version` từ terminal.

2.  **Cài đặt thư viện Python**:
    Di chuyển vào thư mục dự án và chạy lệnh:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Cấu hình (Tùy chọn)**:
    *   Dự án sẽ tự động tạo `auth_key` nếu chưa có.
    *   Bạn có thể tạo file `config.yaml` trong thư mục gốc hoặc `data/.config.yaml` để tùy chỉnh cấu hình (tham khảo mã nguồn để biết các trường cấu hình).

4.  **Khởi chạy Server**:
    ```bash
    python app.py
    ```
    *   Server sẽ lắng nghe WebSocket tại cổng **8011** (mặc định).
    *   Server HTTP (OTA/API) tại cổng **8012** (mặc định).

### Cách 2: Chạy bằng Docker

Dự án đã bao gồm `Dockerfile` tối ưu.

1.  **Build Docker Image**:
    ```bash
    docker build -t xiaozhi-server .
    ```

2.  **Chạy Container**:
    ```bash
    docker run -d -p 8011:8011 -p 8012:8012 --name xiaozhi-instance xiaozhi-server
    ```

## 📂 Cấu trúc dự án

*   `app.py`: Điểm khởi chạy chính của ứng dụng.
*   `config/`: Chứa các logic tải cấu hình và thiết lập log.
*   `core/`: Chứa logic cốt lõi của server (WebSocket, HTTP, tiện ích xử lý).
*   `requirements.txt`: Danh sách các thư viện phụ thuộc.
*   `Dockerfile`: Cấu hình để build Docker image.

## 📝 Lưu ý

*   **Bảo mật**: Không để lộ địa chỉ WebSocket công khai mà không có biện pháp bảo vệ.
*   **WebSocket**: Không truy cập trực tiếp địa chỉ `ws://...` bằng trình duyệt, hãy sử dụng các công cụ test chuyên dụng hoặc trang test đi kèm (nếu có).


