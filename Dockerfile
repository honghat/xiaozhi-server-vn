# Sử dụng python 3.10-slim làm base image
FROM python:3.10-slim

# Thiết lập biến môi trường
# Ngăn Python tạo các tệp .pyc
ENV PYTHONDONTWRITEBYTECODE=1
# Đảm bảo đầu ra Python được in trực tiếp vào terminal (không đệm)
ENV PYTHONUNBUFFERED=1
# Thiết lập encoding
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Cài đặt các gói hệ thống cần thiết
# ffmpeg: Xử lý âm thanh/video
# libopus0: Codec âm thanh Opus
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ffmpeg \
    libopus0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Sao chép requirements.txt trước để tận dụng Docker cache
COPY requirements.txt .

# Cài đặt các thư viện Python
# Nâng cấp pip và cài đặt các gói từ requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn dự án vào container
COPY . .

# Tạo các thư mục cần thiết (nếu chưa có)
RUN mkdir -p tmp data

# Khai báo các port mà ứng dụng sử dụng
# 8011: WebSocket port (mặc định)
# 8012: HTTP/OTA port (mặc định)
EXPOSE 8011
EXPOSE 8012

# Lệnh khởi chạy ứng dụng
CMD ["python", "app.py"]
