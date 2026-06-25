"""
Tệp WSGI (Web Server Gateway Interface) — điểm vào chuẩn để triển khai
dự án Django lên server thật (Apache, Nginx+Gunicorn, uWSGI...).

Khi server HTTP nhận request, nó sẽ gọi biến `application` ở file này
để chuyển tiếp request vào Django.

Trong quá trình phát triển (`python manage.py runserver`) file này ít dùng,
chỉ thật sự cần khi đưa lên môi trường production.
"""

import os

# Lấy hàm get_wsgi_application — hàm này trả về một "callable" có khả năng
# xử lý HTTP request theo chuẩn WSGI.
from django.core.wsgi import get_wsgi_application

# Trỏ DJANGO_SETTINGS_MODULE tới file settings.py của dự án.
# setdefault: chỉ đặt nếu biến chưa có sẵn trong môi trường.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cau_hinh_he_thong.settings')

# Biến `application` là đối tượng WSGI mà server sẽ gọi.
# Tên `application` là quy ước bắt buộc theo chuẩn WSGI (PEP 3333).
application = get_wsgi_application()
