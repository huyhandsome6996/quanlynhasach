"""
Tệp hop_thoai_them_sua.py — Hộp thoại Thêm/Sửa sản phẩm (Tkinter)
===================================================================

Một lớp duy nhất CuaSoThemSua — dùng chung cho Thêm và Sửa.
Khi `du_lieu_cu=None`: chế độ Thêm mới.
Khi `du_lieu_cu=dict`: chế độ Sửa (đổ dữ liệu vào form).
"""

import tkinter as tk
from tkinter import ttk, messagebox


# Danh sách 5 loại hàng + các trường riêng từng loại.
CAC_LOAI_HANG = ['Sách', 'Tạp chí', 'Báo giấy', 'Luận văn', 'Bản thảo']


class CuaSoThemSua:
    """Hộp thoại modal để thêm hoặc sửa 1 sản phẩm."""

    def __init__(self, parent, quan_ly, du_lieu_cu=None):
        """
        parent      : Cửa sổ cha.
        quan_ly     : QuanLyTrungTam.
        du_lieu_cu  : None = thêm mới; dict = sửa.
        """
        self.quan_ly = quan_ly
        self.du_lieu_cu = du_lieu_cu
        self.ket_qua = None  # Sẽ chứa dict dữ liệu user nhập khi OK.

        self.top = tk.Toplevel(parent)
        self.top.title('Sửa sản phẩm' if du_lieu_cu else 'Thêm sản phẩm')
        self.top.geometry('450x520+450+150')
        self.top.transient(parent)
        self.top.grab_set()

        self._tao_giao_dien()

    def _tao_giao_dien(self):
        """Tạo form với các trường động theo loại hàng."""
        frame = ttk.Frame(self.top, padding=20)
        frame.pack(fill='both', expand=True)

        # === CÁC TRƯỜNG CHUNG ===
        ttk.Label(frame, text='Loại hàng:').grid(row=0, column=0, sticky='e', padx=5, pady=5)
        # Combobox chọn loại (chế độ Sửa thì khóa không cho đổi).
        self.var_loai = tk.StringVar()
        self.combo_loai = ttk.Combobox(frame, textvariable=self.var_loai,
                                        values=CAC_LOAI_HANG, state='readonly', width=22)
        self.combo_loai.grid(row=0, column=1, padx=5, pady=5)
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
        ttk.Button(frame_nut, text='Lưu', command=self._luu).pack(side='left', padx=10)
        ttk.Button(frame_nut, text='Hủy', command=self.top.destroy).pack(side='left', padx=10)

        # === NẾU LÀ SỬA → ĐỔ DỮ LIỆU CŨ VÀO FORM ===
        if self.du_lieu_cu:
            self.var_loai.set(self.du_lieu_cu.get('loai_hang', ''))
            # Lock combobox (không cho đổi loại khi sửa).
            self.combo_loai.config(state='disabled')
            self.entry_ma.insert(0, self.du_lieu_cu.get('ma_so', ''))
            self.entry_ma.config(state='disabled')  # Mã số không đổi khi sửa.
            self.entry_ten.insert(0, self.du_lieu_cu.get('ten_san_pham', ''))
            self.entry_gia.insert(0, str(self.du_lieu_cu.get('gia_co_ban', '')))
            self.entry_ton.insert(0, str(self.du_lieu_cu.get('ton_kho', '')))
            self._cap_nhat_truong_rieng()
        else:
            # Mặc định chọn loại đầu tiên.
            self.var_loai.set(CAC_LOAI_HANG[0])
            self._cap_nhat_truong_rieng()

    def _cap_nhat_truong_rieng(self):
        """Xóa các entry cũ + tạo entry mới theo loại đang chọn."""
        # Xóa widget cũ.
        for w in self.frame_rieng.winfo_children():
            w.destroy()
        self.entries_rieng.clear()

        loai = self.var_loai.get()
        # Định nghĩa trường riêng cho từng loại.
        truong_rieng = {
            'Sách':      [('tac_gia', 'Tác giả:'), ('nha_xuat_ban', 'Nhà xuất bản:')],
            'Tạp chí':   [('so_phat_hanh', 'Số phát hành:')],
            'Báo giấy':  [('ngay_xuat_ban', 'Ngày xuất bản:')],
            'Luận văn':  [('tac_gia', 'Tác giả:'), ('truong_dai_hoc', 'Trường ĐH:')],
            'Bản thảo':  [('tac_gia', 'Tác giả:'), ('trang_thai', 'Tình trạng:')],
        }
        ds_truong = truong_rieng.get(loai, [])

        # Tạo từng cột label + entry.
        for i, (key, label) in enumerate(ds_truong):
            ttk.Label(self.frame_rieng, text=label).grid(row=i, column=0, sticky='e', padx=5, pady=3)
            e = ttk.Entry(self.frame_rieng, width=25)
            e.grid(row=i, column=1, padx=5, pady=3)
            self.entries_rieng[key] = e
            # Nếu là sửa → đổ giá trị cũ vào.
            if self.du_lieu_cu and key in self.du_lieu_cu:
                e.insert(0, str(self.du_lieu_cu[key]))
            elif key == 'trang_thai' and not self.du_lieu_cu:
                e.insert(0, 'Chưa duyệt')  # Giá trị mặc định cho Bản thảo.

    def _luu(self):
        """Đọc dữ liệu form → gói thành dict → trả về cho caller."""
        # Lấy dữ liệu trường chung.
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

        # Gọi QuanLyTrungTam để lưu.
        if self.du_lieu_cu:
            # Chế độ Sửa.
            du_lieu['ma_so'] = self.du_lieu_cu['ma_so']  # Đảm bảo mã không đổi.
            ok, msg = self.quan_ly.sua_san_pham(du_lieu)
        else:
            ok, msg = self.quan_ly.them_san_pham(du_lieu)

        if ok:
            self.ket_qua = du_lieu
            messagebox.showinfo('Thành công', msg, parent=self.top)
            self.top.destroy()
        else:
            messagebox.showerror('Lỗi', msg, parent=self.top)
