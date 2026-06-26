"""
Tệp gio_hang_dk.py — ĐIỀU KHIỂN cho Giỏ hàng + Thanh toán
============================================================

Cầu nối giữa UI (KhungGioHangUI) và Thuật toán (them_vao_gio, xem_gio_hang,
xoa_khoi_gio, thanh_toan).
Điều khiển luồng:
    - Nút "+ Thêm vào giỏ" → gọi them_vao_gio với mã đang chọn trong bảng chính.
    - Nút "- Bỏ khỏi giỏ"  → gọi xoa_khoi_gio với mã đang chọn trong giỏ.
    - Nút "💰 Thanh toán"  → gọi thanh_toan → hiện hộp thoại hóa đơn.
"""

# Import thuật toán giỏ hàng.
from .gio_hang_tt import them_vao_gio, xem_gio_hang, xoa_khoi_gio, thanh_toan
# Import messagebox để hiện hóa đơn.
from tkinter import messagebox


class DieuKhienGioHang:
    """Lớp điều khiển Giỏ hàng + Thanh toán."""

    def __init__(self, ui_gio, danh_sach, gio_hang):
        """
        Khởi tạo điều khiển.

        Tham số:
            ui_gio    : đối tượng KhungGioHangUI.
            danh_sach : DSLK đôi toàn cục (để tìm sp khi enqueue).
            gio_hang  : HangDoi toàn cục.
        """
        self.ui = ui_gio
        self.danh_sach = danh_sach
        self.gio_hang = gio_hang

    # ----------------------------------------------------------------
    # GẮN SỰ KIỆN CHO CÁC NÚT
    # ----------------------------------------------------------------
    def gan_su_kien(self, lay_ma_dang_chon_bang_chinh):
        """
        Gắn command cho 3 nút + lưu callback để lấy mã đang chọn trong bảng chính.

        Tham số:
            lay_ma_dang_chon_bang_chinh : hàm callback trả về mã số đang chọn
                                          trong bảng sản phẩm (để thêm vào giỏ).
        """
        # Lưu callback.
        self._lay_ma_bang_chinh = lay_ma_dang_chon_bang_chinh
        # Gắn command.
        self.ui.btn_them.config(command=self.xu_ly_them_vao_gio)
        self.ui.btn_xoa.config(command=self.xu_ly_xoa_khoi_gio)
        self.ui.btn_thanh_toan.config(command=self.xu_ly_thanh_toan)

    # ----------------------------------------------------------------
    # XỬ LÝ THÊM VÀO GIỎ
    # ----------------------------------------------------------------
    def xu_ly_them_vao_gio(self):
        """Enqueue sản phẩm đang chọn trong bảng chính vào giỏ."""
        # Lấy mã đang chọn từ bảng chính (thông qua callback).
        ma = self._lay_ma_bang_chinh()
        if not ma:
            messagebox.showwarning('Chưa chọn', 'Vui lòng chọn 1 dòng trong bảng sản phẩm.')
            return
        # Gọi thuật toán.
        ok, msg = them_vao_gio(self.danh_sach, self.gio_hang, ma)
        if ok:
            self.cap_nhat_gio_hang()
        else:
            messagebox.showerror('Lỗi', msg)

    # ----------------------------------------------------------------
    # XỬ LÝ BỎ KHỎI GIỎ
    # ----------------------------------------------------------------
    def xu_ly_xoa_khoi_gio(self):
        """Xóa 1 món đang chọn trong bảng giỏ."""
        ma = self.ui.lay_ma_dang_chon()
        if not ma:
            messagebox.showwarning('Chưa chọn', 'Vui lòng chọn món cần bỏ trong giỏ.')
            return
        ok, msg = xoa_khoi_gio(self.gio_hang, ma)
        if ok:
            self.cap_nhat_gio_hang()
        else:
            messagebox.showerror('Lỗi', msg)

    # ----------------------------------------------------------------
    # XỬ LÝ THANH TOÁN
    # ----------------------------------------------------------------
    def xu_ly_thanh_toan(self):
        """Dequeue toàn bộ giỏ → hiện hóa đơn."""
        ok, msg, hoa_don = thanh_toan(self.gio_hang)
        if ok:
            # Tạo chuỗi chi tiết hóa đơn.
            chi_tiet = '\n'.join([f"  - {m['ten_san_pham']}: {m['gia_ban']:,.0f}đ"
                                   for m in hoa_don['cac_mon']])
            # Hiện hộp thoại hóa đơn.
            messagebox.showinfo(
                'Thanh toán thành công',
                f"{msg}\n\nChi tiết:\n{chi_tiet}\n\nTổng: {hoa_don['tong_tien']:,.0f}đ"
            )
            self.cap_nhat_gio_hang()
        else:
            messagebox.showwarning('Thông báo', msg)

    # ----------------------------------------------------------------
    # CẬP NHẬT LẠI BẢNG GIỎ + TỔNG TIỀN
    # ----------------------------------------------------------------
    def cap_nhat_gio_hang(self):
        """Vẽ lại bảng giỏ + cập nhật label tổng tiền."""
        # Lấy ds + tổng + số lượng từ thuật toán.
        ds, tong, so_luong = xem_gio_hang(self.gio_hang)
        # Xóa dòng cũ.
        self.ui.xoa_tat_ca_dong()
        # Thêm từng món vào bảng.
        for mon in ds:
            self.ui.them_dong(mon)
        # Cập nhật tổng.
        self.ui.cap_nhat_tong(tong, so_luong)
