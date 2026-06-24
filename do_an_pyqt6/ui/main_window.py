import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
                             QMessageBox, QLineEdit, QLabel, QComboBox, QDialog)
from PyQt6.QtCore import Qt

from models.linked_list import DanhSachLienKetDoi
from models.ngan_xep import NganXep       # Stack LIFO - dùng cho Undo/Redo
from models.hang_doi import HangDoi       # Queue FIFO - dùng cho Giỏ hàng
from models.subclasses import Sach, TapChi, Bao, LuanVan, BanThao
from ui.dialogs import HopThoaiThemMoi
from ui.hop_thoai_gio_hang import HopThoaiGioHang


class CuaSoChinh(QMainWindow):
    def __init__(self, nguoi_dung_hien_tai=None):
        super().__init__()
        self.setWindowTitle("Hệ Thống Quản Lý Cửa Hàng Sách (PyQt6 + Linked List + Stack + Queue)")
        self.resize(1100, 700)

        # ===== THÔNG TIN NGƯỜI DÙNG ĐĂNG NHẬP (PHÂN QUYỀN) =====
        # - Admin    : toàn quyền (xem + thêm + sửa + xóa + giỏ hàng)
        # - Nhân viên: KHÔNG được XÓA (chỉ xem + thêm + sửa + giỏ hàng)
        self.nguoi_dung = nguoi_dung_hien_tai

        # ===== CÁC CẤU TRÚC DỮ LIỆU CHÍNH =====
        # 1. Danh sách liên kết đôi: chứa toàn bộ mặt hàng trên RAM
        self.danh_sach = DanhSachLienKetDoi()
        # 2. Ngăn xếp Undo (LIFO): lưu thao tác để hoàn tác
        self.ngan_xep_hoan_tac = NganXep()
        # 3. Ngăn xếp Redo (LIFO): lưu thao tác đã hoàn tác để làm lại
        self.ngan_xep_lam_lai = NganXep()
        # 4. Hàng đợi Giỏ hàng (FIFO): chứa các sản phẩm khách muốn mua
        self.gio_hang = HangDoi()

        self.thiet_lap_giao_dien()
        self.doc_du_lieu_tu_file()
        self.cap_nhat_tieu_de_theo_quyen()

    # ==================================================================
    # THIẾT LẬP GIAO DIỆN
    # ==================================================================
    def thiet_lap_giao_dien(self):
        widget_chinh = QWidget()
        layout_chinh = QVBoxLayout()

        # ----- KHU VỰC TÌM KIẾM (CÓ CHỌN TIÊU CHÍ) + SẮP XẾP -----
        layout_cong_cu = QHBoxLayout()

        # Ô nhập từ khóa
        self.nhap_tim_kiem = QLineEdit()
        self.nhap_tim_kiem.setPlaceholderText("Nhập từ khóa cần tìm...")

        # Combo chọn tiêu chí tìm kiếm (TÊN / MÃ / LOẠI)
        self.cb_tieu_chi_tim = QComboBox()
        self.cb_tieu_chi_tim.addItems(["Tất cả", "Theo Tên", "Theo Mã", "Theo Loại"])

        nut_tim_kiem = QPushButton("🔍 Tìm Kiếm")
        nut_tim_kiem.clicked.connect(self.xu_ly_tim_kiem)

        nut_lam_moi = QPushButton("🔄 Tải Lại Bảng")
        nut_lam_moi.clicked.connect(self.cap_nhat_bang_hien_thi)

        # Combo chọn tiêu chí sắp xếp
        self.cb_sap_xep = QComboBox()
        self.cb_sap_xep.addItems([
            "Giá bán tăng dần",
            "Giá bán giảm dần",
            "Tên A-Z",
            "Tên Z-A",
            "Số lượng tồn kho tăng"
        ])
        nut_sap_xep = QPushButton("🔀 Sắp Xếp (Merge Sort)")
        nut_sap_xep.setStyleSheet("background-color: #FF9800; color: white;")
        nut_sap_xep.clicked.connect(self.xu_ly_sap_xep)

        layout_cong_cu.addWidget(QLabel("Từ khóa:"))
        layout_cong_cu.addWidget(self.nhap_tim_kiem)
        layout_cong_cu.addWidget(self.cb_tieu_chi_tim)
        layout_cong_cu.addWidget(nut_tim_kiem)
        layout_cong_cu.addWidget(nut_lam_moi)

        layout_cong_cu.addStretch()  # Khoảng trống ở giữa

        layout_cong_cu.addWidget(QLabel("Sắp xếp:"))
        layout_cong_cu.addWidget(self.cb_sap_xep)
        layout_cong_cu.addWidget(nut_sap_xep)
        layout_chinh.addLayout(layout_cong_cu)

        # ----- BẢNG HIỂN THỊ DỮ LIỆU -----
        self.bang_du_lieu = QTableWidget()
        self.bang_du_lieu.setColumnCount(7)
        self.bang_du_lieu.setHorizontalHeaderLabels(
            ["Mã Số", "Phân Loại", "Tên Sản Phẩm", "Giá Cơ Bản", "Giá Bán", "Số Lượng", "Đặc Điểm Riêng"]
        )
        self.bang_du_lieu.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # Không cho sửa trực tiếp trên bảng
        self.bang_du_lieu.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout_chinh.addWidget(self.bang_du_lieu)

        # ----- DÒNG NÚT CHỨC NĂNG CHÍNH (THÊM/SỬA/XÓA/THỐNG KÊ) -----
        layout_chuc_nang = QHBoxLayout()

        nut_them = QPushButton("➕ Thêm Mặt Hàng")
        nut_them.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; font-size: 14px; padding: 10px;")
        nut_them.clicked.connect(self.hien_thi_form_them)

        nut_sua = QPushButton("✏️ Sửa Mặt Hàng")
        nut_sua.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; font-size: 14px; padding: 10px;")
        nut_sua.clicked.connect(self.hien_thi_form_sua)

        self.nut_xoa = QPushButton("🗑️ Xóa Mặt Hàng")
        self.nut_xoa.setStyleSheet("background-color: #f44336; color: white; font-weight: bold; font-size: 14px; padding: 10px;")
        self.nut_xoa.clicked.connect(self.xu_ly_xoa_san_pham)

        nut_thong_ke = QPushButton("📊 Xem Thống Kê")
        nut_thong_ke.setStyleSheet("background-color: #9C27B0; color: white; font-weight: bold; font-size: 14px; padding: 10px;")
        nut_thong_ke.clicked.connect(self.xu_ly_thong_ke)

        # Nút đăng xuất (để đổi tài khoản)
        nut_dang_xuat = QPushButton("🚪 Đăng Xuất")
        nut_dang_xuat.setStyleSheet("background-color: #616161; color: white; font-weight: bold; font-size: 14px; padding: 10px;")
        nut_dang_xuat.clicked.connect(self.xu_ly_dang_xuat)

        layout_chuc_nang.addWidget(nut_them)
        layout_chuc_nang.addWidget(nut_sua)
        layout_chuc_nang.addWidget(self.nut_xoa)
        layout_chuc_nang.addWidget(nut_thong_ke)
        layout_chuc_nang.addWidget(nut_dang_xuat)
        layout_chinh.addLayout(layout_chuc_nang)

        # ----- DÒNG NÚT UNDO/REDO + GIỎ HÀNG -----
        layout_mo_rong = QHBoxLayout()

        nut_hoan_tac = QPushButton("↩️ Hoàn Tác (Undo)")
        nut_hoan_tac.setStyleSheet("background-color: #607D8B; color: white; font-weight: bold; font-size: 14px; padding: 10px;")
        nut_hoan_tac.clicked.connect(self.xu_ly_hoan_tac)

        nut_lam_lai = QPushButton("↪️ Làm Lại (Redo)")
        nut_lam_lai.setStyleSheet("background-color: #795548; color: white; font-weight: bold; font-size: 14px; padding: 10px;")
        nut_lam_lai.clicked.connect(self.xu_ly_lam_lai)

        nut_them_gio = QPushButton("🛒 Thêm Vào Giỏ")
        nut_them_gio.setStyleSheet("background-color: #009688; color: white; font-weight: bold; font-size: 14px; padding: 10px;")
        nut_them_gio.clicked.connect(self.xu_ly_them_vao_gio)

        nut_xem_gio = QPushButton("🛍️ Xem Giỏ Hàng")
        nut_xem_gio.setStyleSheet("background-color: #FF5722; color: white; font-weight: bold; font-size: 14px; padding: 10px;")
        nut_xem_gio.clicked.connect(self.xu_ly_xem_gio_hang)

        layout_mo_rong.addWidget(nut_hoan_tac)
        layout_mo_rong.addWidget(nut_lam_lai)
        layout_mo_rong.addWidget(nut_them_gio)
        layout_mo_rong.addWidget(nut_xem_gio)
        layout_chinh.addLayout(layout_mo_rong)

        widget_chinh.setLayout(layout_chinh)
        self.setCentralWidget(widget_chinh)

    # ==================================================================
    # PHÂN QUYỀN (Admin / Nhân viên)
    # ==================================================================
    def cap_nhat_tieu_de_theo_quyen(self):
        """
        Cập nhật tiêu đề + ẩn/hiện nút Xóa tùy theo quyền người dùng.
        - Admin    : được XÓA, tiêu đề ghi 'Admin'
        - Nhân viên: KHÔNG được XÓA, tiêu đề ghi 'Nhân viên'
        """
        if self.nguoi_dung is None:
            # Trường hợp không đăng nhập (dự phòng) → mặc định là admin
            vai_tro = "Admin"
            self.nut_xoa.show()
        elif self.nguoi_dung.la_admin():
            vai_tro = "Admin"
            self.nut_xoa.show()  # Admin được phép xóa
        else:
            vai_tro = "Nhân viên"
            self.nut_xoa.hide()  # Nhân viên KHÔNG được xóa → ẩn nút

        # Cập nhật tiêu đề cửa sổ cho người dùng biết đang đăng nhập bằng tài khoản nào
        self.setWindowTitle(
            f"Hệ Thống Quản Lý Cửa Hàng Sách  |  "
            f"Đăng nhập: {self.nguoi_dung.ten_dang_nhap if self.nguoi_dung else '?'} ({vai_tro})"
        )

    def xu_ly_dang_xuat(self):
        """Đóng cửa sổ chính để quay về màn hình đăng nhập."""
        xac_nhan = QMessageBox.question(
            self, "Đăng xuất",
            "Bạn có muốn đăng xuất và quay về màn hình đăng nhập?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if xac_nhan == QMessageBox.StandardButton.Yes:
            self.close()  # Đóng cửa sổ chính → main.py sẽ chạy lại màn hình đăng nhập

    # ==================================================================
    # XỬ LÝ: THÊM / SỬA / XÓA  (CÓ LƯU LỊCH SỬ ĐỂ UNDO/REDO)
    # ==================================================================
    def hien_thi_form_them(self):
        """Mở hộp thoại Thêm sản phẩm mới."""
        hop_thoai = HopThoaiThemMoi(self)  # Không truyền san_pham_cu → chế độ THÊM
        if hop_thoai.exec() == QDialog.DialogCode.Accepted:
            sp_moi = hop_thoai.san_pham_moi

            # Kiểm tra trùng mã ID trước khi thêm
            if self.danh_sach.tim_kiem_theo_ma(sp_moi.ma_so):
                QMessageBox.warning(self, "Lỗi", "Mã sản phẩm này đã tồn tại trong kho!")
                return

            # Thêm vào Danh Sách Liên Kết Đôi
            self.danh_sach.them_vao_cuoi(sp_moi)
            self.luu_du_lieu_ra_file()
            self.cap_nhat_bang_hien_thi()

            # Ghi vào Stack Undo (để có thể Hoàn Tác được)
            # Thao tác này là "THÊM" → Undo sẽ XÓA sản phẩm đó đi
            self.ngan_xep_hoan_tac.day_vao({"thao_tac": "them", "sp": sp_moi})
            # Khi có thao tác mới → xóa sạch ngăn xếp Redo (chuỗi redo bị đứt)
            self.ngan_xep_lam_lai.xoa_tat_ca()

            QMessageBox.information(self, "Thành công", "Đã lưu mặt hàng mới thành công!")

    def hien_thi_form_sua(self):
        """Mở hộp thoại Sửa sản phẩm đang chọn trên bảng."""
        dong_dang_chon = self.bang_du_lieu.currentRow()
        if dong_dang_chon < 0:
            QMessageBox.warning(self, "Cảnh Báo", "Bạn chưa click chọn sản phẩm nào trên bảng!")
            return

        ma_so = self.bang_du_lieu.item(dong_dang_chon, 0).text()
        sp_cu = self.danh_sach.tim_kiem_theo_ma(ma_so)
        if sp_cu is None:
            QMessageBox.warning(self, "Lỗi", "Không tìm thấy sản phẩm trong danh sách!")
            return

        # Mở hộp thoại ở chế độ SỬA (truyền sp_cu vào)
        hop_thoai = HopThoaiThemMoi(self, san_pham_cu=sp_cu)
        if hop_thoai.exec() == QDialog.DialogCode.Accepted:
            sp_sua = hop_thoai.san_pham_moi

            # Cập nhật dữ liệu: xóa node cũ, thêm node mới
            self.danh_sach.xoa_nut_theo_ma(ma_so)
            self.danh_sach.them_vao_cuoi(sp_sua)

            self.luu_du_lieu_ra_file()
            self.cap_nhat_bang_hien_thi()

            # Ghi vào Stack Undo (để có thể Hoàn Tác được)
            # Thao tác này là "SỬA" → Undo sẽ khôi phục lại sp_cu
            self.ngan_xep_hoan_tac.day_vao({
                "thao_tac": "sua",
                "sp_cu": sp_cu,    # Sản phẩm trước khi sửa
                "sp_moi": sp_sua   # Sản phẩm sau khi sửa
            })
            # Khi có thao tác mới → xóa sạch ngăn xếp Redo
            self.ngan_xep_lam_lai.xoa_tat_ca()

            QMessageBox.information(self, "Thành công", "Đã cập nhật thông tin sản phẩm!")

    def xu_ly_xoa_san_pham(self):
        """Xóa sản phẩm đang chọn trên bảng."""
        # ----- KIỂM TRA PHÂN QUYỀN -----
        # Chỉ Admin mới được xóa. Nhân viên không được (nút đã ẩn nhưng vẫn chặn cho chắc)
        if self.nguoi_dung is not None and not self.nguoi_dung.la_admin():
            QMessageBox.warning(
                self, "Không Đủ Quyền",
                "Bạn là 'Nhân viên' nên KHÔNG ĐƯỢC PHÉP XÓA sản phẩm.\n"
                "Vui lòng liên hệ Admin để thực hiện thao tác này."
            )
            return

        dong_dang_chon = self.bang_du_lieu.currentRow()
        if dong_dang_chon < 0:
            QMessageBox.warning(self, "Cảnh Báo", "Bạn chưa click chọn sản phẩm nào trên bảng!")
            return

        ma_so = self.bang_du_lieu.item(dong_dang_chon, 0).text()

        # Hộp thoại xác nhận trước khi xóa
        xac_nhan = QMessageBox.question(
            self, "Xác nhận xóa",
            f"Bạn có chắc chắn muốn xóa vĩnh viễn sản phẩm mã '{ma_so}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if xac_nhan == QMessageBox.StandardButton.Yes:
            # Phải lưu sản phẩm bị xóa TRƯỚC khi xóa (để có thể Undo)
            sp_bi_xoa = self.danh_sach.tim_kiem_theo_ma(ma_so)
            thanh_cong = self.danh_sach.xoa_nut_theo_ma(ma_so)
            if thanh_cong:
                self.luu_du_lieu_ra_file()
                self.cap_nhat_bang_hien_thi()

                # Ghi vào Stack Undo (để có thể Hoàn Tác được)
                # Thao tác này là "XÓA" → Undo sẽ THÊM lại sản phẩm đó
                self.ngan_xep_hoan_tac.day_vao({"thao_tac": "xoa", "sp": sp_bi_xoa})
                # Khi có thao tác mới → xóa sạch ngăn xếp Redo
                self.ngan_xep_lam_lai.xoa_tat_ca()

                QMessageBox.information(self, "Thành công", "Đã xóa xong!")
            else:
                QMessageBox.warning(self, "Lỗi", "Không thể xóa. Có lỗi xảy ra.")

    # ==================================================================
    # XỬ LÝ: UNDO / REDO (sử dụng Stack LIFO)
    # ==================================================================
    def xu_ly_hoan_tac(self):
        """
        HOÀN TÁC (UNDO) thao tác gần nhất.
        - Lấy 1 mục từ Stack Undo.
        - Tùy loại thao tác (them/xoa/sua) mà đảo ngược lại.
        - Đẩy mục đó sang Stack Redo (để có thể làm lại).
        """
        if self.ngan_xep_hoan_tac.rong():
            QMessageBox.information(self, "Hoàn Tác", "Không còn thao tác nào để hoàn tác!")
            return

        # Lấy thao tác gần nhất ra khỏi Stack Undo
        thao_tac = self.ngan_xep_hoan_tac.lay_ra()
        kieu = thao_tac["thao_tac"]

        if kieu == "them":
            # Đã THÊM → bây giờ XÓA để hoàn tác
            sp = thao_tac["sp"]
            self.danh_sach.xoa_nut_theo_ma(sp.ma_so)

        elif kieu == "xoa":
            # Đã XÓA → bây giờ THÊM lại để hoàn tác
            sp = thao_tac["sp"]
            self.danh_sach.them_vao_cuoi(sp)

        elif kieu == "sua":
            # Đã SỬA từ sp_cu → sp_moi → bây giờ khôi phục lại sp_cu
            ma_so = thao_tac["sp_moi"].ma_so
            self.danh_sach.xoa_nut_theo_ma(ma_so)
            self.danh_sach.them_vao_cuoi(thao_tac["sp_cu"])

        # Đẩy thao tác này sang Stack Redo (để có thể Làm Lại)
        self.ngan_xep_lam_lai.day_vao(thao_tac)

        # Lưu + vẽ lại bảng
        self.luu_du_lieu_ra_file()
        self.cap_nhat_bang_hien_thi()
        QMessageBox.information(self, "Hoàn Tác", f"Đã hoàn tác thao tác '{kieu}' thành công!")

    def xu_ly_lam_lai(self):
        """
        LÀM LẠI (REDO) thao tác vừa bị hoàn tác.
        - Lấy 1 mục từ Stack Redo.
        - Thực hiện lại thao tác đó.
        - Đẩy mục đó trở lại Stack Undo.
        """
        if self.ngan_xep_lam_lai.rong():
            QMessageBox.information(self, "Làm Lại", "Không còn thao tác nào để làm lại!")
            return

        # Lấy thao tác ra khỏi Stack Redo
        thao_tac = self.ngan_xep_lam_lai.lay_ra()
        kieu = thao_tac["thao_tac"]

        if kieu == "them":
            # Làm lại THÊM → thêm lại sp
            self.danh_sach.them_vao_cuoi(thao_tac["sp"])

        elif kieu == "xoa":
            # Làm lại XÓA → xóa sp
            self.danh_sach.xoa_nut_theo_ma(thao_tac["sp"].ma_so)

        elif kieu == "sua":
            # Làm lại SỬA → áp dụng sp_moi
            ma_so = thao_tac["sp_cu"].ma_so
            self.danh_sach.xoa_nut_theo_ma(ma_so)
            self.danh_sach.them_vao_cuoi(thao_tac["sp_moi"])

        # Đẩy thao tác trở lại Stack Undo
        self.ngan_xep_hoan_tac.day_vao(thao_tac)

        # Lưu + vẽ lại bảng
        self.luu_du_lieu_ra_file()
        self.cap_nhat_bang_hien_thi()
        QMessageBox.information(self, "Làm Lại", f"Đã làm lại thao tác '{kieu}' thành công!")

    # ==================================================================
    # XỬ LÝ: TÌM KIẾM NÂNG CAO (TÊN / MÃ / LOẠI)
    # ==================================================================
    def xu_ly_tim_kiem(self):
        """
        Tìm kiếm nâng cao theo tiêu chí người dùng chọn:
        - "Tất cả":    tìm trong cả mã + tên + loại
        - "Theo Tên":  chỉ tìm trong tên
        - "Theo Mã":   chỉ tìm trong mã số
        - "Theo Loại": chỉ tìm trong loại mặt hàng (Sách/Tạp chí/Báo...)
        """
        tu_khoa = self.nhap_tim_kiem.text().strip().lower()
        if not tu_khoa:
            self.cap_nhat_bang_hien_thi()  # Trả về tất cả nếu không nhập gì
            return

        tieu_chi = self.cb_tieu_chi_tim.currentText()
        # Bảng dịch tên lớp Python ↔ tiếng Việt (để tìm theo loại)
        bang_ten = {
            "Sach": "sách", "TapChi": "tạp chí", "Bao": "báo",
            "LuanVan": "luận văn", "BanThao": "bản thảo"
        }

        ket_qua = []
        for sp in self.danh_sach.duyet_danh_sach():
            # Tìm theo từng tiêu chí
            if tieu_chi == "Tất cả":
                # Tìm trong cả mã, tên, loại
                loai_viet = bang_ten.get(sp.__class__.__name__, "")
                if (tu_khoa in sp.ma_so.lower()
                        or tu_khoa in sp.ten.lower()
                        or tu_khoa in loai_viet):
                    ket_qua.append(sp)

            elif tieu_chi == "Theo Tên":
                if tu_khoa in sp.ten.lower():
                    ket_qua.append(sp)

            elif tieu_chi == "Theo Mã":
                if tu_khoa in sp.ma_so.lower():
                    ket_qua.append(sp)

            elif tieu_chi == "Theo Loại":
                loai_viet = bang_ten.get(sp.__class__.__name__, "")
                if tu_khoa in loai_viet:
                    ket_qua.append(sp)

        if not ket_qua:
            QMessageBox.information(self, "Tìm kiếm", "Không tìm thấy sản phẩm nào!")
        self.hien_thi_mang_len_bang(ket_qua)

    # ==================================================================
    # XỬ LÝ: SẮP XẾP (MERGE SORT)
    # ==================================================================
    def xu_ly_sap_xep(self):
        """Sắp xếp danh sách bằng thuật toán Merge Sort trên Linked List."""
        lua_chon = self.cb_sap_xep.currentText()

        if lua_chon == "Giá bán tăng dần":
            self.danh_sach.sap_xep(tieu_chi="gia_co_ban", tang_dan=True)
        elif lua_chon == "Giá bán giảm dần":
            self.danh_sach.sap_xep(tieu_chi="gia_co_ban", tang_dan=False)
        elif lua_chon == "Tên A-Z":
            self.danh_sach.sap_xep(tieu_chi="ten", tang_dan=True)
        elif lua_chon == "Tên Z-A":
            self.danh_sach.sap_xep(tieu_chi="ten", tang_dan=False)
        elif lua_chon == "Số lượng tồn kho tăng":
            self.danh_sach.sap_xep(tieu_chi="so_luong", tang_dan=True)

        self.cap_nhat_bang_hien_thi()
        QMessageBox.information(self, "Thuật Toán",
                                f"Đã áp dụng Merge Sort trên Danh sách liên kết: {lua_chon}")

    # ==================================================================
    # XỬ LÝ: THỐNG KÊ (đắt nhất, rẻ nhất, sắp hết, TỔNG GIÁ TRỊ KHO)
    # ==================================================================
    def xu_ly_thong_ke(self):
        """Hiển thị thống kê tổng quan kho hàng."""
        mang_du_lieu = self.danh_sach.duyet_danh_sach()
        if not mang_du_lieu:
            QMessageBox.information(self, "Thống kê", "Kho hàng hiện đang trống!")
            return

        tong_san_pham = len(mang_du_lieu)
        # Dùng tinh_gia_ban() — đây chính là TÍNH ĐA HÌNH
        dat_nhat = max(mang_du_lieu, key=lambda x: x.tinh_gia_ban())
        re_nhat = min(mang_du_lieu, key=lambda x: x.tinh_gia_ban())

        # Danh sách sản phẩm sắp hết hàng (tồn kho < 5)
        san_pham_sap_het = [sp.ten for sp in mang_du_lieu if sp.so_luong < 5]
        canh_bao_sl = ", ".join(san_pham_sap_het) if san_pham_sap_het else "Không có"

        # TỔNG GIÁ TRỊ KHO = Tổng (giá bán × số lượng) của tất cả sản phẩm
        tong_gia_tri_kho = sum(sp.tinh_gia_ban() * sp.so_luong for sp in mang_du_lieu)

        van_ban_thong_ke = (
            f"📊 TỔNG QUAN KHO HÀNG:\n\n"
            f"- Tổng số mặt hàng khác nhau: {tong_san_pham}\n"
            f"- Sản phẩm đắt tiền nhất: {dat_nhat.ten} (Giá bán: {dat_nhat.tinh_gia_ban():,.0f} đ)\n"
            f"- Sản phẩm rẻ tiền nhất: {re_nhat.ten} (Giá bán: {re_nhat.tinh_gia_ban():,.0f} đ)\n"
            f"- 💰 TỔNG GIÁ TRỊ KHO: {tong_gia_tri_kho:,.0f} đ\n\n"
            f"⚠️ CẢNH BÁO SẮP HẾT HÀNG (< 5 cái):\n"
            f"- {canh_bao_sl}"
        )
        QMessageBox.information(self, "Báo Cáo Thống Kê", van_ban_thong_ke)

    # ==================================================================
    # XỬ LÝ: GIỎ HÀNG (sử dụng Queue FIFO)
    # ==================================================================
    def xu_ly_them_vao_gio(self):
        """Thêm sản phẩm đang chọn vào giỏ hàng (Queue - FIFO)."""
        dong_dang_chon = self.bang_du_lieu.currentRow()
        if dong_dang_chon < 0:
            QMessageBox.warning(self, "Cảnh Báo", "Bạn chưa chọn sản phẩm nào trên bảng!")
            return

        ma_so = self.bang_du_lieu.item(dong_dang_chon, 0).text()
        sp = self.danh_sach.tim_kiem_theo_ma(ma_so)
        if sp is None:
            QMessageBox.warning(self, "Lỗi", "Không tìm thấy sản phẩm!")
            return

        if sp.so_luong <= 0:
            QMessageBox.warning(self, "Hết Hàng", "Sản phẩm này đã hết tồn kho!")
            return

        # Thêm sản phẩm vào CUỐI hàng đợi (FIFO)
        self.gio_hang.them_vao(sp)
        QMessageBox.information(
            self, "Đã Thêm Vào Giỏ",
            f"Đã thêm '{sp.ten}' vào giỏ.\n"
            f"Giỏ hiện có: {self.gio_hang.so_luong} món."
        )

    def xu_ly_xem_gio_hang(self):
        """Mở hộp thoại Giỏ Hàng để xem/xóa/thanh toán."""
        hop_thoai = HopThoaiGioHang(self)
        hop_thoai.exec()

    # ==================================================================
    # CÁC HÀM HIỂN THỊ VÀ LƯU TRỮ
    # ==================================================================
    def cap_nhat_bang_hien_thi(self):
        """Lấy toàn bộ mảng từ LinkedList và hiển thị lên bảng."""
        tat_ca = self.danh_sach.duyet_danh_sach()
        self.hien_thi_mang_len_bang(tat_ca)

    def hien_thi_mang_len_bang(self, mang_san_pham):
        """Vẽ mảng sản phẩm lên bảng QTableWidget."""
        self.bang_du_lieu.setRowCount(0)  # Xóa trắng bảng
        for sp in mang_san_pham:
            dong_moi = self.bang_du_lieu.rowCount()
            self.bang_du_lieu.insertRow(dong_moi)

            # Tính đa hình: lấy tên Class của đối tượng rồi dịch sang tiếng Việt
            loai_sp = sp.__class__.__name__
            bang_ten = {
                "Sach": "Sách", "TapChi": "Tạp Chí", "Bao": "Báo",
                "LuanVan": "Luận Văn", "BanThao": "Bản Thảo"
            }
            loai_sp = bang_ten.get(loai_sp, loai_sp)

            self.bang_du_lieu.setItem(dong_moi, 0, QTableWidgetItem(sp.ma_so))
            self.bang_du_lieu.setItem(dong_moi, 1, QTableWidgetItem(loai_sp))
            self.bang_du_lieu.setItem(dong_moi, 2, QTableWidgetItem(sp.ten))
            self.bang_du_lieu.setItem(dong_moi, 3, QTableWidgetItem(f"{sp.gia_co_ban:,.0f} đ"))
            # Cột Giá Bán gọi phương thức tinh_gia_ban() — TÍNH ĐA HÌNH
            self.bang_du_lieu.setItem(dong_moi, 4, QTableWidgetItem(f"{sp.tinh_gia_ban():,.0f} đ"))
            self.bang_du_lieu.setItem(dong_moi, 5, QTableWidgetItem(str(sp.so_luong)))

            # Nối thông tin riêng theo từng loại (kiểm tra bằng isinstance)
            thong_tin = ""
            if isinstance(sp, Sach):
                thong_tin = f"TG: {sp.tac_gia} | NXB: {sp.nha_xuat_ban}"
            elif isinstance(sp, TapChi):
                thong_tin = f"Số PH: {sp.so_phat_hanh}"
            elif isinstance(sp, Bao):
                thong_tin = f"Ngày PH: {sp.ngay_phat_hanh}"
            elif isinstance(sp, LuanVan):
                thong_tin = f"Trường ĐH: {sp.truong_dai_hoc}"
            elif isinstance(sp, BanThao):
                thong_tin = f"Trạng thái: {sp.tinh_trang}"

            self.bang_du_lieu.setItem(dong_moi, 6, QTableWidgetItem(thong_tin))

    def doc_du_lieu_tu_file(self):
        """Đọc dữ liệu từ SQLite và nạp vào Linked List."""
        from data.sqlite_db import doc_du_lieu_sqlite
        try:
            mang_sp = doc_du_lieu_sqlite()
            for sp in mang_sp:
                self.danh_sach.them_vao_cuoi(sp)
            self.cap_nhat_bang_hien_thi()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi Nghiêm Trọng", f"Lỗi CSDL SQLite: {str(e)}")

    def luu_du_lieu_ra_file(self):
        """Lưu dữ liệu từ Linked List xuống SQLite."""
        from data.sqlite_db import luu_du_lieu_sqlite
        mang_tam = self.danh_sach.duyet_danh_sach()
        try:
            thanh_cong = luu_du_lieu_sqlite(mang_tam)
            if not thanh_cong:
                QMessageBox.warning(self, "Lỗi", "Không thể lưu dữ liệu xuống CSDL!")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi Nghiêm Trọng", f"Lỗi khi lưu SQLite: {str(e)}")
