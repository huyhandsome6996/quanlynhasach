"""
Tệp them_san_pham_ui.py — GIAO DIỆN cho form Thêm sản phẩm
============================================================

Hiển thị form modal cho user nhập các trường:
    - Trường chung: Loại, Mã, Tên, Giá, Tồn.
    - Trường riêng: thay đổi theo loại hàng (vd: Sách có Tác giả + NXB).

Lớp này dùng CHUNG cho cả Thêm và Sửa (khi sửa thì truyền du_lieu_cu).
"""

import tkinter as tk
from tkinter import ttk, messagebox

# Danh sách 5 loại hàng hợp lệ — để hiển thị trong Combobox.
CAC_LOAI_HANG = ['Sách', 'Tạp chí', 'Báo giấy', 'Luận văn', 'Bản thảo']


class FormThemSuaUI:
    """
    Hộp thoại modal Thêm/Sửa sản phẩm.
    - Khi du_lieu_cu=None: chế độ Thêm mới.
    - Khi du_lieu_cu=dict: chế độ Sửa (đổ dữ liệu cũ vào form, khóa mã + loại).
    """

    def __init__(self, parent, du_lieu_cu=None):
        """
        Khởi tạo form.

        Tham số:
            parent     : cửa sổ cha.
            du_lieu_cu : None = thêm mới; dict = sửa.
        """
        self.du_lieu_cu = du_lieu_cu
        # ket_qua sẽ chứa dict dữ liệu user nhập khi nhấn Lưu.
        self.ket_qua = None

        # Tạo cửa sổ Toplevel modal.
        self.top = tk.Toplevel(parent)
        self.top.title('Sửa sản phẩm' if du_lieu_cu else 'Thêm sản phẩm')
        self.top.geometry('450x520+450+150')
        self.top.transient(parent)
        self.top.grab_set()

        # Gọi hàm tạo giao diện.
        self._tao_giao_dien()

    def _tao_giao_dien(self):
        """Tạo form với các trường động theo loại hàng."""
        # Frame chính, padding 20px.
        frame = ttk.Frame(self.top, padding=20)
        frame.pack(fill='both', expand=True)

        # === CÁC TRƯỜNG CHUNG ===
        ttk.Label(frame, text='Loại hàng:').grid(row=0, column=0, sticky='e', padx=5, pady=5)
        # Combobox chọn loại (chế độ Sửa thì khóa không cho đổi).
        self.var_loai = tk.StringVar()
        self.combo_loai = ttk.Combobox(frame, textvariable=self.var_loai,
                                        values=CAC_LOAI_HANG, state='readonly', width=22)
        self.combo_loai.grid(row=0, column=1, padx=5, pady=5)
        # Khi user đổi loại → cập nhật lại các trường riêng.
        self.combo_loai.bind('<<ComboboxSelected>>', lambda e: self._cap_nhat_truong_rieng())

        ttk.Label(frame, text='Mã số:').grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.entry_ma = ttk.Entry(frame, width=25)
        self.entry_ma.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text='Tên sản phẩm:').grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.entry_ten = ttk.Entry(frame, width=25)
        self.entry_ten.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame, text='Giá cơ bản (đ):').grid(row=3, column=0, sticky='e', padx=5, pady=5)
        self.entry_gia = ttk.Entry(frame, width=25)
        self.entry_gia.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(frame, text='Tồn kho:').grid(row=4, column=0, sticky='e', padx=5, pady=5)
        self.entry_ton = ttk.Entry(frame, width=25)
        self.entry_ton.grid(row=4, column=1, padx=5, pady=5)

        # === KHUNG TRƯỜNG RIÊNG (động theo loại) ===
        ttk.Separator(frame, orient='horizontal').grid(row=5, column=0, columnspan=2,
                                                        sticky='ew', pady=10)
        ttk.Label(frame, text='Thông tin riêng theo loại:',
                  font=('Arial', 10, 'italic')).grid(row=6, column=0, columnspan=2, sticky='w')

        # Frame chứa các entry động.
        self.frame_rieng = ttk.Frame(frame)
        self.frame_rieng.grid(row=7, column=0, columnspan=2, sticky='ew', pady=5)
        # Dict lưu các entry trường riêng (key=tên trường).
        self.entries_rieng = {}

        # === NÚT BẤM ===
        frame_nut = ttk.Frame(frame)
        frame_nut.grid(row=8, column=0, columnspan=2, pady=15)
        # Nút Lưu — gắn command sau bởi Điều khiển.
        self.btn_luu = ttk.Button(frame_nut, text='Lưu')
        self.btn_luu.pack(side='left', padx=10)
        ttk.Button(frame_nut, text='Hủy', command=self.top.destroy).pack(side='left', padx=10)

        # === NẾU LÀ SỬA → ĐỔ DỮ LIỆU CŨ VÀO FORM ===
        if self.du_lieu_cu:
            # Chế độ Sửa: đổ dữ liệu cũ.
            self.var_loai.set(self.du_lieu_cu.get('loai_hang', ''))
            # Khóa combobox loại (không cho đổi loại khi sửa).
            self.combo_loai.config(state='disabled')
            self.entry_ma.insert(0, self.du_lieu_cu.get('ma_so', ''))
            # Khóa mã số (không cho đổi mã khi sửa).
            self.entry_ma.config(state='disabled')
            self.entry_ten.insert(0, self.du_lieu_cu.get('ten_san_pham', ''))
            self.entry_gia.insert(0, str(self.du_lieu_cu.get('gia_co_ban', '')))
            self.entry_ton.insert(0, str(self.du_lieu_cu.get('ton_kho', '')))
            # Tạo các trường riêng + đổ giá trị cũ.
            self._cap_nhat_truong_rieng()
        else:
            # Chế độ Thêm: mặc định chọn loại đầu tiên.
            self.var_loai.set(CAC_LOAI_HANG[0])
            self._cap_nhat_truong_rieng()

    def _cap_nhat_truong_rieng(self):
        """Xóa các entry cũ + tạo entry mới theo loại đang chọn."""
        # Xóa widget cũ trong frame_rieng.
        for w in self.frame_rieng.winfo_children():
            w.destroy()
        self.entries_rieng.clear()

        loai = self.var_loai.get()
        # Định nghĩa trường riêng cho từng loại — key=tên trường, label=nhãn hiển thị.
        truong_rieng = {
            'Sách':      [('tac_gia', 'Tác giả:'), ('nha_xuat_ban', 'Nhà xuất bản:')],
            'Tạp chí':   [('so_phat_hanh', 'Số phát hành:')],
            'Báo giấy':  [('ngay_xuat_ban', 'Ngày xuất bản:')],
            'Luận văn':  [('tac_gia', 'Tác giả:'), ('truong_dai_hoc', 'Trường ĐH:')],
            'Bản thảo':  [('tac_gia', 'Tác giả:'), ('trang_thai', 'Tình trạng:')],
        }
        ds_truong = truong_rieng.get(loai, [])

        # Tạo từng cặp label + entry.
        for i, (key, label) in enumerate(ds_truong):
            ttk.Label(self.frame_rieng, text=label).grid(row=i, column=0, sticky='e', padx=5, pady=3)
            e = ttk.Entry(self.frame_rieng, width=25)
            e.grid(row=i, column=1, padx=5, pady=3)
            # Lưu entry vào dict để sau đọc giá trị.
            self.entries_rieng[key] = e
            # Nếu là sửa → đổ giá trị cũ vào.
            if self.du_lieu_cu and key in self.du_lieu_cu:
                e.insert(0, str(self.du_lieu_cu[key]))
            elif key == 'trang_thai' and not self.du_lieu_cu:
                # Mặc định "Chưa duyệt" cho Bản thảo mới.
                e.insert(0, 'Chưa duyệt')

    # ----------------------------------------------------------------
    # CÁC HÀM TIỆN ÍCH CHO ĐIỀU KHIỂN GỌI
    # ----------------------------------------------------------------
    def lay_du_lieu(self):
        """Đọc toàn bộ dữ liệu form → trả về dict."""
        # Trường chung.
        du_lieu = {
            'loai_hang':    self.var_loai.get().strip(),
            'ma_so':        self.entry_ma.get().strip(),
            'ten_san_pham': self.entry_ten.get().strip(),
            'gia_co_ban':   self.entry_gia.get().strip(),
            'ton_kho':      self.entry_ton.get().strip(),
        }
        # Thêm trường riêng.
        for key, entry in self.entries_rieng.items():
            du_lieu[key] = entry.get().strip()
        return du_lieu

    def bao_loi(self, thong_bao):
        """Hiển thị hộp thoại lỗi."""
        messagebox.showerror('Lỗi', thong_bao, parent=self.top)

    def bao_thanh_cong(self, thong_bao):
        """Hiển thị hộp thoại thành công."""
        messagebox.showinfo('Thành công', thong_bao, parent=self.top)

    def dong(self):
        """Đóng form."""
        self.top.destroy()
