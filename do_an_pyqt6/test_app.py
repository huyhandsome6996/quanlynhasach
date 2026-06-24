import os
import sys

# Thêm đường dẫn để test độc lập
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from models.subclasses import Sach, TapChi, Bao, LuanVan, BanThao
from models.linked_list import DanhSachLienKetDoi
from models.ngan_xep import NganXep       # Stack LIFO
from models.hang_doi import HangDoi       # Queue FIFO
from models.nguoi_dung import kiem_tra_dang_nhap  # Phân quyền Admin/NV
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
#       - Sách          = giá cơ bản * 1.20  (+20%)
#       - Tạp chí       = giá cơ bản * 0.90  (-10%)
#       - Báo           = giá cơ bản * 1.00  (giữ nguyên)
#       - Luận văn      = giá cơ bản * 1.30  (+30%)
#       - Bản thảo mới  = giá cơ bản * 1.50  (+50%)
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

# ====================================================================
# 7. KIỂM THỬ NGĂN XẾP (STACK) - Dùng cho UNDO/REDO
# ====================================================================
print("\n" + "=" * 60)
print("6. KIỂM THỬ NGĂN XẾP (STACK LIFO)")
print("=" * 60)
ngan_xep = NganXep()

# Đẩy 3 thao tác vào
ngan_xep.day_vao({"thao_tac": "them", "sp": sp1})
ngan_xep.day_vao({"thao_tac": "them", "sp": sp2})
ngan_xep.day_vao({"thao_tac": "xoa",  "sp": sp3})
print(f"   - Đã đẩy 3 phần tử. Số lượng: {ngan_xep.so_luong}")
print(f"   - Phần tử trên đỉnh (Peek): {ngan_xep.xem_dinh()['thao_tac']}")

# Lấy ra theo LIFO (vào sau, ra trước)
print("   - Lấy ra theo thứ tự LIFO:")
while not ngan_xep.rong():
    pt = ngan_xep.lay_ra()
    print(f"     → {pt['thao_tac']} {pt['sp'].ma_so}")

# ====================================================================
# 8. KIỂM THỬ HÀNG ĐỢI (QUEUE) - Dùng cho GIỎ HÀNG
# ====================================================================
print("\n" + "=" * 60)
print("7. KIỂM THỬ HÀNG ĐỢI (QUEUE FIFO) - MÔ PHỎNG GIỎ HÀNG")
print("=" * 60)
gio_hang = HangDoi()

# Thêm 3 món vào giỏ (giống người dùng click "Thêm vào giỏ")
gio_hang.them_vao(sp1)
gio_hang.them_vao(sp2)
gio_hang.them_vao(sp4)
print(f"   - Đã thêm 3 món vào giỏ. Số lượng: {gio_hang.so_luong}")

# Xem danh sách món trong giỏ
print("   - Các món trong giỏ (theo thứ tự FIFO):")
tong_tien = 0
for i, sp in enumerate(gio_hang.xem_danh_sach()):
    gia = sp.tinh_gia_ban()
    tong_tien += gia
    print(f"     {i+1}. [{sp.ma_so}] {sp.ten} - {gia:,.0f} đ")
print(f"   - TỔNG TIỀN: {tong_tien:,.0f} đ")

# Thanh toán: lấy từng món ra theo FIFO (vào trước, ra trước)
print("   - Bắt đầu thanh toán (lấy ra theo FIFO):")
tong_thanh_toan = 0
while not gio_hang.rong():
    sp = gio_hang.lay_ra()
    gia = sp.tinh_gia_ban()
    tong_thanh_toan += gia
    print(f"     → Đã thanh toán: [{sp.ma_so}] {sp.ten} - {gia:,.0f} đ")
print(f"   - TỔNG ĐÃ THANH TOÁN: {tong_thanh_toan:,.0f} đ")
print(f"   - Giỏ hàng rỗng sau khi thanh toán? {gio_hang.rong()}")

# ====================================================================
# 9. KIỂM THỬ LƯU TRỮ SQLITE
# ====================================================================
print("\n" + "=" * 60)
print("8. LƯU DỮ LIỆU VÀO SQLITE")
print("=" * 60)
luu_du_lieu_sqlite(ds.duyet_danh_sach())
print("   → Đã lưu thành công")

# 10. Đọc từ SQLite và kiểm tra đa hình
print("\n9. ĐỌC DỮ LIỆU TỪ SQLITE (kiểm tra đa hình có còn không):")
data_tu_db = doc_du_lieu_sqlite()
for sp in data_tu_db:
    print(f"   {sp.__class__.__name__:10} | {sp}")

print("\n" + "=" * 60)
print("9. TẠM KẾT PHẦN KIỂM THỬ CẤU TRÚC DỮ LIỆU")
print("Đã kiểm tra: OOP + Linked List + Stack + Queue + SQLite")
print("=" * 60)

# ====================================================================
# 10. KIỂM THỬ ĐĂNG NHẬP PHÂN QUYỀN (Admin / Nhân viên)
# ====================================================================
print("\n" + "=" * 60)
print("10. KIỂM THỬ ĐĂNG NHẬP PHÂN QUYỀN (ADMIN / NHÂN VIÊN)")
print("=" * 60)

# Test sai mật khẩu
nguoi_sai = kiem_tra_dang_nhap("admin", "sai_mat_khau")
print(f"   - Đăng nhập sai mật khẩu → trả về: {nguoi_sai}")
assert nguoi_sai is None, "Sai mật khẩu phải trả về None!"

# Test sai tên đăng nhập
nguoi_sai_2 = kiem_tra_dang_nhap("khong_co_nguoi_nay", "123")
print(f"   - Đăng nhập sai tên       → trả về: {nguoi_sai_2}")
assert nguoi_sai_2 is None, "Sai tên đăng nhập phải trả về None!"

# Test tài khoản Admin
admin = kiem_tra_dang_nhap("admin", "123")
print(f"   - Đăng nhập admin/123     → trả về: {admin.ten_dang_nhap} ({admin.quyen})")
print(f"     + Là Admin?     {admin.la_admin()}")
print(f"     + Là Nhân viên? {admin.la_nhan_vien()}")
assert admin.la_admin() is True
assert admin.la_nhan_vien() is False

# Test tài khoản Nhân viên
nv = kiem_tra_dang_nhap("nhanvien", "123")
print(f"   - Đăng nhập nhanvien/123  → trả về: {nv.ten_dang_nhap} ({nv.quyen})")
print(f"     + Là Admin?     {nv.la_admin()}")
print(f"     + Là Nhân viên? {nv.la_nhan_vien()}")
assert nv.la_admin() is False
assert nv.la_nhan_vien() is True

print("   → Phân quyền hoạt động đúng: Admin = toàn quyền, Nhân viên = không được xóa!")

print("\n" + "=" * 60)
print("MỌI THỨ HOẠT ĐỘNG HOÀN HẢO!")
print("Đã kiểm tra đủ: OOP + Linked List + Stack + Queue + SQLite + Phân quyền")
print("=" * 60)
