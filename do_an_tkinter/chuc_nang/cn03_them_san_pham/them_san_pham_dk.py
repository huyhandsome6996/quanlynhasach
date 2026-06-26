"""
Tệp them_san_pham_dk.py — ĐIỀU KHIỂN cho chức năng Thêm sản phẩm
==================================================================

Cầu nối giữa UI (FormThemSuaUI) và Thuật toán (them_san_pham).
Điều khiển luồng: mở form → đọc dữ liệu → gọi thuật toán → thông báo kết quả.
"""

# Import thuật toán thêm sản phẩm.
from .them_san_pham_tt import them_san_pham
# Import UI form Thêm/Sửa.
from .them_san_pham_ui import FormThemSuaUI


class DieuKhienThemSanPham:
    """Lớp điều khiển chức năng Thêm sản phẩm."""

    def __init__(self, danh_sach, bo_undoredo):
        """
        Khởi tạo điều khiển.

        Tham số:
            danh_sach   : DSLK đôi toàn cục.
            bo_undoredo : dict 2 Stack undo/redo toàn cục.
        """
        self.danh_sach = danh_sach
        self.bo_undoredo = bo_undoredo

    # ----------------------------------------------------------------
    # MỞ FORM THÊM SẢN PHẨM (MODAL)
    # ----------------------------------------------------------------
    def mo_form_them(self, parent):
        """
        Mở form Thêm sản phẩm modal. Chờ user nhập → lưu → đóng form.

        Tham số:
            parent : cửa sổ cha.

        Trả về:
            True nếu đã thêm thành công (để caller nạp lại bảng).
            False nếu user hủy.
        """
        # Tạo form Thêm (du_lieu_cu=None → chế độ Thêm).
        form = FormThemSuaUI(parent, du_lieu_cu=None)
        # Gắn sự kiện nút Lưu → hàm xử lý lưu.
        form.btn_luu.config(command=lambda: self._xu_ly_luu(form))

        # Chờ đến khi form đóng.
        parent.wait_window(form.top)

        # Trả về True nếu có kết quả (đã thêm).
        return form.ket_qua is not None

    # ----------------------------------------------------------------
    # XỬ LÝ LƯU SẢN PHẨM MỚI
    # ----------------------------------------------------------------
    def _xu_ly_luu(self, form):
        """
        Đọc dữ liệu từ form → gọi thuật toán → thông báo kết quả.

        Tham số:
            form : đối tượng FormThemSuaUI.
        """
        # Lấy dữ liệu từ form.
        du_lieu = form.lay_du_lieu()
        # Gọi thuật toán thêm.
        ok, msg = them_san_pham(self.danh_sach, self.bo_undoredo, du_lieu)
        if ok:
            # Lưu kết quả để caller biết là đã thêm.
            form.ket_qua = du_lieu
            form.bao_thanh_cong(msg)
            form.dong()
        else:
            # Lỗi → báo lỗi + giữ form để user sửa.
            form.bao_loi(msg)
