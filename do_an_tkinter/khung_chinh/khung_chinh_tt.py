"""
Tệp khung_chinh_tt.py — THUẬT TOÁN / STATE cho Cửa sổ chính
=============================================================

Lớp QuanLyTrungTam — giữ trạng thái toàn cục của ứng dụng:
    - danh_sach : DoublyLinkedList (DSLK đôi) chứa toàn bộ sản phẩm.
    - bo_undoredo : dict 2 Stack (NganXep) 'undo' + 'redo'.
    - gio_hang  : HangDoi (Queue FIFO).
    - nguoi_dung_hien_tai : NguoiDung đang đăng nhập (None = chưa login).

Vai trò: bộ điều phối trung tâm — giữ tham chiếu các cấu trúc dữ liệu
toàn cục, sau đó UI/Điều khiển các chức năng sẽ thao tác qua các tham chiếu này.

Lớp này ủy quyền các thao tác cho các module thuật toán trong
chuc_nang/*/_tt.py — bản chất nó là facade (mặt tiền) để mã cũ và
test_app.py tiếp tục chạy được.
"""

import os

# Import các cấu trúc dữ liệu tự cài đặt.
from loi_thuat_toan.danh_sach_lien_ket import DoublyLinkedList
from loi_thuat_toan.cau_truc_du_lieu import NganXep, HangDoi
# Import hàm kết nối SQLite.
from loi_thuat_toan.ket_noi_sqlite import (
    tao_bang_neu_chua_co,
    tai_du_lieu,
    tao_du_lieu_mau_neu_rong,
)
# Import hàm quản lý người dùng.
from loi_thuat_toan.nguoi_dung import (
    khoi_tao_nguoi_dung_mac_dinh,
    kiem_tra_dang_nhap,
)


class QuanLyTrungTam:
    """
    Lớp quản lý trung tâm — giữ các cấu trúc dữ liệu toàn cục + cung cấp
    API cho UI/Điều khiển gọi (bọc qua các module chuc_nang/*/_tt.py).
    """

    def __init__(self):
        """Khởi tạo — chưa có gì cho tới khi khoi_tao() được gọi."""
        # DSLK đôi chứa toàn bộ mặt hàng.
        self.danh_sach = None
        # Dict chứa 2 Stack: 'undo' và 'redo'.
        self.bo_undoredo = None
        # Queue giỏ hàng.
        self.gio_hang = None
        # Người dùng đang đăng nhập (None = chưa login).
        self.nguoi_dung_hien_tai = None

    # ========================================================
    # KHỞI TẠO HỆ THỐNG
    # ========================================================
    def khoi_tao(self):
        """Tạo DB + bảng + dữ liệu mẫu + nạp vào DSLK + tạo Stack/Queue."""
        try:
            # Tạo bảng SQLite nếu chưa có.
            tao_bang_neu_chua_co()
            # Nếu DB rỗng → chèn 5 sản phẩm mẫu.
            tao_du_lieu_mau_neu_rong()
            # Tạo 2 tài khoản mặc định: admin/123 + nhanvien/123.
            khoi_tao_nguoi_dung_mac_dinh()

            # Tạo DSLK đôi rỗng rồi tải dữ liệu từ SQLite vào.
            self.danh_sach = DoublyLinkedList()
            tai_du_lieu(self.danh_sach)

            # 2 Stack cho Undo/Redo.
            self.bo_undoredo = {
                'undo': NganXep(),
                'redo': NganXep()
            }
            # 1 Queue cho giỏ hàng.
            self.gio_hang = HangDoi()

            print(f'[KHOI TAO] Da nap {self.danh_sach.so_luong} mat hang.')
            return True
        except Exception as loi:
            print(f'[LOI KHOI TAO] {loi}')
            return False

    # ========================================================
    # NHÓM 1: ĐĂNG NHẬP / PHÂN QUYỀN  → ủy quyền cho 01_dang_nhap_phan_quyen
    # ========================================================
    def dang_nhap(self, ten_dang_nhap, mat_khau):
        """Kiểm tra đăng nhập. Trả về (True, nguoi_dung) hoặc (False, msg)."""
        try:
            nguoi_dung = kiem_tra_dang_nhap(ten_dang_nhap, mat_khau)
            if nguoi_dung is None:
                return False, 'Sai tên đăng nhập hoặc mật khẩu.'
            self.nguoi_dung_hien_tai = nguoi_dung
            return True, nguoi_dung
        except Exception as loi:
            return False, f'Lỗi: {loi}'

    def dang_xuat(self):
        """Đăng xuất — reset người dùng hiện tại."""
        self.nguoi_dung_hien_tai = None

    def la_admin(self):
        """Kiểm tra user hiện tại có phải admin không."""
        return (self.nguoi_dung_hien_tai is not None and
                self.nguoi_dung_hien_tai.vai_tro == 'admin')

    # ========================================================
    # NHÓM 2: ĐỌC DANH SÁCH  → ủy quyền cho 02_doc_danh_sach
    # ========================================================
    def lay_danh_sach(self):
        """Trả về list dict toàn bộ sản phẩm."""
        # Import hàm từ module chức năng.
        from chuc_nang.cn02_doc_danh_sach.doc_danh_sach_tt import lay_danh_sach as _lay
        return _lay(self.danh_sach)

    # ========================================================
    # NHÓM 3: THÊM SẢN PHẨM  → ủy quyền cho 03_them_san_pham
    # ========================================================
    def them_san_pham(self, du_lieu):
        """Thêm sản phẩm mới. Trả về (True, msg) hoặc (False, msg)."""
        from chuc_nang.cn03_them_san_pham.them_san_pham_tt import them_san_pham as _them
        return _them(self.danh_sach, self.bo_undoredo, du_lieu)

    # ========================================================
    # NHÓM 4: SỬA SẢN PHẨM  → ủy quyền cho 04_sua_san_pham
    # ========================================================
    def sua_san_pham(self, du_lieu):
        """Cập nhật sản phẩm theo mã."""
        from chuc_nang.cn04_sua_san_pham.sua_san_pham_tt import sua_san_pham as _sua
        return _sua(self.danh_sach, self.bo_undoredo, du_lieu)

    # ========================================================
    # NHÓM 5: XÓA SẢN PHẨM  → ủy quyền cho 05_xoa_san_pham
    # ========================================================
    def xoa_san_pham(self, ma_so):
        """Xóa sản phẩm (chỉ admin). Trả về (True, msg) hoặc (False, msg)."""
        from chuc_nang.cn05_xoa_san_pham.xoa_san_pham_tt import xoa_san_pham as _xoa
        return _xoa(self.danh_sach, self.bo_undoredo, ma_so, self.la_admin())

    # ========================================================
    # NHÓM 6: TÌM KIẾM + SẮP XẾP  → ủy quyền cho 06_tim_kiem_sap_xep
    # ========================================================
    def tim_kiem(self, tu_khoa, tieu_chi='ten'):
        """Trả về list dict kết quả tìm."""
        from chuc_nang.cn06_tim_kiem_sap_xep.tim_kiem_sap_xep_tt import tim_kiem as _tk
        return _tk(self.danh_sach, tu_khoa, tieu_chi)

    def sap_xep(self, tieu_chi='gia_ban'):
        """Sắp xếp DSLK bằng Merge Sort + trả về list dict."""
        from chuc_nang.cn06_tim_kiem_sap_xep.tim_kiem_sap_xep_tt import sap_xep as _sx
        return _sx(self.danh_sach, tieu_chi)

    # ========================================================
    # NHÓM 7: THỐNG KÊ  → ủy quyền cho 07_thong_ke
    # ========================================================
    def lay_thong_ke(self):
        """Trả về dict thống kê."""
        from chuc_nang.cn07_thong_ke.thong_ke_tt import lay_thong_ke as _tk
        return _tk(self.danh_sach)

    # ========================================================
    # NHÓM 8: UNDO / REDO  → ủy quyền cho 08_hoan_tac_lam_lai
    # ========================================================
    def hoan_tac(self):
        """Undo — hoàn tác thao tác gần nhất."""
        from chuc_nang.cn08_hoan_tac_lam_lai.hoan_tac_lam_lai_tt import hoan_tac as _ht
        return _ht(self.danh_sach, self.bo_undoredo)

    def lam_lai(self):
        """Redo — làm lại thao tác đã undo."""
        from chuc_nang.cn08_hoan_tac_lam_lai.hoan_tac_lam_lai_tt import lam_lai as _ll
        return _ll(self.danh_sach, self.bo_undoredo)

    def trang_thai_undoredo(self):
        """Trả về dict trạng thái undo/redo (cho UI bật/tắt nút)."""
        from chuc_nang.cn08_hoan_tac_lam_lai.hoan_tac_lam_lai_tt import trang_thai as _tt
        return _tt(self.bo_undoredo)

    # ========================================================
    # NHÓM 9: GIỎ HÀNG  → ủy quyền cho 09_gio_hang
    # ========================================================
    def them_vao_gio(self, ma_so):
        """Enqueue sản phẩm vào giỏ."""
        from chuc_nang.cn09_gio_hang.gio_hang_tt import them_vao_gio as _tvg
        return _tvg(self.danh_sach, self.gio_hang, ma_so)

    def xem_gio_hang(self):
        """Trả về (list dict, tong_tien, so_luong)."""
        from chuc_nang.cn09_gio_hang.gio_hang_tt import xem_gio_hang as _xgh
        return _xgh(self.gio_hang)

    def xoa_khoi_gio(self, ma_so):
        """Xóa 1 món khỏi giỏ."""
        from chuc_nang.cn09_gio_hang.gio_hang_tt import xoa_khoi_gio as _xkg
        return _xkg(self.gio_hang, ma_so)

    def thanh_toan(self):
        """Dequeue toàn bộ giỏ → trả hóa đơn."""
        from chuc_nang.cn09_gio_hang.gio_hang_tt import thanh_toan as _tt
        return _tt(self.gio_hang)
