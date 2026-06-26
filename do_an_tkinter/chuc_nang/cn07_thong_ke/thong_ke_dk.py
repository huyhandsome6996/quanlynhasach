"""
Tệp thong_ke_dk.py — ĐIỀU KHIỂN cho chức năng Thống kê
========================================================

Cầu nối giữa UI (KhungThongKeUI) và Thuật toán (lay_thong_ke).
Điều khiển: gọi thuật toán → cập nhật các label trong UI.
"""

# Import thuật toán thống kê.
from .thong_ke_tt import lay_thong_ke


class DieuKhienThongKe:
    """Lớp điều khiển Thống kê."""

    def __init__(self, ui_thong_ke, danh_sach):
        """
        Khởi tạo điều khiển.

        Tham số:
            ui_thong_ke : đối tượng KhungThongKeUI.
            danh_sach   : DSLK đôi toàn cục.
        """
        self.ui = ui_thong_ke
        self.danh_sach = danh_sach

    # ----------------------------------------------------------------
    # CẬP NHẬT THỐNG KÊ LÊN UI
    # ----------------------------------------------------------------
    def cap_nhat(self):
        """Gọi thuật toán + cập nhật 5 label trên UI."""
        # Lấy dict thống kê từ thuật toán.
        tk = lay_thong_ke(self.danh_sach)
        if not tk:
            # Nếu rỗng → reset UI về mặc định.
            self.ui.dat_mac_dinh()
            return

        # Cập nhật từng label.
        self.ui.cap_nhat_tong_so(tk.get('tong_so', 0))

        # Mặt hàng đắt nhất.
        dat = tk.get('dat_nhat')
        if dat:
            self.ui.cap_nhat_dat_nhat(dat.get('ten_san_pham', '-'),
                                       dat.get('gia_ban', 0))
        else:
            self.ui.lbl_dat.config(text='Đắt nhất: -')

        # Mặt hàng rẻ nhất.
        re = tk.get('re_nhat')
        if re:
            self.ui.cap_nhat_re_nhat(re.get('ten_san_pham', '-'),
                                      re.get('gia_ban', 0))
        else:
            self.ui.lbl_re.config(text='Rẻ nhất: -')

        # Tổng giá trị kho.
        self.ui.cap_nhat_tri_kho(tk.get('tong_gia_tri_kho', 0))

        # Số mặt hàng sắp hết.
        self.ui.cap_nhat_sap_het(len(tk.get('sap_het_hang', [])))
