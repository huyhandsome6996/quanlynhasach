# ================================================================
# 👤 PHỤ TRÁCH: BÙI GIA NGỌ
# ----------------------------------------------------------------
# 📚 KIẾN THỨC CẦN HỌC ĐI THI:
#    1. SQLite - tạo bảng CREATE TABLE IF NOT EXISTS
#    2. SQLite - INSERT, DELETE, SELECT (câu lệnh SQL cơ bản)
#    3. Thư viện sqlite3 của Python: connect, cursor, execute, commit
#    4. Kết hợp OOP + CSDL: dùng TÍNH ĐA HÌNH khi đọc/ghi sản phẩm
#    5. Xử lý ngoại lệ try/except để chương trình không bị crash
# ----------------------------------------------------------------
# 📝 NỘI DUNG FILE:
#    Toàn bộ thao tác lưu/đọc dữ liệu xuống file SQLite. Bảng SanPham
#    có 7 cột (ma_so, loai, ten, gia_co_ban, so_luong, thong_tin_1,
#    thong_tin_2). Khi đọc lên, dùng đa hình để tạo đúng lớp con.
# ================================================================

import sqlite3
import os
from models.subclasses import Sach, TapChi, Bao, LuanVan, BanThao

# Đường dẫn tới file cơ sở dữ liệu SQLite
DB_PATH = "data/quan_ly_nha_sach.db"


def khoi_tao_db():
    """Tạo thư mục data và bảng SanPham nếu chưa tồn tại."""
    if not os.path.exists("data"):
        os.makedirs("data")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Bảng SanPham dùng để chứa mọi thể loại mặt hàng
    # Các cột thong_tin_1, thong_tin_2 chứa thuộc tính riêng theo từng loại
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS SanPham (
        ma_so        TEXT PRIMARY KEY,
        loai         TEXT NOT NULL,
        ten          TEXT NOT NULL,
        gia_co_ban   REAL NOT NULL,
        so_luong     INTEGER NOT NULL,
        thong_tin_1  TEXT,
        thong_tin_2  TEXT
    )
    ''')
    conn.commit()
    conn.close()


def doc_du_lieu_sqlite():
    """
    Đọc toàn bộ sản phẩm từ SQLite và trả về danh sách các đối tượng (đa hình).
    Có xử lý ngoại lệ: nếu DB bị hỏng hoặc không tồn tại, trả về danh sách rỗng.
    """
    try:
        khoi_tao_db()
        danh_sach = []
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM SanPham")
        rows = cursor.fetchall()

        for row in rows:
            ma_so, loai, ten, gia_co_ban, so_luong, t1, t2 = row
            # Dùng TÍNH ĐA HÌNH để tạo đúng đối tượng lớp con
            if loai == "Sach":
                sp = Sach(ma_so, ten, gia_co_ban, so_luong, t1, t2)
            elif loai == "TapChi":
                sp = TapChi(ma_so, ten, gia_co_ban, so_luong, t1)
            elif loai == "Bao":
                sp = Bao(ma_so, ten, gia_co_ban, so_luong, t1)
            elif loai == "LuanVan":
                sp = LuanVan(ma_so, ten, gia_co_ban, so_luong, t1)
            elif loai == "BanThao":
                sp = BanThao(ma_so, ten, gia_co_ban, so_luong, t1)
            else:
                continue  # Bỏ qua dòng lỗi
            danh_sach.append(sp)

        conn.close()
        return danh_sach

    except Exception as loi:
        print(f"[LỖI] Không đọc được CSDL: {loi}")
        return []


def luu_du_lieu_sqlite(mang_san_pham):
    """
    Lưu toàn bộ danh sách sản phẩm vào SQLite.
    Cách đơn giản nhất: XÓA HẾT rồi THÊM LẠI (đồng bộ từ Linked List xuống DB).
    Có xử lý ngoại lệ: nếu lỗi thì in ra, không làm crash chương trình.
    """
    try:
        khoi_tao_db()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Xóa dữ liệu cũ để đồng bộ
        cursor.execute("DELETE FROM SanPham")

        for sp in mang_san_pham:
            data = sp.to_dict()
            loai = data["loai"]
            t1 = ""
            t2 = ""

            # Lấy thuộc tính riêng theo từng loại mặt hàng
            if loai == "Sach":
                t1 = data.get("tac_gia", "")
                t2 = data.get("nha_xuat_ban", "")
            elif loai == "TapChi":
                t1 = data.get("so_phat_hanh", "")
            elif loai == "Bao":
                t1 = data.get("ngay_phat_hanh", "")
            elif loai == "LuanVan":
                t1 = data.get("truong_dai_hoc", "")
            elif loai == "BanThao":
                t1 = data.get("tinh_trang", "")

            cursor.execute('''
                INSERT INTO SanPham (ma_so, loai, ten, gia_co_ban, so_luong, thong_tin_1, thong_tin_2)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (sp.ma_so, loai, sp.ten, sp.gia_co_ban, sp.so_luong, t1, t2))

        conn.commit()
        conn.close()
        return True

    except Exception as loi:
        print(f"[LỖI] Không lưu được CSDL: {loi}")
        return False
