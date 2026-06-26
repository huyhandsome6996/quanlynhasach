"""
Tệp hoan_tac_lam_lai_tt.py — THUẬT TOÁN cho Undo/Redo (Stack LIFO)
====================================================================

Bao gồm 3 hàm:
    1. hoan_tac(danh_sach, bo_undoredo)  — UNDO: hoàn tác thao tác gần nhất.
    2. lam_lai(danh_sach, bo_undoredo)   — REDO: làm lại thao tác vừa undo.
    3. trang_thai(bo_undoredo)            — trả về dict trạng thái (cho UI bật/tắt nút).

Nguyên lý Stack LIFO:
    - Undo: LẤY RA (pop) thao tác trên đỉnh Undo Stack → đảo ngược tác động → đẩy sang Redo Stack.
    - Redo: LẤY RA (pop) thao tác trên đỉnh Redo Stack → áp dụng lại → đẩy sang Undo Stack.

Mỗi thao tác có dạng dict: {'loai': 'them'|'sua'|'xoa', 'du_lieu_cu': dict, 'du_lieu_moi': dict}.
"""

# Import các hàm SQLite để ghi/xóa khi undo/redo.
from loi_thuat_toan.ket_noi_sqlite import luu_mot_san_pham, cap_nhat_san_pham, xoa_mot_san_pham
# Import 5 lớp OOP để tái tạo đối tượng từ dict (dùng khi Undo thao tác xóa).
from loi_thuat_toan.lop_doi_tuong import Sach, TapChi, BaoGiay, LuanVan, BanThao
# Import DoublyLinkedList (type hint).
from loi_thuat_toan.danh_sach_lien_ket import DoublyLinkedList


# ============================================================
# HÀM TIỆN ÍCH NỘI BỘ — TÁI TẠO ĐỐI TƯỢNG TỪ DICT
# ============================================================
def _tao_doi_tuong_tu_dict(d):
    """
    Tái tạo đối tượng MatHang từ dict (dùng cho Undo thao tác xóa).

    Tham số:
        d : dict chứa các trường của sản phẩm.

    Trả về:
        Đối tượng Sach/TapChi/BaoGiay/LuanVan/BanThao tương ứng, hoặc None nếu lỗi.
    """
    try:
        loai = d.get('loai_hang')
        # Phân nhánh theo loại — dùng đa hình OOP.
        if loai == 'Sách':
            return Sach(d['ma_so'], d['ten_san_pham'], d['gia_co_ban'],
                        d['ton_kho'], d.get('tac_gia', ''), d.get('nha_xuat_ban', ''))
        elif loai == 'Tạp chí':
            return TapChi(d['ma_so'], d['ten_san_pham'], d['gia_co_ban'],
                          d['ton_kho'], d.get('so_phat_hanh', ''))
        elif loai == 'Báo giấy':
            return BaoGiay(d['ma_so'], d['ten_san_pham'], d['gia_co_ban'],
                           d['ton_kho'], d.get('ngay_xuat_ban', ''))
        elif loai == 'Luận văn':
            return LuanVan(d['ma_so'], d['ten_san_pham'], d['gia_co_ban'],
                           d['ton_kho'], d.get('tac_gia', ''),
                           d.get('truong_dai_hoc', ''), '')
        elif loai == 'Bản thảo':
            return BanThao(d['ma_so'], d['ten_san_pham'], d['gia_co_ban'],
                           d['ton_kho'], d.get('tac_gia', ''),
                           d.get('tinh_trang', ''))
    except Exception as loi:
        print(f'[LOI tao doi tuong] {loi}')
    return None


# ============================================================
# HÀM UNDO — HOÀN TÁC THAO TÁC GẦN NHẤT
# ============================================================
def hoan_tac(danh_sach: DoublyLinkedList, bo_undoredo: dict):
    """
    Undo — hoàn tác thao tác gần nhất.

    Tham số:
        danh_sach   : DSLK đôi toàn cục.
        bo_undoredo : dict 2 Stack undo/redo.

    Trả về:
        (True,  thong_bao) nếu undo thành công.
        (False, thong_bao) nếu không có thao tác để undo hoặc lỗi.
    """
    try:
        # Lấy thao tác trên đỉnh Undo Stack (pop).
        thao_tac = bo_undoredo['undo'].lay_ra()
        if thao_tac is None:
            return False, 'Không có thao tác để hoàn tác.'

        # Đẩy sang Redo Stack (để có thể redo sau).
        bo_undoredo['redo'].day_vao(thao_tac)

        # Phân nhánh theo loại thao tác để đảo ngược tác động.
        loai = thao_tac['loai']

        if loai == 'them':
            # Undo THÊM → XÓA sản phẩm vừa thêm.
            ma = thao_tac['du_lieu_moi']['ma_so']
            danh_sach.xoa_node(ma)
            xoa_mot_san_pham(ma)
            return True, f'Đã hoàn tác: xóa "{thao_tac["du_lieu_moi"]["ten_san_pham"]}".'

        elif loai == 'xoa':
            # Undo XÓA → THÊM LẠI sản phẩm đã xóa.
            cu = thao_tac['du_lieu_cu']
            sp = _tao_doi_tuong_tu_dict(cu)
            if sp:
                danh_sach.them_vao_cuoi(sp)
                luu_mot_san_pham(sp)
            return True, f'Đã hoàn tác: thêm lại "{cu["ten_san_pham"]}".'

        elif loai == 'sua':
            # Undo SỬA → đặt lại dữ liệu cũ.
            cu = thao_tac['du_lieu_cu']
            ma = cu['ma_so']
            # Dict dữ liệu cần khôi phục.
            dl = {
                'ten_san_pham': cu['ten_san_pham'],
                'gia_co_ban':   cu['gia_co_ban'],
                'ton_kho':      cu['ton_kho']
            }
            # Thêm các trường riêng nếu có.
            for k in ['tac_gia', 'nha_xuat_ban', 'so_phat_hanh',
                      'ngay_xuat_ban', 'truong_dai_hoc', 'tinh_trang']:
                if k in cu:
                    dl[k] = cu[k]
            sp = danh_sach.tim_theo_ma_so(ma)
            if sp:
                danh_sach.cap_nhat_node(ma, dl)
                cap_nhat_san_pham(sp)
            return True, f'Đã hoàn tác: khôi phục "{cu["ten_san_pham"]}".'

        return False, 'Thao tác không xác định.'
    except Exception as loi:
        return False, f'Lỗi: {loi}'


# ============================================================
# HÀM REDO — LÀM LẠI THAO TÁC VỪA UNDO
# ============================================================
def lam_lai(danh_sach: DoublyLinkedList, bo_undoredo: dict):
    """
    Redo — làm lại thao tác đã undo.

    Tham số:
        danh_sach   : DSLK đôi toàn cục.
        bo_undoredo : dict 2 Stack undo/redo.

    Trả về:
        (True,  thong_bao) nếu redo thành công.
        (False, thong_bao) nếu không có thao tác để redo hoặc lỗi.
    """
    try:
        # Lấy thao tác trên đỉnh Redo Stack (pop).
        thao_tac = bo_undoredo['redo'].lay_ra()
        if thao_tac is None:
            return False, 'Không có thao tác để làm lại.'

        # Đẩy lại sang Undo Stack.
        bo_undoredo['undo'].day_vao(thao_tac)

        # Phân nhánh theo loại thao tác để áp dụng lại.
        loai = thao_tac['loai']

        if loai == 'them':
            # Redo THÊM → THÊM LẠI sản phẩm.
            moi = thao_tac['du_lieu_moi']
            sp = _tao_doi_tuong_tu_dict(moi)
            if sp:
                danh_sach.them_vao_cuoi(sp)
                luu_mot_san_pham(sp)
            return True, f'Đã làm lại: thêm "{moi["ten_san_pham"]}".'

        elif loai == 'xoa':
            # Redo XÓA → XÓA LẠI sản phẩm.
            ma = thao_tac['du_lieu_cu']['ma_so']
            danh_sach.xoa_node(ma)
            xoa_mot_san_pham(ma)
            return True, f'Đã làm lại: xóa "{thao_tac["du_lieu_cu"]["ten_san_pham"]}".'

        elif loai == 'sua':
            # Redo SỬA → áp dụng lại dữ liệu mới.
            moi = thao_tac['du_lieu_moi']
            ma = moi['ma_so']
            dl = {
                'ten_san_pham': moi['ten_san_pham'],
                'gia_co_ban':   moi['gia_co_ban'],
                'ton_kho':      moi['ton_kho']
            }
            for k in ['tac_gia', 'nha_xuat_ban', 'so_phat_hanh',
                      'ngay_xuat_ban', 'truong_dai_hoc', 'tinh_trang']:
                if k in moi:
                    dl[k] = moi[k]
            sp = danh_sach.tim_theo_ma_so(ma)
            if sp:
                danh_sach.cap_nhat_node(ma, dl)
                cap_nhat_san_pham(sp)
            return True, f'Đã làm lại: cập nhật "{moi["ten_san_pham"]}".'

        return False, 'Thao tác không xác định.'
    except Exception as loi:
        return False, f'Lỗi: {loi}'


# ============================================================
# HÀM TRẠNG THÁI — CHO UI BẬT/TẮT NÚT
# ============================================================
def trang_thai(bo_undoredo: dict):
    """
    Trả về dict trạng thái Undo/Redo để UI bật/tắt nút.

    Trả về:
        {
            'co_the_undo': True/False,
            'co_the_redo': True/False,
            'so_undo':     int,
            'so_redo':     int,
        }
    """
    return {
        'co_the_undo': not bo_undoredo['undo'].rong(),
        'co_the_redo': not bo_undoredo['redo'].rong(),
        'so_undo':     bo_undoredo['undo'].so_luong,
        'so_redo':     bo_undoredo['redo'].so_luong,
    }
