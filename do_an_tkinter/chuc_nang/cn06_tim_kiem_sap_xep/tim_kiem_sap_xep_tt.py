"""
Tệp tim_kiem_sap_xep_tt.py — THUẬT TOÁN cho Tìm kiếm + Sắp xếp
=================================================================

Bao gồm 2 hàm:
    1. tim_kiem(danh_sach, tu_khoa, tieu_chi) — tìm theo tên/mã/loại.
    2. sap_xep(danh_sach, tieu_chi)            — sắp xếp DSLK bằng Merge Sort.

Trả về list dict để UI hiển thị trực tiếp (không cần chuyển đổi thêm).
"""

# Import DoublyLinkedList (type hint).
from loi_thuat_toan.danh_sach_lien_ket import DoublyLinkedList


def tim_kiem(danh_sach: DoublyLinkedList, tu_khoa: str, tieu_chi: str = 'ten'):
    """
    Tìm kiếm sản phẩm theo từ khóa + tiêu chí.

    Tham số:
        danh_sach : DSLK đôi toàn cục.
        tu_khoa   : chuỗi user nhập (đã strip).
        tieu_chi  : 'ten' | 'ma' | 'loai' — tìm theo tên / mã / loại hàng.

    Trả về:
        List[dict] — danh sách các sản phẩm khớp (mỗi sp là 1 dict).
        Trả về [] nếu không tìm thấy hoặc lỗi.
    """
    try:
        # Chuẩn hóa từ khóa (strip khoảng trắng 2 đầu).
        tu_khoa = tu_khoa.strip()
        # Nếu từ khóa rỗng → trả về toàn bộ danh sách (như không lọc).
        if not tu_khoa:
            return danh_sach.chuyen_thanh_danh_sach()

        # Phân nhánh theo tiêu chí.
        if tieu_chi == 'ma':
            # Tìm chính xác theo mã → trả về list có 0 hoặc 1 phần tử.
            sp = danh_sach.tim_theo_ma_so(tu_khoa)
            return [sp.chuyen_thanh_dict()] if sp else []

        elif tieu_chi == 'loai':
            # Tìm theo loại hàng (so khớp chứa, không phân biệt HOA/thường).
            kq = danh_sach.tim_theo_the_loai(tu_khoa)

        else:
            # Mặc định: tìm theo tên (so khớp chứa).
            kq = danh_sach.tim_kiem(tu_khoa)

        # Chuyển list đối tượng → list dict.
        return [sp.chuyen_thanh_dict() for sp in kq if hasattr(sp, 'chuyen_thanh_dict')]
    except Exception as loi:
        print(f'[LOI tim_kiem] {loi}')
        return []


def sap_xep(danh_sach: DoublyLinkedList, tieu_chi: str = 'gia_ban'):
    """
    Sắp xếp DSLK bằng Merge Sort (O(n log n)) + trả về list dict.

    Tham số:
        danh_sach : DSLK đôi toàn cục.
        tieu_chi  : 'gia_ban' | 'ten_san_pham' | 'ton_kho'.

    Trả về:
        List[dict] — danh sách đã sắp xếp.
        Trả về [] nếu lỗi.
    """
    try:
        # Gọi hàm sap_xep_tron của DSLK (đã tự cài đặt Merge Sort).
        danh_sach.sap_xep_tron(tieu_chi)
        # Trả về list dict để UI hiển thị.
        return danh_sach.chuyen_thanh_danh_sach()
    except Exception as loi:
        print(f'[LOI sap_xep] {loi}')
        return []
