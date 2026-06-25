"""
Tệp apps.py — Cấu hình riêng của ứng dụng `ung_dung_giao_tiep`.

Mỗi app trong Django có thể có một lớp AppConfig để khai báo metadata
(tên, nhãn, cấu hình mặc định...). Django tự động tìm lớp này khi app
được thêm vào INSTALLED_APPS trong settings.py.
"""

# Nhập lớp cơ sở AppConfig mà mọi cấu hình app phải kế thừa.
from django.apps import AppConfig


# Lớp cấu hình cho ứng dụng `ung_dung_giao_tiep`.
# Tên lớp thường viết theo CamelCase + hậu tố Config.
class UngDungGiaoTiepConfig(AppConfig):
    # `name` là đường dẫn Python đầy đủ đến app (từ thư mục gốc dự án).
    # Phải khớp với tên thư mục và tên trong INSTALLED_APPS.
    name = 'ung_dung_giao_tiep'

    # Có thể ghi đè các thuộc tính khác:
    #   default_auto_field = 'django.db.models.BigAutoField'
    #   verbose_name = 'Ứng dụng giao tiếp'
    # Nhưng ở đây giữ mặc định — không cần tùy biến thêm.
