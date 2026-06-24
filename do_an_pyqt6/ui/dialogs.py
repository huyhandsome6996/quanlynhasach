from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QComboBox, 
                             QMessageBox, QSpinBox, QDoubleSpinBox)
from models.subclasses import Sach, TapChi, Bao, LuanVan, BanThao

class HopThoaiThemMoi(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thêm Sản Phẩm Mới")
        self.resize(400, 350)
        self.thiet_lap_giao_dien()

    def thiet_lap_giao_dien(self):
        layout_chinh = QVBoxLayout()

        # Chọn Loại sản phẩm
        layout_loai = QHBoxLayout()
        layout_loai.addWidget(QLabel("Loại Sản Phẩm:"))
        self.cb_loai = QComboBox()
        self.cb_loai.addItems(["Sách", "Tạp Chí", "Báo", "Luận Văn", "Bản Thảo"])
        self.cb_loai.currentTextChanged.connect(self.thay_doi_loai)
        layout_loai.addWidget(self.cb_loai)
        layout_chinh.addLayout(layout_loai)

        # Thông tin chung (Mã, Tên, Giá, Số lượng)
        self.nhap_ma = QLineEdit()
        self.nhap_ten = QLineEdit()
        
        self.nhap_gia = QDoubleSpinBox()
        self.nhap_gia.setMaximum(999999999) # Giá tối đa
        self.nhap_gia.setSuffix(" VNĐ")
        
        self.nhap_sl = QSpinBox()
        self.nhap_sl.setMaximum(99999) # Số lượng tối đa

        layout_chinh.addWidget(QLabel("Mã số:"))
        layout_chinh.addWidget(self.nhap_ma)
        layout_chinh.addWidget(QLabel("Tên sản phẩm:"))
        layout_chinh.addWidget(self.nhap_ten)
        layout_chinh.addWidget(QLabel("Giá bán:"))
        layout_chinh.addWidget(self.nhap_gia)
        layout_chinh.addWidget(QLabel("Số lượng trong kho:"))
        layout_chinh.addWidget(self.nhap_sl)

        # Thông tin riêng biệt (Tùy loại mặt hàng)
        self.nhan_rieng_1 = QLabel("Tác giả:")
        self.nhap_rieng_1 = QLineEdit()
        self.nhan_rieng_2 = QLabel("Nhà xuất bản:")
        self.nhap_rieng_2 = QLineEdit()

        layout_chinh.addWidget(self.nhan_rieng_1)
        layout_chinh.addWidget(self.nhap_rieng_1)
        layout_chinh.addWidget(self.nhan_rieng_2)
        layout_chinh.addWidget(self.nhap_rieng_2)

        # Các Nút bấm
        layout_nut = QHBoxLayout()
        nut_luu = QPushButton("Lưu Dữ Liệu")
        nut_luu.setStyleSheet("background-color: #4CAF50; color: white;")
        nut_luu.clicked.connect(self.kiem_tra_va_luu)
        
        nut_huy = QPushButton("Hủy Bỏ")
        nut_huy.setStyleSheet("background-color: #f44336; color: white;")
        nut_huy.clicked.connect(self.reject)
        
        layout_nut.addWidget(nut_luu)
        layout_nut.addWidget(nut_huy)
        layout_chinh.addLayout(layout_nut)

        self.setLayout(layout_chinh)
        self.thay_doi_loai() # Chạy lần đầu để ẩn/hiện đúng

    def thay_doi_loai(self):
        loai = self.cb_loai.currentText()
        if loai == "Sách":
            self.nhan_rieng_1.setText("Tác giả:")
            self.nhan_rieng_2.setText("Nhà xuất bản:")
            self.nhan_rieng_1.show()
            self.nhap_rieng_1.show()
            self.nhan_rieng_2.show()
            self.nhap_rieng_2.show()
        elif loai == "Tạp Chí":
            self.nhan_rieng_1.setText("Số phát hành:")
            self.nhan_rieng_1.show()
            self.nhap_rieng_1.show()
            self.nhan_rieng_2.hide()
            self.nhap_rieng_2.hide()
        elif loai == "Báo":
            self.nhan_rieng_1.setText("Ngày phát hành (dd/mm/yyyy):")
            self.nhan_rieng_1.show()
            self.nhap_rieng_1.show()
            self.nhan_rieng_2.hide()
            self.nhap_rieng_2.hide()
        elif loai == "Luận Văn":
            self.nhan_rieng_1.setText("Trường Đại học:")
            self.nhan_rieng_1.show()
            self.nhap_rieng_1.show()
            self.nhan_rieng_2.hide()
            self.nhap_rieng_2.hide()
        else:
            self.nhan_rieng_1.setText("Tình trạng (mới/cũ):")
            self.nhan_rieng_1.show()
            self.nhap_rieng_1.show()
            self.nhan_rieng_2.hide()
            self.nhap_rieng_2.hide()

    def kiem_tra_va_luu(self):
        ma = self.nhap_ma.text().strip()
        ten = self.nhap_ten.text().strip()
        
        # Bắt lỗi không nhập liệu
        if not ma or not ten:
            QMessageBox.warning(self, "Lỗi Nhập Liệu", "Vui lòng nhập đầy đủ Mã và Tên sản phẩm!")
            return
        
        loai = self.cb_loai.currentText()
        gia = self.nhap_gia.value()
        sl = self.nhap_sl.value()
        thong_tin_1 = self.nhap_rieng_1.text().strip()
        thong_tin_2 = self.nhap_rieng_2.text().strip()

        # Áp dụng tính đa hình để tạo đúng Đối Tượng Lớp Con
        if loai == "Sách":
            self.san_pham_moi = Sach(ma, ten, gia, sl, thong_tin_1, thong_tin_2)
        elif loai == "Tạp Chí":
            self.san_pham_moi = TapChi(ma, ten, gia, sl, thong_tin_1)
        elif loai == "Báo":
            self.san_pham_moi = Bao(ma, ten, gia, sl, thong_tin_1)
        elif loai == "Luận Văn":
            self.san_pham_moi = LuanVan(ma, ten, gia, sl, thong_tin_1)
        else:
            self.san_pham_moi = BanThao(ma, ten, gia, sl, thong_tin_1)

        # Chấp nhận và đóng hộp thoại
        self.accept()
