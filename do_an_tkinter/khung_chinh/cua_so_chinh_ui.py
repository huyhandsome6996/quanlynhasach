"""
Tệp cua_so_chinh_ui.py — GIAO DIỆN cho Cửa sổ chính
=====================================================

Tạo cấu trúc UI của cửa sổ chính sau khi đăng nhập:
    - Thanh đầu trang: tiêu đề + thông tin user + nút Đăng xuất.
    - Thanh công cụ: nút Thêm/Sửa/Xóa + Undo/Redo + Tìm/Sắp xếp.
    - Khung chính (PanedWindow): bảng sản phẩm (trái) + khung phải (thống kê + giỏ).
    - Thanh chân: trạng thái.

UI chỉ vẽ widget + lưu reference. Mọi logic gắn sự kiện do Điều khiển thực hiện.
"""

import tkinter as tk
from tkinter import ttk

# Import UI các nhóm chức năng con.
from chuc_nang.cn02_doc_danh_sach.doc_danh_sach_ui import BangSanPhamUI
from chuc_nang.cn06_tim_kiem_sap_xep.tim_kiem_sap_xep_ui import ThanhTimKiemSapXepUI
from chuc_nang.cn07_thong_ke.thong_ke_ui import KhungThongKeUI
from chuc_nang.cn08_hoan_tac_lam_lai.hoan_tac_lam_lai_ui import ThanhUndoRedoUI
from chuc_nang.cn09_gio_hang.gio_hang_ui import KhungGioHangUI


class CuaSoChinhUI:
    """Cửa sổ chính — hiển thị sau khi đăng nhập thành công."""

    def __init__(self, root, ho_ten, vai_tro):
        """
        Khởi tạo UI cửa sổ chính.

        Tham số:
            root    : Tk root.
            ho_ten  : tên user đang đăng nhập (hiển thị).
            vai_tro : 'admin' hoặc 'nhan_vien' (hiển thị).
        """
        self.root = root

        # Cấu hình cửa sổ.
        root.title(f'Quản lý nhà sách — {ho_ten} ({vai_tro})')
        root.geometry('1100x700+100+50')

        # Lưu vai trò để Điều khiển biết có ẩn nút Xóa không (nhân viên không được xóa).
        self.vai_tro = vai_tro

        # Bắt đầu vẽ UI.
        self._tao_giao_dien()

    # ========================================================
    # TẠO GIAO DIỆN
    # ========================================================
    def _tao_giao_dien(self):
        """Tạo toàn bộ widget của cửa sổ chính."""
        # === THANH ĐẦU TRANG ===
        frame_dau = ttk.Frame(self.root, padding=10)
        frame_dau.pack(fill='x')
        ttk.Label(frame_dau, text='QUẢN LÝ NHÀ SÁCH',
                  font=('Arial', 16, 'bold')).pack(side='left')
        # Khung thông tin user bên phải.
        frame_user = ttk.Frame(frame_dau)
        frame_user.pack(side='right')
        self.lbl_ten_user = ttk.Label(frame_user, text='')
        self.lbl_ten_user.pack(side='left', padx=5)
        self.lbl_vai_tro = ttk.Label(frame_user, foreground='blue')
        self.lbl_vai_tro.pack(side='left', padx=5)
        # Nút đăng xuất — command gắn bởi Điều khiển.
        self.btn_dang_xuat = ttk.Button(frame_user, text='Đăng xuất')
        self.btn_dang_xuat.pack(side='left', padx=5)

        # === THANH CÔNG CỤ ===
        frame_cc = ttk.Frame(self.root, padding=(10, 0, 10, 5))
        frame_cc.pack(fill='x')

        # Nhóm nút Thêm/Sửa/Xóa.
        self.btn_them = ttk.Button(frame_cc, text='➕ Thêm', width=10)
        self.btn_them.pack(side='left', padx=2)
        self.btn_sua = ttk.Button(frame_cc, text='✏ Sửa', width=10)
        self.btn_sua.pack(side='left', padx=2)
        self.btn_xoa = ttk.Button(frame_cc, text='🗑 Xóa', width=10)
        self.btn_xoa.pack(side='left', padx=2)
        ttk.Separator(frame_cc, orient='vertical').pack(side='left', fill='y', padx=8)

        # Nhóm Undo/Redo — dùng UI của folder 08.
        self.ui_undoredo = ThanhUndoRedoUI(frame_cc)
        ttk.Separator(frame_cc, orient='vertical').pack(side='left', fill='y', padx=8)

        # Nhóm Tìm kiếm + Sắp xếp — dùng UI của folder 06.
        self.ui_tim_sx = ThanhTimKiemSapXepUI(frame_cc)

        # === KHUNG CHÍNH: BẢNG DỮ LIỆU + KHUNG BÊN PHẢI ===
        # PanedWindow cho phép kéo đổi tỷ lệ.
        paned = ttk.PanedWindow(self.root, orient='horizontal')
        paned.pack(fill='both', expand=True, padx=10, pady=5)

        # === BẢNG DỮ LIỆU (trái) — dùng UI của folder 02 ===
        frame_bang = ttk.LabelFrame(paned, text='Danh sách sản phẩm', padding=5)
        paned.add(frame_bang, weight=3)
        # BangSanPhamUI tự tạo Treeview + scrollbar trong frame_bang.
        self.ui_bang = BangSanPhamUI(frame_bang)
        # Bind double-click vào dòng → mở dialog Sửa (gắn bởi Điều khiển).
        # (Điều khiển sẽ bind sau.)

        # === KHUNG BÊN PHẢI (phải) — chứa Thống kê + Giỏ hàng ===
        frame_phai = ttk.Frame(paned)
        paned.add(frame_phai, weight=2)

        # Khung Thống kê — dùng UI của folder 07.
        self.ui_thong_ke = KhungThongKeUI(frame_phai)

        # Khung Giỏ hàng — dùng UI của folder 09.
        self.ui_gio_hang = KhungGioHangUI(frame_phai)

        # === THANH CHÂN ===
        frame_chan = ttk.Frame(self.root, padding=5)
        frame_chan.pack(side='bottom', fill='x')
        self.lbl_trang_thai = ttk.Label(frame_chan, text='Sẵn sàng.', foreground='gray')
        self.lbl_trang_thai.pack(side='left')

    # ========================================================
    # CÁC HÀM TIỆN ÍCH CHO ĐIỀU KHIỂN GỌI
    # ========================================================
    def cap_nhat_user(self, ho_ten, vai_tro):
        """Cập nhật label tên user + vai trò (dùng khi đăng xuất → đăng nhập lại)."""
        self.lbl_ten_user.config(text=f'Xin chào: {ho_ten}')
        self.lbl_vai_tro.config(text=f'({vai_tro})')
        # Cập nhật luôn tiêu đề cửa sổ.
        self.root.title(f'Quản lý nhà sách — {ho_ten} ({vai_tro})')

    def dat_trang_thai(self, msg):
        """Cập nhật thanh trạng thái."""
        self.lbl_trang_thai.config(text=msg)

    def bind_double_click_bang(self, ham_xu_ly):
        """Gắn sự kiện double-click vào dòng bảng → hàm xử lý (mở form Sửa)."""
        self.ui_bang.tree.bind('<Double-1>', lambda e: ham_xu_ly())
