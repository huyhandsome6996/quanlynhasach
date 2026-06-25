"""
Tệp điều hướng URL của ứng dụng ung_dung_giao_tiep.

Đăng ký tất cả endpoint cho 9 nhóm chức năng theo barem chấm điểm.
"""

from django.urls import path
from . import xu_ly_yeu_cau

# Django yêu cầu biến phải tên là 'urlpatterns'
urlpatterns = [
    # ============================================================
    # NHÓM 1: ĐĂNG NHẬP / ĐĂNG XUẤT / PHÂN QUYỀN
    # ============================================================
    path('',                      xu_ly_yeu_cau.trang_chu,         name='trang_chu'),
    path('dang-nhap',             xu_ly_yeu_cau.trang_dang_nhap,   name='trang_dang_nhap'),
    path('api/dang-nhap',         xu_ly_yeu_cau.xu_ly_dang_nhap,   name='xu_ly_dang_nhap'),
    path('api/dang-xuat',         xu_ly_yeu_cau.xu_ly_dang_xuat,   name='xu_ly_dang_xuat'),
    path('dang-xuat',             xu_ly_yeu_cau.xu_ly_dang_xuat,   name='dang_xuat_get'),
    path('api/nguoi-dung',        xu_ly_yeu_cau.thong_tin_nguoi_dung, name='thong_tin_nguoi_dung'),

    # ============================================================
    # NHÓM 2: ĐỌC DANH SÁCH
    # ============================================================
    path('danh-sach',             xu_ly_yeu_cau.lay_danh_sach,     name='lay_danh_sach'),

    # ============================================================
    # NHÓM 3: THÊM SẢN PHẨM
    # ============================================================
    path('them-san-pham',         xu_ly_yeu_cau.them_san_pham,     name='them_san_pham'),

    # ============================================================
    # NHÓM 4: SỬA SẢN PHẨM
    # ============================================================
    path('sua-san-pham',          xu_ly_yeu_cau.sua_san_pham,      name='sua_san_pham'),

    # ============================================================
    # NHÓM 5: XÓA SẢN PHẨM (CHỈ ADMIN)
    # ============================================================
    path('xoa-san-pham',          xu_ly_yeu_cau.xoa_san_pham,      name='xoa_san_pham'),

    # ============================================================
    # NHÓM 6: TÌM KIẾM + SẮP XẾP
    # ============================================================
    path('tim-kiem',              xu_ly_yeu_cau.tim_kiem_san_pham, name='tim_kiem_san_pham'),
    path('sap-xep',               xu_ly_yeu_cau.sap_xep_danh_sach, name='sap_xep_danh_sach'),

    # ============================================================
    # NHÓM 7: THỐNG KÊ
    # ============================================================
    path('thong-ke',              xu_ly_yeu_cau.lay_thong_ke,      name='lay_thong_ke'),

    # ============================================================
    # NHÓM 8: UNDO / REDO (STACK LIFO)
    # ============================================================
    path('hoan-tac',              xu_ly_yeu_cau.hoan_tac,          name='hoan_tac'),
    path('lam-lai',               xu_ly_yeu_cau.lam_lai,           name='lam_lai'),

    # ============================================================
    # NHÓM 9: GIỎ HÀNG (QUEUE FIFO)
    # ============================================================
    path('them-gio-hang',         xu_ly_yeu_cau.them_vao_gio_hang, name='them_vao_gio_hang'),
    path('xem-gio-hang',          xu_ly_yeu_cau.xem_gio_hang,      name='xem_gio_hang'),
    path('xoa-gio-hang',          xu_ly_yeu_cau.xoa_khoi_gio_hang, name='xoa_khoi_gio_hang'),
    path('thanh-toan',            xu_ly_yeu_cau.thanh_toan,        name='thanh_toan'),
]
