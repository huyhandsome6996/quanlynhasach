"""
Tệp cua_so_chinh_dk.py — ĐIỀU KHIỂN cho Cửa sổ chính
======================================================

Lớp DieuKhienCuaSoChinh — ghép tất cả các Điều khiển chức năng con
(01_dang_nhap → 09_gio_hang) vào UI cửa sổ chính (CuaSoChinhUI).

Trách nhiệm:
    1. Tạo các đối tượng Điều khiển con (DieuKhienThemSanPham, ...).
    2. Gắn command cho các nút trên UI cửa sổ chính.
    3. Cung cấp hàm refresh_all() để nạp lại toàn bộ UI sau khi có thay đổi.
    4. Xử lý đăng xuất (ẩn cửa sổ chính → mở lại form đăng nhập → cập nhật user).
"""

from tkinter import messagebox

# Import UI cửa sổ chính.
from .cua_so_chinh_ui import CuaSoChinhUI
# Import UI đăng nhập (để mở lại khi đăng xuất).
from chuc_nang.cn01_dang_nhap_phan_quyen.dang_nhap_ui import CuaSoDangNhapUI
# Import các Điều khiển chức năng con.
from chuc_nang.cn02_doc_danh_sach.doc_danh_sach_dk import DieuKhienDocDanhSach
from chuc_nang.cn03_them_san_pham.them_san_pham_dk import DieuKhienThemSanPham
from chuc_nang.cn04_sua_san_pham.sua_san_pham_dk import DieuKhienSuaSanPham
from chuc_nang.cn05_xoa_san_pham.xoa_san_pham_dk import DieuKhienXoaSanPham
from chuc_nang.cn06_tim_kiem_sap_xep.tim_kiem_sap_xep_dk import DieuKhienTimKiemSapXep
from chuc_nang.cn07_thong_ke.thong_ke_dk import DieuKhienThongKe
from chuc_nang.cn08_hoan_tac_lam_lai.hoan_tac_lam_lai_dk import DieuKhienHoanTacLamLai
from chuc_nang.cn09_gio_hang.gio_hang_dk import DieuKhienGioHang


class DieuKhienCuaSoChinh:
    """Lớp điều khiển cửa sổ chính — ghép tất cả chức năng lại."""

    def __init__(self, root, quan_ly, nguoi_dung):
        """
        Khởi tạo + vẽ UI + gắn sự kiện.

        Tham số:
            root       : Tk root.
            quan_ly    : QuanLyTrungTam đã khởi tạo.
            nguoi_dung : NguoiDung vừa đăng nhập.
        """
        self.root = root
        self.quan_ly = quan_ly
        self.nguoi_dung = nguoi_dung

        # Tạo UI cửa sổ chính.
        self.ui = CuaSoChinhUI(root, nguoi_dung.ho_ten, nguoi_dung.vai_tro)
        # Cập nhật label user.
        self.ui.cap_nhat_user(nguoi_dung.ho_ten, nguoi_dung.vai_tro)

        # Nếu là nhân viên → ẩn nút Xóa (vì không được phép xóa).
        if nguoi_dung.vai_tro != 'admin':
            self.ui.btn_xoa.config(state='disabled')

        # Tạo các Điều khiển con — truyền UI + state từ QuanLyTrungTam.
        self.dk_danh_sach = DieuKhienDocDanhSach(
            self.ui.ui_bang, quan_ly.danh_sach)
        self.dk_them = DieuKhienThemSanPham(
            quan_ly.danh_sach, quan_ly.bo_undoredo)
        self.dk_sua = DieuKhienSuaSanPham(
            quan_ly.danh_sach, quan_ly.bo_undoredo)
        self.dk_xoa = DieuKhienXoaSanPham(
            quan_ly.danh_sach, quan_ly.bo_undoredo)
        self.dk_tim_sx = DieuKhienTimKiemSapXep(
            self.ui.ui_tim_sx, quan_ly.danh_sach, self.ui.ui_bang)
        self.dk_thong_ke = DieuKhienThongKe(
            self.ui.ui_thong_ke, quan_ly.danh_sach)
        self.dk_undoredo = DieuKhienHoanTacLamLai(
            self.ui.ui_undoredo, quan_ly.danh_sach, quan_ly.bo_undoredo)
        self.dk_gio_hang = DieuKhienGioHang(
            self.ui.ui_gio_hang, quan_ly.danh_sach, quan_ly.gio_hang)

        # Gắn command cho các nút.
        self._gan_su_kien()

        # Nạp dữ liệu ban đầu lên UI.
        self.refresh_all()

    # ========================================================
    # GẮN SỰ KIỆN CHO CÁC NÚT
    # ========================================================
    def _gan_su_kien(self):
        """Gắn command cho các nút trên UI cửa sổ chính."""
        # Nút Đăng xuất.
        self.ui.btn_dang_xuat.config(command=self._dang_xuat)

        # Nút Thêm/Sửa/Xóa.
        self.ui.btn_them.config(command=self._them_san_pham)
        self.ui.btn_sua.config(command=self._sua_san_pham)
        self.ui.btn_xoa.config(command=self._xoa_san_pham)

        # Double-click vào dòng bảng → Sửa.
        self.ui.bind_double_click_bang(self._sua_san_pham)

        # Thanh Tìm/Sắp xếp — gọi gan_su_kien của dk con.
        self.dk_tim_sx.gan_su_kien()
        # Thanh Undo/Redo — gọi gan_su_kien + truyền 2 callback để sau undo/redo
        # sẽ nạp lại bảng + thống kê.
        self.dk_undoredo.gan_su_kien(
            cap_nhat_bang=lambda: self.dk_danh_sach.nap_lai(),
            cap_nhat_thong_ke=self.dk_thong_ke.cap_nhat
        )
        # Giỏ hàng — gọi gan_su_kien + truyền callback lấy mã đang chọn trong bảng chính.
        self.dk_gio_hang.gan_su_kien(
            lay_ma_dang_chon_bang_chinh=self.ui.ui_bang.lay_ma_dang_chon
        )

    # ========================================================
    # REFRESH TOÀN BỘ UI
    # ========================================================
    def refresh_all(self):
        """Nạp lại toàn bộ UI: bảng + thống kê + giỏ + nút Undo/Redo."""
        so_luong = self.dk_danh_sach.nap_lai()
        self.dk_thong_ke.cap_nhat()
        self.dk_gio_hang.cap_nhat_gio_hang()
        self.dk_undoredo.cap_nhat_trang_thai()
        self.ui.dat_trang_thai(f'Đã tải {so_luong} mặt hàng.')

    # ========================================================
    # XỬ LÝ THÊM SẢN PHẨM
    # ========================================================
    def _them_san_pham(self):
        """Mở form Thêm → nếu lưu thành công → refresh_all."""
        da_them = self.dk_them.mo_form_them(self.root)
        if da_them:
            self.refresh_all()

    # ========================================================
    # XỬ LÝ SỬA SẢN PHẨM
    # ========================================================
    def _sua_san_pham(self):
        """Lấy mã đang chọn → mở form Sửa → nếu lưu → refresh_all."""
        ma = self.ui.ui_bang.lay_ma_dang_chon()
        if not ma:
            messagebox.showwarning('Chưa chọn', 'Vui lòng chọn 1 dòng để sửa.')
            return
        da_sua = self.dk_sua.mo_form_sua(self.root, ma)
        if da_sua:
            self.refresh_all()

    # ========================================================
    # XỬ LÝ XÓA SẢN PHẨM
    # ========================================================
    def _xoa_san_pham(self):
        """Lấy mã đang chọn → gọi điều khiển xóa → nếu xóa OK → refresh_all."""
        ma = self.ui.ui_bang.lay_ma_dang_chon()
        if not ma:
            messagebox.showwarning('Chưa chọn', 'Vui lòng chọn 1 dòng để xóa.')
            return
        da_xoa = self.dk_xoa.xu_ly_xoa(self.root, ma, self.quan_ly.la_admin())
        if da_xoa:
            self.refresh_all()

    # ========================================================
    # ĐĂNG XUẤT
    # ========================================================
    def _dang_xuat(self):
        """
        Đăng xuất → ẩn cửa sổ chính → mở lại form đăng nhập →
        nếu login OK → cập nhật user + hiện lại cửa sổ chính.
        Nếu user đóng form → thoát app.
        """
        # Hỏi xác nhận.
        if not messagebox.askyesno('Xác nhận', 'Bạn có chắc muốn đăng xuất?'):
            return

        # Reset user hiện tại.
        self.quan_ly.dang_xuat()

        # Ẩn cửa sổ chính.
        self.root.withdraw()

        # Mở form đăng nhập modal.
        form = CuaSoDangNhapUI(self.root)
        # Gắn phím Enter + nút Đăng nhập → kiểm tra login.
        from chuc_nang.cn01_dang_nhap_phan_quyen.dang_nhap_tt import BoDangNhap
        bo = BoDangNhap()
        # Dùng inline function để xử lý login (tương tự dang_nhap_dk.py).
        def _xu_ly_dang_nhap():
            ten = form.lay_ten_dang_nhap()
            mk = form.lay_mat_khau()
            if not ten or not mk:
                form.bao_loi('Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.')
                return
            ok, ket_qua = bo.dang_nhap(ten, mk)
            if ok:
                form.nguoi_dung = ket_qua
                form.dong()
            else:
                form.bao_loi(ket_qua)
                form.xoa_mat_khau()

        form.entry_mk.bind('<Return>', lambda e: _xu_ly_dang_nhap())
        form.btn_dn.config(command=_xu_ly_dang_nhap)
        self.root.wait_window(form.top)

        # Nếu login OK → cập nhật user + hiện lại cửa sổ chính.
        if form.nguoi_dung:
            self.nguoi_dung = form.nguoi_dung
            # Cập nhật QuanLyTrungTam để các hàm check quyền biết user mới.
            self.quan_ly.nguoi_dung_hien_tai = form.nguoi_dung
            # Cập nhật UI.
            self.ui.cap_nhat_user(form.nguoi_dung.ho_ten, form.nguoi_dung.vai_tro)
            # Bật/tắt nút Xóa theo quyền.
            if form.nguoi_dung.vai_tro == 'admin':
                self.ui.btn_xoa.config(state='normal')
            else:
                self.ui.btn_xoa.config(state='disabled')
            # Hiện lại cửa sổ chính.
            self.root.deiconify()
            # Nạp lại dữ liệu.
            self.refresh_all()
        else:
            # User đóng form đăng nhập → thoát app.
            self.root.quit()
