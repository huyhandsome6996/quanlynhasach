"""
Tệp thong_ke_ui.py — GIAO DIỆN cho chức năng Thống kê
======================================================

Tạo 1 LabelFrame "Thống kê" chứa 5 Label:
    - Tổng số mặt hàng.
    - Mặt hàng đắt nhất.
    - Mặt hàng rẻ nhất.
    - Tổng giá trị kho.
    - Số mặt hàng sắp hết (tồn ≤ 5).

UI chỉ vẽ widget + lưu reference các label để Điều khiển cập nhật nội dung.
"""

from tkinter import ttk


class KhungThongKeUI:
    """Khung hiển thị các chỉ số thống kê."""

    def __init__(self, parent):
        """
        Tạo khung thống kê trong parent.

        Tham số:
            parent : widget cha (thường là Frame bên phải cửa sổ chính).
        """
        # LabelFrame có tiêu đề "Thống kê", padding 10px.
        frame = ttk.LabelFrame(parent, text='Thống kê', padding=10)
        frame.pack(fill='x', pady=(0, 5))
        # Lưu reference để caller có thể truy cập frame nếu cần.
        self.frame = frame

        # 5 label hiển thị 5 chỉ số.
        self.lbl_tong_so = ttk.Label(frame, text='Tổng số: 0')
        self.lbl_tong_so.pack(anchor='w')

        self.lbl_dat = ttk.Label(frame, text='Đắt nhất: -')
        self.lbl_dat.pack(anchor='w')

        self.lbl_re = ttk.Label(frame, text='Rẻ nhất: -')
        self.lbl_re.pack(anchor='w')

        self.lbl_tri_kho = ttk.Label(frame, text='Tổng giá trị kho: 0đ')
        self.lbl_tri_kho.pack(anchor='w')

        # Foreground='red' để cảnh báo nổi bật.
        self.lbl_sap_het = ttk.Label(frame, text='Sắp hết (<5): 0', foreground='red')
        self.lbl_sap_het.pack(anchor='w')

    # ----------------------------------------------------------------
    # CÁC HÀM TIỆN ÍCH CHO ĐIỀU KHIỂN GỌI
    # ----------------------------------------------------------------
    def cap_nhat_tong_so(self, so):
        """Cập nhật label tổng số mặt hàng."""
        self.lbl_tong_so.config(text=f'Tổng số: {so} mặt hàng')

    def cap_nhat_dat_nhat(self, ten, gia):
        """Cập nhật label mặt hàng đắt nhất."""
        self.lbl_dat.config(text=f'Đắt nhất: {ten} ({gia:,.0f}đ)')

    def cap_nhat_re_nhat(self, ten, gia):
        """Cập nhật label mặt hàng rẻ nhất."""
        self.lbl_re.config(text=f'Rẻ nhất: {ten} ({gia:,.0f}đ)')

    def cap_nhat_tri_kho(self, tong):
        """Cập nhật label tổng giá trị kho."""
        self.lbl_tri_kho.config(text=f'Tổng giá trị kho: {tong:,.0f}đ')

    def cap_nhat_sap_het(self, so):
        """Cập nhật label số mặt hàng sắp hết."""
        self.lbl_sap_het.config(text=f'Sắp hết (<5): {so}')

    def dat_mac_dinh(self):
        """Reset tất cả label về giá trị mặc định."""
        self.lbl_tong_so.config(text='Tổng số: 0')
        self.lbl_dat.config(text='Đắt nhất: -')
        self.lbl_re.config(text='Rẻ nhất: -')
        self.lbl_tri_kho.config(text='Tổng giá trị kho: 0đ')
        self.lbl_sap_het.config(text='Sắp hết (<5): 0')
