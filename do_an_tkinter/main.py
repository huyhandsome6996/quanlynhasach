"""
Tệp main.py — Điểm vào của ứng dụng Tkinter
==============================================

Khởi tạo:
    1. QuanLyTrungTam (state container) — nạp DB + dữ liệu mẫu + DSLK + Stack/Queue.
    2. Tk root window.
    3. Form đăng nhập (chuc_nang/01_dang_nhap_phan_quyen) → nếu OK →
       mở Cửa sổ chính (khung_chinh/cua_so_chinh_dk).

Cách chạy:
    cd do_an_tkinter
    python main.py
"""

import tkinter as tk

# Import state container.
from quan_ly_trung_tam import QuanLyTrungTam
# Import UI + Điều khiển đăng nhập.
from chuc_nang.cn01_dang_nhap_phan_quyen.dang_nhap_ui import CuaSoDangNhapUI
from chuc_nang.cn01_dang_nhap_phan_quyen.dang_nhap_tt import BoDangNhap
# Import Điều khiển cửa sổ chính.
from khung_chinh.cua_so_chinh_dk import DieuKhienCuaSoChinh


def main():
    """Hàm chính — khởi tạo ứng dụng."""
    # Khởi tạo state container — bộ não của ứng dụng.
    qly = QuanLyTrungTam()
    if not qly.khoi_tao():
        # Nếu lỗi khởi tạo → in ra + thoát.
        print('LỖI: Không khởi tạo được hệ thống.')
        return

    # Tạo root Tk (cửa sổ chính của Tkinter).
    root = tk.Tk()
    # Tạm thời KHÔNG ẩn root (bỏ root.withdraw()) để Windows chịu hiện icon dưới Taskbar.
    root.title("Quản lý nhà sách")
    root.geometry("100x100")

    # Tạo bộ thuật toán đăng nhập.
    bo_dn = BoDangNhap()

    # Hiện form đăng nhập modal.
    form = CuaSoDangNhapUI(root)
    # Gắn phím Enter + nút Đăng nhập → xử lý đăng nhập.

    def _xu_ly_dang_nhap():
        """Hàm xử lý: đọc form → gọi bo_dn.dang_nhap → đóng form nếu OK."""
        ten = form.lay_ten_dang_nhap()
        mk = form.lay_mat_khau()
        # Validate cơ bản.
        if not ten or not mk:
            form.bao_loi('Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.')
            return
        # Gọi hàm thuật toán đăng nhập.
        ok, ket_qua = bo_dn.dang_nhap(ten, mk)
        if ok:
            # OK → lưu người dùng vào form + đóng form.
            form.nguoi_dung = ket_qua
            form.dong()
        else:
            # Sai → báo lỗi + xóa ô mật khẩu.
            form.bao_loi(ket_qua)
            form.xoa_mat_khau()

    # Gắn sự kiện.
    form.entry_mk.bind('<Return>', lambda e: _xu_ly_dang_nhap())
    form.btn_dn.config(command=_xu_ly_dang_nhap)
    # Chờ đến khi form bị đóng.
    root.wait_window(form.top)

    # Nếu đăng nhập thành công → mở cửa sổ chính.
    if form.nguoi_dung:
        # Cập nhật người dùng hiện tại vào QuanLyTrungTam.
        qly.nguoi_dung_hien_tai = form.nguoi_dung
        # Hiện root.
        root.deiconify()
        # Tạo Điều khiển cửa sổ chính (tự vẽ UI + gắn sự kiện).
        app = DieuKhienCuaSoChinh(root, qly, form.nguoi_dung)
        # Vòng lặp chính — chạy đến khi user đóng.
        root.mainloop()
    else:
        # User đóng form đăng nhập mà không login → thoát.
        root.destroy()


if __name__ == '__main__':
    main()
