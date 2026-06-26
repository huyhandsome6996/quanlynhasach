"""
Tệp thong_ke_tt.py — THUẬT TOÁN cho chức năng Thống kê
========================================================

Chứa hàm lay_thong_ke(danh_sach) — gọi hàm thong_ke() của DSLK để lấy:
    - tong_so           : tổng số mặt hàng.
    - dat_nhat          : dict mặt hàng có giá bán cao nhất.
    - re_nhat           : dict mặt hàng có giá bán thấp nhất.
    - sap_het_hang      : list dict các mặt hàng tồn kho ≤ 5.
    - theo_loai         : dict số lượng + tổng tồn theo từng loại.
    - tong_gia_tri_kho  : tổng giá trị hàng trong kho (gia_co_ban × ton_kho).
    - tong_ton_kho      : tổng số sản phẩm tồn.
"""

# Import DoublyLinkedList (type hint).
from loi_thuat_toan.danh_sach_lien_ket import DoublyLinkedList


def lay_thong_ke(danh_sach: DoublyLinkedList):
    """
    Trả về dict thống kê toàn bộ danh sách.

    Tham số:
        danh_sach : DSLK đôi toàn cục.

    Trả về:
        Dict — chứa các key đã liệt kê ở docstring module.
        Trả về {} nếu lỗi.
    """
    try:
        # Gọi hàm thong_ke() của DSLK — đã tự cài đặt duyệt + tích lũy.
        return danh_sach.thong_ke()
    except Exception as loi:
        print(f'[LOI thong_ke] {loi}')
        return {}
