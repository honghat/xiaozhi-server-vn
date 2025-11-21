import os
from config.config_loader import read_config, get_project_dir, load_config


default_config_file = "config.yaml"
config_file_valid = False


def check_config_file():
    global config_file_valid
    if config_file_valid:
        return
    """
    Kiểm tra cấu hình đơn giản, chỉ nhắc người dùng về tình trạng sử dụng tệp cấu hình
    """
    custom_config_file = get_project_dir() + "data/." + default_config_file
    if not os.path.exists(custom_config_file):
        raise FileNotFoundError(
            "Không tìm thấy tệp data/.config.yaml, vui lòng xác nhận tệp cấu hình này có tồn tại theo hướng dẫn"
        )

    # Kiểm tra xem có đọc cấu hình từ API không
    config = load_config()
    if config.get("read_config_from_api", False):
        print("Đọc cấu hình từ API")
        old_config_origin = read_config(custom_config_file)
        if old_config_origin.get("selected_module") is not None:
            error_msg = "Tệp cấu hình của bạn dường như chứa cả cấu hình bảng điều khiển thông minh và cấu hình cục bộ:\n"
            error_msg += "\nKhuyên bạn:\n"
            error_msg += "1. Sao chép tệp config_from_api.yaml ở thư mục gốc vào data, đổi tên thành .config.yaml\n"
            error_msg += "2. Cấu hình địa chỉ giao diện và khóa theo hướng dẫn\n"
            raise ValueError(error_msg)
    config_file_valid = True
