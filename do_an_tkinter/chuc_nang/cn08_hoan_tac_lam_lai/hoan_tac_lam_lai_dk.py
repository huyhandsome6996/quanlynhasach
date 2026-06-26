"""
Tệp hoan_tac_lam_lai_dk.py — ĐIỀU KHIỂN cho Undo/Redo
=======================================================

Cầu nối giữa UI (ThanhUndoRedoUI) và Thuật toán (hoan_tac, lam_lai, trang_thai).
Điều khiển luồng:
    - Nút Undo → gọi hoan_tac → cập nhật UI.
    - Nút Redo → gọi lam_lai  → cập nhật UI.
    - Hàm cap_nhat_trang_thai → bật/tắt nút theo Stack.
"""

# Import thuật toán Undo/Redo.
from .hoan_tac_lam_lai_tt import hoan_tac, lam_lai, trang_thai


class DieuKhienHoanTacLamLai:
    """Lớp điều khiển Undo/Redo."""

    def __init__(self, ui_undoredo, danh_sach, bo_undoredo):
        """
        Khởi tạo điều khiển.

        Tham số:
            ui_undoredo : đối tượng ThanhUndoRedoUI.
            danh_sach   : DSLK đôi toàn cục.
            bo_undoredo : dict 2 Stack undo/redo toàn cục.
        """
        self.ui = ui_undoredo
        self.danh_sach = danh_sach
        self.bo_undoredo = bo_undoredo

    # ----------------------------------------------------------------
    # GẮN SỰ KIỆN CHO CÁC NÚT
    # ----------------------------------------------------------------
    def gan_su_kien(self, cap_nhat_bang, cap_nhat_thong_ke):
        """
        Gắn command cho 2 nút + lưu 2 callback để gọi sau undo/redo.

        Tham số:
            cap_nhat_bang       : hàm callback để nạp lại bảng sau undo/redo.
            cap_nhat_thong_ke   : hàm callback để cập nhật thống kê.
        """
        # Lưu 2 callback.
        self._cap_nhat_bang = cap_nhat_bang
        self._cap_nhat_thong_ke = cap_nhat_thong_ke

        # Gắn command.
        self.ui.btn_hoan_tac.config(command=self.xu_ly_hoan_tac)
        self.ui.btn_lam_lai.config(command=self.xu_ly_lam_lai)

    # ----------------------------------------------------------------
    # XỬ LÝ UNDO
    # ----------------------------------------------------------------
    def xu_ly_hoan_tac(self):
        """Gọi thuật toán Undo → cập nhật UI."""
        # Gọi thuật toán.
        ok, msg = hoan_tac(self.danh_sach, self.bo_undoredo)
        # Cập nhật trạng thái nút.
        self.cap_nhat_trang_thai()
        if ok:
            # Sau undo → nạp lại bảng + thống kê.
            self._cap_nhat_bang()
            self._cap_nhat_thong_ke()
        return ok, msg

    # ----------------------------------------------------------------
    # XỬ LÝ REDO
    # ----------------------------------------------------------------
    def xu_ly_lam_lai(self):
        """Gọi thuật toán Redo → cập nhật UI."""
        ok, msg = lam_lai(self.danh_sach, self.bo_undoredo)
        self.cap_nhat_trang_thai()
        if ok:
            self._cap_nhat_bang()
            self._cap_nhat_thong_ke()
        return ok, msg

    # ----------------------------------------------------------------
    # CẬP NHẬT TRẠNG THÁI NÚT (BẬT/TẮT)
    # ----------------------------------------------------------------
    def cap_nhat_trang_thai(self):
        """Lấy trạng thái Stack → bật/tắt 2 nút."""
        tt = trang_thai(self.bo_undoredo)
        self.ui.bat_hoan_tac(tt['co_the_undo'])
        self.ui.bat_lam_lai(tt['co_the_redo'])
