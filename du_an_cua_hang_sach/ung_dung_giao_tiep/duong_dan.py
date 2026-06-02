"""
Tệp điều hướng các đường dẫn (URL) của ứng dụng giao tiếp.
Mỗi đường dẫn được gắn với một hàm xử lý yêu cầu tương ứng trong xu_ly_yeu_cau.py.
"""

from django.urls import path
from . import xu_ly_yeu_cau

# Danh sách các đường dẫn URL của ứng dụng
danh_sach_duong_dan = [
    # Trang chủ - Hiển thị giao diện chính
    path('', xu_ly_yeu_cau.trang_chu, name='trang_chu'),

    # API: Lấy danh sách tất cả mặt hàng
    path('danh-sach', xu_ly_yeu_cau.lay_danh_sach, name='lay_danh_sach'),

    # API: Thêm sản phẩm mới
    path('them-san-pham', xu_ly_yeu_cau.them_san_pham, name='them_san_pham'),

    # API: Xóa sản phẩm theo mã số
    path('xoa-san-pham', xu_ly_yeu_cau.xoa_san_pham, name='xoa_san_pham'),

    # API: Tìm kiếm sản phẩm theo từ khóa
    path('tim-kiem', xu_ly_yeu_cau.tim_kiem_san_pham, name='tim_kiem_san_pham'),

    # API: Sắp xếp danh sách theo tiêu chí
    path('sap-xep', xu_ly_yeu_cau.sap_xep_danh_sach, name='sap_xep_danh_sach'),
]
