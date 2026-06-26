"""
Tệp dang_nhap_tt.py — THUẬT TOÁN cho chức năng Đăng nhập + Phân quyền
======================================================================

Thuật toán (logic) — KHÔNG chứa code giao diện (UI).
UI nằm ở dang_nhap_ui.py. Điểu khiển nằm ở dang_nhap_dk.py.

Chứa:
    - BoDangNhap: lớp đóng gói logic đăng nhập / đăng xuất / kiểm tra quyền.

Tái sử dụng hàm `kiem_tra_dang_nhap` từ loi_thuat_toan.nguoi_dung (đã có sẵn).
"""

# Import hàm kiểm tra đăng nhập từ thư viện thuật toán (loi_thuat_toan/).
from loi_thuat_toan.nguoi_dung import kiem_tra_dang_nhap


class BoDangNhap:
    """
    Bộ thuật toán đăng nhập.
    Giữ người dùng đang đăng nhập hiện tại + cung cấp hàm tiện ích kiểm tra quyền.
    """

    def __init__(self):
        """Khởi tạo: chưa có người dùng nào đăng nhập."""
        # nguoi_dung_hien_tai = None nghĩa là chưa login.
        self.nguoi_dung_hien_tai = None

    # ----------------------------------------------------------------
    # HÀM ĐĂNG NHẬP
    # ----------------------------------------------------------------
    def dang_nhap(self, ten_dang_nhap, mat_khau):
        """
        Kiểm tra đăng nhập.

        Tham số:
            ten_dang_nhap : str — tên đăng nhập user nhập.
            mat_khau      : str — mật khẩu user nhập.

        Trả về:
            (True,  nguoi_dung) nếu đăng nhập đúng.
            (False, thong_bao)  nếu sai tên/mật khẩu hoặc lỗi.
        """
        try:
            # Gọi hàm kiểm tra từ thư viện (đã bọc try/except ở tầng dưới).
            nguoi_dung = kiem_tra_dang_nhap(ten_dang_nhap, mat_khau)
            # Nếu hàm trả về None → sai tên hoặc mật khẩu.
            if nguoi_dung is None:
                return False, 'Sai tên đăng nhập hoặc mật khẩu.'
            # Lưu người dùng hiện tại vào bộ.
            self.nguoi_dung_hien_tai = nguoi_dung
            return True, nguoi_dung
        except Exception as loi:
            # Bất kỳ lỗi nào khác → trả về tuple (False, thông báo lỗi).
            return False, f'Lỗi: {loi}'

    # ----------------------------------------------------------------
    # HÀM ĐĂNG XUẤT
    # ----------------------------------------------------------------
    def dang_xuat(self):
        """Đăng xuất — reset người dùng hiện tại về None."""
        self.nguoi_dung_hien_tai = None

    # ----------------------------------------------------------------
    # HÀM KIỂM TRA PHÂN QUYỀN
    # ----------------------------------------------------------------
    def la_admin(self):
        """
        Kiểm tra người dùng hiện tại có phải admin không.
        Trả về True nếu là admin, ngược lại False.
        """
        # Phải có user đăng nhập VÀ vai_tro của user đó == 'admin'.
        return (self.nguoi_dung_hien_tai is not None and
                self.nguoi_dung_hien_tai.vai_tro == 'admin')
