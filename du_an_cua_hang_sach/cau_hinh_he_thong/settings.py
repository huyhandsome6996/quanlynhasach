"""
Tệp cấu hình hệ thống của dự án Django.
Chứa các cài đặt cho ứng dụng, cơ sở dữ liệu, tệp tĩnh, mẫu, v.v.
"""

from pathlib import Path
import os

# Đường dẫn gốc của dự án
BASE_DIR = Path(__file__).resolve().parent.parent

# Khóa bảo mật (Chỉ dùng cho môi trường phát triển)
SECRET_KEY = 'django-insecure-a4@lbf20iek_gw3b7^y5@c_)_1g0=*u8wf+9(x15cq(@z&aslk'

# Chế độ gỡ lỗi (Đổi thành False khi triển khai thực tế)
DEBUG = True

# Các host được phép truy cập
ALLOWED_HOSTS = ['*']

# Danh sách ứng dụng đã cài đặt
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ung_dung_giao_tiep',
]

# Các middleware xử lý yêu cầu/phản hồi
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Tệp điều hướng URL chính của dự án
ROOT_URLCONF = 'cau_hinh_he_thong.duong_dan'

# Cấu hình mẫu (Templates) - Trỏ đến thư mục giao_dien
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'giao_dien')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Ứng dụng WSGI
WSGI_APPLICATION = 'cau_hinh_he_thong.wsgi.application'

# Cấu hình cơ sở dữ liệu SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Kiểm tra mật khẩu
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Quốc tế hóa
LANGUAGE_CODE = 'vi'
TIME_ZONE = 'Asia/Ho_Chi_Minh'
USE_I18N = True
USE_TZ = True

# Cấu hình tệp tĩnh (CSS, JavaScript, Hình ảnh)
# Trỏ đến thư mục tep_tinh chứa mã lệnh và hình thức
STATIC_URL = 'tep_tinh/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'tep_tinh'),
]

# Đường dẫn mặc định cho trường tự động tăng
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
