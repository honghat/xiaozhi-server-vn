# Dockerfile đơn giản để build chỉ xiaozhi-server từ thư mục gốc
# Sử dụng: docker build -t xiaozhi-server .

FROM python:3.10-slim

# Thiết lập biến môi trường
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# Cài đặt các gói hệ thống cần thiết
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ffmpeg \
    libopus0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Thiết lập thư mục làm việc
WORKDIR /app

# Sao chép requirements.txt từ thư mục đúng
COPY main/xiaozhi-server/requirements.txt .

# Cài đặt các thư viện Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn xiaozhi-server
COPY main/xiaozhi-server/ .

# Tạo các thư mục cần thiết
RUN mkdir -p tmp data

# Khai báo các port
EXPOSE 8011 8012

# Lệnh khởi chạy ứng dụng
CMD ["python", "app.py"]
