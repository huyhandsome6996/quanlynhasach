import os
import sys

# Thêm đường dẫn để test độc lập
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from models.subclasses import Sach, TapChi, Bao, LuanVan, BanThao
from models.linked_list import DanhSachLienKetDoi
from data.sqlite_db import luu_du_lieu_sqlite, doc_du_lieu_sqlite

print("=" * 60)
print("BẮT ĐẦU KIỂM THỬ ĐỒ ÁN PYQT6")
print("=" * 60)

# 1. Dọn dẹp DB cũ để test từ đầu
db_path = "data/quan_ly_nha_sach.db"
if os.path.exists(db_path):
    os.remove(db_path)

# 2. Khởi tạo đối tượng OOP (Tính Đa Hình)
#    Mỗi loại có cách tính giá bán khác nhau:
#       - Sách      = giá cơ bản * 1.20  (+20%)
#       - Tạp chí    = giá cơ bản * 0.90  (-10%)
#       - Báo        = giá cơ bản * 1.00  (giữ nguyên)
#       - Luận văn   = giá cơ bản * 1.30  (+30%)
#       - Bản thảo mới = giá cơ bản * 1.50 (+50%)
sp1 = Sach("S01", "Lập trình C++ Nâng cao",  100000, 10, "Bjarne",   "NXB Trẻ")
sp2 = TapChi("T01", "Công Nghệ PC",           50000, 20, "Số 15")
sp3 = Bao("B01",   "Báo Tuổi Trẻ",            5000,  100, "25/06/2025")
sp4 = LuanVan("LV01", "Luận văn AI",          200000, 3, "ĐH Bách Khoa")
sp5 = BanThao("BT01", "Bản thảo AI",          100000, 1, "mới")

# 3. Đưa vào Danh Sách Liên Kết Đôi (Doubly Linked List)
ds = DanhSachLienKetDoi()
ds.them_vao_cuoi(sp1)
ds.them_vao_cuoi(sp2)
ds.them_vao_cuoi(sp3)
ds.them_vao_cuoi(sp4)
ds.them_vao_cuoi(sp5)

print("\n1. KIỂM TRA TÍNH ĐA HÌNH (tinh_gia_ban):")
print(f"   - Sách     '{sp1.ten}': giá cơ bản {sp1.gia_co_ban:,.0f} → giá bán {sp1.tinh_gia_ban():,.0f}")
print(f"   - Tạp chí   '{sp2.ten}': giá cơ bản {sp2.gia_co_ban:,.0f} → giá bán {sp2.tinh_gia_ban():,.0f}")
print(f"   - Báo       '{sp3.ten}': giá cơ bản {sp3.gia_co_ban:,.0f} → giá bán {sp3.tinh_gia_ban():,.0f}")
print(f"   - Luận văn  '{sp4.ten}': giá cơ bản {sp4.gia_co_ban:,.0f} → giá bán {sp4.tinh_gia_ban():,.0f}")
print(f"   - Bản thảo  '{sp5.ten}': giá cơ bản {sp5.gia_co_ban:,.0f} → giá bán {sp5.tinh_gia_ban():,.0f}")

print("\n2. DANH SÁCH BAN ĐẦU (trước khi sắp xếp):")
for sp in ds.duyet_danh_sach():
    print("   ", sp)

# 4. Kiểm thử Thuật toán Merge Sort trên Linked List
ds.sap_xep(tieu_chi="gia_co_ban", tang_dan=True)
print("\n3. SAU KHI SẮP XẾP BẰNG MERGE SORT (Giá cơ bản tăng dần):")
for sp in ds.duyet_danh_sach():
    print("   ", sp)

# 5. Kiểm thử tìm kiếm trên Linked List
print("\n4. TÌM KIẾM SẢN PHẨM MÃ 'T01':")
ket_qua = ds.tim_kiem_theo_ma("T01")
print("   →", ket_qua)

# 6. Kiểm thử xóa trên Linked List
print("\n5. XÓA SẢN PHẨM MÃ 'B01':")
ds.xoa_nut_theo_ma("B01")
print(f"   → Còn lại {ds.so_luong} sản phẩm trong danh sách")

# 7. Kiểm thử Lưu trữ SQLite
print("\n6. LƯU DỮ LIỆU VÀO SQLITE:")
luu_du_lieu_sqlite(ds.duyet_danh_sach())
print("   → Đã lưu thành công")

# 8. Đọc từ SQLite và kiểm tra đa hình
print("\n7. ĐỌC DỮ LIỆU TỪ SQLITE (kiểm tra đa hình có còn không):")
data_tu_db = doc_du_lieu_sqlite()
for sp in data_tu_db:
    print(f"   {sp.__class__.__name__:10} | {sp}")

print("\n" + "=" * 60)
print("MỌI THỨ HOẠT ĐỘNG HOÀN HẢO!")
print("=" * 60)
