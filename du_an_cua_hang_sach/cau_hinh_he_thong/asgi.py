"""
Tệp ASGI (Asynchronous Server Gateway Interface) — điểm vào cho các ứng dụng
Django bất đồng bộ (hỗ trợ WebSocket, HTTP/2, long-poll...).

Khác biệt với WSGI (đồng bộ), ASGI cho phép xử lý nhiều request cùng lúc
bằng asyncio. Dự án này không dùng WebSocket nên file này chỉ để đầy đủ
theo chuẩn Django — server phát triển sẽ ưu tiên dùng file settings.py
thông qua manage.py runserver.
"""

import os

# Lấy hàm get_asgi_application — tạo đối tượng ASGI callable.
from django.core.asgi import get_asgi_application

# Trỏ DJANGO_SETTINGS_MODULE tới file cấu hình settings.py.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cau_hinh_he_thong.settings')

# Biến `application` là điểm vào ASGI — server ASGI (Daphne, Uvicorn...)
# sẽ gọi biến này để xử lý request.
application = get_asgi_application()
