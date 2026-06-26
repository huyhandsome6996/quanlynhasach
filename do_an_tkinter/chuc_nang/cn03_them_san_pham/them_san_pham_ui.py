"""
Tệp them_san_pham_ui.py — GIAO DIỆN cho chức năng Thêm sản phẩm
================================================================

Hiển thị form modal cho user nhập các trường:
    - Trường chung: Loại, Mã, Tên, Giá, Tồn.
    - Trường riêng: thay đổi theo loại hàng (vd: Sách có Tác giả + NXB).

Vì form Thêm và form Sửa gần như giống hệt nhau (chỉ khác chế độ),
nên UI thực sự nằm ở chuc_nang/_shared/form_them_sua_ui.py (dùng chung).
File này chỉ RE-EXPORT lớp FormThemSuaUI để mã điều khiển trong folder
03_them_san_pham có thể import theo quy ước "_ui".
"""

# Import lớp FormThemSuaUI + danh sách loại hàng từ thư mục _shared.
from chuc_nang._shared.form_them_sua_ui import FormThemSuaUI, CAC_LOAI_HANG

# Re-export để mã ngoài có thể dùng: from .them_san_pham_ui import FormThemSuaUI.
__all__ = ['FormThemSuaUI', 'CAC_LOAI_HANG']
