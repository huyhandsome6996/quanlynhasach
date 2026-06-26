"""
Tệp xoa_san_pham_dk.py — ĐIỀU KHIỂN cho chức năng Xóa sản phẩm
==============================================================

Cầu nối giữa UI (xoa_san_pham_ui) và Thuật toán (xoa_san_pham).
Luồng:
    1. Lấy mã sản phẩm đang chọn trong bảng (do caller truyền vào).
    2. Hiện hộp thoại xác nhận YES/NO.
    3. Nếu Yes → gọi thuật toán xoa_san_pham.
    4. Xử lý kết quả → hiện thông báo tương ứng.
"""

# Import thuật toán xóa.
from .xoa_san_pham_tt import xoa_san_pham
# Import UI (các hàm tiện ích show dialog).
from .xoa_san_pham_ui import hoi_xac_nhan_xoa, bao_loi, bao_thanh_cong


class DieuKhienXoaSanPham:
    """Lớp điều khiển chức năng Xóa sản phẩm."""

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
    # XỬ LÝ XÓA SẢN PHẨM
    # ----------------------------------------------------------------
    def xu_ly_xoa(self, parent, ma_so, la_admin):
        """
        Xóa 1 sản phẩm theo mã số.

        Tham số:
            parent   : cửa sổ cha (để show messagebox).
            ma_so    : mã sản phẩm cần xóa.
            la_admin : True nếu user hiện tại là admin.

        Trả về:
            True nếu đã xóa thành công (để caller nạp lại bảng).
            False nếu user hủy hoặc xóa thất bại.
        """
        # Trường hợp không có mã (caller báo lỗi rồi thì không cần làm gì).
        if not ma_so:
            bao_loi(parent, 'Vui lòng chọn 1 dòng trong bảng để xóa.')
            return False

        # Hiện hộp thoại xác nhận YES/NO.
        if not hoi_xac_nhan_xoa(parent, ma_so):
            # User nhấn No → không làm gì.
            return False

        # Gọi thuật toán xóa.
        ok, msg = xoa_san_pham(self.danh_sach, self.bo_undoredo, ma_so, la_admin)
        if ok:
            # Thành công → hiện thông báo + trả về True để caller nạp lại bảng.
            bao_thanh_cong(parent, msg)
            return True
        else:
            # Thất bại (không phải admin / không tìm thấy / lỗi) → báo lỗi.
            bao_loi(parent, msg)
            return False
