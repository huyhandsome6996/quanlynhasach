"""
Tệp doc_danh_sach_tt.py — THUẬT TOÁN cho chức năng Đọc danh sách sản phẩm
==========================================================================

Chứa hàm đọc toàn bộ mặt hàng từ DSLK đôi và trả về danh sách dict để UI hiển thị.
"""

# Import lớp DSLK đôi từ thư viện thuật toán.
from loi_thuat_toan.danh_sach_lien_ket import DoublyLinkedList


def lay_danh_sach(danh_sach: DoublyLinkedList):
    """
    Đọc toàn bộ mặt hàng trong DSLK đôi và trả về list dict.

    Tham số:
        danh_sach : đối tượng DoublyLinkedList chứa các MatHang.

    Trả về:
        List[dict] — mỗi dict là 1 mặt hàng (ma_so, ten, loai_hang, gia, ton, rieng...).
        Trả về [] nếu lỗi hoặc DSLK rỗng.
    """
    try:
        # Nếu DSLK chưa khởi tạo → trả về danh sách rỗng.
        if danh_sach is None:
            return []
        # Gọi hàm có sẵn của DoublyLinkedList để chuyển DSLK → list dict.
        return danh_sach.chuyen_thanh_danh_sach()
    except Exception as loi:
        # Lỗi bất kỳ → in ra + trả về danh sách rỗng để UI không bị crash.
        print(f'[LOI doc_danh_sach] {loi}')
        return []
