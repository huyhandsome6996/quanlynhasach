"""
Tệp gio_hang_tt.py — THUẬT TOÁN cho Giỏ hàng (Queue FIFO) + Thanh toán
========================================================================

Bao gồm 4 hàm:
    1. them_vao_gio(danh_sach, gio_hang, ma_so)         — Enqueue 1 sản phẩm.
    2. xem_gio_hang(gio_hang)                            — Xem toàn bộ giỏ + tổng tiền.
    3. xoa_khoi_gio(gio_hang, ma_so)                     — Bỏ 1 món khỏi giỏ.
    4. thanh_toan(gio_hang)                              — Dequeue toàn bộ → trả hóa đơn.

Nguyên lý Queue FIFO:
    - them_vao_gio → them_vao (enqueue vào cuối).
    - thanh_toan  → lay_ra   (dequeue từ đầu → món vào trước thanh toán trước).
"""

# Import lớp HangDoi (type hint).
from loi_thuat_toan.cau_truc_du_lieu import HangDoi
# Import DoublyLinkedList (type hint).
from loi_thuat_toan.danh_sach_lien_ket import DoublyLinkedList


# ============================================================
# THÊM VÀO GIỎ (ENQUEUE)
# ============================================================
def them_vao_gio(danh_sach: DoublyLinkedList, gio_hang: HangDoi, ma_so: str):
    """
    Enqueue 1 sản phẩm vào giỏ hàng.

    Tham số:
        danh_sach : DSLK đôi toàn cục (để tìm sản phẩm theo mã).
        gio_hang  : HangDoi toàn cục.
        ma_so     : mã sản phẩm cần thêm.

    Trả về:
        (True,  thong_bao) nếu thêm thành công.
        (False, thong_bao_loi) nếu không tìm thấy sản phẩm hoặc lỗi.
    """
    try:
        # Tìm sản phẩm trong DSLK.
        sp = danh_sach.tim_theo_ma_so(ma_so)
        if sp is None:
            return False, f'Không tìm thấy sản phẩm mã {ma_so}.'

        # Tạo dict món hàng (chỉ lấy thông tin cần thiết để hiển thị + tính tiền).
        mon = {
            'ma_so':        sp.ma_so,
            'ten_san_pham': sp.ten_san_pham,
            'gia_ban':      sp.tinh_gia_ban(),   # Đa hình — giá bán theo loại.
            'loai_hang':    sp.loai_hang
        }
        # Enqueue vào cuối hàng đợi.
        gio_hang.them_vao(mon)
        return True, f'Đã thêm "{sp.ten_san_pham}" vào giỏ.'
    except Exception as loi:
        return False, f'Lỗi: {loi}'


# ============================================================
# XEM GIỎ HÀNG
# ============================================================
def xem_gio_hang(gio_hang: HangDoi):
    """
    Xem toàn bộ giỏ + tính tổng tiền.

    Tham số:
        gio_hang : HangDoi toàn cục.

    Trả về:
        (ds_mon, tong_tien, so_luong) — tuple 3 phần tử.
        Trả về ([], 0, 0) nếu lỗi.
    """
    try:
        # Lấy list dict các món trong giỏ (theo thứ tự FIFO).
        ds = gio_hang.xem_danh_sach()
        # Tính tổng tiền — cộng dồn giá_ban của từng món.
        tong = sum(mon.get('gia_ban', 0) for mon in ds)
        # Trả về tuple 3 phần tử.
        return ds, tong, gio_hang.so_luong
    except Exception as loi:
        print(f'[LOI xem_gio_hang] {loi}')
        return [], 0, 0


# ============================================================
# XÓA KHỎI GIỎ
# ============================================================
def xoa_khoi_gio(gio_hang: HangDoi, ma_so: str):
    """
    Xóa 1 món khỏi giỏ theo mã số (user đổi ý).

    Tham số:
        gio_hang : HangDoi toàn cục.
        ma_so    : mã món cần bỏ.

    Trả về:
        (True,  thong_bao)         nếu xóa được.
        (False, thong_bao_loi)     nếu không có mã trong giỏ.
    """
    try:
        # Gọi hàm xoa_theo_ma của HangDoi (tự cài đặt — duyệt tìm + bỏ qua Node).
        if gio_hang.xoa_theo_ma(ma_so):
            return True, f'Đã xóa "{ma_so}" khỏi giỏ.'
        return False, f'Không có "{ma_so}" trong giỏ.'
    except Exception as loi:
        return False, f'Lỗi: {loi}'


# ============================================================
# THANH TOÁN (DEQUEUE ALL)
# ============================================================
def thanh_toan(gio_hang: HangDoi):
    """
    Dequeue toàn bộ giỏ → trả hóa đơn chi tiết.

    Tham số:
        gio_hang : HangDoi toàn cục.

    Trả về:
        (True,  thong_bao, hoa_don)  nếu thanh toán thành công.
        (False, thong_bao, None)     nếu giỏ rỗng hoặc lỗi.

        hoa_don là dict: {'cac_mon': list, 'tong_tien': float, 'so_mon': int}.
    """
    try:
        # Nếu giỏ rỗng → không thanh toán được.
        if gio_hang.rong():
            return False, 'Giỏ hàng trống.', None

        # Dequeue toàn bộ — lấy từng món từ đầu hàng đến khi rỗng.
        cac_mon = []
        tong = 0
        while not gio_hang.rong():
            mon = gio_hang.lay_ra()   # Dequeue từ đầu (FIFO — món vào trước ra trước).
            cac_mon.append(mon)
            tong += mon.get('gia_ban', 0)

        # Gói hóa đơn.
        hoa_don = {
            'cac_mon':   cac_mon,
            'tong_tien': tong,
            'so_mon':    len(cac_mon)
        }
        return True, f'Đã thanh toán {len(cac_mon)} món, tổng {tong:,.0f}đ.', hoa_don
    except Exception as loi:
        return False, f'Lỗi: {loi}', None
