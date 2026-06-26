"""
Test đầy đủ các tính năng theo barem chấm điểm:
1) Đăng nhập phân quyền (admin/nhanvien)
2) OOP đa hình (5 lớp con)
3) DoublyLinkedList + Merge Sort
4) Stack LIFO (Undo/Redo)
5) Queue FIFO (Giỏ hàng)
6) SQLite CRUD
7) Tìm kiếm nâng cao
"""

import os, sys, json

# Cấu hình Django
sys.path.insert(0, os.path.abspath('.'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cau_hinh_he_thong.settings')

import django
django.setup()

# Khởi tạo DB + dữ liệu mẫu
from ung_dung_giao_tiep.loi_thuat_toan.ket_noi_sqlite import tao_bang_neu_chua_co, lay_duong_dan_db
from ung_dung_giao_tiep.loi_thuat_toan.nguoi_dung import khoi_tao_nguoi_dung_mac_dinh, kiem_tra_dang_nhap

# Xóa DB cũ để test từ đầu
duong_dan_db = lay_duong_dan_db()
if os.path.exists(duong_dan_db):
    os.remove(duong_dan_db)
    print(f'Đã xóa DB cũ: {duong_dan_db}')

tao_bang_neu_chua_co()
khoi_tao_nguoi_dung_mac_dinh()

# Import các lớp cần test
from ung_dung_giao_tiep.loi_thuat_toan.lop_doi_tuong import MatHang, Sach, TapChi, BaoGiay, LuanVan, BanThao
from ung_dung_giao_tiep.loi_thuat_toan.danh_sach_lien_ket import DoublyLinkedList
from ung_dung_giao_tiep.loi_thuat_toan.cau_truc_du_lieu import NganXep, HangDoi

SO_TEST = 0
SO_PASS = 0

def kiem_tra(ten, dieu_kien, chi_tiet=''):
    global SO_TEST, SO_PASS
    SO_TEST += 1
    if dieu_kien:
        SO_PASS += 1
        print(f'  [PASS] {ten}')
    else:
        print(f'  [FAIL] {ten} {chi_tiet}')


print('=' * 70)
print('TEST 1: ĐĂNG NHHẬP PHÂN QUYỀN')
print('=' * 70)

# Test sai mật khẩu
nguoi = kiem_tra_dang_nhap('admin', 'sai_mat_khau')
kiem_tra('Sai mật khẩu → None', nguoi is None)

# Test sai tên đăng nhập
nguoi = kiem_tra_dang_nhap('khong_ton_tai', '123')
kiem_tra('Sai tên đăng nhập → None', nguoi is None)

# Test admin đúng
nguoi = kiem_tra_dang_nhap('admin', '123')
kiem_tra('admin/123 → không None', nguoi is not None)
kiem_tra('admin/123 → la_admin() True', nguoi and nguoi.la_admin())

# Test nhân viên đúng
nguoi = kiem_tra_dang_nhap('nhanvien', '123')
kiem_tra('nhanvien/123 → không None', nguoi is not None)
kiem_tra('nhanvien/123 → la_admin() False', nguoi and not nguoi.la_admin())


print()
print('=' * 70)
print('TEST 2: OOP ĐA HÌNH - 5 LỚP CON')
print('=' * 70)

sach = Sach('MH001', 'Sách Python', 100000, 10, 'Tác giả A', 'NXB Giáo dục')
kiem_tra('Sach.tinh_gia_ban() = 110000 (gia*1.1)', abs(sach.tinh_gia_ban() - 110000) < 0.01)

tap_chi = TapChi('MH002', 'Tạp chí KH', 50000, 20, 'Số 12')
kiem_tra('TapChi.tinh_gia_ban() = 52500 (gia*1.05)', abs(tap_chi.tinh_gia_ban() - 52500) < 0.01)

bao = BaoGiay('MH003', 'Báo ND', 8000, 100, '2025-06-25')
kiem_tra('BaoGiay.tinh_gia_ban() = 8000 (không phụ thu)', abs(bao.tinh_gia_ban() - 8000) < 0.01)

luan_van = LuanVan('MH004', 'Luận văn KS', 200000, 5, 'Trần B', 'ĐH BK', '2024')
kiem_tra('LuanVan.tinh_gia_ban() = 240000 (gia*1.2)', abs(luan_van.tinh_gia_ban() - 240000) < 0.01)

ban_thao = BanThao('MH005', 'Bản thảo S', 80000, 3, 'Lê C', 'Chưa duyệt')
kiem_tra('BanThao.tinh_gia_ban() = 92000 (gia*1.15)', abs(ban_thao.tinh_gia_ban() - 92000) < 0.01)

# Đa hình qua cha
ds_hang = [sach, tap_chi, bao, luan_van, ban_thao]
for h in ds_hang:
    kiem_tra(f'{h.__class__.__name__} là con MatHang', isinstance(h, MatHang))


print()
print('=' * 70)
print('TEST 3: DOUBLY LINKED LIST + MERGE SORT')
print('=' * 70)

ds = DoublyLinkedList()
for h in ds_hang:
    ds.them_vao_cuoi(h)

kiem_tra('Số lượng = 5', ds.so_luong == 5)
kiem_tra('Tim MH003 → "Báo ND"', ds.tim_theo_ma_so('MH003').ten_san_pham == 'Báo ND')
kiem_tra('Tim MH999 → None', ds.tim_theo_ma_so('MH999') is None)

# Merge Sort theo giá bán
ds.sap_xep_tron('gia_ban')
danh_sach = ds.chuyen_thanh_danh_sach()
gia_sap_xep = [item['gia_ban'] for item in danh_sach]
kiem_tra('Merge Sort theo giá bán', gia_sap_xep == sorted(gia_sap_xep),
         f'thực tế: {gia_sap_xep}')

# Xóa
ket_qua = ds.xoa_node('MH003')
kiem_tra('Xóa MH003 → True', ket_qua)
kiem_tra('Sau xóa: số lượng = 4', ds.so_luong == 4)

# Tìm kiếm theo tên
ket_qua = ds.tim_kiem('python')
kiem_tra("Tìm 'python' → 1 kết quả", len(ket_qua) == 1)


print()
print('=' * 70)
print('TEST 4: STACK LIFO (CHO UNDO/REDO)')
print('=' * 70)

stack = NganXep()
stack.day_vao('A')
stack.day_vao('B')
stack.day_vao('C')

kiem_tra('Số lượng = 3', stack.so_luong == 3)
kiem_tra('Lay_ra() = "C" (LIFO)', stack.lay_ra() == 'C')
kiem_tra('Lay_ra() = "B" (LIFO)', stack.lay_ra() == 'B')
kiem_tra('Lay_ra() = "A" (LIFO)', stack.lay_ra() == 'A')
kiem_tra('Stack rỗng sau khi lấy hết', stack.rong())


print()
print('=' * 70)
print('TEST 5: QUEUE FIFO (CHO GIỎ HÀNG)')
print('=' * 70)

queue = HangDoi()
queue.them_vao('Sách 1')
queue.them_vao('Sách 2')
queue.them_vao('Sách 3')

kiem_tra('Số lượng = 3', queue.so_luong == 3)
kiem_tra('Lay_ra() = "Sách 1" (FIFO)', queue.lay_ra() == 'Sách 1')
kiem_tra('Lay_ra() = "Sách 2" (FIFO)', queue.lay_ra() == 'Sách 2')
kiem_tra('Lay_ra() = "Sách 3" (FIFO)', queue.lay_ra() == 'Sách 3')
kiem_tra('Queue rỗng sau khi lấy hết', queue.rong())


print()
print('=' * 70)
print('TEST 6: SQLITE CRUD')
print('=' * 70)

from ung_dung_giao_tiep.loi_thuat_toan.ket_noi_sqlite import (
    luu_mot_san_pham, tai_du_lieu, cap_nhat_san_pham, xoa_mot_san_pham
)

# Lưu 1 sản phẩm
luu_mot_san_pham(sach)
ds_moi = DoublyLinkedList()
tai_du_lieu(ds_moi)
kiem_tra('Lưu + Tải lại → có MH001', ds_moi.tim_theo_ma_so('MH001') is not None)
kiem_tra('MH001 ten = "Sách Python"', ds_moi.tim_theo_ma_so('MH001').ten_san_pham == 'Sách Python')

# Cập nhật
sach.ten_san_pham = 'Sách Python 2025'
cap_nhat_san_pham(sach)
ds_moi2 = DoublyLinkedList()
tai_du_lieu(ds_moi2)
kiem_tra('Cập nhật tên → "Sách Python 2025"',
         ds_moi2.tim_theo_ma_so('MH001').ten_san_pham == 'Sách Python 2025')

# Xóa
xoa_mot_san_pham('MH001')
ds_moi3 = DoublyLinkedList()
tai_du_lieu(ds_moi3)
kiem_tra('Xóa MH001 → không còn', ds_moi3.tim_theo_ma_so('MH001') is None)


print()
print('=' * 70)
print('TEST 7: TRY/EXCEPT CHO 7 THAO TÁC')
print('=' * 70)

from ung_dung_giao_tiep import xu_ly_yeu_cau
xu_ly_yeu_cau.khoi_tao_danh_sach()

# Kiểm tra các hàm có bọc try/except không (đọc source)
import inspect
src_them = inspect.getsource(xu_ly_yeu_cau.them_san_pham)
src_sua  = inspect.getsource(xu_ly_yeu_cau.sua_san_pham)
src_xoa  = inspect.getsource(xu_ly_yeu_cau.xoa_san_pham)
src_undo = inspect.getsource(xu_ly_yeu_cau.hoan_tac)
src_redo = inspect.getsource(xu_ly_yeu_cau.lam_lai)
src_them_gio = inspect.getsource(xu_ly_yeu_cau.them_vao_gio_hang)
src_thanh_toan = inspect.getsource(xu_ly_yeu_cau.thanh_toan)

kiem_tra('them_san_pham có try/except', 'try:' in src_them and 'except' in src_them)
kiem_tra('sua_san_pham có try/except', 'try:' in src_sua and 'except' in src_sua)
kiem_tra('xoa_san_pham có try/except', 'try:' in src_xoa and 'except' in src_xoa)
kiem_tra('hoan_tac có try/except', 'try:' in src_undo and 'except' in src_undo)
kiem_tra('lam_lai có try/except', 'try:' in src_redo and 'except' in src_redo)
kiem_tra('them_vao_gio_hang có try/except', 'try:' in src_them_gio and 'except' in src_them_gio)
kiem_tra('thanh_toan có try/except', 'try:' in src_thanh_toan and 'except' in src_thanh_toan)


print()
print('=' * 70)
print(f'KẾT QUẢ: {SO_PASS}/{SO_TEST} PASS')
print('=' * 70)

if SO_PASS == SO_TEST:
    print('TẤT CẢ TEST ĐỀU PASS ✓')
    sys.exit(0)
else:
    print(f'CÓ {SO_TEST - SO_PASS} TEST FAIL ✗')
    sys.exit(1)
