"""
Tệp điều hướng URL chính của dự án.
Điều hướng tất cả yêu cầu đến ứng dụng ung_dung_giao_tiep.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

danh_sach_duong_dan = [
    path('admin/', admin.site.urls),
    # Tất cả đường dẫn khác được xử lý bởi ứng dụng giao tiếp
    path('', include('ung_dung_giao_tiep.duong_dan')),
]

# Phục vụ tệp tĩnh trong chế độ gỡ lỗi
if settings.DEBUG:
    danh_sach_duong_dan += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else None)
