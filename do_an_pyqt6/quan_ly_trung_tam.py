"""
Tệp quản_ly_trung_tam.py — Lớp QuanLyTrungTam
================================================

Đóng vai trò như "bộ não" của ứng dụng Tkinter — thay thế vai trò của
file xu_ly_yeu_cau.py trong bản Django. Lớp này giữ các biến toàn cục
(DSLK đôi, Stack Undo/Redo, Queue giỏ hàng) và cung cấp các hàm xử lý
cho UI gọi.

Tất cả tính năng giống hệt bản Django:
    1) Đăng nhập / phân quyền (admin / nhân viên)
    2) Đọc danh sách
    3) Thêm / 4) Sửa / 5) Xóa sản phẩm (chỉ admin được xóa)
    6) Tìm kiếm + Sắp xếp (Merge Sort)
    7) Thống kê
    8) Undo / Redo (Stack LIFO)
    9) Giỏ hàng (Queue FIFO) + thanh toán

Mỗi thao tác đều bọc try/except để bắt lỗi.
"""

import os
from loi_thuat_toan.danh_sach_lien_ket import DoublyLinkedList
from loi_thuat_toan.cau_truc_du_lieu import NganXep, HangDoi
from loi_thuat_toan.ket_noi_sqlite import (
    tao_bang_neu_chua_co,
    tai_du_lieu,
    luu_mot_san_pham,
    cap_nhat_san_pham,
    xoa_mot_san_pham,
    tao_du_lieu_mau_neu_rong,
)
from loi_thuat_toan.nguoi_dung import (
    khoi_tao_nguoi_dung_mac_dinh,
    kiem_tra_dang_nhap,
    NguoiDung,
)
from loi_thuat_toan.lop_doi_tuong import Sach, TapChi, BaoGiay, LuanVan, BanThao


class QuanLyTrungTam:
    """
    Lớp singleton giữ trạng thái ứng dụng và cung cấp API cho UI.
    """

    def __init__(self):
        """Khởi tạo bộ quản lý: chưa có gì cho tới khi khoi_tao() được gọi."""
        # DSLK đôi chứa toàn bộ mặt hàng.
        self.danh_sach = None
        # Dict chứa 2 Stack: 'undo' và 'redo'.
        self.bo_undoredo = None
        # Queue giỏ hàng.
        self.gio_hang = None
        # Người dùng đang đăng nhập (None = chưa login).
        self.nguoi_dung_hien_tai = None

    # ========================================================
    # KHỞI TẠO HỆ THỐNG
    # ========================================================
    def khoi_tao(self):
        """Tạo DB + bảng + dữ liệu mẫu + nạp vào DSLK + tạo Stack/Queue."""
        try:
            # Tạo bảng SQLite nếu chưa có (chạy 1 lần đầu).
            tao_bang_neu_chua_co()
            # Nếu DB rỗng → chèn 5 sản phẩm mẫu để test.
            tao_du_lieu_mau_neu_rong()
            # Tạo 2 tài khoản mặc định: admin/admin123 + nhanvien/nv123.
            khoi_tao_nguoi_dung_mac_dinh()

            # Tạo DSLK đôi rỗng rồi tải dữ liệu từ SQLite vào.
            self.danh_sach = DoublyLinkedList()
            tai_du_lieu(self.danh_sach)

            # 2 Stack cho Undo/Redo.
            self.bo_undoredo = {
                'undo': NganXep(),
                'redo': NganXep()
            }
            # 1 Queue cho giỏ hàng.
            self.gio_hang = HangDoi()

            print(f'[KHOI TAO] Da nap {self.danh_sach.so_luong} mat hang.')
            return True
        except Exception as loi:
            print(f'[LOI KHOI TAO] {loi}')
            return False

    # ========================================================
    # NHÓM 1: ĐĂNG NHẬP / PHÂN QUYỀN
    # ========================================================
    def dang_nhap(self, ten_dang_nhap, mat_khau):
        """
        Kiểm tra đăng nhập. Trả về (True, nguoi_dung) nếu đúng,
        (False, thong_bao_loi) nếu sai.
        """
        try:
            nguoi_dung = kiem_tra_dang_nhap(ten_dang_nhap, mat_khau)
            if nguoi_dung is None:
                return False, 'Sai tên đăng nhập hoặc mật khẩu.'
            self.nguoi_dung_hien_tai = nguoi_dung
            return True, nguoi_dung
        except Exception as loi:
            return False, f'Lỗi: {loi}'

    def dang_xuat(self):
        """Đăng xuất — reset người dùng hiện tại."""
        self.nguoi_dung_hien_tai = None

    def la_admin(self):
        """Kiểm tra user hiện tại có phải admin không."""
        return (self.nguoi_dung_hien_tai is not None and
                self.nguoi_dung_hien_tai.vai_tro == 'admin')

    # ========================================================
    # NHÓM 2: ĐỌC DANH SÁCH
    # ========================================================
    def lay_danh_sach(self):
        """Trả về list dict toàn bộ sản phẩm."""
        try:
            return self.danh_sach.chuyen_thanh_danh_sach()
        except Exception as loi:
            print(f'[LOI] {loi}')
            return []

    # ========================================================
    # NHÓM 3: THÊM SẢN PHẨM
    # ========================================================
    def them_san_pham(self, du_lieu):
        """
        Thêm sản phẩm mới. du_lieu là dict chứa các trường.
        Trả về (True, thong_bao) hoặc (False, thong_bao_loi).
        """
        try:
            loai_hang = du_lieu.get('loai_hang', '').strip()
            ma_so = du_lieu.get('ma_so', '').strip()
            ten = du_lieu.get('ten_san_pham', '').strip()
            gia = float(du_lieu.get('gia_co_ban', 0))
            ton = int(du_lieu.get('ton_kho', 0))

            if not ma_so or not ten or not loai_hang:
                return False, 'Vui lòng điền đầy đủ mã, tên, loại.'
            if gia < 0 or ton < 0:
                return False, 'Giá / tồn kho không được âm.'
            if self.danh_sach.tim_theo_ma_so(ma_so) is not None:
                return False, f'Mã "{ma_so}" đã tồn tại.'

            # Tạo đối tượng theo loại (đa hình OOP).
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
                return False, 'Loại hàng không hợp lệ.'

            # Lưu DSLK + SQLite.
            self.danh_sach.them_vao_cuoi(sp)
            luu_mot_san_pham(sp)

            # Ghi Undo.
            self.bo_undoredo['undo'].day_vao({
                'loai': 'them',
                'du_lieu_cu': None,
                'du_lieu_moi': sp.chuyen_thanh_dict()
            })
            self.bo_undoredo['redo'].xoa_tat_ca()

            return True, f'Đã thêm "{ten}" vào cửa hàng.'
        except ValueError:
            return False, 'Giá / tồn kho phải là số.'
        except Exception as loi:
            return False, f'Lỗi: {loi}'

    # ========================================================
    # NHÓM 4: SỬA SẢN PHẨM
    # ========================================================
    def sua_san_pham(self, du_lieu):
        """Cập nhật sản phẩm theo mã."""
        try:
            ma_so = du_lieu.get('ma_so', '').strip()
            if not ma_so:
                return False, 'Mã số không được trống.'

            sp_cu = self.danh_sach.tim_theo_ma_so(ma_so)
            if sp_cu is None:
                return False, f'Không tìm thấy sản phẩm mã {ma_so}.'

            du_lieu_cu = sp_cu.chuyen_thanh_dict()
            du_lieu_moi = {
                'ten_san_pham': du_lieu.get('ten_san_pham', '').strip(),
                'gia_co_ban':   float(du_lieu.get('gia_co_ban', 0)),
                'ton_kho':      int(du_lieu.get('ton_kho', 0)),
            }
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

            self.danh_sach.cap_nhat_node(ma_so, du_lieu_moi)
            cap_nhat_san_pham(sp_cu)

            self.bo_undoredo['undo'].day_vao({
                'loai': 'sua',
                'du_lieu_cu': du_lieu_cu,
                'du_lieu_moi': sp_cu.chuyen_thanh_dict()
            })
            self.bo_undoredo['redo'].xoa_tat_ca()

            return True, f'Đã cập nhật "{du_lieu_moi["ten_san_pham"]}".'
        except ValueError:
            return False, 'Giá / tồn kho phải là số.'
        except Exception as loi:
            return False, f'Lỗi: {loi}'

    # ========================================================
    # NHÓM 5: XÓA SẢN PHẨM (CHỈ ADMIN)
    # ========================================================
    def xoa_san_pham(self, ma_so):
        """Xóa sản phẩm. Trả về (True, msg) hoặc (False, msg)."""
        try:
            # Kiểm tra phân quyền.
            if not self.la_admin():
                return False, 'BẠN LÀ NHÂN VIÊN - KHÔNG ĐƯỢC PHÉP XÓA SẢN PHẨM.'

            sp_cu = self.danh_sach.tim_theo_ma_so(ma_so)
            if sp_cu is None:
                return False, f'Không tìm thấy sản phẩm mã {ma_so}.'

            du_lieu_cu = sp_cu.chuyen_thanh_dict()
            if self.danh_sach.xoa_node(ma_so):
                xoa_mot_san_pham(ma_so)
                self.bo_undoredo['undo'].day_vao({
                    'loai': 'xoa',
                    'du_lieu_cu': du_lieu_cu,
                    'du_lieu_moi': None
                })
                self.bo_undoredo['redo'].xoa_tat_ca()
                return True, f'Đã xóa sản phẩm mã {ma_so}.'
            return False, 'Không tìm thấy sản phẩm.'
        except Exception as loi:
            return False, f'Lỗi: {loi}'

    # ========================================================
    # NHÓM 6: TÌM KIẾM + SẮP XẾP
    # ========================================================
    def tim_kiem(self, tu_khoa, tieu_chi='ten'):
        """Trả về list dict kết quả tìm."""
        try:
            tu_khoa = tu_khoa.strip()
            if tieu_chi == 'ma':
                sp = self.danh_sach.tim_theo_ma_so(tu_khoa)
                return [sp.chuyen_thanh_dict()] if sp else []
            elif tieu_chi == 'loai':
                kq = self.danh_sach.tim_theo_the_loai(tu_khoa)
            else:
                kq = self.danh_sach.tim_kiem(tu_khoa)
            return [sp.chuyen_thanh_dict() for sp in kq if hasattr(sp, 'chuyen_thanh_dict')]
        except Exception as loi:
            print(f'[LOI] {loi}')
            return []

    def sap_xep(self, tieu_chi='gia_ban'):
        """Sắp xếp DSLK bằng Merge Sort + trả về list dict."""
        try:
            self.danh_sach.sap_xep_tron(tieu_chi)
            return self.danh_sach.chuyen_thanh_danh_sach()
        except Exception as loi:
            print(f'[LOI] {loi}')
            return []

    # ========================================================
    # NHÓM 7: THỐNG KÊ
    # ========================================================
    def lay_thong_ke(self):
        """Trả về dict thống kê."""
        try:
            return self.danh_sach.thong_ke()
        except Exception as loi:
            print(f'[LOI] {loi}')
            return {}

    # ========================================================
    # NHÓM 8: UNDO / REDO
    # ========================================================
    def hoan_tac(self):
        """Undo — hoàn tác thao tác gần nhất."""
        try:
            thao_tac = self.bo_undoredo['undo'].lay_ra()
            if thao_tac is None:
                return False, 'Không có thao tác để hoàn tác.'
            self.bo_undoredo['redo'].day_vao(thao_tac)
            loai = thao_tac['loai']

            if loai == 'them':
                # Undo THÊM → XÓA.
                ma = thao_tac['du_lieu_moi']['ma_so']
                self.danh_sach.xoa_node(ma)
                xoa_mot_san_pham(ma)
                return True, f'Đã hoàn tác: xóa "{thao_tac["du_lieu_moi"]["ten_san_pham"]}".'

            elif loai == 'xoa':
                # Undo XÓA → THÊM LẠI.
                cu = thao_tac['du_lieu_cu']
                sp = self._tao_doi_tuong_tu_dict(cu)
                if sp:
                    self.danh_sach.them_vao_cuoi(sp)
                    luu_mot_san_pham(sp)
                return True, f'Đã hoàn tác: thêm lại "{cu["ten_san_pham"]}".'

            elif loai == 'sua':
                # Undo SỬA → đặt lại dữ liệu cũ.
                cu = thao_tac['du_lieu_cu']
                ma = cu['ma_so']
                dl = {
                    'ten_san_pham': cu['ten_san_pham'],
                    'gia_co_ban':   cu['gia_co_ban'],
                    'ton_kho':      cu['ton_kho']
                }
                for k in ['tac_gia', 'nha_xuat_ban', 'so_phat_hanh',
                          'ngay_xuat_ban', 'truong_dai_hoc', 'tinh_trang']:
                    if k in cu:
                        dl[k] = cu[k]
                sp = self.danh_sach.tim_theo_ma_so(ma)
                if sp:
                    self.danh_sach.cap_nhat_node(ma, dl)
                    cap_nhat_san_pham(sp)
                return True, f'Đã hoàn tác: khôi phục "{cu["ten_san_pham"]}".'

            return False, 'Thao tác không xác định.'
        except Exception as loi:
            return False, f'Lỗi: {loi}'

    def lam_lai(self):
        """Redo — làm lại thao tác đã undo."""
        try:
            thao_tac = self.bo_undoredo['redo'].lay_ra()
            if thao_tac is None:
                return False, 'Không có thao tác để làm lại.'
            self.bo_undoredo['undo'].day_vao(thao_tac)
            loai = thao_tac['loai']

            if loai == 'them':
                moi = thao_tac['du_lieu_moi']
                sp = self._tao_doi_tuong_tu_dict(moi)
                if sp:
                    self.danh_sach.them_vao_cuoi(sp)
                    luu_mot_san_pham(sp)
                return True, f'Đã làm lại: thêm "{moi["ten_san_pham"]}".'

            elif loai == 'xoa':
                ma = thao_tac['du_lieu_cu']['ma_so']
                self.danh_sach.xoa_node(ma)
                xoa_mot_san_pham(ma)
                return True, f'Đã làm lại: xóa "{thao_tac["du_lieu_cu"]["ten_san_pham"]}".'

            elif loai == 'sua':
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
                sp = self.danh_sach.tim_theo_ma_so(ma)
                if sp:
                    self.danh_sach.cap_nhat_node(ma, dl)
                    cap_nhat_san_pham(sp)
                return True, f'Đã làm lại: cập nhật "{moi["ten_san_pham"]}".'

            return False, 'Thao tác không xác định.'
        except Exception as loi:
            return False, f'Lỗi: {loi}'

    def trang_thai_undoredo(self):
        """Trả về dict trạng thái undo/redo (cho UI bật/tắt nút)."""
        return {
            'co_the_undo': not self.bo_undoredo['undo'].rong(),
            'co_the_redo': not self.bo_undoredo['redo'].rong(),
            'so_undo':     self.bo_undoredo['undo'].so_luong,
            'so_redo':     self.bo_undoredo['redo'].so_luong,
        }

    # ========================================================
    # NHÓM 9: GIỎ HÀNG (QUEUE FIFO)
    # ========================================================
    def them_vao_gio(self, ma_so):
        """Enqueue sản phẩm vào giỏ."""
        try:
            sp = self.danh_sach.tim_theo_ma_so(ma_so)
            if sp is None:
                return False, f'Không tìm thấy sản phẩm mã {ma_so}.'
            mon = {
                'ma_so':        sp.ma_so,
                'ten_san_pham': sp.ten_san_pham,
                'gia_ban':      sp.tinh_gia_ban(),
                'loai_hang':    sp.loai_hang
            }
            self.gio_hang.them_vao(mon)
            return True, f'Đã thêm "{sp.ten_san_pham}" vào giỏ.'
        except Exception as loi:
            return False, f'Lỗi: {loi}'

    def xem_gio_hang(self):
        """Trả về list dict món trong giỏ + tổng tiền."""
        try:
            ds = self.gio_hang.xem_danh_sach()
            tong = sum(mon.get('gia_ban', 0) for mon in ds)
            return ds, tong, self.gio_hang.so_luong
        except Exception as loi:
            print(f'[LOI] {loi}')
            return [], 0, 0

    def xoa_khoi_gio(self, ma_so):
        """Xóa 1 món khỏi giỏ."""
        try:
            if self.gio_hang.xoa_theo_ma(ma_so):
                return True, f'Đã xóa "{ma_so}" khỏi giỏ.'
            return False, f'Không có "{ma_so}" trong giỏ.'
        except Exception as loi:
            return False, f'Lỗi: {loi}'

    def thanh_toan(self):
        """Dequeue toàn bộ giỏ → trả hóa đơn."""
        try:
            if self.gio_hang.rong():
                return False, 'Giỏ hàng trống.', None
            cac_mon = []
            tong = 0
            while not self.gio_hang.rong():
                mon = self.gio_hang.lay_ra()
                cac_mon.append(mon)
                tong += mon.get('gia_ban', 0)
            hoa_don = {
                'cac_mon':  cac_mon,
                'tong_tien': tong,
                'so_mon':   len(cac_mon)
            }
            return True, f'Đã thanh toán {len(cac_mon)} món, tổng {tong:,.0f}đ.', hoa_don
        except Exception as loi:
            return False, f'Lỗi: {loi}', None

    # ========================================================
    # HÀM TIỆN ÍCH NỘI BỘ
    # ========================================================
    def _tao_doi_tuong_tu_dict(self, d):
        """Tái tạo đối tượng MatHang từ dict (dùng cho Undo xóa)."""
        try:
            loai = d.get('loai_hang')
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
