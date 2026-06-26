"""
Tệp cua_so_chinh.py — Cửa sổ chính của ứng dụng Tkinter
=========================================================

Chứa:
    - Thanh đầu trang: hiển thị user + nút đăng xuất.
    - Thanh công cụ: Tìm kiếm, Sắp xếp, Undo, Redo.
    - Bảng dữ liệu (Treeview): danh sách sản phẩm.
    - Khung thống kê: tổng số, đắt nhất, rẻ nhất...
    - Khung giỏ hàng: danh sách món + tổng tiền + nút thanh toán.
    - Thanh chân: trạng thái + số lượng.

Tất cả thao tác gọi qua `QuanLyTrungTam` (không gọi trực tiếp DSLK/SQLite).
"""

import tkinter as tk
from tkinter import ttk, messagebox

from ui.dang_nhap import CuaSoDangNhap
from ui.hop_thoai_them_sua import CuaSoThemSua


class CuaSoChinh:
    """Cửa sổ chính — hiển thị sau khi đăng nhập thành công."""

    def __init__(self, root, quan_ly, nguoi_dung):
        """
        root       : Tk root.
        quan_ly    : QuanLyTrungTam đã khởi tạo.
        nguoi_dung : NguoiDung vừa đăng nhập.
        """
        self.root = root
        self.quan_ly = quan_ly
        self.nguoi_dung = nguoi_dung

        self.root.title(f'Quản lý nhà sách — {nguoi_dung.ho_ten} ({nguoi_dung.vai_tro})')
        self.root.geometry('1100x700+100+50')

        self._tao_giao_dien()
        self._cap_nhat_bang()
        self._cap_nhat_thong_ke()
        self._cap_nhat_gio_hang()
        self._cap_nhat_nut_undoredo()

    # ========================================================
    # TẠO GIAO DIỆN
    # ========================================================
    def _tao_giao_dien(self):
        """Tạo toàn bộ widget của cửa sổ chính."""
        # === THANH ĐẦU TRANG ===
        frame_dau = ttk.Frame(self.root, padding=10)
        frame_dau.pack(fill='x')
        ttk.Label(frame_dau, text='QUẢN LÝ NHÀ SÁCH',
                  font=('Arial', 16, 'bold')).pack(side='left')
        # Khung thông tin user.
        frame_user = ttk.Frame(frame_dau)
        frame_user.pack(side='right')
        ttk.Label(frame_user, text=f'Xin chào: {self.nguoi_dung.ho_ten}').pack(side='left', padx=5)
        ttk.Label(frame_user, text=f'({self.nguoi_dung.vai_tro})',
                  foreground='blue').pack(side='left', padx=5)
        ttk.Button(frame_user, text='Đăng xuất', command=self._dang_xuat).pack(side='left', padx=5)

        # === THANH CÔNG CỤ ===
        frame_cc = ttk.Frame(self.root, padding=(10, 0, 10, 5))
        frame_cc.pack(fill='x')

        # Nhóm nút Thêm/Sửa/Xóa.
        ttk.Button(frame_cc, text='➕ Thêm', width=10,
                   command=self._them_san_pham).pack(side='left', padx=2)
        ttk.Button(frame_cc, text='✏ Sửa', width=10,
                   command=self._sua_san_pham).pack(side='left', padx=2)
        ttk.Button(frame_cc, text='🗑 Xóa', width=10,
                   command=self._xoa_san_pham).pack(side='left', padx=2)
        # Separator.
        ttk.Separator(frame_cc, orient='vertical').pack(side='left', fill='y', padx=8)

        # Nhóm Undo/Redo.
        self.btn_undo = ttk.Button(frame_cc, text='↶ Hoàn tác', width=12,
                                    command=self._hoan_tac)
        self.btn_undo.pack(side='left', padx=2)
        self.btn_redo = ttk.Button(frame_cc, text='↷ Làm lại', width=12,
                                    command=self._lam_lai)
        self.btn_redo.pack(side='left', padx=2)
        ttk.Separator(frame_cc, orient='vertical').pack(side='left', fill='y', padx=8)

        # Nhóm tìm kiếm.
        ttk.Label(frame_cc, text='Tìm:').pack(side='left', padx=2)
        self.entry_tk = ttk.Entry(frame_cc, width=15)
        self.entry_tk.pack(side='left', padx=2)
        self.entry_tk.bind('<Return>', lambda e: self._tim_kiem())
        # Combobox tiêu chí tìm.
        self.var_tk_tieu_chi = tk.StringVar(value='ten')
        ttk.Combobox(frame_cc, textvariable=self.var_tk_tieu_chi,
                     values=['ten', 'ma', 'loai'], state='readonly', width=6).pack(side='left', padx=2)
        ttk.Button(frame_cc, text='Tìm', command=self._tim_kiem).pack(side='left', padx=2)
        ttk.Button(frame_cc, text='↻ Làm mới', command=self._lam_moi).pack(side='left', padx=2)
        ttk.Separator(frame_cc, orient='vertical').pack(side='left', fill='y', padx=8)

        # Nhóm sắp xếp.
        ttk.Label(frame_cc, text='Sắp xếp:').pack(side='left', padx=2)
        self.var_sx_tieu_chi = tk.StringVar(value='gia_ban')
        ttk.Combobox(frame_cc, textvariable=self.var_sx_tieu_chi,
                     values=['gia_ban', 'ten_san_pham', 'ton_kho'], state='readonly',
                     width=12).pack(side='left', padx=2)
        ttk.Button(frame_cc, text='Sắp xếp', command=self._sap_xep).pack(side='left', padx=2)

        # === KHUNG CHÍNH: BẢNG DỮ LIỆU + GIỎ HÀNG ===
        # Dùng PanedWindow: kéo để thay đổi tỷ lệ.
        paned = ttk.PanedWindow(self.root, orient='horizontal')
        paned.pack(fill='both', expand=True, padx=10, pady=5)

        # === BẢNG DỮ LIỆU (Treeview) ===
        frame_bang = ttk.LabelFrame(paned, text='Danh sách sản phẩm', padding=5)
        paned.add(frame_bang, weight=3)

        # Cột: Mã, Tên, Loại, Giá cơ bản, Tồn kho, Giá bán, Thông tin riêng.
        columns = ('ma', 'ten', 'loai', 'gia_cb', 'ton', 'gia_ban', 'rieng')
        self.tree = ttk.Treeview(frame_bang, columns=columns, show='headings', height=15)
        # Định nghĩa header + độ rộng từng cột.
        self.tree.heading('ma', text='Mã số')
        self.tree.heading('ten', text='Tên sản phẩm')
        self.tree.heading('loai', text='Loại')
        self.tree.heading('gia_cb', text='Giá cơ bản')
        self.tree.heading('ton', text='Tồn kho')
        self.tree.heading('gia_ban', text='Giá bán (đã tính)')
        self.tree.heading('rieng', text='Thông tin riêng')
        self.tree.column('ma', width=70, anchor='center')
        self.tree.column('ten', width=200)
        self.tree.column('loai', width=80, anchor='center')
        self.tree.column('gia_cb', width=100, anchor='e')
        self.tree.column('ton', width=70, anchor='center')
        self.tree.column('gia_ban', width=110, anchor='e')
        self.tree.column('rieng', width=250)
        # Scrollbar dọc.
        scrollbar = ttk.Scrollbar(frame_bang, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Bind double-click vào dòng → mở dialog Sửa.
        self.tree.bind('<Double-1>', lambda e: self._sua_san_pham())

        # === KHUNG BÊN PHẢI: THỐNG KÊ + GIỎ HÀNG ===
        frame_phai = ttk.Frame(paned)
        paned.add(frame_phai, weight=2)

        # --- Thống kê ---
        frame_tk = ttk.LabelFrame(frame_phai, text='Thống kê', padding=10)
        frame_tk.pack(fill='x', pady=(0, 5))
        self.lbl_tong_so = ttk.Label(frame_tk, text='Tổng số: 0')
        self.lbl_tong_so.pack(anchor='w')
        self.lbl_dat = ttk.Label(frame_tk, text='Đắt nhất: -')
        self.lbl_dat.pack(anchor='w')
        self.lbl_re = ttk.Label(frame_tk, text='Rẻ nhất: -')
        self.lbl_re.pack(anchor='w')
        self.lbl_tri_kho = ttk.Label(frame_tk, text='Tổng giá trị kho: 0đ')
        self.lbl_tri_kho.pack(anchor='w')
        self.lbl_sap_het = ttk.Label(frame_tk, text='Sắp hết (<5): 0', foreground='red')
        self.lbl_sap_het.pack(anchor='w')

        # --- Giỏ hàng ---
        frame_gio = ttk.LabelFrame(frame_phai, text='🛒 Giỏ hàng (Queue FIFO)', padding=10)
        frame_gio.pack(fill='both', expand=True)

        # Bảng giỏ hàng.
        columns_gio = ('ma', 'ten', 'gia', 'loai')
        self.tree_gio = ttk.Treeview(frame_gio, columns=columns_gio, show='headings', height=8)
        self.tree_gio.heading('ma', text='Mã')
        self.tree_gio.heading('ten', text='Tên')
        self.tree_gio.heading('gia', text='Giá bán')
        self.tree_gio.heading('loai', text='Loại')
        self.tree_gio.column('ma', width=60, anchor='center')
        self.tree_gio.column('ten', width=150)
        self.tree_gio.column('gia', width=90, anchor='e')
        self.tree_gio.column('loai', width=70, anchor='center')
        self.tree_gio.pack(fill='both', expand=True)

        # Nút thêm vào giỏ (lấy từ dòng đang chọn trong bảng chính).
        ttk.Button(frame_gio, text='+ Thêm vào giỏ',
                   command=self._them_vao_gio).pack(side='left', pady=5)
        ttk.Button(frame_gio, text='- Bỏ khỏi giỏ',
                   command=self._xoa_khoi_gio).pack(side='left', pady=5, padx=5)
        ttk.Button(frame_gio, text='💰 Thanh toán',
                   command=self._thanh_toan).pack(side='right', pady=5)

        # Tổng tiền giỏ.
        self.lbl_tong_gio = ttk.Label(frame_gio, text='Tổng: 0đ',
                                       font=('Arial', 11, 'bold'), foreground='green')
        self.lbl_tong_gio.pack(side='right', pady=5, padx=10)

        # === THANH CHÂN ===
        frame_chan = ttk.Frame(self.root, padding=5)
        frame_chan.pack(side='bottom', fill='x')
        self.lbl_trang_thai = ttk.Label(frame_chan, text='Sẵn sàng.', foreground='gray')
        self.lbl_trang_thai.pack(side='left')

    # ========================================================
    # CẬP NHẬT UI
    # ========================================================
    def _cap_nhat_bang(self, danh_sach=None):
        """Vẽ lại bảng sản phẩm. Nếu không truyền ds → tải từ QuanLy."""
        # Xóa hết dòng cũ.
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Lấy danh sách mới nếu không truyền.
        if danh_sach is None:
            danh_sach = self.quan_ly.lay_danh_sach()

        # Thêm từng sản phẩm vào Treeview.
        for sp in danh_sach:
            # Tạo chuỗi thông tin riêng theo loại.
            rieng = self._str_truong_rieng(sp)
            # Format giá tiền có dấu phẩy.
            gia_cb = f"{sp.get('gia_co_ban', 0):,.0f}"
            gia_ban = f"{sp.get('gia_ban', 0):,.0f}"
            self.tree.insert('', 'end', values=(
                sp.get('ma_so', ''),
                sp.get('ten_san_pham', ''),
                sp.get('loai_hang', ''),
                gia_cb,
                sp.get('ton_kho', 0),
                gia_ban,
                rieng
            ))

        # Cập nhật thanh trạng thái.
        self._dat_trang_thai(f'Đã tải {len(danh_sach)} mặt hàng.')

    def _str_truong_rieng(self, sp):
        """Tạo chuỗi hiển thị thông tin riêng theo loại hàng."""
        loai = sp.get('loai_hang', '')
        if loai == 'Sách':
            return f"Tác giả: {sp.get('tac_gia', '')} | NXB: {sp.get('nha_xuat_ban', '')}"
        elif loai == 'Tạp chí':
            return f"Số phát hành: {sp.get('so_phat_hanh', '')}"
        elif loai == 'Báo giấy':
            return f"Ngày XB: {sp.get('ngay_xuat_ban', '')}"
        elif loai == 'Luận văn':
            return f"Tác giả: {sp.get('tac_gia', '')} | Trường: {sp.get('truong_dai_hoc', '')}"
        elif loai == 'Bản thảo':
            return f"Tác giả: {sp.get('tac_gia', '')} | TT: {sp.get('tinh_trang', '')}"
        return ''

    def _cap_nhat_thong_ke(self):
        """Lấy dict thống kê từ QuanLy + cập nhật các label."""
        tk = self.quan_ly.lay_thong_ke()
        if not tk:
            return
        self.lbl_tong_so.config(text=f"Tổng số: {tk.get('tong_so', 0)} mặt hàng")
        self.lbl_dat.config(text=f"Đắt nhất: {tk.get('dat_nhat', '-')}")
        self.lbl_re.config(text=f"Rẻ nhất: {tk.get('re_nhat', '-')}")
        self.lbl_tri_kho.config(text=f"Tổng giá trị kho: {tk.get('tong_gia_tri_kho', 0):,.0f}đ")
        self.lbl_sap_het.config(text=f"Sắp hết (<5): {len(tk.get('sap_het_hang', []))}")

    def _cap_nhat_gio_hang(self):
        """Vẽ lại bảng giỏ + tổng tiền."""
        # Xóa cũ.
        for item in self.tree_gio.get_children():
            self.tree_gio.delete(item)

        ds, tong, so_luong = self.quan_ly.xem_gio_hang()
        for mon in ds:
            self.tree_gio.insert('', 'end', values=(
                mon.get('ma_so', ''),
                mon.get('ten_san_pham', ''),
                f"{mon.get('gia_ban', 0):,.0f}",
                mon.get('loai_hang', '')
            ))
        self.lbl_tong_gio.config(text=f"Tổng: {tong:,.0f}đ ({so_luong} món)")

    def _cap_nhat_nut_undoredo(self):
        """Bật/tắt nút Undo/Redo theo trạng thái."""
        tt = self.quan_ly.trang_thai_undoredo()
        self.btn_undo.config(state='normal' if tt['co_the_undo'] else 'disabled')
        self.btn_redo.config(state='normal' if tt['co_the_redo'] else 'disabled')

    def _dat_trang_thai(self, msg):
        """Cập nhật thanh trạng thái."""
        self.lbl_trang_thai.config(text=msg)

    # ========================================================
    # XỬ LÝ SỰ KIỆN
    # ========================================================
    def _them_san_pham(self):
        """Mở dialog Thêm sản phẩm."""
        hop = CuaSoThemSua(self.root, self.quan_ly, du_lieu_cu=None)
        self.root.wait_window(hop.top)  # Đợi đến khi đóng dialog.
        if hop.ket_qua:
            self._cap_nhat_bang()
            self._cap_nhat_thong_ke()
            self._cap_nhat_nut_undoredo()

    def _sua_san_pham(self):
        """Mở dialog Sửa sản phẩm (lấy dòng đang chọn)."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('Chưa chọn', 'Vui lòng chọn 1 dòng để sửa.')
            return
        # Lấy values từ dòng đang chọn.
        values = self.tree.item(selected[0], 'values')
        ma = values[0]
        # Tìm dict đầy đủ từ QuanLy.
        sp = self.quan_ly.danh_sach.tim_theo_ma_so(ma)
        if sp is None:
            messagebox.showerror('Lỗi', f'Không tìm thấy sản phẩm {ma}.')
            return
        # Mở dialog sửa.
        hop = CuaSoThemSua(self.root, self.quan_ly, du_lieu_cu=sp.chuyen_thanh_dict())
        self.root.wait_window(hop.top)
        if hop.ket_qua:
            self._cap_nhat_bang()
            self._cap_nhat_thong_ke()
            self._cap_nhat_nut_undoredo()

    def _xoa_san_pham(self):
        """Xóa sản phẩm đang chọn (chỉ Admin)."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('Chưa chọn', 'Vui lòng chọn 1 dòng để xóa.')
            return
        values = self.tree.item(selected[0], 'values')
        ma = values[0]
        # Hỏi xác nhận.
        if not messagebox.askyesno('Xác nhận', f'Bạn có chắc muốn xóa sản phẩm "{ma}"?'):
            return
        # Gọi hàm xóa.
        ok, msg = self.quan_ly.xoa_san_pham(ma)
        if ok:
            messagebox.showinfo('Thành công', msg)
            self._cap_nhat_bang()
            self._cap_nhat_thong_ke()
            self._cap_nhat_nut_undoredo()
        else:
            messagebox.showerror('Lỗi', msg)

    def _tim_kiem(self):
        """Tìm kiếm theo từ khóa + tiêu chí."""
        tu_khoa = self.entry_tk.get().strip()
        tieu_chi = self.var_tk_tieu_chi.get()
        kq = self.quan_ly.tim_kiem(tu_khoa, tieu_chi)
        self._cap_nhat_bang(kq)
        self._dat_trang_thai(f'Tìm thấy {len(kq)} kết quả cho "{tu_khoa}".')

    def _sap_xep(self):
        """Sắp xếp DSLK theo tiêu chí + vẽ lại bảng."""
        tieu_chi = self.var_sx_tieu_chi.get()
        kq = self.quan_ly.sap_xep(tieu_chi)
        self._cap_nhat_bang(kq)
        self._dat_trang_thai(f'Đã sắp xếp theo {tieu_chi}.')

    def _lam_moi(self):
        """Làm mới bảng từ DB."""
        self._cap_nhat_bang()
        self._cap_nhat_thong_ke()

    def _hoan_tac(self):
        """Undo."""
        ok, msg = self.quan_ly.hoan_tac()
        if ok:
            self._cap_nhat_bang()
            self._cap_nhat_thong_ke()
            self._cap_nhat_nut_undoredo()
            self._dat_trang_thai(msg)
        else:
            messagebox.showinfo('Thông báo', msg)

    def _lam_lai(self):
        """Redo."""
        ok, msg = self.quan_ly.lam_lai()
        if ok:
            self._cap_nhat_bang()
            self._cap_nhat_thong_ke()
            self._cap_nhat_nut_undoredo()
            self._dat_trang_thai(msg)
        else:
            messagebox.showinfo('Thông báo', msg)

    def _them_vao_gio(self):
        """Thêm dòng đang chọn vào giỏ (Enqueue)."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning('Chưa chọn', 'Vui lòng chọn 1 dòng để thêm vào giỏ.')
            return
        values = self.tree.item(selected[0], 'values')
        ma = values[0]
        ok, msg = self.quan_ly.them_vao_gio(ma)
        if ok:
            self._cap_nhat_gio_hang()
            self._dat_trang_thai(msg)
        else:
            messagebox.showerror('Lỗi', msg)

    def _xoa_khoi_gio(self):
        """Xóa 1 món khỏi giỏ."""
        selected = self.tree_gio.selection()
        if not selected:
            messagebox.showwarning('Chưa chọn', 'Vui lòng chọn món cần bỏ.')
            return
        values = self.tree_gio.item(selected[0], 'values')
        ma = values[0]
        ok, msg = self.quan_ly.xoa_khoi_gio(ma)
        if ok:
            self._cap_nhat_gio_hang()
        else:
            messagebox.showerror('Lỗi', msg)

    def _thanh_toan(self):
        """Thanh toán toàn bộ giỏ (Dequeue all)."""
        ok, msg, hoa_don = self.quan_ly.thanh_toan()
        if ok:
            # Hiển thị hóa đơn.
            chi_tiet = '\n'.join([f"  - {m['ten_san_pham']}: {m['gia_ban']:,.0f}đ"
                                   for m in hoa_don['cac_mon']])
            messagebox.showinfo('Thanh toán thành công',
                                 f"{msg}\n\nChi tiết:\n{chi_tiet}\n\nTổng: {hoa_don['tong_tien']:,.0f}đ")
            self._cap_nhat_gio_hang()
        else:
            messagebox.showwarning('Thông báo', msg)

    # ========================================================
    # ĐĂNG XUẤT
    # ========================================================
    def _dang_xuat(self):
        """Đăng xuất → hiện lại form đăng nhập → mở cửa sổ chính với user mới."""
        if not messagebox.askyesno('Xác nhận', 'Bạn có chắc muốn đăng xuất?'):
            return
        self.quan_ly.dang_xuat()
        # Ẩn cửa sổ chính.
        self.root.withdraw()
        # Hiện form đăng nhập.
        hop = CuaSoDangNhap(self.root, self.quan_ly)
        self.root.wait_window(hop.top)
        if hop.nguoi_dung:
            # Cập nhật user + mở lại.
            self.nguoi_dung = hop.nguoi_dung
            self.root.title(f'Quản lý nhà sách — {self.nguoi_dung.ho_ten} '
                            f'({self.nguoi_dung.vai_tro})')
            self.root.deiconify()
            self._cap_nhat_bang()
            self._cap_nhat_thong_ke()
            self._cap_nhat_gio_hang()
            self._cap_nhat_nut_undoredo()
        else:
            # User đóng form đăng nhập → thoát app.
            self.root.quit()
