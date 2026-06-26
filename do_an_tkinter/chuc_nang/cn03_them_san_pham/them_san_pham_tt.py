"""
Tệp them_san_pham_tt.py — THUẬT TOÁN cho chức năng Thêm sản phẩm
=================================================================

Chứa hàm thêm 1 sản phẩm mới vào DSLK + SQLite + ghi lịch sử Undo.
Hỗ trợ 5 loại (Sách, Tạp chí, Báo giấy, Luận văn, Bản thảo) — OOP đa hình.
"""

# Import 5 lớp con OOP để tạo đối tượng theo loại.
from loi_thuat_toan.lop_doi_tuong import Sach, TapChi, BaoGiay, LuanVan, BanThao
# Import hàm lưu sản phẩm vào SQLite.
from loi_thuat_toan.ket_noi_sqlite import luu_mot_san_pham
# Import lớp DoublyLinkedList (chỉ để type hint).
from loi_thuat_toan.danh_sach_lien_ket import DoublyLinkedList
# Import lớp NganXep (Stack) cho Undo/Redo.
from loi_thuat_toan.cau_truc_du_lieu import NganXep


def them_san_pham(danh_sach: DoublyLinkedList, bo_undoredo: dict, du_lieu: dict):
    """
    Thêm 1 sản phẩm mới.

    Tham số:
        danh_sach    : DSLK đôi chứa toàn bộ sản phẩm.
        bo_undoredo  : dict có 2 key 'undo' và 'redo' (mỗi key là 1 NganXep).
        du_lieu      : dict chứa thông tin sản phẩm user nhập từ form.

    Trả về:
        (True,  thong_bao) nếu thêm thành công.
        (False, thong_bao_loi) nếu validate lỗi hoặc exception.
    """
    try:
        # Lấy + làm sạch các trường chung.
        loai_hang = du_lieu.get('loai_hang', '').strip()
        ma_so     = du_lieu.get('ma_so', '').strip()
        ten       = du_lieu.get('ten_san_pham', '').strip()
        gia       = float(du_lieu.get('gia_co_ban', 0))   # Ép kiểu float.
        ton       = int(du_lieu.get('ton_kho', 0))        # Ép kiểu int.

        # Validate cơ bản: không được để trống mã/tên/loại.
        if not ma_so or not ten or not loai_hang:
            return False, 'Vui lòng điền đầy đủ mã, tên, loại.'
        # Validate giá/tồn phải >= 0.
        if gia < 0 or ton < 0:
            return False, 'Giá / tồn kho không được âm.'
        # Validate mã không được trùng.
        if danh_sach.tim_theo_ma_so(ma_so) is not None:
            return False, f'Mã "{ma_so}" đã tồn tại.'

        # Tạo đối tượng theo loại — OOP đa hình (mỗi lớp con có hàm tinh_gia_ban riêng).
        if loai_hang == 'Sách':
            sp = Sach(ma_so, ten, gia, ton,
                      du_lieu.get('tac_gia', '').strip(),
                      du_lieu.get('nha_xuat_ban', '').strip())
        elif loai_hang == 'Tạp chí':
            sp = TapChi(ma_so, ten, gia, ton,
                        du_lieu.get('so_phat_hanh', '').strip())
        elif loai_hang == 'Báo giấy':
            sp = BaoGiay(ma_so, ten, gia, ton,
                         du_lieu.get('ngay_xuat_ban', '').strip())
        elif loai_hang == 'Luận văn':
            sp = LuanVan(ma_so, ten, gia, ton,
                         du_lieu.get('tac_gia', '').strip(),
                         du_lieu.get('truong_dai_hoc', '').strip(), '')
        elif loai_hang == 'Bản thảo':
            sp = BanThao(ma_so, ten, gia, ton,
                         du_lieu.get('tac_gia', '').strip(),
                         du_lieu.get('trang_thai', 'Chưa duyệt').strip())
        else:
            # Loại không nằm trong 5 loại cho phép.
            return False, 'Loại hàng không hợp lệ.'

        # Lưu vào DSLK (RAM) + SQLite (ổ cứng).
        danh_sach.them_vao_cuoi(sp)
        luu_mot_san_pham(sp)

        # Ghi vào Stack Undo: thao tác 'them' + dữ liệu mới (để undo sẽ xóa).
        bo_undoredo['undo'].day_vao({
            'loai': 'them',
            'du_lieu_cu': None,
            'du_lieu_moi': sp.chuyen_thanh_dict()
        })
        # Xóa Redo vì có thao tác mới → không thể redo thao tác cũ.
        bo_undoredo['redo'].xoa_tat_ca()

        return True, f'Đã thêm "{ten}" vào cửa hàng.'
    except ValueError:
        # Lỗi khi ép kiểu số — vd: user nhập "abc" vào ô giá.
        return False, 'Giá / tồn kho phải là số.'
    except Exception as loi:
        # Bất kỳ lỗi nào khác.
        return False, f'Lỗi: {loi}'
