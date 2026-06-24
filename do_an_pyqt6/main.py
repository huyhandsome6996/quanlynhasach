import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import CuaSoChinh

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
    
    cua_so = CuaSoChinh()
    cua_so.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    chay_ung_dung()
