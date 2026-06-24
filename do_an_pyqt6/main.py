import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import CuaSoChinh
from ui.hop_thoai_dang_nhap import HopThoaiDangNhap


def chay_ung_dung():
    app = QApplication(sys.argv)

    # CSS (QSS) cho PyQt6 - Đơn giản, đẹp mắt
    app.setStyleSheet("""
        QMainWindow {
            background-color: #f5f7fa;
        }
        QPushButton {
            border-radius: 5px;
            padding: 8px 15px;
            background-color: #ffffff;
            border: 1px solid #d1d5db;
            color: #374151;
            font-size: 13px;
        }
        QPushButton:hover {
            background-color: #f3f4f6;
        }
        QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
            padding: 8px;
            border: 1px solid #cbd5e1;
            border-radius: 4px;
            background-color: white;
            font-size: 13px;
        }
        QTableWidget {
            background-color: white;
            alternate-background-color: #f8fafc;
            selection-background-color: #bae6fd;
            selection-color: #0f172a;
            border: 1px solid #e2e8f0;
            border-radius: 5px;
            font-size: 13px;
        }
        QHeaderView::section {
            background-color: #334155;
            color: white;
            font-weight: bold;
            padding: 8px;
            border: 0px;
            font-size: 13px;
        }
        QLabel {
            font-size: 13px;
            color: #1e293b;
            font-weight: bold;
        }
    """)

    # ===== VÒNG LẶP ĐĂNG NHẬP =====
    # Mỗi lần đăng xuất sẽ quay lại đây để đăng nhập lại
    while True:
        # 1. Hiện màn hình đăng nhập
        man_hinh_dang_nhap = HopThoaiDangNhap()
        ket_qua = man_hinh_dang_nhap.exec()

        # 2. Nếu bấm "Thoát" hoặc đóng cửa sổ → kết thúc chương trình
        if ket_qua != HopThoaiDangNhap.DialogCode.Accepted:
            print("Đã thoát chương trình.")
            return 0

        # 3. Nếu đăng nhập thành công → mở cửa sổ chính, truyền người dùng vào
        nguoi_dung = man_hinh_dang_nhap.nguoi_dung_hien_tai
        cua_so = CuaSoChinh(nguoi_dung_hien_tai=nguoi_dung)
        cua_so.show()

        # 4. Chạy app cho đến khi cửa sổ chính bị đóng
        #    (khi bấm "Đăng xuất" cửa sổ sẽ đóng → app.exec() trả về)
        app.exec()

        # 5. Hỏi xem có muốn đăng nhập lại bằng tài khoản khác không
        #    (nếu đóng bằng nút X thì cũng coi như đăng xuất)
        print("Đã đăng xuất. Quay lại màn hình đăng nhập...")


if __name__ == "__main__":
    sys.exit(chay_ung_dung())
