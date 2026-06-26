"""
Tệp điều hướng URL CHÍNH của toàn bộ dự án (cau_hinh_he_thong/duong_dan.py).
---------------------------------------------------------------------------
Trong Django, khi người dùng gõ một địa chỉ web (URL) thì Django sẽ tra trong
biến `urlpatterns` ở file này để biết cần gọi view nào để xử lý.

File này chỉ điều hướng 2 nhóm chính:
  1. /admin/*       → giao diện admin có sẵn của Django
  2. mọi đường khác → giao cho file duong_dan.py của app 'ung_dung_giao_tiep'
                     (file đó sẽ định nghĩa 17 endpoint cụ thể).
"""

# Nhập admin site có sẵn của Django (giao diện /admin).
from django.contrib import admin

# `path`    : hàm định nghĩa 1 URL pattern (đường dẫn → view).
# `include` : hàm "chuyển tiếp" một nhóm URL sang file duong_dan.py khác.
from django.urls import path, include

# Nhập settings để kiểm tra DEBUG (chỉ phục vụ tệp tĩnh khi đang debug).
from django.conf import settings

# Nhập hàm static() để thêm route phục vụ tệp tĩnh trong chế độ DEBUG.
from django.conf.urls.static import static

# Django bắt buộc biến này phải tên là `urlpatterns`.
# Mỗi phần tử là kết quả của path(...) — một cặp (URL → view).
urlpatterns = [
    # /admin/ → vào giao diện quản trị có sẵn của Django (tạo user, xem DB...).
    path('admin/', admin.site.urls),

    # path('', ...) nghĩa là URL gốc '/'. include(...) nghĩa là "chuyển tiếp
    # toàn bộ đường dẫn con sang file ung_dung_giao_tiep/duong_dan.py".
    # Ví dụ: /danh-sach sẽ được file đó xử lý tiếp.
    path('', include('ung_dung_giao_tiep.duong_dan')),
]

# Khi DEBUG=True, Django không tự phục vụ tệp tĩnh (CSS/JS/hình) — phải thêm
# thủ công bằng cách nối (+=) kết quả của hàm static() vào urlpatterns.
# static(url, document_root=...) tạo ra các route:
#   /tep_tinh/... → file tương ứng trong thư mục tep_tinh/.
if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,                                                        # Tiền tố URL = 'tep_tinh/'
        document_root=settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else None  # Thư mục gốc
    )
