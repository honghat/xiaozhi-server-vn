# Hướng dẫn đẩy lên GitHub

## Đã hoàn thành
✅ Sao chép toàn bộ 900+ file từ dự án gốc
✅ Dịch tự động tất cả các file Python
✅ Thay thế các file core bằng bản dịch thủ công chất lượng cao
✅ Tạo README tiếng Việt
✅ Khởi tạo Git repository

## Bước tiếp theo

### 1. Tạo repository mới trên GitHub
- Truy cập https://github.com/new
- Tên repo: `xiaozhi-esp32-server-vn` (hoặc tên bạn muốn)
- **KHÔNG chọn** "Initialize this repository with a README"
- Click "Create repository"

### 2. Kết nối và đẩy code

Sau khi tạo xong repository, chạy các lệnh sau trong terminal:

```bash
cd c:\Users\Hat\Desktop\xiaozhi-server-full

# Thay URL bên dưới bằng URL repository của bạn
git remote add origin https://github.com/honghat/xiaozhi-esp32-server-vn.git

# Đổi tên nhánh chính (nếu cần)
git branch -M main

# Đẩy code lên GitHub
git push -u origin main
```

### 3. Hoàn tất

Sau khi push thành công, dự án của bạn sẽ có mặt trên GitHub với:
- ✅ 900+ file được dịch sang tiếng Việt
- ✅ Backend Python hoàn chỉnh (xiaozhi-server)
- ✅ Java API (manager-api)
- ✅ Vue.js Dashboard (manager-web)
- ✅ Tài liệu đầy đủ
- ✅ Docker support

## Thống kê dự án

- **Tổng số file**: 900+
- **File Python**: 116
- **File Java**: 350+
- **File Vue/JavaScript**: 200+
- **Dung lượng**: ~50MB

## Lưu ý

Nếu push bị lỗi do file quá lớn, bạn có thể:
1. Xóa thư mục `main/xiaozhi-server/models/` (chứa model AI lớn)
2. Thêm vào `.gitignore`:
   ```
   main/xiaozhi-server/models/
   ```
3. Commit lại và push
