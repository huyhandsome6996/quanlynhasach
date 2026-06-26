"""
Tệp sua_san_pham_ui.py — GIAO DIỆN cho chức năng Sửa sản phẩm
==============================================================

Hiển thị form modal cho user chỉnh sửa các trường của 1 sản phẩm:
    - Trường chung: Tên, Giá, Tồn (Mã + Loại bị khóa vì không đổi được).
    - Trường riêng: hiển thị theo loại của sản phẩm đang sửa.

Vì form Thêm và form Sửa gần như giống nhau, UI thực sự nằm ở
chuc_nang/_shared/form_them_sua_ui.py. File này RE-EXPORT lớp đó
để mã điều khiển trong folder 04_sua_san_pham import theo quy ước "_ui".
"""

# Import lớp FormThemSuaUI dùng chung.
from chuc_nang._shared.form_them_sua_ui import FormThemSuaUI

# Re-export.
__all__ = ['FormThemSuaUI']
