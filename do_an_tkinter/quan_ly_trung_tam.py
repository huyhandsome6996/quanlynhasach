"""
Tệp quan_ly_trung_tam.py — Lớp QuanLyTrungTam (FACADE)
=======================================================

File này được GIỮ LẠI để mã cũ (test_app.py) tiếp tục chạy được sau khi
đã tái cấu trúc theo pattern "mỗi chức năng = 1 folder có 3 file _tt/_ui/_dk".

Thực tế logic đã được chuyển vào:
    - khung_chinh/khung_chinh_tt.py  ← state container (chính là lớp này).
    - chuc_nang/NN_*/*_tt.py          ← thuật toán từng chức năng.

File này chỉ re-export lớp QuanLyTrungTam từ khung_chinh/khung_chinh_tt.py.
"""

# Import + re-export lớp QuanLyTrungTam từ khung_chinh.
from khung_chinh.khung_chinh_tt import QuanLyTrungTam

# Cho phép: from quan_ly_trung_tam import QuanLyTrungTam.
__all__ = ['QuanLyTrungTam']
