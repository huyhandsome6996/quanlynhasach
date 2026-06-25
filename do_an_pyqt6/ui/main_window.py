# ================================================================
# 👤 PHỤ TRÁCH: HỒ QUANG HUY
# ----------------------------------------------------------------
# 📚 KIẾN THỨC CẦN HỌC ĐI THI:
#    1. PyQt6 - QMainWindow, QHBoxLayout, QVBoxLayout, QTableWidget
#    2. Bắt sự kiện click nút (.clicked.connect)
#    3. Undo/Redo dùng 2 Stack (LIFO) - đây là phần thi hay hỏi
#    4. Giỏ hàng dùng Queue (FIFO) - kết nối với hang_doi.py
#    5. Phân quyền: ẩn/hiện nút Xóa theo vai trò (Admin/Nhân viên)
#    6. Thống kê: tính tổng giá trị kho bằng TÍNH ĐA HÌNH
#    7. Tìm kiếm nâng cao theo: Tất cả / Tên / Mã / Loại
#    8. Sắp xếp theo: Tên / Mã / Giá cơ bản / Giá bán / Số lượng
# ----------------------------------------------------------------
# 📝 NỘI DUNG FILE:
#    Toàn bộ giao diện chính + logic xử lý của chương trình.
# ================================================================

import os # Nhập thư viện hệ điều hành (hiện tại không dùng nhiều nhưng có thể cần thiết)
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
                             QMessageBox, QLineEdit, QLabel, QComboBox, QDialog) # Nhập các "Viên gạch" để xây dựng đồ họa từ thư viện PyQt6
from PyQt6.QtCore import Qt # Nhập các hằng số cài đặt của PyQt6 (như canh lề)

# Nạp các khuôn mẫu (Classes) do nhóm tự code ở thư mục models
from models.linked_list import DanhSachLienKetDoi # Cấu trúc dữ liệu chính (thay cho list python thông thường)
from models.ngan_xep import NganXep       # Cấu trúc Stack (Vào sau Ra trước) - dùng cho Undo/Redo
from models.hang_doi import HangDoi       # Cấu trúc Queue (Vào trước Ra trước) - dùng cho Giỏ hàng
from models.subclasses import Sach, TapChi, Bao, LuanVan, BanThao # Các lớp con thể hiện Tính Đa Hình
from ui.dialogs import HopThoaiThemMoi # Cửa sổ nhỏ (Form) dùng để nhập chữ
from ui.hop_thoai_gio_hang import HopThoaiGioHang # Cửa sổ nhỏ hiển thị danh sách giỏ hàng


class CuaSoChinh(QMainWindow): # CuaSoChinh được thừa kế toàn bộ tính năng của QMainWindow (cửa sổ gốc của PyQt6)
    def __init__(self, nguoi_dung_hien_tai=None): # Hàm khởi tạo, tự động chạy đầu tiên khi mở app
        super().__init__() # Đánh thức hàm khởi tạo của thằng Cha (QMainWindow) để nó chuẩn bị khung viền, nút X tắt app...
        self.setWindowTitle("Hệ Thống Quản Lý Cửa Hàng Sách (PyQt6 + Linked List + Stack + Queue)") # Đặt tên hiển thị ở dải băng trên cùng
        self.resize(1100, 700) # Ép kích thước phần mềm: Chiều ngang 1100 pixels, chiều dọc 700 pixels

        # Lưu lại thông tin xem ai đang xài app (admin hay nhan_vien) để lát nữa chặn quyền
        self.nguoi_dung = nguoi_dung_hien_tai

        # ===== CÁC CẤU TRÚC DỮ LIỆU CHÍNH (NÃO BỘ CỦA PHẦN MỀM) =====
        # 1. Tạo cái "Kho ảo" trên RAM (Danh sách liên kết đôi) để chứa hàng hóa
        self.danh_sach = DanhSachLienKetDoi()
        
        # 2. Tạo cuốn sổ tay 1 (Ngăn xếp Undo LIFO). Làm gì sai thì xé trang cuối vứt đi để quay lại lúc đầu
        self.ngan_xep_hoan_tac = NganXep()
        
        # 3. Tạo cuốn sổ tay 2 (Ngăn xếp Redo LIFO). Lỡ Undo nhầm thì moi lại cái thao tác vừa bị hủy
        self.ngan_xep_lam_lai = NganXep()
        
        # 4. Tạo một cái Rổ (Hàng đợi Queue FIFO) để khách nhặt sách bỏ vào chờ tính tiền
        self.gio_hang = HangDoi()

        self.thiet_lap_giao_dien() # Gọi hàm vẽ đồ họa (vẽ các nút bấm, ô chữ)
        self.doc_du_lieu_tu_file() # Gọi hàm khui kho (lấy dữ liệu từ file CSDL ổ cứng đổ vào cái Kho ảo RAM)
        self.cap_nhat_tieu_de_theo_quyen() # Kích hoạt chế độ kiểm duyệt: Mày là nhân viên thì tao giấu nút Xóa đi

    # ==================================================================
    # THIẾT LẬP GIAO DIỆN (Nơi chứa các code xếp gạch, không có thuật toán nhiều)
    # ==================================================================
    def thiet_lap_giao_dien(self):
        widget_chinh = QWidget() # Tạo một cái bảng vẽ trống trải
        layout_chinh = QVBoxLayout() # Đặt quy tắc: Tất cả nút bấm ném vào đây sẽ bị xếp theo DỌC (V = Vertical) từ trên xuống

        # ----- KHU VỰC TÌM KIẾM + SẮP XẾP -----
        layout_cong_cu = QHBoxLayout() # Tạo khu vực mới nằm NGANG (H = Horizontal)

        self.nhap_tim_kiem = QLineEdit() # Cái ô màu trắng để người dùng gõ chữ vào
        self.nhap_tim_kiem.setPlaceholderText("Nhập từ khóa cần tìm...") # Chữ mờ mờ gợi ý trong ô

        self.cb_tieu_chi_tim = QComboBox() # Cái nút bấm xổ xuống (Dropdown list) để chọn kiểu tìm kiếm
        self.cb_tieu_chi_tim.addItems(["Tất cả", "Theo Tên", "Theo Mã", "Theo Loại"]) # Thêm 4 cục lựa chọn vào Dropdown

        nut_tim_kiem = QPushButton("🔍 Tìm Kiếm") # Tạo cái Nút có chữ "Tìm Kiếm"
        nut_tim_kiem.clicked.connect(self.xu_ly_tim_kiem) # Gắn dây điện: Hễ ai click nút này thì máy tự chạy hàm xu_ly_tim_kiem()

        nut_lam_moi = QPushButton("🔄 Tải Lại Bảng") # Tạo cái Nút "Tải lại"
        nut_lam_moi.clicked.connect(self.cap_nhat_bang_hien_thi) # Gắn dây điện để load lại dữ liệu

        self.cb_sap_xep = QComboBox() # Dropdown list cho việc Sắp xếp
        self.cb_sap_xep.addItems(["Giá bán tăng dần", "Giá bán giảm dần", "Tên A-Z", "Tên Z-A", "Số lượng tồn kho tăng"])
        
        nut_sap_xep = QPushButton("🔀 Sắp Xếp (Merge Sort)") # Tạo Nút Sắp xếp
        nut_sap_xep.setStyleSheet("background-color: #FF9800; color: white;") # Trang điểm cho Nút: Đổi nền sang cam, chữ trắng
        nut_sap_xep.clicked.connect(self.xu_ly_sap_xep) # Bấm nút thì chạy hàm xu_ly_sap_xep()

        # Ném các Nút và Ô chữ vào cái mâm nằm Ngang (layout_cong_cu)
        layout_cong_cu.addWidget(QLabel("Từ khóa:"))
        layout_cong_cu.addWidget(self.nhap_tim_kiem)
        layout_cong_cu.addWidget(self.cb_tieu_chi_tim)
        layout_cong_cu.addWidget(nut_tim_kiem)
        layout_cong_cu.addWidget(nut_lam_moi)
        layout_cong_cu.addStretch()  # Tạo một khoảng trống vô hình đẩy phần tìm kiếm sang trái, phần sắp xếp sang phải
        layout_cong_cu.addWidget(QLabel("Sắp xếp:"))
        layout_cong_cu.addWidget(self.cb_sap_xep)
        layout_cong_cu.addWidget(nut_sap_xep)
        
        layout_chinh.addLayout(layout_cong_cu) # Ném nguyên cái mâm Ngang này vào cái Dọc khổng lồ

        # ----- BẢNG HIỂN THỊ DỮ LIỆU -----
        self.bang_du_lieu = QTableWidget() # Khởi tạo một cái Bảng Excel phiên bản PyQt6
        self.bang_du_lieu.setColumnCount(7) # Kẻ 7 cột
        self.bang_du_lieu.setHorizontalHeaderLabels(["Mã Số", "Phân Loại", "Tên Sản Phẩm", "Giá Cơ Bản", "Giá Bán", "Số Lượng", "Đặc Điểm Riêng"]) # Điền tiêu đề cho 7 cột
        self.bang_du_lieu.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch) # Lệnh ép các cột tự động giãn dài ra cho kín màn hình
        self.bang_du_lieu.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers) # Cấm người dùng double click vào ô để sửa chữ (Khóa chế độ sửa)
        layout_chinh.addWidget(self.bang_du_lieu) # Quăng cái Bảng vào layout dọc

        # ----- DÒNG NÚT CHỨC NĂNG CHÍNH -----
        layout_chuc_nang = QHBoxLayout() # Lại tạo một cái mâm nằm Ngang chứa các Nút

        nut_them = QPushButton("➕ Thêm Mặt Hàng")
        nut_them.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; font-size: 14px; padding: 10px;") # Trang điểm Nút xanh lá
        nut_them.clicked.connect(self.hien_thi_form_them) # Gắn nút Thêm vào hàm hien_thi_form_them()

        nut_sua = QPushButton("✏️ Sửa Mặt Hàng")
        nut_sua.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; font-size: 14px; padding: 10px;")
        nut_sua.clicked.connect(self.hien_thi_form_sua)

        self.nut_xoa = QPushButton("🗑️ Xóa Mặt Hàng") # Gắn chữ 'self' để lát nữa còn giấu nó đi được
        self.nut_xoa.setStyleSheet("background-color: #f44336; color: white; font-weight: bold; font-size: 14px; padding: 10px;")
        self.nut_xoa.clicked.connect(self.xu_ly_xoa_san_pham)

        nut_thong_ke = QPushButton("📊 Xem Thống Kê")
        nut_thong_ke.setStyleSheet("background-color: #9C27B0; color: white; font-weight: bold; font-size: 14px; padding: 10px;")
        nut_thong_ke.clicked.connect(self.xu_ly_thong_ke)

        nut_dang_xuat = QPushButton("🚪 Đăng Xuất")
        nut_dang_xuat.setStyleSheet("background-color: #616161; color: white; font-weight: bold; font-size: 14px; padding: 10px;")
        nut_dang_xuat.clicked.connect(self.xu_ly_dang_xuat)

        # Quăng hết Nút vào mâm Ngang
        layout_chuc_nang.addWidget(nut_them)
        layout_chuc_nang.addWidget(nut_sua)
        layout_chuc_nang.addWidget(self.nut_xoa)
        layout_chuc_nang.addWidget(nut_thong_ke)
        layout_chuc_nang.addWidget(nut_dang_xuat)
        layout_chinh.addLayout(layout_chuc_nang) # Quăng mâm Ngang vào layout Dọc chính

        # ----- DÒNG NÚT UNDO/REDO + GIỎ HÀNG -----
        layout_mo_rong = QHBoxLayout() # Mâm Ngang phụ

        nut_hoan_tac = QPushButton("↩️ Hoàn Tác (Undo)")
        nut_hoan_tac.setStyleSheet("background-color: #607D8B; color: white; font-weight: bold; font-size: 14px; padding: 10px;")
        nut_hoan_tac.clicked.connect(self.xu_ly_hoan_tac) # Gắn hàm xử lý Undo

        nut_lam_lai = QPushButton("↪️ Làm Lại (Redo)")
        nut_lam_lai.setStyleSheet("background-color: #795548; color: white; font-weight: bold; font-size: 14px; padding: 10px;")
        nut_lam_lai.clicked.connect(self.xu_ly_lam_lai) # Gắn hàm xử lý Redo

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

        widget_chinh.setLayout(layout_chinh) # Sau khi gom hết đồ vào layout Dọc chính, dán cái layout đó vào bảng vẽ trống ban đầu
        self.setCentralWidget(widget_chinh) # Ép cái bảng vẽ đó làm Trung tâm của toàn bộ phần mềm

    # ==================================================================
    # PHÂN QUYỀN (Admin / Nhân viên)
    # ==================================================================
    def cap_nhat_tieu_de_theo_quyen(self):
        """Hàm này làm 2 việc: Viết chữ lên thanh ngang trên cùng + Giấu nút Xóa nếu là Nhân viên"""
        if self.nguoi_dung is None: # Dự phòng lỡ ai chạy thẳng app mà không qua đăng nhập
            vai_tro = "Admin"
            self.nut_xoa.show() # Lệnh .show() là Lộ diện cái nút
        elif self.nguoi_dung.la_admin(): # Lệnh này lôi Class NguoiDung ra hỏi xem có phải admin ko
            vai_tro = "Admin"
            self.nut_xoa.show()  # Admin được phép xóa nên Hiện nút
        else:
            vai_tro = "Nhân viên"
            self.nut_xoa.hide()  # Nhân viên thì KHÔNG được xóa → .hide() là lệnh Tàng hình

        # Cập nhật tên thanh ngang để biết ai đang dùng app
        self.setWindowTitle(
            f"Hệ Thống Quản Lý Cửa Hàng Sách  |  "
            f"Đăng nhập: {self.nguoi_dung.ten_dang_nhap if self.nguoi_dung else '?'} ({vai_tro})"
        )

    def xu_ly_dang_xuat(self):
        """Hỏi ý kiến trước khi đăng xuất"""
        xac_nhan = QMessageBox.question( # Bật hộp thoại hỏi Yes/No
            self, "Đăng xuất",
            "Bạn có muốn đăng xuất và quay về màn hình đăng nhập?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if xac_nhan == QMessageBox.StandardButton.Yes: # Nếu người dùng bấm Yes
            self.close()  # Tự sát (Đóng cửa sổ chính này lại). Khi cửa sổ chết, main.py sẽ vớt lên màn hình Login

    # ==================================================================
    # XỬ LÝ: THÊM / SỬA / XÓA (CÓ GHI VÀO SỔ TAY ĐỂ HOÀN TÁC)
    # ==================================================================
    def hien_thi_form_them(self):
        """Hàm gọi cửa sổ phụ lên để người dùng gõ chữ tạo sách mới"""
        hop_thoai = HopThoaiThemMoi(self)  # Sinh ra 1 cái cửa sổ phụ tên là HopThoaiThemMoi
        if hop_thoai.exec() == QDialog.DialogCode.Accepted: # Lệnh .exec() làm ngưng phần mềm chờ bạn bấm. Bấm nút Lưu (Accepted) thì chạy tiếp code dưới
            try: # Try/Except là Bùa hộ mệnh. Bọc code lại lỡ có lỗi thì nó chỉ in cảnh báo chứ không văng app
                sp_moi = hop_thoai.san_pham_moi # Móc cuốn Sách vừa được xưởng bên dialogs.py đúc xong ra đây

                # Kiểm tra xem mã cuốn sách này có bị trùng với mấy cuốn trong Kho ảo (DanhSachLienKet) chưa
                if self.danh_sach.tim_kiem_theo_ma(sp_moi.ma_so):
                    QMessageBox.warning(self, "Lỗi", "Mã sản phẩm này đã tồn tại trong kho!")
                    return # Thấy trùng mã thì Bóp Cổ (return) dừng chạy luôn hàm này

                self.danh_sach.them_vao_cuoi(sp_moi) # Nhét cuốn sách mới tinh vào Kho ảo trên RAM
                self.luu_du_lieu_ra_file() # Mở hầm cầu, gọi sqlite_db copy y chang Kho RAM đổ xuống ổ cứng
                self.cap_nhat_bang_hien_thi() # F5 lại giao diện để khách thấy sách mới lên kệ

                # --- GHI NHỚ CHO CHỨC NĂNG UNDO ---
                # Vì vừa THÊM xong, nên mình ghi vào trang cuối cuốn Sổ tay Undo: Mày vừa "them" cuốn "sp_moi"
                self.ngan_xep_hoan_tac.day_vao({"thao_tac": "them", "sp": sp_moi})
                
                # Chú ý: Đã làm hành động mới tinh thì phải đốt Sổ tay Redo đi (để đứt chuỗi)
                self.ngan_xep_lam_lai.xoa_tat_ca()

                QMessageBox.information(self, "Thành công", "Đã lưu mặt hàng mới thành công!")
            except Exception as e:
                # Nếu bùa hộ mệnh (Try) phát hiện lỗi (ổ cứng đầy, DB khóa, virus...) thì nó chạy vào đây
                QMessageBox.critical(self, "Lỗi Nghiêm Trọng", f"Đã có lỗi xảy ra khi THÊM sản phẩm:\n{str(e)}")

    def hien_thi_form_sua(self):
        """Hàm dùng để bắt thằng sách đang chọn trên bảng và sửa ruột nó"""
        dong_dang_chon = self.bang_du_lieu.currentRow() # Nhìn lên bảng, dò xem con chuột máy tính đang tô xanh dòng số mấy (dòng đầu = 0)
        if dong_dang_chon < 0: # Nếu bằng -1 nghĩa là chưa tô xanh dòng nào cả
            QMessageBox.warning(self, "Cảnh Báo", "Bạn chưa click chọn sản phẩm nào trên bảng!")
            return # Đuổi đi

        ma_so = self.bang_du_lieu.item(dong_dang_chon, 0).text() # Chọt tay vào cột số 0 (cột Mã Số) của dòng bị tô xanh để móc ra cái chữ Mã ("S01")
        sp_cu = self.danh_sach.tim_kiem_theo_ma(ma_so) # Vào Kho ảo lôi cuốn Sách Cũ có mã đó ra
        if sp_cu is None:
            return

        hop_thoai = HopThoaiThemMoi(self, san_pham_cu=sp_cu) # Gọi Form nhập liệu lên, nhưng truyền cuốn Sách Cũ vào để form tự động chép chữ ra các ô cho mình đỡ gõ lại
        if hop_thoai.exec() == QDialog.DialogCode.Accepted:
            try:
                sp_sua = hop_thoai.san_pham_moi # Rút cuốn sách MỚI VỪA CHỈNH SỬA ra

                self.danh_sach.xoa_nut_theo_ma(ma_so) # Code Linked List: Nhổ bỏ cây rễ cũ (cuốn sách cũ)
                self.danh_sach.them_vao_cuoi(sp_sua) # Code Linked List: Gắn chồi non mới (cuốn sách mới) vào

                self.luu_du_lieu_ra_file() # Chép Kho ảo đè xuống Ổ cứng
                self.cap_nhat_bang_hien_thi() # F5 Bảng

                # --- GHI NHỚ CHO CHỨC NĂNG UNDO ---
                # Vừa SỬA xong, nên ghi vào sổ Undo: "Tao vừa 'sua', đây là cái xác sp_cu, đây là bản thể sp_moi"
                self.ngan_xep_hoan_tac.day_vao({
                    "thao_tac": "sua",
                    "sp_cu": sp_cu,    # Phải giữ lại cái xác cũ thì lát nữa mới Undo biến về như cũ được
                    "sp_moi": sp_sua
                })
                self.ngan_xep_lam_lai.xoa_tat_ca() # Đốt sổ Redo

                QMessageBox.information(self, "Thành công", "Đã cập nhật thông tin sản phẩm!")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi Nghiêm Trọng", f"Đã có lỗi xảy ra khi SỬA sản phẩm:\n{str(e)}")

    def xu_ly_xoa_san_pham(self):
        """Hàm giết bỏ 1 sản phẩm"""
        # Nếu cố tình lách luật bấm nút (mặc dù đã ẩn) thì tường lửa chặn lại
        if self.nguoi_dung is not None and not self.nguoi_dung.la_admin():
            QMessageBox.warning(self, "Không Đủ Quyền", "Bạn là 'Nhân viên' nên KHÔNG ĐƯỢC PHÉP XÓA.")
            return

        dong_dang_chon = self.bang_du_lieu.currentRow() # Coi đang bôi đen dòng nào
        if dong_dang_chon < 0: return

        ma_so = self.bang_du_lieu.item(dong_dang_chon, 0).text() # Lấy Mã của tử tù ra

        xac_nhan = QMessageBox.question(self, "Xác nhận xóa", f"Bạn có chắc muốn xóa vĩnh viễn mã '{ma_so}'?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) # Hỏi cung tử tù lần cuối
        if xac_nhan == QMessageBox.StandardButton.Yes:
            try:
                # TRƯỚC KHI GIẾT TỬ TÙ, PHẢI NHÂN BẢN NÓ CẤT VÀO NGĂN ĐÁ CHỜ UNDO HỒI SINH
                sp_bi_xoa = self.danh_sach.tim_kiem_theo_ma(ma_so) 
                
                thanh_cong = self.danh_sach.xoa_nut_theo_ma(ma_so) # Trảm thủ tử tù trên Kho RAM
                if thanh_cong:
                    self.luu_du_lieu_ra_file() # Mang xác đi chôn dưới Ổ cứng CSDL
                    self.cap_nhat_bang_hien_thi() # F5 để bảng xóa xác mờ đi

                    # Ghi vào Sổ tay Undo: "Vừa 'xoa' thằng sp_bi_xoa, cầm lấy xác nó này"
                    self.ngan_xep_hoan_tac.day_vao({"thao_tac": "xoa", "sp": sp_bi_xoa})
                    self.ngan_xep_lam_lai.xoa_tat_ca() # Đốt sổ Redo

                    QMessageBox.information(self, "Thành công", "Đã xóa xong!")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi Nghiêm Trọng", f"Lỗi XÓA:\n{str(e)}")

    # ==================================================================
    # XỬ LÝ: UNDO / REDO (ÁP DỤNG STACK LIFO)
    # ==================================================================
    def xu_ly_hoan_tac(self):
        """Hàm thuốc hối hận. Quay ngược thời gian 1 bước."""
        if self.ngan_xep_hoan_tac.rong(): # Nếu sổ Undo rách sạch giấy
            QMessageBox.information(self, "Hoàn Tác", "Không còn thao tác nào để hoàn tác!")
            return

        thao_tac = self.ngan_xep_hoan_tac.lay_ra() # Xé trang cuối của Sổ Undo ra đọc xem nãy làm cái mẹ gì
        kieu = thao_tac["thao_tac"] # Coi nãy làm gì: "them", hay "sua", hay "xoa"

        try:
            if kieu == "them":
                # Nãy lỡ THÊM đồ vào Kho → Thuốc giải: Móc nó ra đem VỨT XÓA đi
                sp = thao_tac["sp"]
                self.danh_sach.xoa_nut_theo_ma(sp.ma_so)

            elif kieu == "xoa":
                # Nãy lỡ giết XÓA đi 1 đứa → Thuốc giải: Ép cái xác THÊM lại vào kho cho nó hồi sinh
                sp = thao_tac["sp"]
                self.danh_sach.them_vao_cuoi(sp)

            elif kieu == "sua":
                # Nãy lỡ SỬA đổi dung nhan thành sp_moi → Thuốc giải: Giết bỏ sp_moi, rước sp_cu về lại
                ma_so = thao_tac["sp_moi"].ma_so
                self.danh_sach.xoa_nut_theo_ma(ma_so)
                self.danh_sach.them_vao_cuoi(thao_tac["sp_cu"])

            # Cầm tờ giấy vừa xé dán bù vào cho Sổ REDO (nhỡ Lão Ngáo đòi trở lại tương lai)
            self.ngan_xep_lam_lai.day_vao(thao_tac)

            self.luu_du_lieu_ra_file() # Lưu đè xuống ổ cứng
            self.cap_nhat_bang_hien_thi() # F5 Bảng
            QMessageBox.information(self, "Hoàn Tác", f"Đã hoàn tác thao tác '{kieu}' thành công!")
        except Exception as e:
            # Nếu uống thuốc hối hận mà bị sặc (lỗi), thì dán trang giấy lại cho Sổ Undo kẻo mất dấu
            self.ngan_xep_hoan_tac.day_vao(thao_tac)
            QMessageBox.critical(self, "Lỗi", f"Lỗi HOÀN TÁC:\n{str(e)}")

    def xu_ly_lam_lai(self):
        """Hàm Độc Dược Cỗ Máy Thời Gian - Tới tương lai (Hủy bỏ cái Undo vừa làm)"""
        if self.ngan_xep_lam_lai.rong(): # Nếu Sổ Redo rỗng không
            QMessageBox.information(self, "Làm Lại", "Không còn thao tác nào để làm lại!")
            return

        thao_tac = self.ngan_xep_lam_lai.lay_ra() # Xé trang cuối Sổ Redo ra
        kieu = thao_tac["thao_tac"]

        try:
            if kieu == "them":
                # Làm lại hành động THÊM lúc đầu → Ném lại đồ vào Kho
                self.danh_sach.them_vao_cuoi(thao_tac["sp"])

            elif kieu == "xoa":
                # Làm lại hành động XÓA lúc đầu → Giết lại thằng đó
                self.danh_sach.xoa_nut_theo_ma(thao_tac["sp"].ma_so)

            elif kieu == "sua":
                # Làm lại hành động SỬA lúc đầu → Giết sp_cu, rước sp_moi về
                ma_so = thao_tac["sp_cu"].ma_so
                self.danh_sach.xoa_nut_theo_ma(ma_so)
                self.danh_sach.them_vao_cuoi(thao_tac["sp_moi"])

            # Trả lại tờ giấy cho Sổ Undo
            self.ngan_xep_hoan_tac.day_vao(thao_tac)

            self.luu_du_lieu_ra_file()
            self.cap_nhat_bang_hien_thi()
            QMessageBox.information(self, "Làm Lại", f"Đã làm lại thao tác '{kieu}' thành công!")
        except Exception as e:
            self.ngan_xep_lam_lai.day_vao(thao_tac)
            QMessageBox.critical(self, "Lỗi", f"Lỗi LÀM LẠI:\n{str(e)}")

    # ==================================================================
    # XỬ LÝ: TÌM KIẾM BẰNG PHƯƠNG PHÁP CHÀ DUYỆT TUYẾN TÍNH TRÊN LINKED LIST
    # ==================================================================
    def xu_ly_tim_kiem(self):
        """Hàm lọc ra những cuốn sách khớp với chữ mà khách gõ"""
        tu_khoa = self.nhap_tim_kiem.text().strip().lower() # Lấy chữ khách gõ, chặt 2 đầu khoảng trắng (strip), ép thành chữ thường mờ (lower) để so sánh cho khỏi phân biệt hoa/thường
        if not tu_khoa:
            self.cap_nhat_bang_hien_thi()  # Nếu gõ để trống thì trả lại nguyên bảng ban đầu
            return

        tieu_chi = self.cb_tieu_chi_tim.currentText() # Lấy cái dropdown list xem khách chọn tìm theo MÃ hay theo TÊN
        bang_ten = {
            "Sach": "sách", "TapChi": "tạp chí", "Bao": "báo", "LuanVan": "luận văn", "BanThao": "bản thảo"
        }

        ket_qua = [] # Mở 1 cái rổ trống để hốt những quyển sách khớp yêu cầu vào đây
        
        # Lệnh for này chạy bằng hàm duyet_danh_sach() trong Linked List, bốc từng quyển sách ra coi
        for sp in self.danh_sach.duyet_danh_sach():
            if tieu_chi == "Tất cả":
                # Coi hết từ mã, tên, loại. Thấy trùng chữ ở đâu thì lụm
                loai_viet = bang_ten.get(sp.__class__.__name__, "")
                if (tu_khoa in sp.ma_so.lower() or tu_khoa in sp.ten.lower() or tu_khoa in loai_viet):
                    ket_qua.append(sp) # Ném vào rổ
            elif tieu_chi == "Theo Tên":
                if tu_khoa in sp.ten.lower(): ket_qua.append(sp)
            elif tieu_chi == "Theo Mã":
                if tu_khoa in sp.ma_so.lower(): ket_qua.append(sp)
            elif tieu_chi == "Theo Loại":
                loai_viet = bang_ten.get(sp.__class__.__name__, "")
                if tu_khoa in loai_viet: ket_qua.append(sp)

        if not ket_qua: # Nếu cái rổ trống rỗng
            QMessageBox.information(self, "Tìm kiếm", "Không tìm thấy sản phẩm nào!")
        self.hien_thi_mang_len_bang(ket_qua) # Đổ cái rổ lên Bảng cho khách coi

    # ==================================================================
    # XỬ LÝ: SẮP XẾP BẰNG MERGE SORT
    # ==================================================================
    def xu_ly_sap_xep(self):
        """Hàm kích hoạt bộ não Merge Sort tự code bên Linked List"""
        lua_chon = self.cb_sap_xep.currentText() # Nhìn xem người dùng chọn dòng Sắp xếp nào

        # Dựa theo tên người dùng chọn, truyền CHUỖI BIẾN CỨNG (tieu_chi) vào hàm sap_xep()
        # Hàm sap_xep sẽ dùng hàm ma thuật getattr() để bóc thuộc tính này ra tính điểm
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

        self.cap_nhat_bang_hien_thi() # Sort xong thì F5 vẽ lại bảng
        QMessageBox.information(self, "Thuật Toán", f"Đã áp dụng Merge Sort trên Danh sách liên kết: {lua_chon}")

    # ==================================================================
    # XỬ LÝ: THỐNG KÊ (BIỂU DIỄN TÍNH ĐA HÌNH CỦA OOP)
    # ==================================================================
    def xu_ly_thong_ke(self):
        """Hàm gom toán để báo cáo tài chính kho hàng"""
        mang_du_lieu = self.danh_sach.duyet_danh_sach() # Bốc hết kho ra kiểm đếm
        if not mang_du_lieu: return

        tong_san_pham = len(mang_du_lieu)
        
        # 🌟🌟 ĐÂY LÀ ĐIỂM ĂN TIỀN CỦA OOP (ĐA HÌNH):
        # Ta dùng hàm tinh_gia_ban(). Mỗi đứa con (Sach, TapChi) có thể có một cách tính giá bán khác nhau
        # (vd Sách x2, Tạp chí x1.5). Ta cứ gọi tinh_gia_ban(), thằng con nào nó sẽ tự lấy luật của thằng đó mà tính.
        dat_nhat = max(mang_du_lieu, key=lambda x: x.tinh_gia_ban()) # Trích thằng đắt nhất
        re_nhat = min(mang_du_lieu, key=lambda x: x.tinh_gia_ban()) # Trích thằng rẻ nhất

        san_pham_sap_het = [sp.ten for sp in mang_du_lieu if sp.so_luong < 5] # Lọc tụi sắp chết (số lượng < 5)
        canh_bao_sl = ", ".join(san_pham_sap_het) if san_pham_sap_het else "Không có"

        # Tính tổng giá trị toàn kho bằng vòng lặp sum
        tong_gia_tri_kho = sum(sp.tinh_gia_ban() * sp.so_luong for sp in mang_du_lieu)

        # In cái Report ra
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
    # XỬ LÝ: GIỎ HÀNG (ÁP DỤNG CẤU TRÚC QUEUE FIFO)
    # ==================================================================
    def xu_ly_them_vao_gio(self):
        """Khách nhặt 1 món thả vào Giỏ (Hàng đợi tính tiền)"""
        dong_dang_chon = self.bang_du_lieu.currentRow()
        if dong_dang_chon < 0: return

        ma_so = self.bang_du_lieu.item(dong_dang_chon, 0).text()
        sp = self.danh_sach.tim_kiem_theo_ma(ma_so)
        if sp.so_luong <= 0:
            QMessageBox.warning(self, "Hết Hàng", "Sản phẩm này đã hết tồn kho!")
            return

        try:
            # Gọi lệnh ném sách vào cuối Hàng Đợi (Queue). Ai vào trước tính tiền trước.
            self.gio_hang.them_vao(sp)
            QMessageBox.information(self, "Đã Thêm Vào Giỏ", f"Đã thêm '{sp.ten}' vào giỏ.\nGiỏ hiện có: {self.gio_hang.so_luong} món.")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi Nghiêm Trọng", f"Đã có lỗi xảy ra khi THÊM VÀO GIỎ:\n{str(e)}")

    def xu_ly_xem_gio_hang(self):
        """Mở cửa sổ phụng sự Giỏ Hàng"""
        hop_thoai = HopThoaiGioHang(self)
        hop_thoai.exec()

    # ==================================================================
    # CÁC HÀM HIỂN THỊ DỮ LIỆU CỐT LÕI
    # ==================================================================
    def cap_nhat_bang_hien_thi(self):
        """Mệnh lệnh: Dọn dẹp sạch bảng rồi bắt đầu rải Sách lên lại"""
        tat_ca = self.danh_sach.duyet_danh_sach() # Bốc kho Sách trên RAM ra 1 cái mẹt
        self.hien_thi_mang_len_bang(tat_ca) # Cầm cái mẹt rải lên bàn (Bảng đồ họa)

    def hien_thi_mang_len_bang(self, mang_san_pham):
        """Kỹ sư rải gạch: Lấy mảng sách xếp vào ô excel đồ họa PyQt"""
        self.bang_du_lieu.setRowCount(0)  # Cầm chổi quét sạch Bảng đi
        for sp in mang_san_pham:
            dong_moi = self.bang_du_lieu.rowCount() # Đếm xem bảng đang có bao nhiêu dòng để tính chèn thêm dòng
            self.bang_du_lieu.insertRow(dong_moi) # Rạch thêm 1 hàng trắng mới ở cuối bảng

            # Đa Hình lần 2: Hàm __class__.__name__ tự động nội soi xem sách này là con ruột lớp nào (Sach hay Bao hay TapChi)
            loai_sp = sp.__class__.__name__
            bang_ten = {"Sach": "Sách", "TapChi": "Tạp Chí", "Bao": "Báo", "LuanVan": "Luận Văn", "BanThao": "Bản Thảo"}
            loai_sp = bang_ten.get(loai_sp, loai_sp) # Chuyển mã Tây sang mã Việt cho dễ xem

            # Rắc từng chữ vào từng ô (Row, Column)
            self.bang_du_lieu.setItem(dong_moi, 0, QTableWidgetItem(sp.ma_so))
            self.bang_du_lieu.setItem(dong_moi, 1, QTableWidgetItem(loai_sp))
            self.bang_du_lieu.setItem(dong_moi, 2, QTableWidgetItem(sp.ten))
            self.bang_du_lieu.setItem(dong_moi, 3, QTableWidgetItem(f"{sp.gia_co_ban:,.0f} đ"))
            self.bang_du_lieu.setItem(dong_moi, 4, QTableWidgetItem(f"{sp.tinh_gia_ban():,.0f} đ"))
            self.bang_du_lieu.setItem(dong_moi, 5, QTableWidgetItem(str(sp.so_luong)))

            # Lệnh isinstance là máy quét mã vạch kiểm tra huyết thống. Nếu là giống nòi Sách thì ném ruột sách ra.
            thong_tin = ""
            if isinstance(sp, Sach): thong_tin = f"TG: {sp.tac_gia} | NXB: {sp.nha_xuat_ban}"
            elif isinstance(sp, TapChi): thong_tin = f"Số PH: {sp.so_phat_hanh}"
            elif isinstance(sp, Bao): thong_tin = f"Ngày PH: {sp.ngay_phat_hanh}"
            elif isinstance(sp, LuanVan): thong_tin = f"Trường ĐH: {sp.truong_dai_hoc}"
            elif isinstance(sp, BanThao): thong_tin = f"Trạng thái: {sp.tinh_trang}"

            self.bang_du_lieu.setItem(dong_moi, 6, QTableWidgetItem(thong_tin)) # Điền vô cột Đặc điểm riêng

    def doc_du_lieu_tu_file(self):
        """Tài xế giao hàng: Lái xe ra nhà kho SQLite chở hàng đổ vào Kho RAM (LinkedList)"""
        from data.sqlite_db import doc_du_lieu_sqlite # Thuê xe tải SQLite
        try:
            mang_sp = doc_du_lieu_sqlite() # Xúc hàng từ kho lên xe tải
            for sp in mang_sp: # Nhặt từng món hàng trên xe
                self.danh_sach.them_vao_cuoi(sp) # Ném vào rổ Kho RAM (DanhSachLienKet)
            self.cap_nhat_bang_hien_thi() # Rải hàng lên Bảng cho khách coi
        except Exception as e:
            QMessageBox.critical(self, "Lỗi Nghiêm Trọng", f"Lỗi CSDL SQLite: {str(e)}")

    def luu_du_lieu_ra_file(self):
        """Tài xế dọn rác: Cào toàn bộ Kho RAM lên xe đem đổ ngược lại xuống Kho SQLite Ổ cứng"""
        from data.sqlite_db import luu_du_lieu_sqlite
        mang_tam = self.danh_sach.duyet_danh_sach() # Gom hết sách trên Kho RAM vào bịch nilong
        try:
            thanh_cong = luu_du_lieu_sqlite(mang_tam) # Ném cái bịch nilong đó sang hàm CSDL lưu chết xuống ổ đĩa
            if not thanh_cong:
                QMessageBox.warning(self, "Lỗi", "Không thể lưu dữ liệu xuống CSDL!")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi Nghiêm Trọng", f"Lỗi khi lưu SQLite: {str(e)}")
