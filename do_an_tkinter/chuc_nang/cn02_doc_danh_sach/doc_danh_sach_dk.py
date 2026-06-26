"""
Tệp doc_danh_sach_dk.py — ĐIỀU KHIỂN cho chức năng Đọc danh sách
=================================================================

Cầu nối giữa UI (BangSanPhamUI) và Thuật toán (lay_danh_sach).
Điều khiển luồng: gọi thuật toán → đổ kết quả vào UI.
"""

# Import thuật toán đọc danh sách (từ cùng folder).
from .doc_danh_sach_tt import lay_danh_sach
# Import lớp DoublyLinkedList (chỉ để type hint, không bắt buộc).
from loi_thuat_toan.danh_sach_lien_ket import DoublyLinkedList


class DieuKhienDocDanhSach:
    """
    Lớp điều khiển — gắn kết UI và thuật toán đọc danh sách.
    """

    def __init__(self, ui_bang, danh_sach: DoublyLinkedList):
        """
        Khởi tạo điều khiển.

        Tham số:
            ui_bang    : đối tượng BangSanPhamUI (đã tạo sẵn Treeview).
            danh_sach  : đối tượng DoublyLinkedList chứa dữ liệu toàn cục.
        """
        self.ui = ui_bang
        self.danh_sach = danh_sach

    # ----------------------------------------------------------------
    # NẠP LẠI TOÀN BỘ DANH SÁCH TỪ DSLK
    # ----------------------------------------------------------------
    def nap_lai(self):
        """Đọc toàn bộ danh sách từ DSLK → vẽ lại bảng."""
        # Gọi thuật toán lấy danh sách.
        ds = lay_danh_sach(self.danh_sach)
        # Xóa dòng cũ trong bảng.
        self.ui.xoa_tat_ca_dong()
        # Thêm từng sản phẩm vào bảng.
        for sp in ds:
            self.ui.them_dong(sp)
        # Trả về số lượng để caller hiển thị thanh trạng thái.
        return len(ds)

    # ----------------------------------------------------------------
    # HIỂN THỊ DANH SÁCH TÙY CHỈNH (Dùng cho tìm kiếm / sắp xếp)
    # ----------------------------------------------------------------
    def hien_thi_danh_sach(self, ds_dict):
        """
        Hiển thị 1 list dict bất kỳ lên bảng (không tải lại từ DSLK).

        Dùng khi tìm kiếm hoặc sắp xếp — kết quả trả về list dict và ta đổ vào bảng.

        Tham số:
            ds_dict : List[dict] — danh sách dict sản phẩm.
        """
        # Xóa dòng cũ.
        self.ui.xoa_tat_ca_dong()
        # Thêm từng dòng.
        for sp in ds_dict:
            self.ui.them_dong(sp)
        return len(ds_dict)

    # ----------------------------------------------------------------
    # LẤY MÃ SẢN PHẨM ĐANG CHỌN
    # ----------------------------------------------------------------
    def lay_ma_dang_chon(self):
        """Trả về mã số dòng đang chọn — dùng cho Sửa/Xóa/Thêm vào giỏ."""
        return self.ui.lay_ma_dang_chon()
