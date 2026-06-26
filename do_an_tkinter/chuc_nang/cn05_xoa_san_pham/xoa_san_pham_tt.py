"""
Tệp xoa_san_pham_tt.py — THUẬT TOÁN cho chức năng Xóa sản phẩm
================================================================

Chứa hàm xóa 1 sản phẩm theo mã số. Yêu cầu PHÂN QUYỀN: chỉ admin được xóa.
Trả về lỗi cụ thể nếu user là nhân viên (bảo mật theo barem).

Luồng:
    1. Kiểm tra phân quyền — chỉ admin được xóa.
    2. Tìm sản phẩm trong DSLK.
    3. Lưu dict dữ liệu cũ (để Undo khôi phục).
    4. Xóa khỏi DSLK (RAM) + SQLite (ổ cứng).
    5. Đẩy thao tác 'xoa' lên Stack Undo, xóa Redo.
"""

# Import hàm xóa SQLite.
from loi_thuat_toan.ket_noi_sqlite import xoa_mot_san_pham
# Import DoublyLinkedList (type hint).
from loi_thuat_toan.danh_sach_lien_ket import DoublyLinkedList


def xoa_san_pham(danh_sach: DoublyLinkedList, bo_undoredo: dict, ma_so: str, la_admin: bool):
    """
    Xóa 1 sản phẩm theo mã số.

    Tham số:
        danh_sach   : DSLK đôi toàn cục.
        bo_undoredo : dict 2 Stack undo/redo.
        ma_so       : mã sản phẩm cần xóa.
        la_admin    : True nếu user hiện tại là admin (được phép xóa).

    Trả về:
        (True,  thong_bao)         nếu xóa thành công.
        (False, thong_bao_loi)     nếu không phải admin, không tìm thấy, hoặc lỗi.
    """
    try:
        # === BƯỚC 1: KIỂM TRA PHÂN QUYỀN ===
        # Chỉ admin mới được xóa. Nếu là nhân viên → trả về lỗi rõ ràng.
        if not la_admin:
            return False, 'BẠN LÀ NHÂN VIÊN - KHÔNG ĐƯỢC PHÉP XÓA SẢN PHẨM.'

        # === BƯỚC 2: TÌM SẢN PHẨM CẦN XÓA ===
        sp_cu = danh_sach.tim_theo_ma_so(ma_so)
        if sp_cu is None:
            return False, f'Không tìm thấy sản phẩm mã {ma_so}.'

        # === BƯỚC 3: LƯU DỮ LIỆU CŨ (để Undo có thể khôi phục lại) ===
        du_lieu_cu = sp_cu.chuyen_thanh_dict()

        # === BƯỚC 4: XÓA KHỎI DSLK + SQLITE ===
        if danh_sach.xoa_node(ma_so):
            # Đã xóa khỏi DSLK → xóa tiếp trong SQLite.
            xoa_mot_san_pham(ma_so)

            # === BƯỚC 5: GHI LỊCH SỬ UNDO ===
            # Đẩy thao tác 'xoa' lên đỉnh Stack Undo.
            bo_undoredo['undo'].day_vao({
                'loai': 'xoa',
                'du_lieu_cu': du_lieu_cu,
                'du_lieu_moi': None
            })
            # Xóa toàn bộ Redo vì có thao tác mới.
            bo_undoredo['redo'].xoa_tat_ca()

            return True, f'Đã xóa sản phẩm mã {ma_so}.'

        # Nếu xoa_node trả về False → không tìm thấy (đã xử lý ở Bước 2 nhưng
        # phòng hờ trường hợp concurrent).
        return False, 'Không tìm thấy sản phẩm.'
    except Exception as loi:
        # Bất kỳ lỗi nào khác → trả về tuple (False, thông báo lỗi).
        return False, f'Lỗi: {loi}'
