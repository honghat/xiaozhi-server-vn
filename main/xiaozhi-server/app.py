import sys
import uuid
import signal
import asyncio
from aioconsole import ainput
from config.settings import load_config
from config.logger import setup_logging
from core.utils.util import get_local_ip, validate_mcp_endpoint
from core.http_server import SimpleHttpServer
from core.websocket_server import WebSocketServer
from core.utils.util import check_ffmpeg_installed

TAG = __name__
logger = setup_logging()


async def wait_for_exit() -> None:
    """
    Chặn cho đến khi nhận được Ctrl-C / SIGTERM.
    - Unix: Sử dụng add_signal_handler
    - Windows: Phụ thuộc vào KeyboardInterrupt
    """
    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()

    if sys.platform != "win32":  # Unix / macOS
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, stop_event.set)
        await stop_event.wait()
    else:
        # Windows: await một fut luôn pending,
        # để KeyboardInterrupt nổi lên asyncio.run, từ đó loại bỏ vấn đề luồng thường còn sót lại gây chặn thoát tiến trình
        try:
            await asyncio.Future()
        except KeyboardInterrupt:  # Ctrl‑C
            pass


async def monitor_stdin():
    """Giám sát đầu vào tiêu chuẩn, tiêu thụ phím Enter"""
    while True:
        await ainput()  # Chờ nhập không đồng bộ, tiêu thụ phím Enter


async def main():
    check_ffmpeg_installed()
    config = load_config()

    # Độ ưu tiên auth_key: tệp cấu hình server.auth_key > manager-api.secret > tự động tạo
    # auth_key dùng cho xác thực jwt, ví dụ xác thực jwt của giao diện phân tích hình ảnh, tạo token giao diện ota và xác thực websocket
    # Lấy auth_key trong tệp cấu hình
    auth_key = config["server"].get("auth_key", "")

    # Xác thực auth_key, nếu không hợp lệ thì thử dùng manager-api.secret
    if not auth_key or len(auth_key) == 0 or "你" in auth_key:
        auth_key = config.get("manager-api", {}).get("secret", "")
        # Xác thực secret, nếu không hợp lệ thì tạo khóa ngẫu nhiên
        if not auth_key or len(auth_key) == 0 or "你" in auth_key:
            auth_key = str(uuid.uuid4().hex)

    config["server"]["auth_key"] = auth_key

    # Thêm tác vụ giám sát stdin
    stdin_task = asyncio.create_task(monitor_stdin())

    # Khởi động máy chủ WebSocket
    ws_server = WebSocketServer(config)
    ws_task = asyncio.create_task(ws_server.start())
    # Khởi động máy chủ Simple http
    ota_server = SimpleHttpServer(config)
    ota_task = asyncio.create_task(ota_server.start())

    read_config_from_api = config.get("read_config_from_api", False)
    port = int(config["server"].get("http_port", 8012))
    if not read_config_from_api:
        logger.bind(tag=TAG).info(
            "Giao diện OTA là\t\thttp://{}:{}/xiaozhi/ota/",
            get_local_ip(),
            port,
        )
    logger.bind(tag=TAG).info(
        "Giao diện phân tích hình ảnh là\thttp://{}:{}/mcp/vision/explain",
        get_local_ip(),
        port,
    )
    mcp_endpoint = config.get("mcp_endpoint", None)
    if mcp_endpoint is not None and "你" not in mcp_endpoint:
        # Kiểm tra định dạng điểm truy cập MCP
        if validate_mcp_endpoint(mcp_endpoint):
            logger.bind(tag=TAG).info("Điểm truy cập mcp là\t{}", mcp_endpoint)
            # Chuyển đổi địa chỉ điểm truy cập mcp thành điểm gọi
            mcp_endpoint = mcp_endpoint.replace("/mcp/", "/call/")
            config["mcp_endpoint"] = mcp_endpoint
        else:
            logger.bind(tag=TAG).error("Điểm truy cập mcp không đúng quy định")
            config["mcp_endpoint"] = "Địa chỉ websocket điểm truy cập của bạn"

    # Lấy cấu hình WebSocket, sử dụng giá trị mặc định an toàn
    websocket_port = 8011
    server_config = config.get("server", {})
    if isinstance(server_config, dict):
        websocket_port = int(server_config.get("port", 8011))

    logger.bind(tag=TAG).info(
        "Địa chỉ Websocket là\tws://{}:{}/xiaozhi/v1/",
        get_local_ip(),
        websocket_port,
    )

    logger.bind(tag=TAG).info(
        "=======Địa chỉ trên là địa chỉ giao thức websocket, vui lòng không truy cập bằng trình duyệt======="
    )
    logger.bind(tag=TAG).info(
        "Nếu muốn kiểm tra websocket, vui lòng mở test_page.html trong thư mục test bằng trình duyệt Chrome"
    )
    logger.bind(tag=TAG).info(
        "=============================================================\n"
    )

    try:
        await wait_for_exit()  # Chặn cho đến khi nhận được tín hiệu thoát
    except asyncio.CancelledError:
        print("Tác vụ bị hủy, đang dọn dẹp tài nguyên...")
    finally:
        # Hủy tất cả tác vụ (điểm sửa lỗi quan trọng)
        stdin_task.cancel()
        ws_task.cancel()
        if ota_task:
            ota_task.cancel()
        await asyncio.gather(stdin_task, ws_task, ota_task, return_exceptions=True)
        print("Tất cả tác vụ đã được dọn dẹp, chương trình thoát.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
