"""
Tệp cấu hình hệ thống (settings.py) của dự án Django.
-----------------------------------------------------
Mọi cài đặt chung cho toàn bộ dự án đều nằm ở đây:
- Đường dẫn gốc, khóa bảo mật, chế độ gỡ lỗi
- Danh sách ứng dụng đã cài đặt
- Middleware (các lớp xử lý request/response)
- Cấu hình database (SQLite)
- Cấu hình template (HTML), tệp tĩnh (CSS/JS)
- Ngôn ngữ, múi giờ

Tài liệu chính thức: https://docs.djangoproject.com/en/5.0/ref/settings/
"""

# Path là lớp tiện lợi của Python 3 để xử lý đường dẫn
# độc lập với hệ điều hành (dấu gạch chéo / hay \).
from pathlib import Path

# os dùng để ghép đường dẫn (os.path.join) khi cấu hình thư mục template/static.
import os

# Đường dẫn gốc của dự án = thư mục cha của thư mục chứa file settings.py này.
# Ví dụ: file settings nằm ở
#   /du_an_cua_hang_sach/cau_hinh_he_thong/settings.py
# → __file__ = .../settings.py
# → .resolve().parent = .../cau_hinh_he_thong/
# → .parent.parent = .../du_an_cua_hang_sach/   ← đây chính là BASE_DIR.
BASE_DIR = Path(__file__).resolve().parent.parent

# Khóa bí mật dùng để ký các dữ liệu nhạy cảm (session, CSRF token, ...).
# WARNING: 'django-insecure-...' là tiền tố báo chuỗi này chưa an toàn.
# Trong môi trường production (triển khai thật) phải đặt thành chuỗi ngẫu nhiên
# dài 50+ ký tự và KHÔNG được đẩy lên git — lấy từ biến môi trường thay vào đó.
SECRET_KEY = 'django-insecure-a4@lbf20iek_gw3b7^y5@c_)_1g0=*u8wf+9(x15cq(@z&aslk'

# DEBUG = True → Django hiện trang lỗi chi tiết (kèm traceback) khi có exception.
# Rất hữu ích khi phát triển, nhưng PHẢI đặt False khi đưa lên mạng thật
# vì lộ thông tin nhạy cảm nếu để True.
DEBUG = True

# Danh sách host/domain được phép phục vụ request.
# ['*'] nghĩa là chấp nhận mọi host — chỉ dùng khi DEBUG=True.
# Khi production cần ghi cụ thể: ['mydomain.com', 'www.mydomain.com'].
ALLOWED_HOSTS = ['*']

# INSTALLED_APPS — danh sách các ứng dụng Django được kích hoạt trong dự án.
# - 6 dòng đầu là các app có sẵn của Django (admin, auth, sessions, ...).
# - 'ung_dung_giao_tiep' là app do nhóm tự viết, nằm trong thư mục cùng tên.
INSTALLED_APPS = [
    'django.contrib.admin',          # Giao diện quản trị /admin
    'django.contrib.auth',           # Hệ thống xác thực (User, Group, Permission)
    'django.contrib.contenttypes',   # Theo dõi các kiểu nội dung trong DB
    'django.contrib.sessions',       # Lưu session đăng nhập
    'django.contrib.messages',       # Hiển thị thông báo một lần (flash messages)
    'django.contrib.staticfiles',    # Phục vụ tệp tĩnh (CSS/JS/hình)
    'ung_dung_giao_tiep',            # ← ỨNG DỤNG CHÍNH của dự án này
]

# MIDDLEWARE — chuỗi các lớp xử lý request TRƯỚC khi tới view và response
# SAU khi view trả về. Thứ tự rất quan trọng.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',            # Bảo mật (HTTPS, HSTS)
    'django.contrib.sessions.middleware.SessionMiddleware',     # Đọc/ghi session
    'django.middleware.common.CommonMiddleware',                # Chuẩn hóa URL
    'django.middleware.csrf.CsrfViewMiddleware',                # Chống tấn công CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Gán request.user
    'django.contrib.messages.middleware.MessageMiddleware',     # Flash messages
    'django.middleware.clickjacking.XFrameOptionsMiddleware',   # Chống clickjacking
]

# ROOT_URLCONF — Django sẽ đọc file này để biết URL nào → view nào.
# 'cau_hinh_he_thong.duong_dan' tương ứng với
#   cau_hinh_he_thong/duong_dan.py
ROOT_URLCONF = 'cau_hinh_he_thong.duong_dan'

# TEMPLATES — cấu hình bộ xử lý HTML template.
# DIRS: danh sách thư mục chứa file .html (ngoài thư mục app).
# Ở đây trỏ tới thư mục 'giao_dien' để Django tìm trang_chu.html, dang_nhap.html...
TEMPLATES = [
    {
        # Dùng engine template mặc định của Django.
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Thư mục chứa template cấp dự án (templates ở thư mục gốc).
        'DIRS': [os.path.join(BASE_DIR, 'giao_dien')],
        # APP_DIRS=True → Django cũng tìm trong thư mục templates/ của mỗi app.
        'APP_DIRS': True,
        'OPTIONS': {
            # Context processors — các hàm tự động thêm biến vào mọi template:
            'context_processors': [
                'django.template.context_processors.request',   # Thêm biến `request`
                'django.contrib.auth.context_processors.auth',  # Thêm biến `user`
                'django.contrib.messages.context_processors.messages',  # Thêm `messages`
            ],
        },
    },
]

# WSGI_APPLICATION — điểm vào chuẩn WSGI để deploy trên server thật (Gunicorn, uWSGI).
WSGI_APPLICATION = 'cau_hinh_he_thong.wsgi.application'

# DATABASES — cấu hình cơ sở dữ liệu.
# Dự án này dùng SQLite — database một-file (db.sqlite3), không cần cài server.
# Ưu điểm: nhẹ, không cần cấu hình, lý tưởng cho đồ án học tập.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',     # Loại DB = SQLite
        'NAME': BASE_DIR / 'db.sqlite3',            # Đường dẫn file DB
    }
}

# AUTH_PASSWORD_VALIDATORS — các validator kiểm tra độ mạnh mật khẩu
# khi tạo user bằng /admin hoặc createsuperuser.
# (Dự án này tự quản lý bảng người dùng riêng nên không dùng trực tiếp,
# nhưng vẫn giữ để tương thích với Django admin.)
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},  # Mật khẩu không được giống thông tin user
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},            # Độ dài tối thiểu
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},           # Không được quá phổ biến
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},          # Không được toàn số
]

# Quốc tế hóa (i18n) — ngôn ngữ và múi giờ hiển thị.
LANGUAGE_CODE = 'vi'               # Tiếng Việt
TIME_ZONE = 'Asia/Ho_Chi_Minh'     # Múi giờ Việt Nam (UTC+7)
USE_I18N = True                    # Bật dịch thuật
USE_TZ = True                      # Lưu thời gian theo múi giờ (có timezone)

# Cấu hình tệp tĩnh (CSS/JS/hình ảnh) cho frontend.
# STATIC_URL là tiền tố URL công khai: http://127.0.0.1:8000/tep_tinh/...
STATIC_URL = 'tep_tinh/'

# STATICFILES_DIRS — danh sách thư mục chứa tệp tĩnh ngoài (không nằm trong app).
# Django sẽ tìm trong các thư mục này khi chạy collectstatic hoặc DEBUG=True.
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'tep_tinh'),   # → du_an_cua_hang_sach/tep_tinh/
]

# DEFAULT_AUTO_FIELD — kiểu trường khóa chính mặc định cho mọi model.
# BigAutoField = số nguyên tự tăng 64-bit (chuẩn hiện đại của Django).
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
