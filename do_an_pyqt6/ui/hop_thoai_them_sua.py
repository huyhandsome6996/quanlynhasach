"""
Tệp hop_thoai_them_sua.py — Hộp thoại Thêm/Sửa sản phẩm (PyQt6)
==================================================================

Một lớp dùng chung cho Thêm và Sửa. Tự động sinh các trường riêng
theo loại hàng (Sách/Tạp chí/Báo giấy/Luận văn/Bản thảo).
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QComboBox,
    QPushButton, QMessageBox, QHBoxLayout, QFrame, QLabel
)


# 5 loại hàng hỗ trợ.
CAC_LOAI_HANG = ['Sách', 'Tạp chí', 'Báo giấy', 'Luận văn', 'Bản thảo']

# Định nghĩa trường riêng cho từng loại.
TRUONG_RIENG = {
    'Sách':      [('tac_gia', 'Tác giả:'), ('nha_xuat_ban', 'Nhà xuất bản:')],
    'Tạp chí':   [('so_phat_hanh', 'Số phát hành:')],
    'Báo giấy':  [('ngay_xuat_ban', 'Ngày xuất bản:')],
    'Luận văn':  [('tac_gia', 'Tác giả:'), ('truong_dai_hoc', 'Trường ĐH:')],
    'Bản thảo':  [('tac_gia', 'Tác giả:'), ('trang_thai', 'Tình trạng:')],
}


class CuaSoThemSua(QDialog):
    """Hộp thoại Thêm hoặc Sửa sản phẩm."""

    def __init__(self, quan_ly, du_lieu_cu=None, parent=None):
        """
        quan_ly    : QuanLyTrungTam.
        du_lieu_cu : None = Thêm mới; dict = Sửa.
        """
        super().__init__(parent)
        self.quan_ly = quan_ly
        self.du_lieu_cu = du_lieu_cu
        self.ket_qua = None  # Sẽ chứa dict nếu user bấm Lưu.

        self.setWindowTitle('Sửa sản phẩm' if du_lieu_cu else 'Thêm sản phẩm')
        self.setFixedSize(450, 550)

        # Dict lưu các QLineEdit của trường riêng.
        self.entries_rieng = {}

        self._tao_giao_dien()

    def _tao_giao_dien(self):
        """Tạo form."""
        layout = QVBoxLayout(self)

        # Form layout cho các trường chung.
        form_chung = QFormLayout()

        # Combobox chọn loại.
        self.combo_loai = QComboBox()
        self.combo_loai.addItems(CAC_LOAI_HANG)
        self.combo_loai.currentTextChanged.connect(self._cap_nhat_truong_rieng)
        form_chung.addRow('Loại hàng:', self.combo_loai)

        # Entry mã số.
        self.edit_ma = QLineEdit()
        form_chung.addRow('Mã số:', self.edit_ma)

        # Entry tên.
        self.edit_ten = QLineEdit()
        form_chung.addRow('Tên sản phẩm:', self.edit_ten)

        # Entry giá.
        self.edit_gia = QLineEdit()
        form_chung.addRow('Giá cơ bản (đ):', self.edit_gia)

        # Entry tồn kho.
        self.edit_ton = QLineEdit()
        form_chung.addRow('Tồn kho:', self.edit_ton)

        layout.addLayout(form_chung)

        # Đường kẻ phân tách.
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(separator)

        # Tiêu đề phần trường riêng.
        layout.addWidget(QLabel('Thông tin riêng theo loại:'))

        # Container cho các trường riêng (động).
        self.form_rieng = QFormLayout()
        layout.addLayout(self.form_rieng)

        layout.addStretch()

        # Nút bấm.
        frame_nut = QHBoxLayout()
        frame_nut.addStretch()
        btn_luu = QPushButton('Lưu')
        btn_luu.clicked.connect(self._luu)
        btn_huy = QPushButton('Hủy')
        btn_huy.clicked.connect(self.reject)
        frame_nut.addWidget(btn_luu)
        frame_nut.addWidget(btn_huy)
        layout.addLayout(frame_nut)

        # Nếu là Sửa → đổ dữ liệu cũ.
        if self.du_lieu_cu:
            loai = self.du_lieu_cu.get('loai_hang', '')
            idx = self.combo_loai.findText(loai)
            if idx >= 0:
                self.combo_loai.setCurrentIndex(idx)
            # Khóa combobox (không cho đổi loại khi sửa).
            self.combo_loai.setEnabled(False)

            self.edit_ma.setText(self.du_lieu_cu.get('ma_so', ''))
            self.edit_ma.setReadOnly(True)  # Mã không đổi khi sửa.
            self.edit_ten.setText(self.du_lieu_cu.get('ten_san_pham', ''))
            self.edit_gia.setText(str(self.du_lieu_cu.get('gia_co_ban', '')))
            self.edit_ton.setText(str(self.du_lieu_cu.get('ton_kho', '')))

        # Kích hoạt sinh trường riêng cho loại hiện tại.
        self._cap_nhat_truong_rieng()

    def _cap_nhat_truong_rieng(self):
        """Khi đổi loại → xóa các entry cũ + tạo entry mới."""
        # Xóa các widget cũ trong form_rieng.
        while self.form_rieng.count():
            item = self.form_rieng.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()
        self.entries_rieng.clear()

        loai = self.combo_loai.currentText()
        ds_truong = TRUONG_RIENG.get(loai, [])

        for key, label in ds_truong:
            edit = QLineEdit()
            # Nếu là sửa → đổ giá trị cũ.
            if self.du_lieu_cu and key in self.du_lieu_cu:
                edit.setText(str(self.du_lieu_cu[key]))
            elif key == 'trang_thai' and not self.du_lieu_cu:
                edit.setText('Chưa duyệt')
            self.form_rieng.addRow(label, edit)
            self.entries_rieng[key] = edit

    def _luu(self):
        """Đọc form → gọi QuanLyTrungTam → đóng dialog nếu OK."""
        du_lieu = {
            'loai_hang':    self.combo_loai.currentText().strip(),
            'ma_so':        self.edit_ma.text().strip(),
            'ten_san_pham': self.edit_ten.text().strip(),
            'gia_co_ban':   self.edit_gia.text().strip(),
            'ton_kho':      self.edit_ton.text().strip(),
        }
        for key, edit in self.entries_rieng.items():
            du_lieu[key] = edit.text().strip()

        # Gọi hàm Thêm hoặc Sửa.
        if self.du_lieu_cu:
            du_lieu['ma_so'] = self.du_lieu_cu['ma_so']
            ok, msg = self.quan_ly.sua_san_pham(du_lieu)
        else:
            ok, msg = self.quan_ly.them_san_pham(du_lieu)

        if ok:
            self.ket_qua = du_lieu
            QMessageBox.information(self, 'Thành công', msg)
            self.accept()
        else:
            QMessageBox.critical(self, 'Lỗi', msg)
