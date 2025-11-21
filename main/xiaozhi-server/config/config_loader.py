import os
import yaml
from collections.abc import Mapping
from config.manage_api_client import init_service, get_server_config, get_agent_models


def get_project_dir():
    """Lấy thư mục gốc dự án"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"


def read_config(config_path):
    with open(config_path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)
    return config


def load_config():
    """Tải tệp cấu hình"""
    from core.utils.cache.manager import cache_manager, CacheType

    # Kiểm tra bộ nhớ đệm
    cached_config = cache_manager.get(CacheType.CONFIG, "main_config")
    if cached_config is not None:
        return cached_config

    default_config_path = get_project_dir() + "config.yaml"
    custom_config_path = get_project_dir() + "data/.config.yaml"

    # Tải cấu hình mặc định
    default_config = read_config(default_config_path)
    custom_config = read_config(custom_config_path)

    if custom_config.get("manager-api", {}).get("url"):
        config = get_config_from_api(custom_config)
    else:
        # Gộp cấu hình
        config = merge_configs(default_config, custom_config)
    # Khởi tạo thư mục
    ensure_directories(config)

    # Lưu cấu hình vào bộ nhớ đệm
    cache_manager.set(CacheType.CONFIG, "main_config", config)
    return config


def get_config_from_api(config):
    """Lấy cấu hình từ Java API"""
    # Khởi tạo client API
    init_service(config)

    # Lấy cấu hình máy chủ
    config_data = get_server_config()
    if config_data is None:
        raise Exception("Failed to fetch server config from API")

    config_data["read_config_from_api"] = True
    config_data["manager-api"] = {
        "url": config["manager-api"].get("url", ""),
        "secret": config["manager-api"].get("secret", ""),
    }
    # Cấu hình server lấy cục bộ làm chuẩn
    if config.get("server"):
        config_data["server"] = {
            "ip": config["server"].get("ip", ""),
            "port": config["server"].get("port", ""),
            "http_port": config["server"].get("http_port", ""),
            "vision_explain": config["server"].get("vision_explain", ""),
            "auth_key": config["server"].get("auth_key", ""),
        }
    # Nếu máy chủ không có prompt_template, thì đọc từ cấu hình cục bộ
    if not config_data.get("prompt_template"):
        config_data["prompt_template"] = config.get("prompt_template")
    return config_data


def get_private_config_from_api(config, device_id, client_id):
    """Lấy cấu hình riêng tư từ Java API"""
    return get_agent_models(device_id, client_id, config["selected_module"])


def ensure_directories(config):
    """Đảm bảo tất cả đường dẫn cấu hình tồn tại"""
    dirs_to_create = set()
    project_dir = get_project_dir()  # Lấy thư mục gốc dự án
    # Thư mục tệp nhật ký
    log_dir = config.get("log", {}).get("log_dir", "tmp")
    dirs_to_create.add(os.path.join(project_dir, log_dir))

    # Thư mục đầu ra mô-đun ASR/TTS
    for module in ["ASR", "TTS"]:
        if config.get(module) is None:
            continue
        for provider in config.get(module, {}).values():
            output_dir = provider.get("output_dir", "")
            if output_dir:
                dirs_to_create.add(output_dir)

    # Tạo thư mục mô hình dựa trên selected_module
    selected_modules = config.get("selected_module", {})
    for module_type in ["ASR", "LLM", "TTS"]:
        selected_provider = selected_modules.get(module_type)
        if not selected_provider:
            continue
        if config.get(module_type) is None:
            continue
        if config.get(module_type).get(selected_provider) is None:
            continue
        provider_config = config.get(module_type, {}).get(selected_provider, {})
        output_dir = provider_config.get("output_dir")
        if output_dir:
            full_model_dir = os.path.join(project_dir, output_dir)
            dirs_to_create.add(full_model_dir)

    # Tạo thư mục thống nhất (giữ lại việc tạo thư mục data gốc)
    for dir_path in dirs_to_create:
        try:
            os.makedirs(dir_path, exist_ok=True)
        except PermissionError:
            print(f"Cảnh báo: Không thể tạo thư mục {dir_path}, vui lòng kiểm tra quyền ghi")


def merge_configs(default_config, custom_config):
    """
    Gộp cấu hình đệ quy, custom_config ưu tiên cao hơn

    Args:
        default_config: Cấu hình mặc định
        custom_config: Cấu hình tùy chỉnh của người dùng

    Returns:
        Cấu hình sau khi gộp
    """
    if not isinstance(default_config, Mapping) or not isinstance(custom_config, Mapping):
        return custom_config

    merged = dict(default_config)
    for key, value in custom_config.items():
        if key in merged and isinstance(merged[key], Mapping) and isinstance(value, Mapping):
            merged[key] = merge_configs(merged[key], value)
        else:
            merged[key] = value
    return merged
