"""
Tệp dang_nhap_ui.py — GIAO DIỆN cho chức năng Đăng nhập
=========================================================

Chỉ chứa code giao diện (widget Tkinter) — KHÔNG chứa logic nghiệp vụ.
Logic nằm ở dang_nhap_tt.py. Điểu khiển luồng nằm ở dang_nhap_dk.py.
"""

import tkinter as tk
from tkinter import ttk, messagebox


class CuaSoDangNhapUI:
    """
    Cửa sổ giao diện đăng nhập — chạy modal (chặn tương tác cửa sổ cha).
    Sau khi đóng, thuộc tính `nguoi_dung` chứa NguoiDung nếu login OK.
    """

    def __init__(self, parent):
        """
        Khởi tạo cửa sổ đăng nhập.

        Tham số:
            parent : cửa sổ cha (Tk root).
        """
        # Tạo Toplevel (cửa sổ con) — modal.
        self.top = tk.Toplevel(parent)
        self.top.title('Đăng nhập hệ thống')
        self.top.geometry('380x220+500+250')
        # Làm cửa sổ modal: chặn tương tác parent.
        self.top.transient(parent)
        self.top.grab_set()

        # Ép cửa sổ nổi lên trên cùng (đè lên VS Code) để dễ nhìn thấy.
        self.top.lift()
        self.top.attributes('-topmost', True)
        # Bỏ topmost đi ngay lập tức để sau này không bị kẹt dính trên cùng.
        self.top.after(100, lambda: self.top.attributes('-topmost', False))
        self.top.focus_force()

        # Ban đầu chưa có người dùng — sẽ được gán nếu login OK.
        self.nguoi_dung = None

        # Gọi hàm tạo giao diện.
        self._tao_giao_dien()

    def _tao_giao_dien(self):
        """Tạo các widget (label, entry, button) cho form đăng nhập."""
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
        self.entry_ten.focus()  # Focus vào ô này khi mở form.

        # Label + Entry cho mật khẩu (show='*' để ẩn ký tự).
        ttk.Label(frame, text='Mật khẩu:').grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.entry_mk = ttk.Entry(frame, width=25, show='*')
        self.entry_mk.grid(row=2, column=1, padx=5, pady=5)

        # Bind phím Enter → chuyển focus sang ô mật khẩu (nếu đang ở ô tên).
        self.entry_ten.bind('<Return>', lambda e: self.entry_mk.focus())
        # Bind Enter ở ô mật khẩu → gọi hàm xử lý đăng nhập.

        # Nút đăng nhập (columnspan=2 để rộng qua 2 cột).
        self.btn_dn = ttk.Button(frame, text='Đăng nhập')
        self.btn_dn.grid(row=3, column=0, columnspan=2, pady=15, sticky='ew')

        # Gợi ý tài khoản mẫu.
        ttk.Label(frame, text='(Mặc định: admin/123 hoặc nhanvien/123)',
                  foreground='gray').grid(row=4, column=0, columnspan=2)

    # ----------------------------------------------------------------
    # CÁC HÀM TIỆN ÍCH CHO ĐIỀU KHIỂN GỌI
    # ----------------------------------------------------------------
    def lay_ten_dang_nhap(self):
        """Trả về tên đăng nhập user nhập (đã strip khoảng trắng)."""
        return self.entry_ten.get().strip()

    def lay_mat_khau(self):
        """Trả về mật khẩu user nhập (đã strip khoảng trắng)."""
        return self.entry_mk.get().strip()

    def xoa_mat_khau(self):
        """Xóa ô mật khẩu — dùng khi sai mật khẩu để user nhập lại."""
        self.entry_mk.delete(0, tk.END)

    def bao_loi(self, thong_bao):
        """Hiển thị hộp thoại lỗi."""
        messagebox.showerror('Đăng nhập thất bại', thong_bao, parent=self.top)

    def dong(self):
        """Đóng cửa sổ đăng nhập."""
        self.top.destroy()
