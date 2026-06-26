"""
Tệp dang_nhap.py — Cửa sổ đăng nhập (PyQt6)
==============================================

Sử dụng QDialog + QFormLayout để tạo form đăng nhập.
Trả về NguoiDung nếu OK, None nếu hủy.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QLabel, QMessageBox, QHBoxLayout
)
from PyQt6.QtCore import Qt


class CuaSoDangNhap(QDialog):
    """Hộp thoại đăng nhập modal."""

    def __init__(self, quan_ly, parent=None):
        super().__init__(parent)
        self.quan_ly = quan_ly
        self.nguoi_dung = None  # Sẽ chứa NguoiDung nếu OK.

        self.setWindowTitle('Đăng nhập hệ thống')
        self.setFixedSize(380, 220)

        self._tao_giao_dien()

    def _tao_giao_dien(self):
        """Tạo form đăng nhập."""
        layout = QVBoxLayout(self)

        # Tiêu đề.
        title = QLabel('ĐĂNG NHẬP')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet('font-size: 16pt; font-weight: bold;')
        layout.addWidget(title)

        # Form layout: label + entry.
        form = QFormLayout()
        self.edit_ten = QLineEdit()
        self.edit_ten.setPlaceholderText('Tên đăng nhập')
        self.edit_mk = QLineEdit()
        self.edit_mk.setPlaceholderText('Mật khẩu')
        self.edit_mk.setEchoMode(QLineEdit.EchoMode.Password)

        form.addRow('Tên đăng nhập:', self.edit_ten)
        form.addRow('Mật khẩu:', self.edit_mk)
        layout.addLayout(form)

        # Nút.
        frame_nut = QHBoxLayout()
        self.btn_dn = QPushButton('Đăng nhập')
        self.btn_dn.setDefault(True)  # Enter → click nút này.
        self.btn_dn.clicked.connect(self._xu_ly_dang_nhap)
        self.btn_huy = QPushButton('Hủy')
        self.btn_huy.clicked.connect(self.reject)
        frame_nut.addStretch()
        frame_nut.addWidget(self.btn_dn)
        frame_nut.addWidget(self.btn_huy)
        layout.addLayout(frame_nut)

        # Gợi ý.
        hint = QLabel('(Mặc định: admin/123 hoặc nhanvien/123)')
        hint.setStyleSheet('color: gray;')
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(hint)

        # Focus vào ô tên.
        self.edit_ten.setFocus()

    def _xu_ly_dang_nhap(self):
        """Xử lý khi bấm nút Đăng nhập."""
        ten = self.edit_ten.text().strip()
        mk = self.edit_mk.text().strip()

        if not ten or not mk:
            QMessageBox.warning(self, 'Thiếu thông tin',
                                 'Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.')
            return

        ok, ket_qua = self.quan_ly.dang_nhap(ten, mk)
        if ok:
            self.nguoi_dung = ket_qua
            self.accept()  # Đóng dialog với mã QDialog.Accepted.
        else:
            QMessageBox.critical(self, 'Đăng nhập thất bại', ket_qua)
            self.edit_mk.clear()
            self.edit_mk.setFocus()
