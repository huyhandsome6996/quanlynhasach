"""
Tệp dang_nhap.py — Cửa sổ đăng nhập (Tkinter)
================================================

Hiển thị form nhập tên đăng nhập + mật khẩu. Nếu đăng nhập thành công
→ đóng cửa sổ này và mở CửaSoChinh. Nếu sai → báo lỗi bằng messagebox.
"""

import tkinter as tk
from tkinter import ttk, messagebox


class CuaSoDangNhap:
    """
    Cửa sổ đăng nhập — chạy modal (chặn tương tác với cửa sổ chính).
    Sau khi đóng, thuộc tính `nguoi_dung` chứa NguoiDung nếu login OK.
    """

    def __init__(self, parent, quan_ly):
        """
        Khởi tạo cửa sổ đăng nhập.

        Tham số:
            parent   : Cửa sổ cha (root Tk).
            quan_ly  : Đối tượng QuanLyTrungTam để gọi hàm dang_nhap.
        """
        # Tạo Toplevel (cửa sổ con) — modal.
        self.top = tk.Toplevel(parent)
        self.top.title('Đăng nhập hệ thống')
        self.top.geometry('380x220+500+250')
        # Làm cửa sổ modal: bắt sự kiện đóng → không cho tương tác parent.
        self.top.transient(parent)
        self.top.grab_set()
        
        # [MẸO NHỎ] Ép cửa sổ nổi lên trên cùng (đè lên VS Code) để dễ nhìn thấy.
        self.top.lift()
        self.top.attributes('-topmost', True)
        # Bỏ topmost đi ngay lập tức để sau này không bị kẹt dính trên cùng.
        self.top.after(100, lambda: self.top.attributes('-topmost', False))
        self.top.focus_force()

        self.quan_ly = quan_ly
        self.nguoi_dung = None  # Sẽ gán nếu đăng nhập thành công.

        self._tao_giao_dien()

    def _tao_giao_dien(self):
        """Tạo các widget (label, entry, button) cho form."""
        # Frame chứa nội dung, padding 20px các phía.
        frame = ttk.Frame(self.top, padding=20)
        frame.pack(fill='both', expand=True)

        # Tiêu đề.
        ttk.Label(frame, text='ĐĂNG NHẬP',
                  font=('Arial', 16, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0, 15))

        # Label + Entry cho tên đăng nhập.
        ttk.Label(frame, text='Tên đăng nhập:').grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.entry_ten = ttk.Entry(frame, width=25)
        self.entry_ten.grid(row=1, column=1, padx=5, pady=5)
        self.entry_ten.focus()  # Focus vào ô này khi mở.

        # Label + Entry cho mật khẩu (show='*' để ẩn ký tự).
        ttk.Label(frame, text='Mật khẩu:').grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.entry_mk = ttk.Entry(frame, width=25, show='*')
        self.entry_mk.grid(row=2, column=1, padx=5, pady=5)

        # Bind Enter → submit.
        self.entry_mk.bind('<Return>', lambda e: self._xu_ly_dang_nhap())
        self.entry_ten.bind('<Return>', lambda e: self.entry_mk.focus())

        # Nút đăng nhập (columnspan=2 để rộng qua 2 cột).
        ttk.Button(frame, text='Đăng nhập', command=self._xu_ly_dang_nhap).grid(
            row=3, column=0, columnspan=2, pady=15, sticky='ew')

        # Gợi ý tài khoản mẫu.
        ttk.Label(frame, text='(Mặc định: admin/123 hoặc nhanvien/123)',
                  foreground='gray').grid(row=4, column=0, columnspan=2)

    def _xu_ly_dang_nhap(self):
        """Lấy dữ liệu từ form → gọi QuanLyTrungTam.dang_nhap."""
        ten = self.entry_ten.get().strip()
        mk = self.entry_mk.get().strip()

        # Validate: không rỗng.
        if not ten or not mk:
            messagebox.showwarning('Thiếu thông tin',
                                   'Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.',
                                   parent=self.top)
            return

        # Gọi hàm đăng nhập.
        ok, ket_qua = self.quan_ly.dang_nhap(ten, mk)
        if ok:
            self.nguoi_dung = ket_qua
            self.top.destroy()  # Đóng cửa sổ đăng nhập.
        else:
            messagebox.showerror('Đăng nhập thất bại', ket_qua, parent=self.top)
            self.entry_mk.delete(0, tk.END)  # Xóa ô mật khẩu để nhập lại.
