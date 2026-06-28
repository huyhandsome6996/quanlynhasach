"""
Tệp tim_kiem_sap_xep_ui.py — GIAO DIỆN cho Tìm kiếm + Sắp xếp
==============================================================

Tạo 1 thanh công cụ ngang chứa:
    - Ô nhập từ khóa.
    - Combobox chọn tiêu chí tìm (ten / ma / loai).
    - Nút "Tìm" + Nút "Làm mới".
    - Separator.
    - Combobox chọn tiêu chí sắp xếp (gia_ban / ten_san_pham / ton_kho).
    - Nút "Sắp xếp".

UI chỉ vẽ widget + lưu reference để Điều khiển gắn sự kiện.
"""

import tkinter as tk
from tkinter import ttk


class ThanhTimKiemSapXepUI:
    """
    Thanh công cụ Tìm kiếm + Sắp xếp.
    """

    def __init__(self, parent):
        """
        Tạo thanh công cụ trong parent.

        Tham số:
            parent : widget cha (thường là Frame thanh công cụ của cửa sổ chính).
        """
        # === NHÓM TÌM KIẾM ===
        ttk.Label(parent, text='Tìm:').pack(side='left', padx=2)
        # Ô nhập từ khóa.
        self.entry_tu_khoa = ttk.Entry(parent, width=15)
        self.entry_tu_khoa.pack(side='left', padx=2)
        # Combobox tiêu chí tìm.
        self.var_tk_tieu_chi = tk.StringVar(value='ten')
        ttk.Combobox(parent, textvariable=self.var_tk_tieu_chi,
                     values=['ten', 'ma', 'loai'], state='readonly', width=6).pack(side='left', padx=2)
        # Nút "Tìm" — command sẽ gắn bởi Điều khiển.
        self.btn_tim = ttk.Button(parent, text='Tìm', width=6)
        self.btn_tim.pack(side='left', padx=2)
        # Nút "Làm mới" — tải lại toàn bộ danh sách.
        self.btn_lam_moi = ttk.Button(parent, text='↻ Làm mới', width=9)
        self.btn_lam_moi.pack(side='left', padx=2)

        # Separator ngăn cách 2 nhóm.
        ttk.Separator(parent, orient='vertical').pack(side='left', fill='y', padx=8)






        # === NHÓM SẮP XẾP =========================================
        ttk.Label(parent, text='Sắp xếp:').pack(side='left', padx=2)
        # Combobox tiêu chí sắp xếp.
        self.var_sx_tieu_chi = tk.StringVar(value='gia_ban')
        ttk.Combobox(parent, textvariable=self.var_sx_tieu_chi,
                     values=['gia_ban', 'ten_san_pham', 'ton_kho'],
                     state='readonly', width=12).pack(side='left', padx=2)
        # Nút "Sắp xếp".
        self.btn_sap_xep = ttk.Button(parent, text='Sắp xếp', width=9)
        self.btn_sap_xep.pack(side='left', padx=2)

    # ----------------------------------------------------------------
    # CÁC HÀM TIỆN ÍCH CHO ĐIỀU KHIỂN GỌI
    # ----------------------------------------------------------------
    def lay_tu_khoa(self):
        """Trả về từ khóa user nhập (đã strip)."""
        return self.entry_tu_khoa.get().strip()

    def lay_tieu_chi_tim(self):
        """Trả về tiêu chí tìm ('ten' | 'ma' | 'loai')."""
        return self.var_tk_tieu_chi.get()

    def lay_tieu_chi_sap_xep(self):
        """Trả về tiêu chí sắp xếp ('gia_ban' | 'ten_san_pham' | 'ton_kho')."""
        return self.var_sx_tieu_chi.get()

    def bind_enter_tim(self, ham_xu_ly):
        """Gắn phím Enter trong ô từ khóa → hàm xử lý tìm."""
        self.entry_tu_khoa.bind('<Return>', lambda e: ham_xu_ly())
