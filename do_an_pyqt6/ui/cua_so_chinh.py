"""
Tệp cua_so_chinh.py — Cửa sổ chính (PyQt6)
============================================

Sử dụng QMainWindow với:
    - QToolBar: thanh công cụ.
    - QTableWidget: bảng dữ liệu.
    - QDockWidget: panel giỏ hàng (có thể ẩn/hiện).
    - QStatusBar: thanh trạng thái.
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QHeaderView, QPushButton, QLabel, QComboBox,
    QLineEdit, QMessageBox, QToolBar, QStatusBar, QGroupBox,
    QFormLayout, QDockWidget, QFrame, QInputDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction

from ui.hop_thoai_them_sua import CuaSoThemSua
from ui.dang_nhap import CuaSoDangNhap


class CuaSoChinh(QMainWindow):
    """Cửa sổ chính của ứng dụng PyQt6."""

    def __init__(self, quan_ly, nguoi_dung):
        super().__init__()
        self.quan_ly = quan_ly
        self.nguoi_dung = nguoi_dung

        self.setWindowTitle(f'Quản lý nhà sách — {nguoi_dung.ho_ten} ({nguoi_dung.vai_tro})')
        self.resize(1200, 750)

        self._tao_thanh_cong_cu()
        self._tao_khung_trung_tam()
        self._tao_dock_gio_hang()
        self._tao_thanh_trang_thai()

        # Tải dữ liệu ban đầu.
        self._cap_nhat_bang()
        self._cap_nhat_thong_ke()
        self._cap_nhat_gio_hang()
        self._cap_nhat_nut_undoredo()

    # ========================================================
    # THANH CÔNG CỤ
    # ========================================================
    def _tao_thanh_cong_cu(self):
        """Tạo toolbar với các nút bấm."""
        toolbar = QToolBar('Thanh công cụ chính')
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        # Nút Thêm.
        act_them = QAction('➕ Thêm', self)
        act_them.triggered.connect(self._them_san_pham)
        toolbar.addAction(act_them)

        # Nút Sửa.
        act_sua = QAction('✏ Sửa', self)
        act_sua.triggered.connect(self._sua_san_pham)
        toolbar.addAction(act_sua)

        # Nút Xóa.
        act_xoa = QAction('🗑 Xóa', self)
        act_xoa.triggered.connect(self._xoa_san_pham)
        toolbar.addAction(act_xoa)

        toolbar.addSeparator()

        # Nút Undo.
        self.act_undo = QAction('↶ Hoàn tác', self)
        self.act_undo.triggered.connect(self._hoan_tac)
        toolbar.addAction(self.act_undo)

        # Nút Redo.
        self.act_redo = QAction('↷ Làm lại', self)
        self.act_redo.triggered.connect(self._lam_lai)
        toolbar.addAction(self.act_redo)

        toolbar.addSeparator()

        # Widget tìm kiếm (chèn vào toolbar).
        toolbar.addWidget(QLabel(' Tìm: '))
        self.edit_tk = QLineEdit()
        self.edit_tk.setPlaceholderText('Từ khóa...')
        self.edit_tk.setFixedWidth(150)
        self.edit_tk.returnPressed.connect(self._tim_kiem)
        toolbar.addWidget(self.edit_tk)

        self.combo_tk = QComboBox()
        self.combo_tk.addItems(['ten', 'ma', 'loai'])
        self.combo_tk.setFixedWidth(80)
        toolbar.addWidget(self.combo_tk)

        btn_tim = QPushButton('Tìm')
        btn_tim.clicked.connect(self._tim_kiem)
        toolbar.addWidget(btn_tim)

        btn_lam_moi = QPushButton('↻ Làm mới')
        btn_lam_moi.clicked.connect(self._lam_moi)
        toolbar.addWidget(btn_lam_moi)

        toolbar.addSeparator()

        # Widget sắp xếp.
        toolbar.addWidget(QLabel(' Sắp xếp: '))
        self.combo_sx = QComboBox()
        self.combo_sx.addItems(['gia_ban', 'ten_san_pham', 'ton_kho'])
        self.combo_sx.setFixedWidth(130)
        toolbar.addWidget(self.combo_sx)

        btn_sx = QPushButton('Sắp xếp')
        btn_sx.clicked.connect(self._sap_xep)
        toolbar.addWidget(btn_sx)

        # Spacer đẩy các nút bên phải.
        spacer = QWidget()
        spacer.setFixedWidth(20)
        toolbar.addWidget(spacer)

        # Nút đăng xuất (bên phải).
        toolbar.addSeparator()
        lbl_user = QLabel(f' {self.nguoi_dung.ho_ten} ({self.nguoi_dung.vai_tro}) ')
        toolbar.addWidget(lbl_user)
        act_dx = QAction('🚪 Đăng xuất', self)
        act_dx.triggered.connect(self._dang_xuat)
        toolbar.addAction(act_dx)

    # ========================================================
    # KHUNG TRUNG TÂM: BẢNG + THỐNG KÊ
    # ========================================================
    def _tao_khung_trung_tam(self):
        """Tạo widget trung tâm: bảng sản phẩm + group thống kê."""
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setContentsMargins(8, 8, 8, 8)

        # --- Nhóm thống kê (đặt lên đầu) ---
        group_tk = QGroupBox('📊 Thống kê')
        form_tk = QFormLayout()
        form_tk.setContentsMargins(10, 5, 10, 5)
        self.lbl_tong_so = QLabel('0')
        self.lbl_dat = QLabel('-')
        self.lbl_re = QLabel('-')
        self.lbl_tri_kho = QLabel('0đ')
        self.lbl_sap_het = QLabel('0')
        self.lbl_sap_het.setStyleSheet('color: red;')
        form_tk.addRow('Tổng số:', self.lbl_tong_so)
        form_tk.addRow('Đắt nhất:', self.lbl_dat)
        form_tk.addRow('Rẻ nhất:', self.lbl_re)
        form_tk.addRow('Tổng giá trị kho:', self.lbl_tri_kho)
        form_tk.addRow('Sắp hết (<5):', self.lbl_sap_het)
        group_tk.setLayout(form_tk)
        group_tk.setFixedHeight(110)
        layout.addWidget(group_tk)

        # --- Bảng sản phẩm ---
        group_bang = QGroupBox('Danh sách sản phẩm')
        layout_bang = QVBoxLayout(group_bang)
        self.bang = QTableWidget(0, 7)
        self.bang.setHorizontalHeaderLabels([
            'Mã số', 'Tên sản phẩm', 'Loại', 'Giá cơ bản',
            'Tồn kho', 'Giá bán', 'Thông tin riêng'
        ])
        # Cho phép các cột tự co giãn.
        self.bang.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.bang.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.bang.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)
        self.bang.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.bang.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        # Double-click → mở dialog Sửa.
        self.bang.doubleClicked.connect(self._sua_san_pham)
        layout_bang.addWidget(self.bang)
        layout.addWidget(group_bang, 1)

        self.setCentralWidget(central)

    # ========================================================
    # DOCK GIỎ HÀNG (bên phải)
    # ========================================================
    def _tao_dock_gio_hang(self):
        """Tạo QDockWidget chứa giỏ hàng."""
        dock = QDockWidget('🛒 Giỏ hàng (Queue FIFO)', self)
        dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetMovable |
                         QDockWidget.DockWidgetFeature.DockWidgetClosable)

        # Widget chứa nội dung dock.
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Bảng giỏ hàng.
        self.bang_gio = QTableWidget(0, 4)
        self.bang_gio.setHorizontalHeaderLabels(['Mã', 'Tên', 'Giá bán', 'Loại'])
        self.bang_gio.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.bang_gio.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.bang_gio.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.bang_gio, 1)

        # Tổng tiền.
        self.lbl_tong_gio = QLabel('Tổng: 0đ (0 món)')
        self.lbl_tong_gio.setStyleSheet('font-size: 11pt; font-weight: bold; color: green;')
        self.lbl_tong_gio.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.lbl_tong_gio)

        # Nút thao tác giỏ.
        frame_nut = QHBoxLayout()
        btn_them_gio = QPushButton('+ Thêm vào giỏ')
        btn_them_gio.clicked.connect(self._them_vao_gio)
        frame_nut.addWidget(btn_them_gio)
        btn_xoa_gio = QPushButton('- Bỏ')
        btn_xoa_gio.clicked.connect(self._xoa_khoi_gio)
        frame_nut.addWidget(btn_xoa_gio)
        btn_tt = QPushButton('💰 Thanh toán')
        btn_tt.clicked.connect(self._thanh_toan)
        btn_tt.setStyleSheet('background-color: #4CAF50; color: white; font-weight: bold;')
        frame_nut.addWidget(btn_tt)
        layout.addLayout(frame_nut)

        dock.setWidget(widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

    # ========================================================
    # THANH TRẠNG THÁI
    # ========================================================
    def _tao_thanh_trang_thai(self):
        """Tạo QStatusBar."""
        self.lbl_trang_thai = QLabel('Sẵn sàng.')
        sb = QStatusBar()
        sb.addWidget(self.lbl_trang_thai)
        self.setStatusBar(sb)

    # ========================================================
    # CẬP NHẬT UI
    # ========================================================
    def _cap_nhat_bang(self, danh_sach=None):
        """Vẽ lại bảng sản phẩm."""
        if danh_sach is None:
            danh_sach = self.quan_ly.lay_danh_sach()

        self.bang.setRowCount(0)  # Xóa hết dòng.
        for sp in danh_sach:
            row = self.bang.rowCount()
            self.bang.insertRow(row)
            self.bang.setItem(row, 0, QTableWidgetItem(sp.get('ma_so', '')))
            self.bang.setItem(row, 1, QTableWidgetItem(sp.get('ten_san_pham', '')))
            self.bang.setItem(row, 2, QTableWidgetItem(sp.get('loai_hang', '')))
            self.bang.setItem(row, 3, QTableWidgetItem(f"{sp.get('gia_co_ban', 0):,.0f}"))
            self.bang.setItem(row, 4, QTableWidgetItem(str(sp.get('ton_kho', 0))))
            self.bang.setItem(row, 5, QTableWidgetItem(f"{sp.get('gia_ban', 0):,.0f}"))
            self.bang.setItem(row, 6, QTableWidgetItem(self._str_truong_rieng(sp)))

        self.lbl_trang_thai.setText(f'Đã tải {len(danh_sach)} mặt hàng.')

    def _str_truong_rieng(self, sp):
        """Chuỗi hiển thị thông tin riêng theo loại."""
        loai = sp.get('loai_hang', '')
        if loai == 'Sách':
            return f"Tác giả: {sp.get('tac_gia', '')} | NXB: {sp.get('nha_xuat_ban', '')}"
        elif loai == 'Tạp chí':
            return f"Số phát hành: {sp.get('so_phat_hanh', '')}"
        elif loai == 'Báo giấy':
            return f"Ngày XB: {sp.get('ngay_xuat_ban', '')}"
        elif loai == 'Luận văn':
            return f"Tác giả: {sp.get('tac_gia', '')} | Trường: {sp.get('truong_dai_hoc', '')}"
        elif loai == 'Bản thảo':
            return f"Tác giả: {sp.get('tac_gia', '')} | TT: {sp.get('tinh_trang', '')}"
        return ''

    def _cap_nhat_thong_ke(self):
        """Cập nhật các label thống kê."""
        tk = self.quan_ly.lay_thong_ke()
        if not tk:
            return
        self.lbl_tong_so.setText(f"{tk.get('tong_so', 0)} mặt hàng")
        self.lbl_dat.setText(str(tk.get('dat_nhat', '-')))
        self.lbl_re.setText(str(tk.get('re_nhat', '-')))
        self.lbl_tri_kho.setText(f"{tk.get('tong_gia_tri_kho', 0):,.0f}đ")
        self.lbl_sap_het.setText(str(len(tk.get('sap_het_hang', []))))

    def _cap_nhat_gio_hang(self):
        """Vẽ lại bảng giỏ + tổng."""
        self.bang_gio.setRowCount(0)
        ds, tong, sl = self.quan_ly.xem_gio_hang()
        for mon in ds:
            row = self.bang_gio.rowCount()
            self.bang_gio.insertRow(row)
            self.bang_gio.setItem(row, 0, QTableWidgetItem(mon.get('ma_so', '')))
            self.bang_gio.setItem(row, 1, QTableWidgetItem(mon.get('ten_san_pham', '')))
            self.bang_gio.setItem(row, 2, QTableWidgetItem(f"{mon.get('gia_ban', 0):,.0f}"))
            self.bang_gio.setItem(row, 3, QTableWidgetItem(mon.get('loai_hang', '')))
        self.lbl_tong_gio.setText(f'Tổng: {tong:,.0f}đ ({sl} món)')

    def _cap_nhat_nut_undoredo(self):
        """Bật/tắt action Undo/Redo."""
        tt = self.quan_ly.trang_thai_undoredo()
        self.act_undo.setEnabled(tt['co_the_undo'])
        self.act_redo.setEnabled(tt['co_the_redo'])

    # ========================================================
    # XỬ LÝ SỰ KIỆN
    # ========================================================
    def _them_san_pham(self):
        hop = CuaSoThemSua(self.quan_ly, du_lieu_cu=None, parent=self)
        if hop.exec() == 1:  # Accepted.
            self._cap_nhat_bang()
            self._cap_nhat_thong_ke()
            self._cap_nhat_nut_undoredo()

    def _sua_san_pham(self):
        row = self.bang.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Chưa chọn', 'Vui lòng chọn 1 dòng để sửa.')
            return
        ma = self.bang.item(row, 0).text()
        sp = self.quan_ly.danh_sach.tim_theo_ma_so(ma)
        if sp is None:
            QMessageBox.critical(self, 'Lỗi', f'Không tìm thấy sản phẩm {ma}.')
            return
        hop = CuaSoThemSua(self.quan_ly, du_lieu_cu=sp.chuyen_thanh_dict(), parent=self)
        if hop.exec() == 1:
            self._cap_nhat_bang()
            self._cap_nhat_thong_ke()
            self._cap_nhat_nut_undoredo()

    def _xoa_san_pham(self):
        row = self.bang.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Chưa chọn', 'Vui lòng chọn 1 dòng để xóa.')
            return
        ma = self.bang.item(row, 0).text()
        if QMessageBox.question(self, 'Xác nhận',
                                f'Bạn có chắc muốn xóa sản phẩm "{ma}"?') \
           != QMessageBox.StandardButton.Yes:
            return
        ok, msg = self.quan_ly.xoa_san_pham(ma)
        if ok:
            QMessageBox.information(self, 'Thành công', msg)
            self._cap_nhat_bang()
            self._cap_nhat_thong_ke()
            self._cap_nhat_nut_undoredo()
        else:
            QMessageBox.critical(self, 'Lỗi', msg)

    def _tim_kiem(self):
        tu = self.edit_tk.text().strip()
        tc = self.combo_tk.currentText()
        kq = self.quan_ly.tim_kiem(tu, tc)
        self._cap_nhat_bang(kq)
        self.lbl_trang_thai.setText(f'Tìm thấy {len(kq)} kết quả cho "{tu}".')

    def _sap_xep(self):
        tc = self.combo_sx.currentText()
        kq = self.quan_ly.sap_xep(tc)
        self._cap_nhat_bang(kq)
        self.lbl_trang_thai.setText(f'Đã sắp xếp theo {tc}.')

    def _lam_moi(self):
        self._cap_nhat_bang()
        self._cap_nhat_thong_ke()

    def _hoan_tac(self):
        ok, msg = self.quan_ly.hoan_tac()
        if ok:
            self._cap_nhat_bang()
            self._cap_nhat_thong_ke()
            self._cap_nhat_nut_undoredo()
            self.lbl_trang_thai.setText(msg)
        else:
            QMessageBox.information(self, 'Thông báo', msg)

    def _lam_lai(self):
        ok, msg = self.quan_ly.lam_lai()
        if ok:
            self._cap_nhat_bang()
            self._cap_nhat_thong_ke()
            self._cap_nhat_nut_undoredo()
            self.lbl_trang_thai.setText(msg)
        else:
            QMessageBox.information(self, 'Thông báo', msg)

    def _them_vao_gio(self):
        row = self.bang.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Chưa chọn', 'Vui lòng chọn 1 dòng để thêm vào giỏ.')
            return
        ma = self.bang.item(row, 0).text()
        ok, msg = self.quan_ly.them_vao_gio(ma)
        if ok:
            self._cap_nhat_gio_hang()
            self.lbl_trang_thai.setText(msg)
        else:
            QMessageBox.critical(self, 'Lỗi', msg)

    def _xoa_khoi_gio(self):
        row = self.bang_gio.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Chưa chọn', 'Vui lòng chọn món cần bỏ.')
            return
        ma = self.bang_gio.item(row, 0).text()
        ok, msg = self.quan_ly.xoa_khoi_gio(ma)
        if ok:
            self._cap_nhat_gio_hang()
        else:
            QMessageBox.critical(self, 'Lỗi', msg)

    def _thanh_toan(self):
        ok, msg, hoa_don = self.quan_ly.thanh_toan()
        if ok:
            chi_tiet = '\n'.join([f"  - {m['ten_san_pham']}: {m['gia_ban']:,.0f}đ"
                                   for m in hoa_don['cac_mon']])
            QMessageBox.information(self, 'Thanh toán thành công',
                                     f"{msg}\n\nChi tiết:\n{chi_tiet}\n\n"
                                     f"Tổng: {hoa_don['tong_tien']:,.0f}đ")
            self._cap_nhat_gio_hang()
        else:
            QMessageBox.warning(self, 'Thông báo', msg)

    # ========================================================
    # ĐĂNG XUẤT
    # ========================================================
    def _dang_xuat(self):
        if QMessageBox.question(self, 'Xác nhận', 'Bạn có chắc muốn đăng xuất?') \
           != QMessageBox.StandardButton.Yes:
            return
        self.quan_ly.dang_xuat()
        self.hide()
        hop = CuaSoDangNhap(self.quan_ly, parent=self)
        if hop.exec() == 1:  # Accepted = login OK.
            self.nguoi_dung = hop.nguoi_dung
            self.setWindowTitle(f'Quản lý nhà sách — {self.nguoi_dung.ho_ten} '
                                f'({self.nguoi_dung.vai_tro})')
            self.show()
            self._cap_nhat_bang()
            self._cap_nhat_thong_ke()
            self._cap_nhat_gio_hang()
            self._cap_nhat_nut_undoredo()
        else:
            # User hủy → thoát app.
            self.close()
