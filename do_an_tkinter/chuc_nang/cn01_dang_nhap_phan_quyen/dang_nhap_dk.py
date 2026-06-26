"""
Tệp dang_nhap_dk.py — ĐIỀU KHIỂN TRUNG TÂM cho chức năng Đăng nhập
====================================================================

Đóng vai trò "cầu nối" giữa UI (dang_nhap_ui.py) và Thuật toán (dang_nhap_tt.py):
    - UI chỉ quan tâm tới giao diện (vẽ form, bắt sự kiện).
    - Thuật toán chỉ quan tâm tới logic (kiểm tra tên/mật khẩu).
    - Điều khiển: gắn sự kiện UI → gọi thuật toán → xử lý kết quả → cập nhật UI.

Tất cả luồng đăng nhập/đăng xuất đều đi qua lớp Điều khiển này.
"""

# Import giao diện (UI) của chức năng đăng nhập.
from .dang_nhap_ui import CuaSoDangNhapUI
# Import thuật toán (logic) của chức năng đăng nhập.
from .dang_nhap_tt import BoDangNhap


class DieuKhienDangNhap:
    """
    Lớp điều khiển — quản lý luồng đăng nhập / đăng xuất của ứng dụng.
    """

    def __init__(self):
        """Khởi tạo bộ điều khiển + bộ thuật toán đăng nhập."""
        # Tạo 1 đối tượng BoDangNhap (logic) — dùng chung cho toàn app.
        self.bo = BoDangNhap()

    # ----------------------------------------------------------------
    # HIỆN FORM ĐĂNG NHẬP (MODAL)
    # ----------------------------------------------------------------
    def hien_form_dang_nhap(self, parent):
        """
        Hiện form đăng nhập modal. Chờ user nhập → kiểm tra → đóng form.

        Tham số:
            parent : cửa sổ cha (Tk root).

        Trả về:
            NguoiDung nếu đăng nhập thành công, None nếu user đóng form.
        """
        # Tạo đối tượng UI (form đăng nhập).
        form = CuaSoDangNhapUI(parent)

        # Gắn sự kiện: phím Enter ở ô mật khẩu + nút "Đăng nhập" → xử lý đăng nhập.
        form.entry_mk.bind('<Return>', lambda e: self._xu_ly_dang_nhap(form))
        form.btn_dn.config(command=lambda: self._xu_ly_dang_nhap(form))

        # Chờ đến khi form bị đóng (bởi nút đăng nhập thành công hoặc user tắt).
        parent.wait_window(form.top)

        # Trả về người dùng (None nếu user tắt form mà không đăng nhập).
        return form.nguoi_dung

    # ----------------------------------------------------------------
    # XỬ LÝ SỰ KIỆN ĐĂNG NHẬP
    # ----------------------------------------------------------------
    def _xu_ly_dang_nhap(self, form):
        """
        Lấy dữ liệu từ form → gọi thuật toán → xử lý kết quả.

        Tham số:
            form : đối tượng CuaSoDangNhapUI.
        """
        # Lấy tên đăng nhập + mật khẩu từ form.
        ten = form.lay_ten_dang_nhap()
        mk = form.lay_mat_khau()

        # Validate cơ bản: không được để trống.
        if not ten or not mk:
            form.bao_loi('Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.')
            return

        # Gọi hàm thuật toán đăng nhập.
        ok, ket_qua = self.bo.dang_nhap(ten, mk)
        if ok:
            # Nếu OK → lưu người dùng vào form (để parent đọc) → đóng form.
            form.nguoi_dung = ket_qua
            form.dong()
        else:
            # Nếu sai → báo lỗi + xóa ô mật khẩu để user nhập lại.
            form.bao_loi(ket_qua)
            form.xoa_mat_khau()

    # ----------------------------------------------------------------
    # ĐĂNG XUẤT
    # ----------------------------------------------------------------
    def dang_xuat(self):
        """Đăng xuất — gọi hàm đăng xuất của bộ thuật toán."""
        self.bo.dang_xuat()

    # ----------------------------------------------------------------
    # KIỂM TRA PHÂN QUYỀN
    # ----------------------------------------------------------------
    def la_admin(self):
        """Trả về True nếu người dùng hiện tại là admin."""
        return self.bo.la_admin()

    @property
    def nguoi_dung_hien_tai(self):
        """Trả về người dùng đang đăng nhập hiện tại (None nếu chưa login)."""
        return self.bo.nguoi_dung_hien_tai
