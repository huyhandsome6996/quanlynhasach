"""
Tệp main.py — Điểm vào ứng dụng PyQt6
========================================

Khởi tạo:
    1. QApplication (bắt buộc cho mọi app PyQt).
    2. QuanLyTrungTam (DB + DSLK + Stack/Queue).
    3. CửaSoDangNhap → nếu OK → CửaSoChinh.

Cách chạy:
    cd do_an_pyqt6
    python main.py
"""

import sys
from PyQt6.QtWidgets import QApplication

from quan_ly_trung_tam import QuanLyTrungTam
from ui.dang_nhap import CuaSoDangNhap
from ui.cua_so_chinh import CuaSoChinh


def main():
    """Hàm chính."""
    # Khởi tạo QuanLyTrungTam — bộ não của ứng dụng.
    qly = QuanLyTrungTam()
    if not qly.khoi_tao():
        print('LỖI: Không khởi tạo được hệ thống.')
        return

    # Tạo QApplication (bắt buộc).
    app = QApplication(sys.argv)

    # Hiện dialog đăng nhập trước.
    hop_dn = CuaSoDangNhap(qly)
    if hop_dn.exec() == 1:  # Accepted = login OK.
        # Mở cửa sổ chính.
        cua_so = CuaSoChinh(qly, hop_dn.nguoi_dung)
        cua_so.show()
        sys.exit(app.exec())
    # Nếu hủy dialog đăng nhập → thoát luôn.


if __name__ == '__main__':
    main()
