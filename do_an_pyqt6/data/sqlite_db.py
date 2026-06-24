import sqlite3
import os
from models.subclasses import Sach, TapChi, Bao, LuanVan, BanThao

DB_PATH = "data/quan_ly_nha_sach.db"

def khoi_tao_db():
    if not os.path.exists("data"):
        os.makedirs("data")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Bảng SanPham duy nhất để chứa mọi thể loại (Dùng Nullable cho các cột riêng)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS SanPham (
        ma_so TEXT PRIMARY KEY,
        loai TEXT NOT NULL,
        ten TEXT NOT NULL,
        gia_ban REAL NOT NULL,
        so_luong INTEGER NOT NULL,
        thong_tin_1 TEXT,
        thong_tin_2 TEXT
    )
    ''')
    conn.commit()
    conn.close()

def doc_du_lieu_sqlite():
    khoi_tao_db()
    danh_sach = []
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SanPham")
    rows = cursor.fetchall()
    
    for row in rows:
        ma_so, loai, ten, gia_ban, so_luong, t1, t2 = row
        if loai == "Sach":
            sp = Sach(ma_so, ten, gia_ban, so_luong, t1, t2)
        elif loai == "TapChi":
            sp = TapChi(ma_so, ten, gia_ban, so_luong, t1)
        elif loai == "Bao":
            sp = Bao(ma_so, ten, gia_ban, so_luong, t1)
        elif loai == "LuanVan":
            sp = LuanVan(ma_so, ten, gia_ban, so_luong, t1)
        elif loai == "BanThao":
            sp = BanThao(ma_so, ten, gia_ban, so_luong, t1)
        else:
            continue
        danh_sach.append(sp)
    conn.close()
    return danh_sach

def luu_du_lieu_sqlite(mang_san_pham):
    khoi_tao_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Cách đơn giản nhất để đồng bộ từ Linked List xuống Database: Xóa sạch & Thêm lại
    cursor.execute("DELETE FROM SanPham")
    
    for sp in mang_san_pham:
        data = sp.to_dict()
        loai = data["loai"]
        t1 = ""
        t2 = ""
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
        INSERT INTO SanPham (ma_so, loai, ten, gia_ban, so_luong, thong_tin_1, thong_tin_2)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (sp.ma_so, loai, sp.ten, sp.gia_ban, sp.so_luong, t1, t2))
        
    conn.commit()
    conn.close()
