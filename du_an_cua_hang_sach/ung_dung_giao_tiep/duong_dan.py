"""
Tệp điều hướng các đường dẫn (URL) của ứng dụng giao tiếp.
Mỗi đường dẫn được gắn với một hàm xử lý yêu cầu tương ứng trong xu_ly_yeu_cau.py.
"""

from django.urls import path
from . import xu_ly_yeu_cau

# Django yêu cầu biến phải tên là 'urlpatterns'
urlpatterns = [
    # ---- Trang chủ ----
    path('', xu_ly_yeu_cau.trang_chu, name='trang_chu'),

    # ---- API: Quản lý sản phẩm (CRUD) ----
    path('danh-sach', xu_ly_yeu_cau.lay_danh_sach, name='lay_danh_sach'),
    path('them-san-pham', xu_ly_yeu_cau.them_san_pham, name='them_san_pham'),
    path('sua-san-pham', xu_ly_yeu_cau.sua_san_pham, name='sua_san_pham'),
    path('xoa-san-pham', xu_ly_yeu_cau.xoa_san_pham, name='xoa_san_pham'),

    # ---- API: Tìm kiếm và Sắp xếp ----
    path('tim-kiem', xu_ly_yeu_cau.tim_kiem_san_pham, name='tim_kiem_san_pham'),
    path('sap-xep', xu_ly_yeu_cau.sap_xep_danh_sach, name='sap_xep_danh_sach'),

    # ---- API: Thống kê ----
    path('thong-ke', xu_ly_yeu_cau.thong_ke, name='thong_ke'),

    # ---- API: Giỏ hàng (Queue) ----
    path('them-gio-hang', xu_ly_yeu_cau.them_gio_hang, name='them_gio_hang'),
    path('xem-gio-hang', xu_ly_yeu_cau.xem_gio_hang, name='xem_gio_hang'),
    path('xoa-gio-hang', xu_ly_yeu_cau.xoa_gio_hang, name='xoa_gio_hang'),
    path('thanh-toan', xu_ly_yeu_cau.thanh_toan, name='thanh_toan'),

    # ---- API: Undo/Redo (Stack) ----
    path('hoan-tac', xu_ly_yeu_cau.hoan_tac, name='hoan_tac'),
    path('lam-lai', xu_ly_yeu_cau.lam_lai, name='lam_lai'),
]
