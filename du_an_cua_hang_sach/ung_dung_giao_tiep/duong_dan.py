"""
Tệp điều hướng URL của ứng dụng `ung_dung_giao_tiep`.
-----------------------------------------------------
File này định nghĩa 17 endpoint (đường dẫn URL) cho 9 nhóm chức năng
theo đúng barem chấm điểm của môn Lập trình Nâng cao.

Mỗi dòng `path(...)` sẽ ánh xạ:
    URL người dùng gõ  →  hàm view xử lý  (trong file xu_ly_yeu_cau.py)
                         + tên route (name=...) để dùng reverse() trong template.
"""

# Nhập hàm path để định nghĩa một URL pattern.
from django.urls import path

# Nhập module chứa các hàm view xử lý request (cùng thư mục).
# Dấu `.` nghĩa là "module trong cùng package này".
from . import xu_ly_yeu_cau

# Django bắt buộc biến phải tên là `urlpatterns`.
urlpatterns = [
    # ============================================================
    # NHÓM 1: ĐĂNG NHẬP / ĐĂNG XUẤT / PHÂN QUYỀN
    # ============================================================

    # URL gốc '/' → trang_chu (nếu chưa đăng nhập sẽ redirect sang /dang-nhap).
    path('',                      xu_ly_yeu_cau.trang_chu,         name='trang_chu'),

    # GET /dang-nhap → hiện form đăng nhập (HTML).
    path('dang-nhap',             xu_ly_yeu_cau.trang_dang_nhap,   name='trang_dang_nhap'),

    # POST /api/dang-nhap → API kiểm tra tài khoản + mật khẩu, lưu session.
    path('api/dang-nhap',         xu_ly_yeu_cau.xu_ly_dang_nhap,   name='xu_ly_dang_nhap'),

    # POST /api/dang-xuat → API xóa session (dùng fetch).
    path('api/dang-xuat',         xu_ly_yeu_cau.xu_ly_dang_xuat,   name='xu_ly_dang_xuat'),

    # GET /dang-xuat → cũng đăng xuất nhưng dùng thẳng <a href> trong HTML.
    path('dang-xuat',             xu_ly_yeu_cau.xu_ly_dang_xuat,   name='dang_xuat_get'),

    # GET /api/nguoi-dung → API trả về thông tin người dùng đang đăng nhập.
    path('api/nguoi-dung',        xu_ly_yeu_cau.thong_tin_nguoi_dung, name='thong_tin_nguoi_dung'),


    # ============================================================
    # NHÓM 2: ĐỌC DANH SÁCH
    # ============================================================

    # GET /danh-sach → trả JSON toàn bộ mặt hàng trong kho.
    path('danh-sach',             xu_ly_yeu_cau.lay_danh_sach,     name='lay_danh_sach'),


    # ============================================================
    # NHÓM 3: THÊM SẢN PHẨM
    # ============================================================

    # POST /them-san-pham → API thêm 1 mặt hàng mới (5 loại: Sách/Tạp chí/Báo/Luận văn/Bản thảo).
    path('them-san-pham',         xu_ly_yeu_cau.them_san_pham,     name='them_san_pham'),


    # ============================================================
    # NHÓM 4: SỬA SẢN PHẨM
    # ============================================================

    # POST /sua-san-pham → API cập nhật thông tin sản phẩm theo mã số.
    path('sua-san-pham',          xu_ly_yeu_cau.sua_san_pham,      name='sua_san_pham'),


    # ============================================================
    # NHÓM 5: XÓA SẢN PHẨM (CHỈ ADMIN ĐƯỢC XÓA)
    # ============================================================

    # POST /xoa-san-pham → API xóa sản phẩm; view sẽ kiểm tra quyền admin.
    path('xoa-san-pham',          xu_ly_yeu_cau.xoa_san_pham,      name='xoa_san_pham'),


    # ============================================================
    # NHÓM 6: TÌM KIẾM + SẮP XẾP
    # ============================================================

    # GET /tim-kiem?tu_khoa=...&tieu_chi=ten|ma|loai → tìm kiếm nâng cao.
    path('tim-kiem',              xu_ly_yeu_cau.tim_kiem_san_pham, name='tim_kiem_san_pham'),

    # GET /sap-xep?tieu_chi=gia_ban|ten_san_pham|ton_kho → sắp xếp bằng Merge Sort.
    path('sap-xep',               xu_ly_yeu_cau.sap_xep_danh_sach, name='sap_xep_danh_sach'),


    # ============================================================
    # NHÓM 7: THỐNG KÊ
    # ============================================================

    # GET /thong-ke → JSON tổng mặt hàng, sắp hết hàng, tổng giá trị kho, đắt/re nhất.
    path('thong-ke',              xu_ly_yeu_cau.lay_thong_ke,      name='lay_thong_ke'),


    # ============================================================
    # NHÓM 8: UNDO / REDO (STACK LIFO)
    # ============================================================

    # POST /hoan-tac → hoàn tác thao tác gần nhất (Undo).
    path('hoan-tac',              xu_ly_yeu_cau.hoan_tac,          name='hoan_tac'),

    # POST /lam-lai → làm lại thao tác vừa undo (Redo).
    path('lam-lai',               xu_ly_yeu_cau.lam_lai,           name='lam_lai'),


    # ============================================================
    # NHÓM 9: GIỎ HÀNG (QUEUE FIFO)
    # ============================================================

    # POST /them-gio-hang → thêm sản phẩm vào cuối hàng đợi giỏ hàng.
    path('them-gio-hang',         xu_ly_yeu_cau.them_vao_gio_hang, name='them_vao_gio_hang'),

    # GET /xem-gio-hang → liệt kê toàn bộ sản phẩm đang có trong giỏ.
    path('xem-gio-hang',          xu_ly_yeu_cau.xem_gio_hang,      name='xem_gio_hang'),

    # POST /xoa-gio-hang → bỏ 1 sản phẩm ra khỏi giỏ.
    path('xoa-gio-hang',          xu_ly_yeu_cau.xoa_khoi_gio_hang, name='xoa_khoi_gio_hang'),

    # POST /thanh-toan → tính tổng tiền + xóa toàn bộ giỏ (theo FIFO).
    path('thanh-toan',            xu_ly_yeu_cau.thanh_toan,        name='thanh_toan'),
]
