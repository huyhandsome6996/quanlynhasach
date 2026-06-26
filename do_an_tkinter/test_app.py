"""
Tệp test_app.py — Kiểm thử tự động cho ứng dụng Tkinter
=========================================================

Kiểm tra logic (không cần mở GUI):
    1. Khởi tạo hệ thống
    2. Đăng nhập admin/nhanvien
    3. CRUD 5 loại sản phẩm
    4. Tìm kiếm + Sắp xếp
    5. Thống kê
    6. Undo / Redo (Stack LIFO)
    7. Giỏ hàng (Queue FIFO) + thanh toán
    8. Phân quyền (nhân viên không được xóa)
    9. try/except cho 7 thao tác chính

Chạy:
    cd do_an_tkinter
    python test_app.py
"""

import os
import sys

# Thêm thư mục hiện tại vào path để import được `loi_thuat_toan`.
sys.path.insert(0, os.path.abspath('.'))

# Xóa DB cũ để test sạch.
from loi_thuat_toan.ket_noi_sqlite import lay_duong_dan_db
duong_dan_db = lay_duong_dan_db()
if os.path.exists(duong_dan_db):
    os.remove(duong_dan_db)
    print(f'✓ Đã xóa DB cũ: {duong_dan_db}')

# Import các lớp cần test.
from quan_ly_trung_tam import QuanLyTrungTam

SO_TEST = 0
SO_PASS = 0


def kiem_tra(ten, dieu_kien, chi_tiet=''):
    """Hàm tiện ích — in kết quả test."""
    global SO_TEST, SO_PASS
    SO_TEST += 1
    if dieu_kien:
        SO_PASS += 1
        print(f'  [PASS] {ten}')
    else:
        print(f'  [FAIL] {ten} {chi_tiet}')


# ============================================================
# KHỞI TẠO
# ============================================================
print('=' * 70)
print('TEST 1: KHỞI TẠO HỆ THỐNG')
print('=' * 70)
qly = QuanLyTrungTam()
kiem_tra('khoi_tao() trả True', qly.khoi_tao() is True)
kiem_tra('Danh sách có dữ liệu mẫu', qly.danh_sach.so_luong >= 5)


# ============================================================
# ĐĂNG NHẬP + PHÂN QUYỀN
# ============================================================
print()
print('=' * 70)
print('TEST 2: ĐĂNG NHẬP + PHÂN QUYỀN')
print('=' * 70)

# Sai mật khẩu.
ok, msg = qly.dang_nhap('admin', 'sai')
kiem_tra('Sai mật khẩu → False', ok is False)

# Sai tên đăng nhập.
ok, msg = qly.dang_nhap('khongtonai', '123')
kiem_tra('Sai tên đăng nhập → False', ok is False)

# Admin đúng.
ok, nd = qly.dang_nhap('admin', '123')
kiem_tra('Admin đăng nhập OK', ok and nd.vai_tro == 'admin')
kiem_tra('la_admin() trả True', qly.la_admin() is True)

# Nhân viên.
ok, nd = qly.dang_nhap('nhanvien', '123')
kiem_tra('Nhân viên đăng nhập OK', ok and nd.vai_tro == 'nhan_vien')
kiem_tra('la_admin() trả False (nhanvien)', qly.la_admin() is False)


# ============================================================
# THÊM 5 LOẠI SẢN PHẨM
# ============================================================
print()
print('=' * 70)
print('TEST 3: THÊM 5 LOẠI SẢN PHẨM (OOP ĐA HÌNH)')
print('=' * 70)

# Đăng nhập lại admin để test CRUD.
qly.dang_nhap('admin', '123')

so_cu = qly.danh_sach.so_luong

# Sách.
ok, msg = qly.them_san_pham({
    'loai_hang': 'Sách', 'ma_so': 'TK01', 'ten_san_pham': 'Sách Python',
    'gia_co_ban': 100000, 'ton_kho': 10,
    'tac_gia': 'Tác giả A', 'nha_xuat_ban': 'NXB Giáo dục'
})
kiem_tra('Thêm Sách', ok and qly.danh_sach.so_luong == so_cu + 1)

# Tạp chí.
ok, msg = qly.them_san_pham({
    'loai_hang': 'Tạp chí', 'ma_so': 'TK02', 'ten_san_pham': 'Tạp chí IT',
    'gia_co_ban': 50000, 'ton_kho': 20, 'so_phat_hanh': 'Số 12/2025'
})
kiem_tra('Thêm Tạp chí', ok and qly.danh_sach.so_luong == so_cu + 2)

# Báo giấy.
ok, msg = qly.them_san_pham({
    'loai_hang': 'Báo giấy', 'ma_so': 'TK03', 'ten_san_pham': 'Báo Tuổi Trẻ',
    'gia_co_ban': 10000, 'ton_kho': 50, 'ngay_xuat_ban': '26/06/2026'
})
kiem_tra('Thêm Báo giấy', ok and qly.danh_sach.so_luong == so_cu + 3)

# Luận văn.
ok, msg = qly.them_san_pham({
    'loai_hang': 'Luận văn', 'ma_so': 'TK04', 'ten_san_pham': 'Luận văn CNTT',
    'gia_co_ban': 200000, 'ton_kho': 5,
    'tac_gia': 'Sinh viên A', 'truong_dai_hoc': 'ĐH Bách Khoa'
})
kiem_tra('Thêm Luận văn', ok and qly.danh_sach.so_luong == so_cu + 4)

# Bản thảo.
ok, msg = qly.them_san_pham({
    'loai_hang': 'Bản thảo', 'ma_so': 'TK05', 'ten_san_pham': 'Bản thảo Tiểu thuyết',
    'gia_co_ban': 150000, 'ton_kho': 3,
    'tac_gia': 'Nhà văn B', 'trang_thai': 'Đã duyệt'
})
kiem_tra('Thêm Bản thảo', ok and qly.danh_sach.so_luong == so_cu + 5)

# Thêm trùng mã.
ok, msg = qly.them_san_pham({
    'loai_hang': 'Sách', 'ma_so': 'TK01', 'ten_san_pham': 'Trùng mã',
    'gia_co_ban': 100, 'ton_kho': 1, 'tac_gia': 'X', 'nha_xuat_ban': 'Y'
})
kiem_tra('Trùng mã → False', ok is False)


# ============================================================
# SỬA SẢN PHẨM
# ============================================================
print()
print('=' * 70)
print('TEST 4: SỬA SẢN PHẨM')
print('=' * 70)

ok, msg = qly.sua_san_pham({
    'ma_so': 'TK01', 'ten_san_pham': 'Sách Python 2026',
    'gia_co_ban': 120000, 'ton_kho': 8,
    'tac_gia': 'Tác giả A+', 'nha_xuat_ban': 'NXB Mới'
})
kiem_tra('Sửa thành công', ok)
sp = qly.danh_sach.tim_theo_ma_so('TK01')
kiem_tra('Tên đã cập nhật', sp.ten_san_pham == 'Sách Python 2026')
kiem_tra('Giá đã cập nhật', sp.gia_co_ban == 120000)


# ============================================================
# TÌM KIẾM + SẮP XẾP
# ============================================================
print()
print('=' * 70)
print('TEST 5: TÌM KIẾM + SẮP XẾP')
print('=' * 70)

# Tìm theo tên.
kq = qly.tim_kiem('Python', 'ten')
kiem_tra('Tìm theo tên: "Python"', len(kq) == 1 and kq[0]['ma_so'] == 'TK01')

# Tìm theo mã.
kq = qly.tim_kiem('TK02', 'ma')
kiem_tra('Tìm theo mã: TK02', len(kq) == 1 and kq[0]['ten_san_pham'] == 'Tạp chí IT')

# Tìm theo loại.
kq = qly.tim_kiem('Sách', 'loai')
kiem_tra('Tìm theo loại: Sách', len(kq) >= 1)

# Sắp xếp theo giá.
ds = qly.sap_xep('gia_ban')
kiem_tra('Sắp xếp theo giá_ban',
         all(ds[i]['gia_ban'] <= ds[i+1]['gia_ban'] for i in range(len(ds)-1)))


# ============================================================
# XÓA + PHÂN QUYỀN
# ============================================================
print()
print('=' * 70)
print('TEST 6: XÓA + PHÂN QUYỀN')
print('=' * 70)

# Đăng nhập nhân viên → cố xóa → bị chặn.
qly.dang_nhap('nhanvien', '123')
ok, msg = qly.xoa_san_pham('TK03')
kiem_tra('NV cố xóa → bị chặn', ok is False and 'NHÂN VIÊN' in msg.upper())

# Admin xóa.
qly.dang_nhap('admin', '123')
so_cu = qly.danh_sach.so_luong
ok, msg = qly.xoa_san_pham('TK03')
kiem_tra('Admin xóa OK', ok and qly.danh_sach.so_luong == so_cu - 1)


# ============================================================
# UNDO / REDO
# ============================================================
print()
print('=' * 70)
print('TEST 7: UNDO / REDO (STACK LIFO)')
print('=' * 70)

so_cu = qly.danh_sach.so_luong

# Undo xóa TK03 → thêm lại.
ok, msg = qly.hoan_tac()
kiem_tra('Undo xóa → thêm lại TK03', ok and qly.danh_sach.so_luong == so_cu + 1)

# Redo → xóa lại TK03 (lúc này 'xoa TK03' được đẩy lại lên đỉnh undo).
ok, msg = qly.lam_lai()
kiem_tra('Redo → xóa lại TK03', ok and qly.danh_sach.so_luong == so_cu)

# Undo 1: lại undo 'xoa TK03' (vì redo vừa đẩy xoa lên đỉnh undo).
ok, msg = qly.hoan_tac()
kiem_tra('Undo xoa (lần 2)', ok and qly.danh_sach.so_luong == so_cu + 1)
# Undo 2: undo 'sua TK01'.
ok, msg = qly.hoan_tac()
kiem_tra('Undo sửa', ok and qly.danh_sach.so_luong == so_cu + 1)
# Undo 3: undo 'them TK05' → TK05 bị xóa.
ok, msg = qly.hoan_tac()
kiem_tra('Undo thêm', ok and qly.danh_sach.so_luong == so_cu)


# ============================================================
# GIỎ HÀNG (QUEUE FIFO) + THANH TOÁN
# ============================================================
print()
print('=' * 70)
print('TEST 8: GIỎ HÀNG (QUEUE FIFO) + THANH TOÁN')
print('=' * 70)

# Thêm 3 sản phẩm vào giỏ.
qly.them_vao_gio('TK01')
qly.them_vao_gio('TK02')
qly.them_vao_gio('TK04')

ds, tong, sl = qly.xem_gio_hang()
kiem_tra('Giỏ có 3 món', sl == 3)
kiem_tra('Món đầu = TK01 (FIFO)', ds[0]['ma_so'] == 'TK01')
kiem_tra('Tổng tiền > 0', tong > 0)

# Xóa 1 món khỏi giỏ.
ok, msg = qly.xoa_khoi_gio('TK02')
kiem_tra('Xóa TK02 khỏi giỏ', ok and qly.gio_hang.so_luong == 2)

# Thanh toán.
ok, msg, hoa_don = qly.thanh_toan()
kiem_tra('Thanh toán thành công', ok and hoa_don['so_mon'] == 2)
kiem_tra('Hóa đơn có tổng tiền', hoa_don['tong_tien'] > 0)

# Giỏ rỗng sau thanh toán.
ok, msg, hoa_don = qly.thanh_toan()
kiem_tra('Giỏ rỗng sau thanh toán', ok is False)


# ============================================================
# THỐNG KÊ
# ============================================================
print()
print('=' * 70)
print('TEST 9: THỐNG KÊ')
print('=' * 70)

tk = qly.lay_thong_ke()
kiem_tra('Có key tong_so', 'tong_so' in tk)
kiem_tra('Có key dat_nhat', 'dat_nhat' in tk)
kiem_tra('Có key re_nhat', 're_nhat' in tk)
kiem_tra('Có key theo_loai', 'theo_loai' in tk)
kiem_tra('Tổng giá trị kho > 0', tk.get('tong_gia_tri_kho', 0) > 0)


# ============================================================
# TRY/EXCEPT CHO 7 THAO TÁC
# ============================================================
print()
print('=' * 70)
print('TEST 10: TRY/EXCEPT CHO 7 THAO TÁC')
print('=' * 70)

import inspect

# Đọc source của từng hàm để check có 'try:' và 'except'.
for ten_ham in ['them_san_pham', 'sua_san_pham', 'xoa_san_pham',
                 'hoan_tac', 'lam_lai', 'them_vao_gio', 'thanh_toan']:
    fn = getattr(qly, ten_ham)
    src = inspect.getsource(fn)
    co_try = 'try:' in src
    co_except = 'except' in src
    kiem_tra(f'{ten_ham} có try/except', co_try and co_except)


# ============================================================
# TỔNG KẾT
# ============================================================
print()
print('=' * 70)
print(f'KẾT QUẢ: {SO_PASS}/{SO_TEST} PASS')
print('=' * 70)
if SO_PASS == SO_TEST:
    print('TẤT CẢ TEST ĐỀU PASS ✓')
else:
    print(f'CÓ {SO_TEST - SO_PASS} TEST FAIL ✗')
sys.exit(0 if SO_PASS == SO_TEST else 1)
