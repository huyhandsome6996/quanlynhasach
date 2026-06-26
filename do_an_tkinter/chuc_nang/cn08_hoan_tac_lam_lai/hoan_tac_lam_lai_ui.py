"""
Tệp hoan_tac_lam_lai_ui.py — GIAO DIỆN cho Undo/Redo
=====================================================

Tạo 2 nút bấm:
    - btn_hoan_tac: "↶ Hoàn tác" (Undo).
    - btn_lam_lai:  "↷ Làm lại"  (Redo).

UI chỉ vẽ widget + lưu reference để Điều khiển gắn command + bật/tắt.
"""

from tkinter import ttk


class ThanhUndoRedoUI:
    """Thanh chứa 2 nút Undo + Redo."""

    def __init__(self, parent):
        """
        Tạo 2 nút trong parent.

        Tham số:
            parent : widget cha.
        """
        # Nút Undo — command sẽ gắn bởi Điều khiển.
        self.btn_hoan_tac = ttk.Button(parent, text='↶ Hoàn tác', width=12)
        self.btn_hoan_tac.pack(side='left', padx=2)

        # Nút Redo.
        self.btn_lam_lai = ttk.Button(parent, text='↷ Làm lại', width=12)
        self.btn_lam_lai.pack(side='left', padx=2)

    # ----------------------------------------------------------------
    # CÁC HÀM TIỆN ÍCH CHO ĐIỀU KHIỂN GỌI
    # ----------------------------------------------------------------
    def bat_hoan_tac(self, bat=True):
        """Bật/tắt nút Undo."""
        self.btn_hoan_tac.config(state='normal' if bat else 'disabled')

    def bat_lam_lai(self, bat=True):
        """Bật/tắt nút Redo."""
        self.btn_lam_lai.config(state='normal' if bat else 'disabled')

    def vo_hieu_hoa_tat_ca(self):
        """Vô hiệu hóa cả 2 nút (dùng khi chưa có thao tác nào)."""
        self.bat_hoan_tac(False)
        self.bat_lam_lai(False)
