"""
Tệp sua_san_pham_tt.py — THUẬT TOÁN cho chức năng Sửa sản phẩm
================================================================

Chứa hàm cập nhật 1 sản phẩm theo mã số trong DSLK + SQLite + ghi Undo.
"""

# Import hàm cập nhật SQLite.
from loi_thuat_toan.ket_noi_sqlite import cap_nhat_san_pham
# Import DoublyLinkedList (type hint).
from loi_thuat_toan.danh_sach_lien_ket import DoublyLinkedList


def sua_san_pham(danh_sach: DoublyLinkedList, bo_undoredo: dict, du_lieu: dict):
    """
    Cập nhật sản phẩm theo mã số.

    Tham số:
        danh_sach   : DSLK đôi toàn cục.
        bo_undoredo : dict 2 Stack undo/redo.
        du_lieu     : dict chứa mã số + các trường cần cập nhật.

    Trả về:
        (True,  thong_bao) nếu sửa thành công.
        (False, thong_bao_loi) nếu lỗi.
    """
    try:
        # Lấy mã số sản phẩm cần sửa.
        ma_so = du_lieu.get('ma_so', '').strip()
        if not ma_so:
            return False, 'Mã số không được trống.'

        # Tìm sản phẩm cần sửa trong DSLK.
        sp_cu = danh_sach.tim_theo_ma_so(ma_so)
        if sp_cu is None:
            return False, f'Không tìm thấy sản phẩm mã {ma_so}.'

        # Lưu lại dữ liệu cũ (để Undo khôi phục).
        du_lieu_cu = sp_cu.chuyen_thanh_dict()

        # Tạo dict dữ liệu mới — chỉ cập nhật các trường chung + trường riêng theo loại.
        du_lieu_moi = {
            'ten_san_pham': du_lieu.get('ten_san_pham', '').strip(),
            'gia_co_ban':   float(du_lieu.get('gia_co_ban', 0)),
            'ton_kho':      int(du_lieu.get('ton_kho', 0)),
        }
        # Thêm trường riêng theo loại của sản phẩm.
        loai_hang = sp_cu.loai_hang
        if loai_hang == 'Sách':
            du_lieu_moi['tac_gia'] = du_lieu.get('tac_gia', '').strip()
            du_lieu_moi['nha_xuat_ban'] = du_lieu.get('nha_xuat_ban', '').strip()
        elif loai_hang == 'Tạp chí':
            du_lieu_moi['so_phat_hanh'] = du_lieu.get('so_phat_hanh', '').strip()
        elif loai_hang == 'Báo giấy':
            du_lieu_moi['ngay_xuat_ban'] = du_lieu.get('ngay_xuat_ban', '').strip()
        elif loai_hang == 'Luận văn':
            du_lieu_moi['tac_gia'] = du_lieu.get('tac_gia', '').strip()
            du_lieu_moi['truong_dai_hoc'] = du_lieu.get('truong_dai_hoc', '').strip()
        elif loai_hang == 'Bản thảo':
            du_lieu_moi['tac_gia'] = du_lieu.get('tac_gia', '').strip()
            du_lieu_moi['tinh_trang'] = du_lieu.get('trang_thai', '').strip()

        # Cập nhật DSLK (RAM) + SQLite (ổ cứng).
        danh_sach.cap_nhat_node(ma_so, du_lieu_moi)
        cap_nhat_san_pham(sp_cu)

        # Ghi Undo: thao tác 'sua' + dữ liệu cũ + dữ liệu mới.
        bo_undoredo['undo'].day_vao({
            'loai': 'sua',
            'du_lieu_cu': du_lieu_cu,
            'du_lieu_moi': sp_cu.chuyen_thanh_dict()
        })
        # Xóa Redo.
        bo_undoredo['redo'].xoa_tat_ca()

        return True, f'Đã cập nhật "{du_lieu_moi["ten_san_pham"]}".'
    except ValueError:
        # Lỗi ép kiểu số.
        return False, 'Giá / tồn kho phải là số.'
    except Exception as loi:
        return False, f'Lỗi: {loi}'
