import os
import sys

# Thêm đường dẫn để test độc lập
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from models.subclasses import Sach, TapChi, Bao, LuanVan, BanThao
from models.linked_list import DanhSachLienKetDoi
from data.sqlite_db import luu_du_lieu_sqlite, doc_du_lieu_sqlite

print("--- BẮT ĐẦU KIỂM THỬ ---")

# 1. Dọn dẹp DB cũ để test từ đầu
db_path = "data/quan_ly_nha_sach.db"
if os.path.exists(db_path):
    os.remove(db_path)

# 2. Khởi tạo đối tượng OOP (Tính Đa Hình)
sp1 = Sach("S01", "Lập trình C++ Nâng cao", 150000, 10, "Bjarne", "NXB Trẻ")
sp2 = Sach("S02", "Python Cơ Bản", 90000, 5, "Guido", "NXB KHTN")
sp3 = TapChi("T01", "Công Nghệ PC", 45000, 20, "Số 15")
sp4 = BanThao("BT01", "Bản Thảo AI", 200000, 1, "Rất cũ")

# 3. Đưa vào Danh Sách Liên Kết Đôi (Doubly Linked List)
ds = DanhSachLienKetDoi()
ds.them_vao_cuoi(sp1)
ds.them_vao_cuoi(sp2)
ds.them_vao_cuoi(sp3)
ds.them_vao_cuoi(sp4)

print("\n1. TRƯỚC KHI SẮP XẾP:")
for sp in ds.duyet_danh_sach():
    print("   ", sp)

# 4. Kiểm thử Thuật toán Merge Sort trên Linked List
ds.sap_xep(tieu_chi="gia_ban", tang_dan=True)
print("\n2. SAU KHI SẮP XẾP BẰNG MERGE SORT (Giá tăng dần):")
for sp in ds.duyet_danh_sach():
    print("   ", sp)

# 5. Kiểm thử Lưu trữ SQLite
luu_du_lieu_sqlite(ds.duyet_danh_sach())
print("\n3. ĐÃ LƯU DỮ LIỆU VÀO SQLITE THÀNH CÔNG")

# 6. Đọc từ SQLite
data_tu_db = doc_du_lieu_sqlite()
print("\n4. ĐỌC DỮ LIỆU TỪ SQLITE:")
for sp in data_tu_db:
    print("   ", sp)

print("\n--- MỌI THỨ HOẠT ĐỘNG HOÀN HẢO! ---")
