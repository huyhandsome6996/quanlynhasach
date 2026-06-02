"""
Tệp chứa các hàm đọc/ghi vào cơ sở dữ liệu SQLite (db.sqlite3).
Bao gồm: tạo bảng, tải dữ liệu lên RAM, lưu/xóa dữ liệu khi có biến động.

Quy tắc: Tên biến, tên hàm, chú thích sử dụng tiếng Việt.
Ngoại lệ: Các từ khóa SQL chuẩn (SELECT, INSERT, DELETE, CREATE TABLE, v.v.).
"""

import sqlite3
import os


def lay_duong_dan_db():
    """
    Lấy đường dẫn tuyệt đối đến tệp cơ sở dữ liệu SQLite.

    Trả về:
        str: Đường dẫn tuyệt đối đến db.sqlite3.
    """
    # Đường dẫn tương đối từ tệp này đến db.sqlite3
    thu_muc_hien_tai = os.path.dirname(os.path.abspath(__file__))
    duong_dan_du_an = os.path.dirname(os.path.dirname(os.path.dirname(thu_muc_hien_tai)))
    return os.path.join(duong_dan_du_an, 'db.sqlite3')


def tao_bang_neu_chua_co():
    """
    Tạo bảng bang_mat_hang trong SQLite nếu chưa tồn tại.
    Bảng này lưu trữ toàn bộ thông tin về các mặt hàng trong cửa hàng.

    Các cột:
        ma_so: Mã định danh duy nhất (Khóa chính).
        loai_hang: Loại mặt hàng (Sách, Tạp chí, Báo giấy).
        ten_san_pham: Tên sản phẩm.
        gia_co_ban: Giá cơ bản (số thực).
        ton_kho: Số lượng tồn kho (số nguyên).
        tac_gia: Tên tác giả (dùng cho Sách, NULL cho loại khác).
        nha_xuat_ban: Tên nhà xuất bản (dùng cho Sách, NULL cho loại khác).
        so_phat_hanh: Số phát hành (dùng cho Tạp chí, NULL cho loại khác).
        ngay_xuat_ban: Ngày xuất bản (dùng cho Báo giấy, NULL cho loại khác).
    """
    duong_dan = lay_duong_dan_db()
    ket_noi = sqlite3.connect(duong_dan)
    con_tro = ket_noi.cursor()

    con_tro.execute('''
        CREATE TABLE IF NOT EXISTS bang_mat_hang (
            ma_so TEXT PRIMARY KEY,
            loai_hang TEXT NOT NULL,
            ten_san_pham TEXT NOT NULL,
            gia_co_ban REAL NOT NULL,
            ton_kho INTEGER NOT NULL,
            tac_gia TEXT,
            nha_xuat_ban TEXT,
            so_phat_hanh TEXT,
            ngay_xuat_ban TEXT
        )
    ''')

    ket_noi.commit()
    ket_noi.close()


def tai_du_lieu(danh_sach_lien_ket):
    """
    Tải toàn bộ dữ liệu từ SQLite và biến thành đối tượng OOP,
    sau đó đẩy vào danh sách liên kết đôi trên RAM.

    Luồng hoạt động:
        1. Chạy lệnh SELECT * FROM bang_mat_hang để lấy toàn bộ dữ liệu.
        2. Dựa vào cột loai_hang, khởi tạo đối tượng tương ứng (Sach, TapChi, BaoGiay).
        3. Các đối tượng được đưa vào thuộc tính data của các Node
           và dùng hàm them_vao_cuoi() để nối vào danh_sach_lien_ket.

    Tham số:
        danh_sach_lien_ket: Đối tượng DoublyLinkedList để nạp dữ liệu vào.
    """
    from .lop_doi_tuong import Sach, TapChi, BaoGiay

    # Đảm bảo bảng đã tồn tại
    tao_bang_neu_chua_co()

    duong_dan = lay_duong_dan_db()
    ket_noi = sqlite3.connect(duong_dan)
    con_tro = ket_noi.cursor()

    # Lấy toàn bộ dữ liệu từ bảng
    con_tro.execute('SELECT * FROM bang_mat_hang')
    cac_hang = con_tro.fetchall()

    for hang in cac_hang:
        ma_so = hang[0]
        loai_hang = hang[1]
        ten_san_pham = hang[2]
        gia_co_ban = hang[3]
        ton_kho = hang[4]

        # Dựa vào cột loai_hang để khởi tạo đối tượng OOP tương ứng
        if loai_hang == 'Sách':
            tac_gia = hang[5] if hang[5] else ''
            nha_xuat_ban = hang[6] if hang[6] else ''
            san_pham = Sach(ma_so, ten_san_pham, gia_co_ban, ton_kho, tac_gia, nha_xuat_ban)

        elif loai_hang == 'Tạp chí':
            so_phat_hanh = hang[7] if hang[7] else ''
            san_pham = TapChi(ma_so, ten_san_pham, gia_co_ban, ton_kho, so_phat_hanh)

        elif loai_hang == 'Báo giấy':
            ngay_xuat_ban = hang[8] if hang[8] else ''
            san_pham = BaoGiay(ma_so, ten_san_pham, gia_co_ban, ton_kho, ngay_xuat_ban)

        else:
            # Bỏ qua nếu loại hàng không xác định
            continue

        # Đưa đối tượng vào danh sách liên kết đôi
        danh_sach_lien_ket.them_vao_cuoi(san_pham)

    ket_noi.close()


def luu_mot_san_pham(san_pham):
    """
    Lưu một sản phẩm mới vào cơ sở dữ liệu SQLite.
    Chạy lệnh INSERT INTO bang_mat_hang để lưu vĩnh viễn.

    Tham số:
        san_pham: Đối tượng mặt hàng (Sach, TapChi, hoặc BaoGiay) cần lưu.
    """
    duong_dan = lay_duong_dan_db()
    ket_noi = sqlite3.connect(duong_dan)
    con_tro = ket_noi.cursor()

    # Lấy các thuộc tính cơ bản
    ma_so = san_pham.ma_so
    loai_hang = san_pham.loai_hang
    ten_san_pham = san_pham.ten_san_pham
    gia_co_ban = san_pham.gia_co_ban
    ton_kho = san_pham.ton_kho

    # Lấy các thuộc tính riêng tùy theo loại hàng
    tac_gia = getattr(san_pham, 'tac_gia', None)
    nha_xuat_ban = getattr(san_pham, 'nha_xuat_ban', None)
    so_phat_hanh = getattr(san_pham, 'so_phat_hanh', None)
    ngay_xuat_ban = getattr(san_pham, 'ngay_xuat_ban', None)

    con_tro.execute('''
        INSERT INTO bang_mat_hang (ma_so, loai_hang, ten_san_pham, gia_co_ban, ton_kho,
                                    tac_gia, nha_xuat_ban, so_phat_hanh, ngay_xuat_ban)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (ma_so, loai_hang, ten_san_pham, gia_co_ban, ton_kho,
          tac_gia, nha_xuat_ban, so_phat_hanh, ngay_xuat_ban))

    ket_noi.commit()
    ket_noi.close()


def xoa_mot_san_pham(ma_so):
    """
    Xóa một sản phẩm khỏi cơ sở dữ liệu SQLite dựa trên mã số.
    Chạy lệnh DELETE FROM bang_mat_hang WHERE ma_so = ?.

    Tham số:
        ma_so (str): Mã số định danh duy nhất của sản phẩm cần xóa.
    """
    duong_dan = lay_duong_dan_db()
    ket_noi = sqlite3.connect(duong_dan)
    con_tro = ket_noi.cursor()

    con_tro.execute('DELETE FROM bang_mat_hang WHERE ma_so = ?', (ma_so,))

    ket_noi.commit()
    ket_noi.close()
