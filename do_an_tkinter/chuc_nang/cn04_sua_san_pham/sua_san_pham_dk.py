"""
Tệp sua_san_pham_dk.py — ĐIỀU KHIỂN cho chức năng Sửa sản phẩm
==============================================================

Cầu nối giữa UI (FormThemSuaUI) và Thuật toán (sua_san_pham).
Luồng:
    1. Lấy mã sản phẩm đang chọn trong bảng (do caller truyền vào).
    2. Tìm dict đầy đủ từ DSLK để đổ vào form Sửa.
    3. Mở form Sửa modal → chờ user chỉnh.
    4. Khi user nhấn Lưu → gọi thuật toán sua_san_pham → báo kết quả.
"""

# Import thuật toán sửa sản phẩm (cùng folder).
from .sua_san_pham_tt import sua_san_pham
# Import UI form sửa (cùng folder — re-export từ _shared).
from .sua_san_pham_ui import FormThemSuaUI


class DieuKhienSuaSanPham:
    """Lớp điều khiển chức năng Sửa sản phẩm."""

    def __init__(self, danh_sach, bo_undoredo):
        """
        Khởi tạo điều khiển.

        Tham số:
            danh_sach   : DSLK đôi toàn cục (để lấy dict sản phẩm cần sửa).
            bo_undoredo : dict 2 Stack undo/redo toàn cục.
        """
        self.danh_sach = danh_sach
        self.bo_undoredo = bo_undoredo

    # ----------------------------------------------------------------
    # MỞ FORM SỬA SẢN PHẨM (MODAL)
    # ----------------------------------------------------------------
    def mo_form_sua(self, parent, ma_so):
        """
        Mở form Sửa sản phẩm modal. Chờ user chỉnh → lưu → đóng form.

        Tham số:
            parent : cửa sổ cha.
            ma_so  : mã sản phẩm cần sửa.

        Trả về:
            True nếu đã sửa thành công (để caller nạp lại bảng).
            False nếu user hủy hoặc không tìm thấy sản phẩm.
        """
        # Tìm sản phẩm cần sửa trong DSLK.
        sp_cu = self.danh_sach.tim_theo_ma_so(ma_so)
        if sp_cu is None:
            # Không tìm thấy → trả về False để caller báo lỗi.
            return False

        # Lấy dict dữ liệu cũ để đổ vào form.
        du_lieu_cu = sp_cu.chuyen_thanh_dict()

        # Tạo form Sửa (du_lieu_cu != None → chế độ Sửa).
        form = FormThemSuaUI(parent, du_lieu_cu=du_lieu_cu)
        # Gắn sự kiện nút Lưu → hàm xử lý lưu.
        form.btn_luu.config(command=lambda: self._xu_ly_luu(form))

        # Chờ đến khi form đóng.
        parent.wait_window(form.top)

        # Trả về True nếu có kết quả (đã lưu thành công).
        return form.ket_qua is not None

    # ----------------------------------------------------------------
    # XỬ LÝ LƯU SẢN PHẨM ĐÃ SỬA
    # ----------------------------------------------------------------
    def _xu_ly_luu(self, form):
        """
        Đọc dữ liệu từ form → gọi thuật toán → thông báo kết quả.

        Tham số:
            form : đối tượng FormThemSuaUI.
        """
        # Lấy dữ liệu từ form (bao gồm cả mã số đang sửa).
        du_lieu = form.lay_du_lieu()
        # Đảm bảo mã số không bị đổi (form khóa ô mã nhưng phòng hờ).
        du_lieu['ma_so'] = form.du_lieu_cu['ma_so']

        # Gọi thuật toán sửa.
        ok, msg = sua_san_pham(self.danh_sach, self.bo_undoredo, du_lieu)
        if ok:
            # Lưu kết quả để caller biết là đã sửa.
            form.ket_qua = du_lieu
            form.bao_thanh_cong(msg)
            form.dong()
        else:
            # Lỗi → báo lỗi + giữ form để user sửa lại.
            form.bao_loi(msg)
