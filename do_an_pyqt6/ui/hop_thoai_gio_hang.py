# ================================================================
# 👤 PHỤ TRÁCH: PHAN ANH TÚ
# ----------------------------------------------------------------
# 📚 KIẾN THỨC CẦN HỌC ĐI THI:
#    1. PyQt6 - QTableWidget (bảng hiển thị)
#    2. QTableWidgetItem - ô trong bảng
#    3. QHeaderView.ResizeMode.Stretch - tự động giãn cột
#    4. Truy cập đối tượng cha (parent) qua self.cua_so_cha
#    5. Vòng lặp while not <queue>.rong(): để duyệt + lấy ra FIFO
#    6. Đây là giao diện của tính năng "THÊM ĐIỂM": Giỏ hàng dùng Queue
# ----------------------------------------------------------------
# 📝 NỘI DUNG FILE:
#    Hộp thoại HopThoaiGioHang: bảng hiển thị các sản phẩm trong giỏ
#    (theo thứ tự FIFO), nút Bỏ khỏi giỏ, nút Thanh Toán (lấy từng món
#    ra theo FIFO, trừ tồn kho, lưu xuống SQLite).
# ================================================================

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QTableWidget,
                             QTableWidgetItem, QHeaderView, QMessageBox)


class HopThoaiGioHang(QDialog):
    """
    Hộp thoại hiển thị GIỎ HÀNG.
    - Bảng hiển thị các sản phẩm trong giỏ (theo thứ tự FIFO).
    - Nút "Bỏ Khỏi Giỏ" để xóa 1 món đang chọn.
    - Nút "Thanh Toán" để tính tiền và giảm tồn kho.
    - Nút "Đóng" để tắt hộp thoại.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🛒 Giỏ Hàng Của Bạn (Queue - FIFO)")
        self.resize(700, 450)
        self.cua_so_cha = parent  # Giữ tham chiếu tới cửa sổ chính để truy cập giỏ hàng
        self.thiet_lap_giao_dien()
        self.cap_nhat_bang_gio_hang()

    def thiet_lap_giao_dien(self):
        layout_chinh = QVBoxLayout()

        # ----- NHÃN HƯỚNG DẪN -----
        layout_chinh.addWidget(QLabel("Các sản phẩm trong giỏ (vào trước sẽ được thanh toán trước):"))

        # ----- BẢNG HIỂN THỊ GIỎ HÀNG -----
        self.bang_gio_hang = QTableWidget()
        self.bang_gio_hang.setColumnCount(5)
        self.bang_gio_hang.setHorizontalHeaderLabels(
            ["STT", "Mã Số", "Tên Sản Phẩm", "Loại", "Giá Bán"]
        )
        self.bang_gio_hang.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.bang_gio_hang.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout_chinh.addWidget(self.bang_gio_hang)

        # ----- NHÃN TỔNG TIỀN -----
        self.nhan_tong_tien = QLabel("💰 Tổng tiền: 0 đ")
        self.nhan_tong_tien.setStyleSheet("font-size: 16px; font-weight: bold; color: #2E7D32;")
        layout_chinh.addWidget(self.nhan_tong_tien)

        # ----- CÁC NÚT BẤM -----
        layout_nut = QHBoxLayout()

        nut_xoa = QPushButton("🗑️ Bỏ Khỏi Giỏ")
        nut_xoa.setStyleSheet("background-color: #f44336; color: white; font-weight: bold; padding: 8px;")
        nut_xoa.clicked.connect(self.xu_ly_xoa_khoi_gio)

        nut_thanh_toan = QPushButton("💳 Thanh Toán (FIFO)")
        nut_thanh_toan.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 8px;")
        nut_thanh_toan.clicked.connect(self.xu_ly_thanh_toan)

        nut_dong = QPushButton("Đóng")
        nut_dong.setStyleSheet("background-color: #9E9E9E; color: white; font-weight: bold; padding: 8px;")
        nut_dong.clicked.connect(self.close)

        layout_nut.addWidget(nut_xoa)
        layout_nut.addWidget(nut_thanh_toan)
        layout_nut.addWidget(nut_dong)
        layout_chinh.addLayout(layout_nut)

        self.setLayout(layout_chinh)

    def cap_nhat_bang_gio_hang(self):
        """Vẽ lại bảng hiển thị giỏ hàng + tính tổng tiền."""
        danh_sach_gio = self.cua_so_cha.gio_hang.xem_danh_sach()
        self.bang_gio_hang.setRowCount(0)

        tong_tien = 0.0
        bang_ten_loai = {
            "Sach": "Sách", "TapChi": "Tạp Chí", "Bao": "Báo",
            "LuanVan": "Luận Văn", "BanThao": "Bản Thảo"
        }

        for i, sp in enumerate(danh_sach_gio):
            dong_moi = self.bang_gio_hang.rowCount()
            self.bang_gio_hang.insertRow(dong_moi)

            loai = bang_ten_loai.get(sp.__class__.__name__, sp.__class__.__name__)
            gia_ban = sp.tinh_gia_ban()  # Gọi TÍNH ĐA HÌNH
            tong_tien += gia_ban

            self.bang_gio_hang.setItem(dong_moi, 0, QTableWidgetItem(str(i + 1)))
            self.bang_gio_hang.setItem(dong_moi, 1, QTableWidgetItem(sp.ma_so))
            self.bang_gio_hang.setItem(dong_moi, 2, QTableWidgetItem(sp.ten))
            self.bang_gio_hang.setItem(dong_moi, 3, QTableWidgetItem(loai))
            self.bang_gio_hang.setItem(dong_moi, 4, QTableWidgetItem(f"{gia_ban:,.0f} đ"))

        # Cập nhật nhãn tổng tiền
        self.nhan_tong_tien.setText(f"💰 Tổng tiền: {tong_tien:,.0f} đ")

    def xu_ly_xoa_khoi_gio(self):
        """Xóa sản phẩm đang chọn trong bảng ra khỏi giỏ hàng."""
        dong_dang_chon = self.bang_gio_hang.currentRow()
        if dong_dang_chon < 0:
            QMessageBox.warning(self, "Cảnh Báo", "Bạn chưa chọn món nào trong giỏ!")
            return

        ma_so = self.bang_gio_hang.item(dong_dang_chon, 1).text()
        self.cua_so_cha.gio_hang.xoa_theo_ma(ma_so)
        self.cap_nhat_bang_gio_hang()
        QMessageBox.information(self, "Thành Công", f"Đã bỏ món '{ma_so}' khỏi giỏ hàng!")

    def xu_ly_thanh_toan(self):
        """
        Thanh toán toàn bộ giỏ hàng theo thứ tự FIFO.
        - Lấy từng sản phẩm ra khỏi hàng đợi.
        - Giảm số lượng tồn kho của sản phẩm đó đi 1.
        - Lưu xuống CSDL.
        - Xóa sạch giỏ hàng.
        """
        if self.cua_so_cha.gio_hang.rong():
            QMessageBox.warning(self, "Cảnh Báo", "Giỏ hàng đang trống, không thể thanh toán!")
            return

        # Hỏi xác nhận trước khi thanh toán
        xac_nhan = QMessageBox.question(
            self, "Xác nhận thanh toán",
            "Bạn có chắc muốn thanh toán toàn bộ giỏ hàng?\n"
            "Tồn kho của từng sản phẩm sẽ bị trừ đi 1.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if xac_nhan != QMessageBox.StandardButton.Yes:
            return

        tong_tien = 0.0
        so_mon = 0

        # ----- BỌC TRY/EXCEPT ĐỂ CHƯƠNG TRÌNH KHÔNG BỊ CRASH KHI CÓ LỖI -----
        try:
            # Lấy từng món theo thứ tự FIFO (vào trước, ra trước)
            while not self.cua_so_cha.gio_hang.rong():
                sp = self.cua_so_cha.gio_hang.lay_ra()
                # Tìm sản phẩm trong kho để giảm tồn kho
                sp_trong_kho = self.cua_so_cha.danh_sach.tim_kiem_theo_ma(sp.ma_so)
                if sp_trong_kho is not None and sp_trong_kho.so_luong > 0:
                    sp_trong_kho.so_luong -= 1
                    tong_tien += sp.tinh_gia_ban()
                    so_mon += 1

            # Lưu lại dữ liệu xuống SQLite
            self.cua_so_cha.luu_du_lieu_ra_file()
            self.cua_so_cha.cap_nhat_bang_hien_thi()
            self.cap_nhat_bang_gio_hang()

            QMessageBox.information(
                self, "Thanh Toán Thành Công",
                f"Đã thanh toán {so_mon} món hàng.\n"
                f"Tổng tiền: {tong_tien:,.0f} đ\n"
                f"Cảm ơn quý khách!"
            )
            self.close()
        except Exception as e:
            # Nếu có lỗi khi thanh toán → báo lỗi, KHÔNG crash
            QMessageBox.critical(self, "Lỗi Nghiêm Trọng",
                                 f"Đã có lỗi xảy ra khi THANH TOÁN:\n{str(e)}")
