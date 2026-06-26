"""
Tệp xoa_san_pham_ui.py — GIAO DIỆN cho chức năng Xóa sản phẩm
==============================================================

Vì thao tác xóa không cần form nhập liệu (chỉ cần xác nhận YES/NO),
nên file UI này cung cấp 2 hàm tiện ích:
    - hoi_xac_nhan_xoa(parent, ma_so)  → hiện hộp thoại YES/NO.
    - bao_loi(parent, thong_bao)       → hiện hộp thoại lỗi.
    - bao_thanh_cong(parent, thong_bao) → hiện hộp thoại thành công.
"""

# Import messagebox từ tkinter.
from tkinter import messagebox


def hoi_xac_nhan_xoa(parent, ma_so):
    """
    Hiện hộp thoại YES/NO hỏi user có chắc muốn xóa sản phẩm không.

    Tham số:
        parent : cửa sổ cha.
        ma_so  : mã sản phẩm sắp xóa (hiển thị để user rõ).

    Trả về:
        True  nếu user nhấn Yes.
        False nếu user nhấn No.
    """
    # askyesno trả về True/False.
    return messagebox.askyesno(
        'Xác nhận xóa',
        f'Bạn có chắc muốn xóa sản phẩm mã "{ma_so}"?\n'
        f'(Lưu ý: thao tác này có thể Hoàn tác.)'
    )


def bao_loi(parent, thong_bao):
    """Hiện thông báo lỗi."""
    messagebox.showerror('Lỗi', thong_bao, parent=parent)


def bao_thanh_cong(parent, thong_bao):
    """Hiện thông báo thành công."""
    messagebox.showinfo('Thành công', thong_bao, parent=parent)
