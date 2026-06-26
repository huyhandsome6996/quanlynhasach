"""
Tệp gio_hang_ui.py — GIAO DIỆN cho Giỏ hàng (Queue FIFO) + Thanh toán
======================================================================

Tạo 1 LabelFrame "🛒 Giỏ hàng (Queue FIFO)" chứa:
    - Treeview danh sách món trong giỏ (Mã, Tên, Giá bán, Loại).
    - Nút "+ Thêm vào giỏ"  — lấy dòng đang chọn trong bảng chính → enqueue.
    - Nút "- Bỏ khỏi giỏ"   — xóa 1 món đang chọn trong giỏ.
    - Nút "💰 Thanh toán"   — dequeue toàn bộ → hiện hóa đơn.
    - Label tổng tiền.
"""

from tkinter import ttk


class KhungGioHangUI:
    """Khung giỏ hàng + nút thanh toán."""

    def __init__(self, parent):
        """
        Tạo khung giỏ trong parent.

        Tham số:
            parent : widget cha (thường là Frame bên phải cửa sổ chính).
        """
        # LabelFrame có tiêu đề + icon giỏ hàng.
        frame = ttk.LabelFrame(parent, text='🛒 Giỏ hàng (Queue FIFO)', padding=10)
        frame.pack(fill='both', expand=True)
        # Lưu reference để caller truy cập.
        self.frame = frame

        # === BẢNG TREEVIEW CHỨA MÓN TRONG GIỎ ===
        # 4 cột: Mã, Tên, Giá bán, Loại.
        columns_gio = ('ma', 'ten', 'gia', 'loai')
        self.tree_gio = ttk.Treeview(frame, columns=columns_gio, show='headings', height=8)
        self.tree_gio.heading('ma', text='Mã')
        self.tree_gio.heading('ten', text='Tên')
        self.tree_gio.heading('gia', text='Giá bán')
        self.tree_gio.heading('loai', text='Loại')
        self.tree_gio.column('ma', width=60, anchor='center')
        self.tree_gio.column('ten', width=150)
        self.tree_gio.column('gia', width=90, anchor='e')
        self.tree_gio.column('loai', width=70, anchor='center')
        self.tree_gio.pack(fill='both', expand=True)

        # === KHUNG CHỨA 3 NÚT BẤM ===
        frame_nut = ttk.Frame(frame)
        frame_nut.pack(fill='x', pady=5)

        # Nút Thêm vào giỏ — command gắn bởi Điều khiển.
        self.btn_them = ttk.Button(frame_nut, text='+ Thêm vào giỏ')
        self.btn_them.pack(side='left', padx=2)

        # Nút Bỏ khỏi giỏ.
        self.btn_xoa = ttk.Button(frame_nut, text='- Bỏ khỏi giỏ')
        self.btn_xoa.pack(side='left', padx=2)

        # Nút Thanh toán.
        self.btn_thanh_toan = ttk.Button(frame_nut, text='💰 Thanh toán')
        self.btn_thanh_toan.pack(side='right', padx=2)

        # Label tổng tiền — màu xanh, font bold.
        self.lbl_tong_gio = ttk.Label(frame, text='Tổng: 0đ (0 món)',
                                       font=('Arial', 11, 'bold'), foreground='green')
        self.lbl_tong_gio.pack(side='right', pady=5, padx=10)

    # ----------------------------------------------------------------
    # CÁC HÀM TIỆN ÍCH CHO ĐIỀU KHIỂN GỌI
    # ----------------------------------------------------------------
    def xoa_tat_ca_dong(self):
        """Xóa toàn bộ dòng trong bảng giỏ — dùng trước khi vẽ lại."""
        for item in self.tree_gio.get_children():
            self.tree_gio.delete(item)

    def them_dong(self, mon_dict):
        """Thêm 1 dòng vào bảng giỏ từ dict món."""
        self.tree_gio.insert('', 'end', values=(
            mon_dict.get('ma_so', ''),
            mon_dict.get('ten_san_pham', ''),
            f"{mon_dict.get('gia_ban', 0):,.0f}",
            mon_dict.get('loai_hang', '')
        ))

    def lay_ma_dang_chon(self):
        """Trả về mã số món đang chọn trong giỏ, None nếu chưa chọn."""
        selected = self.tree_gio.selection()
        if not selected:
            return None
        values = self.tree_gio.item(selected[0], 'values')
        return values[0]   # Cột 0 = Mã.

    def cap_nhat_tong(self, tong_tien, so_luong):
        """Cập nhật label tổng tiền."""
        self.lbl_tong_gio.config(text=f'Tổng: {tong_tien:,.0f}đ ({so_luong} món)')
