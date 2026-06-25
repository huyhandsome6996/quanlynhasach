"""
Khởi tạo hệ thống — nạp dữ liệu từ SQLite vào RAM.
=====================================================
Chứa biến toàn cục và hàm khởi tạo ban đầu.
"""

import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

# ============================================================
# BIẾN TOÀN CỤC — Giữ trạng thái ứng dụng khi server đang chạy
# ============================================================
# Danh_sach_cua_hang: đối tượng DoublyLinkedList (DSLK đôi) chứa mọi mặt hàng.
#                      None nghĩa là chưa khởi tạo (sẽ tạo trong khoi_tao_danh_sach).
Danh_sach_cua_hang = None
# Bo_undoredo: dict chứa 2 Stack — 'undo' (hoàn tác) và 'redo' (làm lại).
Bo_undoredo        = None
# Gio_hang_hien_tai: đối tượng HangDoi (Queue) — giỏ hàng chung của phiên làm việc.
Gio_hang_hien_tai  = None


# ============================================================
# KHỞI TẠO HỆ THỐNG
# ============================================================

def khoi_tao_danh_sach():
    """
    Khởi tạo DSLK đôi + Undo/Redo + Giỏ hàng; nạp dữ liệu từ SQLite.

    Hàm này chạy 1 lần đầu tiên khi có request đến mà biến toàn cục còn None.
    Sau đó các biến toàn cục được giữ nguyên trong RAM suốt vòng đời server.
    """
    # Khai báo dùng biến toàn cục (global) để có thể GÁN giá trị mới cho chúng.
    global Danh_sach_cua_hang, Bo_undoredo, Gio_hang_hien_tai
    # Import DoublyLinkedList (DSLK đôi) từ module danh_sach_lien_ket.py
    # trong cùng package loi_thuat_toan.
    from ..loi_thuat_toan.danh_sach_lien_ket import DoublyLinkedList
    # Import 2 lớp cấu trúc dữ liệu tự cài đặt: NganXep (Stack) + HangDoi (Queue).
    from ..loi_thuat_toan.cau_truc_du_lieu import NganXep, HangDoi
    # Import hàm tải dữ liệu từ SQLite + hàm tạo dữ liệu mẫu nếu DB rỗng.
    from ..loi_thuat_toan.ket_noi_sqlite import tai_du_lieu, tao_du_lieu_mau_neu_rong
    # Import hàm tạo 2 tài khoản mặc định (admin + nhân viên) nếu chưa có.
    from ..loi_thuat_toan.nguoi_dung import khoi_tao_nguoi_dung_mac_dinh

    # Bảng SQLite + dữ liệu mẫu + tài khoản mẫu (chỉ tạo lần đầu).
    tao_du_lieu_mau_neu_rong()

    # Tạo đối tượng DSLK đôi RỖNG (chưa có node nào).
    Danh_sach_cua_hang = DoublyLinkedList()
    # Tải toàn bộ sản phẩm trong SQLite ra và nhét từng cái vào DSLK đôi.
    tai_du_lieu(Danh_sach_cua_hang)

    # Tạo 2 Stack dùng cho tính năng Undo (hoàn tác) + Redo (làm lại).
    ngan_xep_undo = NganXep()
    ngan_xep_redo = NganXep()
    # Bọc 2 stack vào 1 dict để dễ tham chiếu theo tên.
    Bo_undoredo = {'undo': ngan_xep_undo, 'redo': ngan_xep_redo}

    # Tạo 1 Queue dùng cho giỏ hàng (theo nguyên lý FIFO — vào trước ra trước).
    Gio_hang_hien_tai = HangDoi()

    # Tạo 2 tài khoản mẫu (admin/admin123 và nhanvien/nv123) nếu chưa có.
    khoi_tao_nguoi_dung_mac_dinh()

    # Bọc trong try/except vì một số terminal Windows không in được dấu tiếng Việt.
    try:
        # In thông báo đã nạp bao nhiêu mặt hàng vào DSLK (log ra console server).
        print(f'[KHOI DONG] Da nap {Danh_sach_cua_hang.so_luong} mat hang vao danh sach lien ket doi.')
    # Bắt lỗi UnicodeEncodeError: terminal không hỗ trợ Unicode → in bản không dấu.
    except UnicodeEncodeError:
        print(f'[KHOI DONG] Da nap {Danh_sach_cua_hang.so_luong} mat hang.')


def _lay_du_lieu():
    """
    Hàm tiện ích — trả về tuple (Danh_sach_cua_hang, Bo_undoredo, Gio_hang_hien_tai).
    Các module khác gọi hàm này thay vì import trực tiếp biến toàn cục,
    vì khi dùng `global` để gán lại biến, import trực tiếp sẽ giữ giá trị None cũ.
    """
    return Danh_sach_cua_hang, Bo_undoredo, Gio_hang_hien_tai
