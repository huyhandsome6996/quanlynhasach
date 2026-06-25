# ================================================================
# 👤 PHỤ TRÁCH: PHAN ANH TÚ
# ----------------------------------------------------------------
# 📚 KIẾN THỨC CẦN HỌC ĐI THI:
#    1. PyQt6 - QDialog (hộp thoại pop-up)
#    2. Các widget cơ bản: QLabel, QLineEdit, QComboBox, QSpinBox,
#       QDoubleSpinBox, QPushButton
#    3. Layout: QVBoxLayout (xếp dọc), QHBoxLayout (xếp ngang)
#    4. Bắt sự kiện: .clicked.connect(tên_hàm)
#    5. Kiểm tra dữ liệu nhập (validation): bắt lỗi bỏ trống, sai định dạng
#    6. Tạo đối tượng OOP từ dữ liệu form (gọi constructor lớp con)
# ----------------------------------------------------------------
# 📝 NỘI DUNG FILE:
#    Hộp thoại HopThoaiThemMoi: dùng cho cả THÊM MỚI và SỬA sản phẩm.
#    Form tự ẩn/hiện ô nhập theo loại mặt hàng (Sách có 2 ô: tác giả
#    + NXB, còn Tạp chí chỉ có 1 ô: số phát hành).
# ================================================================

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QComboBox,
                             QMessageBox, QSpinBox, QDoubleSpinBox)
from models.subclasses import Sach, TapChi, Bao, LuanVan, BanThao


class HopThoaiThemMoi(QDialog):
    """
    Hộp thoại để THÊM MỚI hoặc SỬA một sản phẩm.
    - Nếu truyền `san_pham_cu=None`: chế độ THÊM MỚI.
    - Nếu truyền `san_pham_cu=<đối tượng>`: chế độ SỬA (điền sẵn dữ liệu).
    """

    def __init__(self, parent=None, san_pham_cu=None):
        super().__init__(parent)
        self.san_pham_moi = None  # Sẽ chứa đối tượng sau khi bấm "Lưu"

        # Nếu có sản phẩm cũ truyền vào thì là chế độ SỬA
        self.che_do_sua = (san_pham_cu is not None)
        self.san_pham_cu = san_pham_cu

        if self.che_do_sua:
            self.setWindowTitle("Sửa Thông Tin Sản Phẩm")
        else:
            self.setWindowTitle("Thêm Sản Phẩm Mới")

        self.resize(400, 380)
        self.thiet_lap_giao_dien()

        # Nếu đang sửa: điền sẵn dữ liệu cũ vào form
        if self.che_do_sua:
            self.dien_du_lieu_cu()

    def thiet_lap_giao_dien(self):
        layout_chinh = QVBoxLayout()

        # ----- CHỌN LOẠI SẢN PHẨM -----
        layout_loai = QHBoxLayout()
        layout_loai.addWidget(QLabel("Loại Sản Phẩm:"))
        self.cb_loai = QComboBox()
        self.cb_loai.addItems(["Sách", "Tạp Chí", "Báo", "Luận Văn", "Bản Thảo"])
        # Khi sửa thì KHÔNG cho đổi loại (đề phòng dữ liệu lộn xộn)
        if self.che_do_sua:
            self.cb_loai.setEnabled(False)
        else:
            self.cb_loai.currentTextChanged.connect(self.thay_doi_loai)
        layout_loai.addWidget(self.cb_loai)
        layout_chinh.addLayout(layout_loai)

        # ----- THÔNG TIN CHUNG (Mã, Tên, Giá cơ bản, Số lượng) -----
        self.nhap_ma = QLineEdit()
        self.nhap_ten = QLineEdit()

        self.nhap_gia = QDoubleSpinBox()
        self.nhap_gia.setMaximum(999999999)     # Giá tối đa
        self.nhap_gia.setMinimum(0)             # Giá không được âm (yêu cầu đề bài)
        self.nhap_gia.setSuffix(" VNĐ")

        self.nhap_sl = QSpinBox()
        self.nhap_sl.setMaximum(99999)          # Số lượng tối đa
        self.nhap_sl.setMinimum(0)              # Số lượng không được âm

        layout_chinh.addWidget(QLabel("Mã số:"))
        layout_chinh.addWidget(self.nhap_ma)
        layout_chinh.addWidget(QLabel("Tên sản phẩm:"))
        layout_chinh.addWidget(self.nhap_ten)
        layout_chinh.addWidget(QLabel("Giá cơ bản (VNĐ):"))
        layout_chinh.addWidget(self.nhap_gia)
        layout_chinh.addWidget(QLabel("Số lượng trong kho:"))
        layout_chinh.addWidget(self.nhap_sl)

        # ----- THÔNG TIN RIÊNG (Tùy loại mặt hàng) -----
        self.nhan_rieng_1 = QLabel("Tác giả:")
        self.nhap_rieng_1 = QLineEdit()
        self.nhan_rieng_2 = QLabel("Nhà xuất bản:")
        self.nhap_rieng_2 = QLineEdit()

        layout_chinh.addWidget(self.nhan_rieng_1)
        layout_chinh.addWidget(self.nhap_rieng_1)
        layout_chinh.addWidget(self.nhan_rieng_2)
        layout_chinh.addWidget(self.nhap_rieng_2)

        # ----- CÁC NÚT BẤM -----
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
        self.thay_doi_loai()  # Cập nhật label cho đúng loại ban đầu

    def thay_doi_loai(self):
        """Hiển thị đúng ô nhập liệu riêng theo từng loại mặt hàng."""
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
        else:  # Bản Thảo
            self.nhan_rieng_1.setText("Tình trạng (mới/cũ):")
            self.nhan_rieng_1.show()
            self.nhap_rieng_1.show()
            self.nhan_rieng_2.hide()
            self.nhap_rieng_2.hide()

    def dien_du_lieu_cu(self):
        """Điền sẵn dữ liệu sản phẩm cũ vào form (khi chế độ Sửa)."""
        sp = self.san_pham_cu
        # Đặt loại tương ứng
        ten_loai = sp.__class__.__name__
        bang_ten = {"Sach": "Sách", "TapChi": "Tạp Chí", "Bao": "Báo",
                    "LuanVan": "Luận Văn", "BanThao": "Bản Thảo"}
        self.cb_loai.setCurrentText(bang_ten.get(ten_loai, "Sách"))

        # Điền thông tin chung
        self.nhap_ma.setText(sp.ma_so)
        self.nhap_ma.setEnabled(False)  # Không cho đổi mã khi sửa
        self.nhap_ten.setText(sp.ten)
        self.nhap_gia.setValue(sp.gia_co_ban)
        self.nhap_sl.setValue(sp.so_luong)

        # Điền thông tin riêng
        if isinstance(sp, Sach):
            self.nhap_rieng_1.setText(sp.tac_gia)
            self.nhap_rieng_2.setText(sp.nha_xuat_ban)
        elif isinstance(sp, TapChi):
            self.nhap_rieng_1.setText(sp.so_phat_hanh)
        elif isinstance(sp, Bao):
            self.nhap_rieng_1.setText(sp.ngay_phat_hanh)
        elif isinstance(sp, LuanVan):
            self.nhap_rieng_1.setText(sp.truong_dai_hoc)
        elif isinstance(sp, BanThao):
            self.nhap_rieng_1.setText(sp.tinh_trang)

    def kiem_tra_va_luu(self):
        """Kiểm tra dữ liệu hợp lệ rồi mới tạo đối tượng sản phẩm."""
        ma = self.nhap_ma.text().strip()
        ten = self.nhap_ten.text().strip()

        # 1. Bắt lỗi: bắt buộc nhập Mã và Tên
        if not ma or not ten:
            QMessageBox.warning(self, "Lỗi Nhập Liệu",
                                "Vui lòng nhập đầy đủ Mã và Tên sản phẩm!")
            return

        # 2. Bắt lỗi: Giá và Số lượng không được âm (QSpinBox đã chặn, nhưng nhắc lại cho chắc)
        gia = self.nhap_gia.value()
        sl = self.nhap_sl.value()
        if gia < 0 or sl < 0:
            QMessageBox.warning(self, "Lỗi Nhập Liệu",
                                "Giá và số lượng không được âm!")
            return

        loai = self.cb_loai.currentText()
        thong_tin_1 = self.nhap_rieng_1.text().strip()
        thong_tin_2 = self.nhap_rieng_2.text().strip()

        # 3. Bắt lỗi dữ liệu riêng theo từng loại mặt hàng
        if loai == "Sách":
            if not thong_tin_1 or not thong_tin_2:
                QMessageBox.warning(self, "Thiếu Dữ Liệu",
                                    "Vui lòng nhập Tác giả và Nhà xuất bản!")
                return
            self.san_pham_moi = Sach(ma, ten, gia, sl, thong_tin_1, thong_tin_2)

        elif loai == "Tạp Chí":
            if not thong_tin_1:
                QMessageBox.warning(self, "Thiếu Dữ Liệu",
                                    "Vui lòng nhập Số phát hành!")
                return
            self.san_pham_moi = TapChi(ma, ten, gia, sl, thong_tin_1)

        elif loai == "Báo":
            if not thong_tin_1:
                QMessageBox.warning(self, "Thiếu Dữ Liệu",
                                    "Vui lòng nhập Ngày phát hành!")
                return
            # Bắt lỗi định dạng ngày dd/mm/yyyy
            if len(thong_tin_1) < 8:
                QMessageBox.warning(self, "Sai Định Dạng",
                                    "Ngày phát hành phải theo dạng dd/mm/yyyy!")
                return
            self.san_pham_moi = Bao(ma, ten, gia, sl, thong_tin_1)

        elif loai == "Luận Văn":
            if not thong_tin_1:
                QMessageBox.warning(self, "Thiếu Dữ Liệu",
                                    "Vui lòng nhập Trường Đại học!")
                return
            self.san_pham_moi = LuanVan(ma, ten, gia, sl, thong_tin_1)

        else:  # Bản Thảo
            if not thong_tin_1:
                QMessageBox.warning(self, "Thiếu Dữ Liệu",
                                    "Vui lòng nhập Tình trạng (mới/cũ)!")
                return
            # Bắt lỗi: tình trạng chỉ được là "mới" hoặc "cũ"
            if thong_tin_1.lower() not in ["mới", "cu", "cũ"]:
                QMessageBox.warning(self, "Sai Dữ Liệu",
                                    "Tình trạng chỉ được nhập: 'mới' hoặc 'cũ'!")
                return
            self.san_pham_moi = BanThao(ma, ten, gia, sl, thong_tin_1)

        # Tất cả hợp lệ → đóng hộp thoại, trả về Accepted
        self.accept()
