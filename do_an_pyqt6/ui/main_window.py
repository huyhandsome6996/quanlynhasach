import json
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
        self.setWindowTitle("Hệ Thống Quản Lý Cửa Hàng Sách (Sử dụng PyQt6 & Cấu trúc DL)")
        self.resize(900, 600)
        
        # Khởi tạo Cấu trúc dữ liệu chính
        self.danh_sach = DanhSachLienKetDoi()
        self.duong_dan_file = "data/database.json"
        
        self.thiet_lap_giao_dien()
        self.doc_du_lieu_tu_file()

    def thiet_lap_giao_dien(self):
        widget_chinh = QWidget()
        layout_chinh = QVBoxLayout()

        # ---------------- KHU VỰC TÌM KIẾM & SẮP XẾP ----------------
        layout_cong_cu = QHBoxLayout()
        
        # Khung Tìm Kiếm
        self.nhap_tim_kiem = QLineEdit()
        self.nhap_tim_kiem.setPlaceholderText("Nhập mã hoặc tên cần tìm...")
        nut_tim_kiem = QPushButton("Tìm Kiếm")
        nut_tim_kiem.clicked.connect(self.xu_ly_tim_kiem)
        nut_lam_moi = QPushButton("Tải Lại Bảng")
        nut_lam_moi.clicked.connect(self.cap_nhat_bang_hien_thi)
        
        # Khung Sắp Xếp
        self.cb_sap_xep = QComboBox()
        self.cb_sap_xep.addItems(["Giá tăng dần", "Giá giảm dần", "Tên A-Z", "Tên Z-A", "Số lượng tồn kho"])
        nut_sap_xep = QPushButton("Sắp Xếp (Merge Sort)")
        nut_sap_xep.setStyleSheet("background-color: #FF9800; color: white;")
        nut_sap_xep.clicked.connect(self.xu_ly_sap_xep)

        layout_cong_cu.addWidget(QLabel("Tìm kiếm:"))
        layout_cong_cu.addWidget(self.nhap_tim_kiem)
        layout_cong_cu.addWidget(nut_tim_kiem)
        layout_cong_cu.addWidget(nut_lam_moi)
        
        layout_cong_cu.addStretch() # Tạo khoảng trống ở giữa
        
        layout_cong_cu.addWidget(QLabel("Sắp xếp:"))
        layout_cong_cu.addWidget(self.cb_sap_xep)
        layout_cong_cu.addWidget(nut_sap_xep)
        layout_chinh.addLayout(layout_cong_cu)

        # ---------------- BẢNG HIỂN THỊ DỮ LIỆU ----------------
        self.bang_du_lieu = QTableWidget()
        self.bang_du_lieu.setColumnCount(6)
        self.bang_du_lieu.setHorizontalHeaderLabels(["Mã Số", "Phân Loại", "Tên Sản Phẩm", "Giá Bán", "Số Lượng", "Đặc Điểm Riêng"])
        self.bang_du_lieu.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # Không cho sửa trực tiếp trên bảng
        self.bang_du_lieu.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout_chinh.addWidget(self.bang_du_lieu)

        # ---------------- CÁC NÚT CHỨC NĂNG CHÍNH ----------------
        layout_chuc_nang = QHBoxLayout()
        nut_them = QPushButton("Thêm Mặt Hàng")
        nut_them.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; font-size: 14px; padding: 10px;")
        nut_them.clicked.connect(self.hien_thi_form_them)
        
        nut_xoa = QPushButton("Xóa Mặt Hàng")
        nut_xoa.setStyleSheet("background-color: #f44336; color: white; font-weight: bold; font-size: 14px; padding: 10px;")
        nut_xoa.clicked.connect(self.xu_ly_xoa_san_pham)

        nut_thong_ke = QPushButton("Xem Thống Kê")
        nut_thong_ke.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; font-size: 14px; padding: 10px;")
        nut_thong_ke.clicked.connect(self.xu_ly_thong_ke)

        layout_chuc_nang.addWidget(nut_them)
        layout_chuc_nang.addWidget(nut_xoa)
        layout_chuc_nang.addWidget(nut_thong_ke)
        layout_chinh.addLayout(layout_chuc_nang)

        widget_chinh.setLayout(layout_chinh)
        self.setCentralWidget(widget_chinh)

    # ================== CÁC HÀM XỬ LÝ SỰ KIỆN ==================
    def hien_thi_form_them(self):
        hop_thoai = HopThoaiThemMoi(self)
        if hop_thoai.exec() == QDialog.DialogCode.Accepted:
            sp_moi = hop_thoai.san_pham_moi
            
            # Kiểm tra trùng mã ID trước khi thêm (Yêu cầu đề bài)
            if self.danh_sach.tim_kiem_theo_ma(sp_moi.ma_so):
                QMessageBox.warning(self, "Lỗi", "Mã sản phẩm này đã tồn tại trong kho!")
                return
                
            # Thêm vào Danh Sách Liên Kết Đôi
            self.danh_sach.them_vao_cuoi(sp_moi)
            self.luu_du_lieu_ra_file()
            self.cap_nhat_bang_hien_thi()
            QMessageBox.information(self, "Thành công", "Đã lưu mặt hàng mới thành công!")

    def xu_ly_xoa_san_pham(self):
        dong_dang_chon = self.bang_du_lieu.currentRow()
        if dong_dang_chon < 0:
            QMessageBox.warning(self, "Cảnh Báo", "Bạn chưa click chọn sản phẩm nào trên bảng!")
            return
            
        ma_so = self.bang_du_lieu.item(dong_dang_chon, 0).text()
        
        # Hộp thoại cảnh báo
        xac_nhan = QMessageBox.question(
            self, "Xác nhận xóa", 
            f"Bạn có chắc chắn muốn xóa vĩnh viễn sản phẩm mã '{ma_so}'?", 
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if xac_nhan == QMessageBox.StandardButton.Yes:
            # Xóa khỏi danh sách liên kết
            thanh_cong = self.danh_sach.xoa_nut_theo_ma(ma_so)
            if thanh_cong:
                self.luu_du_lieu_ra_file()
                self.cap_nhat_bang_hien_thi()
                QMessageBox.information(self, "Thành công", "Đã xóa xong!")
            else:
                QMessageBox.warning(self, "Lỗi", "Không thể xóa. Có lỗi xảy ra.")

    def xu_ly_tim_kiem(self):
        tu_khoa = self.nhap_tim_kiem.text().strip().lower()
        if not tu_khoa:
            self.cap_nhat_bang_hien_thi() # Trả về tất cả nếu không nhập gì
            return
            
        ket_qua = []
        for sp in self.danh_sach.duyet_danh_sach():
            # Tìm kiếm theo Mã hoặc Tên
            if tu_khoa in sp.ma_so.lower() or tu_khoa in sp.ten.lower():
                ket_qua.append(sp)
                
        self.hien_thi_mang_len_bang(ket_qua)

    def xu_ly_sap_xep(self):
        lua_chon = self.cb_sap_xep.currentText()
        
        if lua_chon == "Giá tăng dần":
            self.danh_sach.sap_xep(tieu_chi="gia_ban", tang_dan=True)
        elif lua_chon == "Giá giảm dần":
            self.danh_sach.sap_xep(tieu_chi="gia_ban", tang_dan=False)
        elif lua_chon == "Tên A-Z":
            self.danh_sach.sap_xep(tieu_chi="ten", tang_dan=True)
        elif lua_chon == "Tên Z-A":
            self.danh_sach.sap_xep(tieu_chi="ten", tang_dan=False)
        elif lua_chon == "Số lượng tồn kho":
            self.danh_sach.sap_xep(tieu_chi="so_luong", tang_dan=True)
        
        self.cap_nhat_bang_hien_thi()
        QMessageBox.information(self, "Thuật Toán", f"Đã áp dụng Merge Sort trên Danh sách liên kết để sắp xếp: {lua_chon}")

    def xu_ly_thong_ke(self):
        mang_du_lieu = self.danh_sach.duyet_danh_sach()
        if not mang_du_lieu:
            QMessageBox.information(self, "Thống kê", "Kho hàng hiện đang trống!")
            return
            
        tong_san_pham = len(mang_du_lieu)
        dat_nhat = max(mang_du_lieu, key=lambda x: x.gia_ban)
        re_nhat = min(mang_du_lieu, key=lambda x: x.gia_ban)
        
        san_pham_sap_het = [sp.ten for sp in mang_du_lieu if sp.so_luong < 5]
        canh_bao_sl = ", ".join(san_pham_sap_het) if san_pham_sap_het else "Không có"
        
        van_ban_thong_ke = (
            f"📊 TỔNG QUAN KHO HÀNG:\n\n"
            f"- Tổng số mặt hàng khác nhau: {tong_san_pham}\n"
            f"- Sản phẩm đắt tiền nhất: {dat_nhat.ten} (Giá: {dat_nhat.gia_ban:,.0f} đ)\n"
            f"- Sản phẩm rẻ tiền nhất: {re_nhat.ten} (Giá: {re_nhat.gia_ban:,.0f} đ)\n\n"
            f"⚠️ CẢNH BÁO SẮP HẾT HÀNG (< 5 cái):\n"
            f"- {canh_bao_sl}"
        )
        QMessageBox.information(self, "Báo Cáo Thống Kê", van_ban_thong_ke)

    # ================== CÁC HÀM HIỂN THỊ VÀ LƯU TRỮ ==================
    def cap_nhat_bang_hien_thi(self):
        # Lấy toàn bộ mảng từ LinkedList
        tat_ca = self.danh_sach.duyet_danh_sach()
        self.hien_thi_mang_len_bang(tat_ca)

    def hien_thi_mang_len_bang(self, mang_san_pham):
        self.bang_du_lieu.setRowCount(0) # Xóa trắng bảng
        for sp in mang_san_pham:
            dong_moi = self.bang_du_lieu.rowCount()
            self.bang_du_lieu.insertRow(dong_moi)
            
            # Tính đa hình: lấy tên Class của đối tượng
            loai_sp = sp.__class__.__name__ 
            if loai_sp == "Sach": loai_sp = "Sách"
            elif loai_sp == "TapChi": loai_sp = "Tạp Chí"
            elif loai_sp == "LuanVan": loai_sp = "Luận Văn"
            elif loai_sp == "BanThao": loai_sp = "Bản Thảo"
            
            self.bang_du_lieu.setItem(dong_moi, 0, QTableWidgetItem(sp.ma_so))
            self.bang_du_lieu.setItem(dong_moi, 1, QTableWidgetItem(loai_sp))
            self.bang_du_lieu.setItem(dong_moi, 2, QTableWidgetItem(sp.ten))
            self.bang_du_lieu.setItem(dong_moi, 3, QTableWidgetItem(f"{sp.gia_ban:,.0f} đ"))
            self.bang_du_lieu.setItem(dong_moi, 4, QTableWidgetItem(str(sp.so_luong)))
            
            # Nối thông tin riêng
            thong_tin = ""
            if isinstance(sp, Sach): thong_tin = f"TG: {sp.tac_gia} | NXB: {sp.nha_xuat_ban}"
            elif isinstance(sp, TapChi): thong_tin = f"Số PH: {sp.so_phat_hanh}"
            elif isinstance(sp, Bao): thong_tin = f"Ngày PH: {sp.ngay_phat_hanh}"
            elif isinstance(sp, LuanVan): thong_tin = f"Trường ĐH: {sp.truong_dai_hoc}"
            elif isinstance(sp, BanThao): thong_tin = f"Trạng thái: {sp.tinh_trang}"
            
            self.bang_du_lieu.setItem(dong_moi, 5, QTableWidgetItem(thong_tin))

    def doc_du_lieu_tu_file(self):
        from data.sqlite_db import doc_du_lieu_sqlite
        try:
            mang_sp = doc_du_lieu_sqlite()
            for sp in mang_sp:
                self.danh_sach.them_vao_cuoi(sp)
            self.cap_nhat_bang_hien_thi()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi Nghiêm Trọng", f"Lỗi CSDL SQLite: {str(e)}")

    def luu_du_lieu_ra_file(self):
        from data.sqlite_db import luu_du_lieu_sqlite
        mang_tam = self.danh_sach.duyet_danh_sach()
        try:
            luu_du_lieu_sqlite(mang_tam)
        except Exception as e:
            QMessageBox.critical(self, "Lỗi Nghiêm Trọng", f"Không thể lưu vào SQLite: {str(e)}")
