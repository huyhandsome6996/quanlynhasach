#!/usr/bin/env python
# ↑ Dòng "shebang" cho hệ điều hành Unix/Linux biết: hãy dùng trình thông dịch
#   python (lấy từ biến môi trường PATH) để chạy file này khi người dùng gõ
#   ./manage.py trực tiếp thay vì `python manage.py`.

"""
Tệp manage.py — CÔNG CỤ QUẢN TRỊ CỦA DJANGO.
-------------------------------------------------
Đây là file "cửa ngõ" để người lập trình giao tiếp với dự án Django qua
dòng lệnh. Mọi lệnh như `runserver`, `migrate`, `createsuperuser`,
`makemigrations`... đều phải chạy qua file này.

Cách chạy phổ biến:
    python manage.py runserver        # Khởi động server phát triển
    python manage.py migrate          # Áp dụng migrations vào DB
    python manage.py createsuperuser  # Tạo tài khoản admin Django
    python manage.py test             # Chạy bộ test
"""

# Nhập module `os` để đọc/ghi biến môi trường (env vars) của hệ điều hành.
import os

# Nhập module `sys` để truy cập danh sách tham số dòng lệnh `sys.argv`.
import sys


def main():
    """
    Hàm chính — được gọi khi chạy `python manage.py <lệnh>`.

    Trách nhiệm:
      1. Đặt biến môi trường DJANGO_SETTINGS_MODULE trỏ tới file settings.py
         để Django biết phải đọc cấu hình từ đâu.
      2. Gọi hàm execute_from_command_line(sys.argv) của Django — hàm này
         sẽ tự phân tích tham số dòng lệnh và chạy lệnh tương ứng
         (runserver, migrate, ...).
    """
    # Đặt biến môi trường DJANGO_SETTINGS_MODULE = 'cau_hinh_he_thong.settings'
    # Tên này khớp với thư mục 'cau_hinh_he_thong' + file 'settings.py'.
    # setdefault() chỉ đặt nếu biến chưa có → cho phép người dùng ghi đè
    # bằng lệnh: DJANGO_SETTINGS_MODULE=khac python manage.py ...
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cau_hinh_he_thong.settings')

    # Khối try/except để bắt lỗi thiếu thư viện Django — trường hợp người dùng
    # quên cài đặt: `pip install django`.
    try:
        # Nhập hàm execute_from_command_line từ django.core.management.
        # Hàm này sẽ đọc sys.argv (ví dụ ['manage.py', 'runserver'])
        # và gọi tới code xử lý tương ứng của Django.
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Nếu ImportError → Django chưa cài → thông báo lỗi thân thiện.
        # Cú pháp `raise ... from exc` giữ nguyên traceback gốc để dễ gỡ lỗi.
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Gọi hàm Django — toàn bộ công việc xử lý lệnh diễn ra ở đây.
    # sys.argv là danh sách tham số: ['manage.py', 'runserver', '8000', ...]
    execute_from_command_line(sys.argv)


# Đoạn kiểm tra "if __name__ == '__main__'" là idiom chuẩn của Python:
# Nghĩa là: chỉ chạy hàm main() KHI file này được chạy TRỰC TIẾP
# (bằng `python manage.py ...`).
# Nếu file này bị import từ nơi khác (rất hiếm khi) thì main() sẽ KHÔNG chạy,
# tránh tác dụng phụ không mong muốn.
if __name__ == '__main__':
    main()
