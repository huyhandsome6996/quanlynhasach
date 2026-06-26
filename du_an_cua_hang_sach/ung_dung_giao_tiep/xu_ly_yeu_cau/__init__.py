"""
Package xu_ly_yeu_cau — chia file views lớn thành các module nhỏ theo nhóm chức năng.
=======================================================================================

Cấu trúc:
    khoi_tao.py           — Biến toàn cục + hàm khởi tạo hệ thống
    xac_thuc.py           — Đăng nhập / Đăng xuất / Phân quyền (NHÓM 1)
    san_pham.py           — CRUD sản phẩm: Đọc / Thêm / Sửa / Xóa (NHÓM 2-5)
    tim_kiem_thong_ke.py  — Tìm kiếm + Sắp xếp + Thống kê (NHÓM 6-7)
    hoan_tac.py           — Undo / Redo bằng Stack LIFO (NHÓM 8)
    gio_hang.py           — Giỏ hàng bằng Queue FIFO (NHÓM 9)

File __init__.py này re-export (xuất lại) tất cả các hàm view ra bên ngoài,
để file duong_dan.py vẫn import được bằng cú pháp cũ:
    from . import xu_ly_yeu_cau
    xu_ly_yeu_cau.trang_chu  ← vẫn hoạt động bình thường.
"""

# KHỞI TẠO HỆ THỐNG (chạy 1 lần đầu)
from .khoi_tao import (
    khoi_tao_danh_sach,
    Danh_sach_cua_hang,
    Bo_undoredo,
    Gio_hang_hien_tai,
)

# NHÓM 1: Xác thực
from .xac_thuc import (
    trang_chu,
    trang_dang_nhap,
    xu_ly_dang_nhap,
    xu_ly_dang_xuat,
    thong_tin_nguoi_dung,
    la_admin,
)

# NHÓM 2-5: Sản phẩm (CRUD)
from .san_pham import (
    lay_danh_sach,
    them_san_pham,
    sua_san_pham,
    xoa_san_pham,
)

# NHÓM 6-7: Tìm kiếm + Thống kê
from .tim_kiem_thong_ke import (
    tim_kiem_san_pham,
    sap_xep_danh_sach,
    lay_thong_ke,
)

# NHÓM 8: Undo / Redo
from .hoan_tac import (
    hoan_tac,
    lam_lai,
)

# NHÓM 9: Giỏ hàng
from .gio_hang import (
    them_vao_gio_hang,
    xem_gio_hang,
    xoa_khoi_gio_hang,
    thanh_toan,
)
