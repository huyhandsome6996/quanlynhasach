"""
Tệp main.py — Điểm vào của ứng dụng Tkinter
==============================================

Khởi tạo:
    1. QuanLyTrungTam (nạp DB + dữ liệu mẫu + DSLK + Stack/Queue).
    2. Tk root window.
    3. Cửa sổ đăng nhập → nếu OK → mở CửaSoChinh.

Cách chạy:
    cd do_an_tkinter
    python main.py
"""

import tkinter as tk
from tkinter import messagebox

# Import business logic.
from quan_ly_trung_tam import QuanLyTrungTam
# Import UI.
from ui.dang_nhap import CuaSoDangNhap
from ui.cua_so_chinh import CuaSoChinh


def main():
    """Hàm chính — khởi tạo ứng dụng."""
    # Khởi tạo QuanLyTrungTam — bộ não của ứng dụng.
    qly = QuanLyTrungTam()
    if not qly.khoi_tao():
        # Nếu lỗi khởi tạo → in ra + thoát.
        print('LỖI: Không khởi tạo được hệ thống.')
        return

    # Tạo root Tk (cửa sổ chính của Tkinter).
    root = tk.Tk()
    # Tạm thời KHÔNG ẩn root (bỏ root.withdraw()) để Windows chịu hiện icon dưới Taskbar!
    root.title("Quản lý nhà sách")
    root.geometry("100x100")

    # Hiện form đăng nhập.
    hop_dn = CuaSoDangNhap(root, qly)
    root.wait_window(hop_dn.top)  # Đợi đến khi đóng form.

    # Nếu đăng nhập thành công → mở cửa sổ chính.
    if hop_dn.nguoi_dung:
        root.deiconify()  # Hiện root.
        app = CuaSoChinh(root, qly, hop_dn.nguoi_dung)
        root.mainloop()   # Vòng lặp chính — chạy đến khi user đóng.
    else:
        root.destroy()  # User đóng form đăng nhập → thoát.


if __name__ == '__main__':
    main()
