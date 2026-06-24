# ================================================================
# 👤 PHỤ TRÁCH: PHAN ANH TÚ
# ----------------------------------------------------------------
# 📚 KIẾN THỨC CẦN HỌC ĐI THI:
#    1. PyQt6 - QDialog + QLineEdit (ô nhập văn bản)
#    2. QLineEdit.EchoMode.Password - ẩn mật khẩu thành dấu chấm
#    3. Bắt sự kiện nhấn Enter: .returnPressed.connect(...)
#    4. Gọi hàm kiểm tra đăng nhập từ models.nguoi_dung
#    5. QMessageBox.warning / .critical / .information - hộp thoại thông báo
#    6. Đây là giao diện của tính năng "THÊM ĐIỂM": Đăng nhập phân quyền
# ----------------------------------------------------------------
# 📝 NỘI DUNG FILE:
#    Hộp thoại HopThoaiDangNhap: form nhập tên đăng nhập + mật khẩu.
#    Nếu đúng -> lưu người dùng vào self.nguoi_dung_hien_tai và đóng
#    hộp thoại (self.accept()). Nếu sai -> báo lỗi và xóa mật khẩu.
# ================================================================

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton,
                             QMessageBox, QFrame)
from PyQt6.QtCore import Qt
from models.nguoi_dung import kiem_tra_dang_nhap


class HopThoaiDangNhap(QDialog):
    """
    Màn hình ĐĂNG NHẬP PHÂN QUYỀN.
    - Admin    : toàn quyền (xem + thêm + sửa + xóa + giỏ hàng)
    - Nhân viên: KHÔNG được XÓA sản phẩm (chỉ xem + thêm + sửa + giỏ hàng)
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🔒 Đăng Nhập Hệ Thống")
        self.setFixedSize(400, 320)
        self.nguoi_dung_hien_tai = None  # Sẽ chứa thông tin người dùng sau khi đăng nhập thành công
        self.thiet_lap_giao_dien()

    def thiet_lap_giao_dien(self):
        layout_chinh = QVBoxLayout()
        layout_chinh.setSpacing(10)

        # ----- TIÊU ĐỀ -----
        nhan_tieu_de = QLabel("📚 QUẢN LÝ CỬA HÀNG SÁCH")
        nhan_tieu_de.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: #047857;"
            "padding: 10px;"
        )
        nhan_tieu_de.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_chinh.addWidget(nhan_tieu_de)

        nhan_phu = QLabel("Vui lòng đăng nhập để tiếp tục")
        nhan_phu.setStyleSheet("font-size: 13px; color: #6B7280;")
        nhan_phu.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_chinh.addWidget(nhan_phu)

        # ----- ĐƯỜNG KẺ NGĂN -----
        duong_ke = QFrame()
        duong_ke.setFrameShape(QFrame.Shape.HLine)
        duong_ke.setStyleSheet("color: #E5E7EB;")
        layout_chinh.addWidget(duong_ke)

        # ----- Ô NHẬP TÊN ĐĂNG NHẬP -----
        layout_chinh.addWidget(QLabel("👤 Tên đăng nhập:"))
        self.nhap_ten = QLineEdit()
        self.nhap_ten.setPlaceholderText("Nhập tên đăng nhập...")
        self.nhap_ten.returnPressed.connect(self.dang_nhap)
        layout_chinh.addWidget(self.nhap_ten)

        # ----- Ô NHẬP MẬT KHẨU -----
        layout_chinh.addWidget(QLabel("🔑 Mật khẩu:"))
        self.nhap_mat_khau = QLineEdit()
        self.nhap_mat_khau.setPlaceholderText("Nhập mật khẩu...")
        self.nhap_mat_khau.setEchoMode(QLineEdit.EchoMode.Password)
        self.nhap_mat_khau.returnPressed.connect(self.dang_nhap)
        layout_chinh.addWidget(self.nhap_mat_khau)

        # ----- NÚT ĐĂNG NHẬP / THOÁT -----
        layout_nut = QHBoxLayout()

        nut_dang_nhap = QPushButton("🚪 Đăng Nhập")
        nut_dang_nhap.setStyleSheet(
            "background-color: #047857; color: white; "
            "font-weight: bold; font-size: 14px; padding: 10px;"
        )
        nut_dang_nhap.clicked.connect(self.dang_nhap)

        nut_thoat = QPushButton("❌ Thoát")
        nut_thoat.setStyleSheet(
            "background-color: #9E9E9E; color: white; "
            "font-weight: bold; font-size: 14px; padding: 10px;"
        )
        nut_thoat.clicked.connect(self.reject)

        layout_nut.addWidget(nut_dang_nhap)
        layout_nut.addWidget(nut_thoat)
        layout_chinh.addLayout(layout_nut)

        # ----- HƯỚNG DẪN TÀI KHOẢN MẪU -----
        nhan_huong_dan = QLabel(
            "💡 Tài khoản mẫu:\n"
            "   • Admin    : admin / 123\n"
            "   • Nhân viên: nhanvien / 123"
        )
        nhan_huong_dan.setStyleSheet(
            "font-size: 12px; color: #6B7280; "
            "background-color: #F9FAFB; padding: 8px; "
            "border-radius: 4px;"
        )
        layout_chinh.addWidget(nhan_huong_dan)

        self.setLayout(layout_chinh)

    def dang_nhap(self):
        """Xử lý sự kiện bấm nút Đăng Nhập."""
        ten = self.nhap_ten.text().strip()
        mk = self.nhap_mat_khau.text().strip()

        # 1. Bắt lỗi bỏ trống
        if not ten or not mk:
            QMessageBox.warning(self, "Thiếu Thông Tin",
                                "Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu!")
            return

        # 2. Kiểm tra tài khoản
        nguoi = kiem_tra_dang_nhap(ten, mk)
        if nguoi is None:
            QMessageBox.critical(self, "Đăng Nhập Thất Bại",
                                 "Sai tên đăng nhập hoặc mật khẩu!\n"
                                 "Vui lòng thử lại.")
            # Xóa trắng ô mật khẩu để người dùng nhập lại
            self.nhap_mat_khau.clear()
            return

        # 3. Đăng nhập thành công → lưu lại + đóng hộp thoại
        self.nguoi_dung_hien_tai = nguoi
        QMessageBox.information(
            self, "Đăng Nhập Thành Công",
            f"Chào mừng '{nguoi.ten_dang_nhap}'!\n"
            f"Vai trò: {'Admin (toàn quyền)' if nguoi.la_admin() else 'Nhân viên (không được xóa)'}"
        )
        self.accept()
