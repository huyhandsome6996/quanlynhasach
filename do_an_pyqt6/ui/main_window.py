import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
                             QMessageBox, QLineEdit, QLabel, QComboBox, QDialog)
from PyQt6.QtCore import Qt

from models.linked_list import DanhSachLienKetDoi
from models.subclasses import Sach, TapChi, Bao, LuanVan, BanThao
from ui.dialogs import HopThoaiThemMoi


class CuaSoChinh(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hệ Thống Quản Lý Cửa Hàng Sách (PyQt6 + Doubly Linked List)")
        self.resize(1000, 650)

        # Cấu trúc dữ liệu chính: Danh sách liên kết đôi
        self.danh_sach = DanhSachLienKetDoi()

        self.thiet_lap_giao_dien()
        self.doc_du_lieu_tu_file()

    # ==================================================================
    # THIẾT LẬP GIAO DIỆN
    # ==================================================================
    def thiet_lap_giao_dien(self):
        widget_chinh = QWidget()
        layout_chinh = QVBoxLayout()

        # ----- KHU VỰC TÌM KIẾM & SẮP XẾP -----
        layout_cong_cu = QHBoxLayout()

        self.nhap_tim_kiem = QLineEdit()
        self.nhap_tim_kiem.setPlaceholderText("Nhập mã hoặc tên cần tìm...")
        nut_tim_kiem = QPushButton("Tìm Kiếm")
        nut_tim_kiem.clicked.connect(self.xu_ly_tim_kiem)

        nut_lam_moi = QPushButton("Tải Lại Bảng")
        nut_lam_moi.clicked.connect(self.cap_nhat_bang_hien_thi)

        self.cb_sap_xep = QComboBox()
        self.cb_sap_xep.addItems([
            "Giá bán tăng dần",
            "Giá bán giảm dần",
            "Tên A-Z",
            "Tên Z-A",
            "Số lượng tồn kho tăng"
        ])
        nut_sap_xep = QPushButton("Sắp Xếp (Merge Sort)")
        nut_sap_xep.setStyleSheet("background-color: #FF9800; color: white;")
        nut_sap_xep.clicked.connect(self.xu_ly_sap_xep)

        layout_cong_cu.addWidget(QLabel("Tìm kiếm:"))
        layout_cong_cu.addWidget(self.nhap_tim_kiem)
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

        # ----- CÁC NÚT CHỨC NĂNG CHÍNH -----
        layout_chuc_nang = QHBoxLayout()

        nut_them = QPushButton("➕ Thêm Mặt Hàng")
        nut_them.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; font-size: 14px; padding: 10px;")
        nut_them.clicked.connect(self.hien_thi_form_them)

        nut_sua = QPushButton("✏️ Sửa Mặt Hàng")
        nut_sua.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; font-size: 14px; padding: 10px;")
        nut_sua.clicked.connect(self.hien_thi_form_sua)

        nut_xoa = QPushButton("🗑️ Xóa Mặt Hàng")
        nut_xoa.setStyleSheet("background-color: #f44336; color: white; font-weight: bold; font-size: 14px; padding: 10px;")
        nut_xoa.clicked.connect(self.xu_ly_xoa_san_pham)

        nut_thong_ke = QPushButton("📊 Xem Thống Kê")
        nut_thong_ke.setStyleSheet("background-color: #9C27B0; color: white; font-weight: bold; font-size: 14px; padding: 10px;")
        nut_thong_ke.clicked.connect(self.xu_ly_thong_ke)

        layout_chuc_nang.addWidget(nut_them)
        layout_chuc_nang.addWidget(nut_sua)
        layout_chuc_nang.addWidget(nut_xoa)
        layout_chuc_nang.addWidget(nut_thong_ke)
        layout_chinh.addLayout(layout_chuc_nang)

        widget_chinh.setLayout(layout_chinh)
        self.setCentralWidget(widget_chinh)

    # ==================================================================
    # CÁC HÀM XỬ LÝ SỰ KIỆN
    # ==================================================================
    def hien_thi_form_them(self):
        """Mở hộp thoại Thêm sản phẩm mới."""
        hop_thoai = HopThoaiThemMoi(self)  # Không truyền san_pham_cu → chế độ THÊM
        if hop_thoai.exec() == QDialog.DialogCode.Accepted:
            sp_moi = hop_thoai.san_pham_moi

            # Kiểm tra trùng mã ID trước khi thêm (yêu cầu đề bài)
            if self.danh_sach.tim_kiem_theo_ma(sp_moi.ma_so):
                QMessageBox.warning(self, "Lỗi", "Mã sản phẩm này đã tồn tại trong kho!")
                return

            # Thêm vào Danh Sách Liên Kết Đôi
            self.danh_sach.them_vao_cuoi(sp_moi)
            self.luu_du_lieu_ra_file()
            self.cap_nhat_bang_hien_thi()
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

            # Cập nhật dữ liệu: xóa node cũ, thêm node mới (giữ nguyên vị trí thì phức tạp,
            # nên đơn giản là xóa cũ + thêm mới vào cuối — đủ cho đồ án học)
            self.danh_sach.xoa_nut_theo_ma(ma_so)
            self.danh_sach.them_vao_cuoi(sp_sua)

            self.luu_du_lieu_ra_file()
            self.cap_nhat_bang_hien_thi()
            QMessageBox.information(self, "Thành công", "Đã cập nhật thông tin sản phẩm!")

    def xu_ly_xoa_san_pham(self):
        """Xóa sản phẩm đang chọn trên bảng."""
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
            thanh_cong = self.danh_sach.xoa_nut_theo_ma(ma_so)
            if thanh_cong:
                self.luu_du_lieu_ra_file()
                self.cap_nhat_bang_hien_thi()
                QMessageBox.information(self, "Thành công", "Đã xóa xong!")
            else:
                QMessageBox.warning(self, "Lỗi", "Không thể xóa. Có lỗi xảy ra.")

    def xu_ly_tim_kiem(self):
        """Tìm kiếm theo Mã hoặc Tên (không phân biệt hoa thường)."""
        tu_khoa = self.nhap_tim_kiem.text().strip().lower()
        if not tu_khoa:
            self.cap_nhat_bang_hien_thi()  # Trả về tất cả nếu không nhập gì
            return

        ket_qua = []
        for sp in self.danh_sach.duyet_danh_sach():
            # Tìm kiếm theo Mã hoặc Tên
            if tu_khoa in sp.ma_so.lower() or tu_khoa in sp.ten.lower():
                ket_qua.append(sp)

        if not ket_qua:
            QMessageBox.information(self, "Tìm kiếm", "Không tìm thấy sản phẩm nào!")
        self.hien_thi_mang_len_bang(ket_qua)

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

        van_ban_thong_ke = (
            f"📊 TỔNG QUAN KHO HÀNG:\n\n"
            f"- Tổng số mặt hàng khác nhau: {tong_san_pham}\n"
            f"- Sản phẩm đắt tiền nhất: {dat_nhat.ten} (Giá bán: {dat_nhat.tinh_gia_ban():,.0f} đ)\n"
            f"- Sản phẩm rẻ tiền nhất: {re_nhat.ten} (Giá bán: {re_nhat.tinh_gia_ban():,.0f} đ)\n\n"
            f"⚠️ CẢNH BÁO SẮP HẾT HÀNG (< 5 cái):\n"
            f"- {canh_bao_sl}"
        )
        QMessageBox.information(self, "Báo Cáo Thống Kê", van_ban_thong_ke)

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
