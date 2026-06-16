"""
Module kết nối cơ sở dữ liệu SQLite.
Lưu trữ dữ liệu bền vững với xử lý ngoại lệ (try-except-finally) đầy đủ.
"""

import sqlite3
import os


def lay_duong_dan_db():
    """Trả về đường dẫn tuyệt đối tới file database SQLite."""
    thu_muc_hien_tai = os.path.dirname(os.path.abspath(__file__))
    duong_dan_du_an = os.path.dirname(os.path.dirname(thu_muc_hien_tai))
    return os.path.join(duong_dan_du_an, 'db.sqlite3')


def tao_bang_neu_chua_co():
    """
    Tạo bảng bang_mat_hang nếu chưa tồn tại.
    Hỗ trợ lưu trữ tất cả 5 loại mặt hàng: Sách, Tạp chí, Báo giấy, Luận văn, Bản thảo.
    Áp dụng try-except-finally để đảm bảo đóng kết nối.
    """
    ket_noi = None
    try:
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
                ngay_xuat_ban TEXT,
                truong_dai_hoc TEXT,
                nam_bao_ve TEXT,
                tinh_trang TEXT
            )
        ''')
        # Tạo bảng người dùng cho đăng nhập phân quyền
        con_tro.execute('''
            CREATE TABLE IF NOT EXISTS bang_nguoi_dung (
                ten_dang_nhap TEXT PRIMARY KEY,
                mat_khau_hash TEXT NOT NULL,
                ho_ten TEXT NOT NULL,
                vai_tro TEXT NOT NULL DEFAULT 'nhan_vien'
            )
        ''')
        ket_noi.commit()
    except sqlite3.Error as loi:
        print(f'[LOI DATABASE] Loi khi tao bang: {str(loi)}')
        raise
    finally:
        if ket_noi:
            ket_noi.close()


def tai_du_lieu(danh_sach_lien_ket):
    """
    Nạp toàn bộ dữ liệu từ SQLite vào Danh sách liên kết đôi.
    Hỗ trợ 5 loại: Sách, Tạp chí, Báo giấy, Luận văn, Bản thảo.
    Áp dụng try-except-finally.
    """
    from .lop_doi_tuong import Sach, TapChi, BaoGiay, LuanVan, BanThao
    tao_bang_neu_chua_co()
    ket_noi = None
    try:
        duong_dan = lay_duong_dan_db()
        ket_noi = sqlite3.connect(duong_dan)
        con_tro = ket_noi.cursor()
        con_tro.execute('SELECT * FROM bang_mat_hang')
        cac_hang = con_tro.fetchall()
        # Lấy tên các cột để truy cập theo tên
        ten_cot = [mo_ta[0] for mo_ta in con_tro.description]
        for hang in cac_hang:
            du_lieu = dict(zip(ten_cot, hang))
            ma_so = du_lieu['ma_so']
            loai_hang = du_lieu['loai_hang']
            ten_san_pham = du_lieu['ten_san_pham']
            gia_co_ban = du_lieu['gia_co_ban']
            ton_kho = du_lieu['ton_kho']

            if loai_hang == 'Sách':
                tac_gia = du_lieu.get('tac_gia') or ''
                nha_xuat_ban = du_lieu.get('nha_xuat_ban') or ''
                san_pham = Sach(ma_so, ten_san_pham, gia_co_ban, ton_kho, tac_gia, nha_xuat_ban)
            elif loai_hang == 'Tạp chí':
                so_phat_hanh = du_lieu.get('so_phat_hanh') or ''
                san_pham = TapChi(ma_so, ten_san_pham, gia_co_ban, ton_kho, so_phat_hanh)
            elif loai_hang == 'Báo giấy':
                ngay_xuat_ban = du_lieu.get('ngay_xuat_ban') or ''
                san_pham = BaoGiay(ma_so, ten_san_pham, gia_co_ban, ton_kho, ngay_xuat_ban)
            elif loai_hang == 'Luận văn':
                tac_gia = du_lieu.get('tac_gia') or ''
                truong_dai_hoc = du_lieu.get('truong_dai_hoc') or ''
                nam_bao_ve = du_lieu.get('nam_bao_ve') or ''
                san_pham = LuanVan(ma_so, ten_san_pham, gia_co_ban, ton_kho, tac_gia, truong_dai_hoc, nam_bao_ve)
            elif loai_hang == 'Bản thảo':
                tac_gia = du_lieu.get('tac_gia') or ''
                tinh_trang = du_lieu.get('tinh_trang') or ''
                san_pham = BanThao(ma_so, ten_san_pham, gia_co_ban, ton_kho, tac_gia, tinh_trang)
            else:
                continue
            danh_sach_lien_ket.them_vao_cuoi(san_pham)
    except sqlite3.Error as loi:
        print(f'[LOI DATABASE] Loi khi tai du lieu: {str(loi)}')
        raise
    finally:
        if ket_noi:
            ket_noi.close()


def luu_mot_san_pham(san_pham):
    """
    Lưu một sản phẩm mới vào SQLite.
    Sử dụng parameterized query để chống SQL Injection.
    Áp dụng try-except-finally.
    """
    ket_noi = None
    try:
        duong_dan = lay_duong_dan_db()
        ket_noi = sqlite3.connect(duong_dan)
        con_tro = ket_noi.cursor()
        con_tro.execute('''
            INSERT INTO bang_mat_hang (ma_so, loai_hang, ten_san_pham, gia_co_ban, ton_kho,
                                        tac_gia, nha_xuat_ban, so_phat_hanh, ngay_xuat_ban,
                                        truong_dai_hoc, nam_bao_ve, tinh_trang)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            san_pham.ma_so,
            san_pham.loai_hang,
            san_pham.ten_san_pham,
            san_pham.gia_co_ban,
            san_pham.ton_kho,
            getattr(san_pham, 'tac_gia', None),
            getattr(san_pham, 'nha_xuat_ban', None),
            getattr(san_pham, 'so_phat_hanh', None),
            getattr(san_pham, 'ngay_xuat_ban', None),
            getattr(san_pham, 'truong_dai_hoc', None),
            getattr(san_pham, 'nam_bao_ve', None),
            getattr(san_pham, 'tinh_trang', None)
        ))
        ket_noi.commit()
    except sqlite3.IntegrityError as loi:
        print(f'[LOI DATABASE] Ma so da ton tai: {str(loi)}')
        raise
    except sqlite3.Error as loi:
        print(f'[LOI DATABASE] Loi khi luu san pham: {str(loi)}')
        raise
    finally:
        if ket_noi:
            ket_noi.close()


def cap_nhat_san_pham(san_pham):
    """
    Cập nhật thông tin sản phẩm trong SQLite.
    Sử dụng parameterized query để chống SQL Injection.
    Áp dụng try-except-finally.
    """
    ket_noi = None
    try:
        duong_dan = lay_duong_dan_db()
        ket_noi = sqlite3.connect(duong_dan)
        con_tro = ket_noi.cursor()
        con_tro.execute('''
            UPDATE bang_mat_hang SET
                loai_hang = ?,
                ten_san_pham = ?,
                gia_co_ban = ?,
                ton_kho = ?,
                tac_gia = ?,
                nha_xuat_ban = ?,
                so_phat_hanh = ?,
                ngay_xuat_ban = ?,
                truong_dai_hoc = ?,
                nam_bao_ve = ?,
                tinh_trang = ?
            WHERE ma_so = ?
        ''', (
            san_pham.loai_hang,
            san_pham.ten_san_pham,
            san_pham.gia_co_ban,
            san_pham.ton_kho,
            getattr(san_pham, 'tac_gia', None),
            getattr(san_pham, 'nha_xuat_ban', None),
            getattr(san_pham, 'so_phat_hanh', None),
            getattr(san_pham, 'ngay_xuat_ban', None),
            getattr(san_pham, 'truong_dai_hoc', None),
            getattr(san_pham, 'nam_bao_ve', None),
            getattr(san_pham, 'tinh_trang', None),
            san_pham.ma_so
        ))
        ket_noi.commit()
        return con_tro.rowcount > 0
    except sqlite3.Error as loi:
        print(f'[LOI DATABASE] Loi khi cap nhat: {str(loi)}')
        raise
    finally:
        if ket_noi:
            ket_noi.close()


def xoa_mot_san_pham(ma_so):
    """
    Xóa một sản phẩm khỏi SQLite theo mã số.
    Áp dụng try-except-finally.
    """
    ket_noi = None
    try:
        duong_dan = lay_duong_dan_db()
        ket_noi = sqlite3.connect(duong_dan)
        con_tro = ket_noi.cursor()
        con_tro.execute('DELETE FROM bang_mat_hang WHERE ma_so = ?', (ma_so,))
        ket_noi.commit()
        return con_tro.rowcount > 0
    except sqlite3.Error as loi:
        print(f'[LOI DATABASE] Loi khi xoa: {str(loi)}')
        raise
    finally:
        if ket_noi:
            ket_noi.close()


# ==================== QUẢN LÝ NGƯỜI DÙNG ====================

def tao_nguoi_dung(ten_dang_nhap, mat_khau_hash, ho_ten, vai_tro='nhan_vien'):
    """Tạo tài khoản người dùng mới."""
    ket_noi = None
    try:
        tao_bang_neu_chua_co()
        duong_dan = lay_duong_dan_db()
        ket_noi = sqlite3.connect(duong_dan)
        con_tro = ket_noi.cursor()
        con_tro.execute('''
            INSERT INTO bang_nguoi_dung (ten_dang_nhap, mat_khau_hash, ho_ten, vai_tro)
            VALUES (?, ?, ?, ?)
        ''', (ten_dang_nhap, mat_khau_hash, ho_ten, vai_tro))
        ket_noi.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    except sqlite3.Error as loi:
        print(f'[LOI DATABASE] Loi khi tao nguoi dung: {str(loi)}')
        raise
    finally:
        if ket_noi:
            ket_noi.close()


def xac_thuc_nguoi_dung(ten_dang_nhap):
    """Lấy thông tin người dùng để xác thực."""
    ket_noi = None
    try:
        tao_bang_neu_chua_co()
        duong_dan = lay_duong_dan_db()
        ket_noi = sqlite3.connect(duong_dan)
        con_tro = ket_noi.cursor()
        con_tro.execute('SELECT * FROM bang_nguoi_dung WHERE ten_dang_nhap = ?', (ten_dang_nhap,))
        ket_qua = con_tro.fetchone()
        if ket_qua:
            return {
                'ten_dang_nhap': ket_qua[0],
                'mat_khau_hash': ket_qua[1],
                'ho_ten': ket_qua[2],
                'vai_tro': ket_qua[3]
            }
        return None
    except sqlite3.Error as loi:
        print(f'[LOI DATABASE] Loi khi xac thuc: {str(loi)}')
        raise
    finally:
        if ket_noi:
            ket_noi.close()


def co_nguoi_dung_nao_chua():
    """Kiểm tra xem đã có tài khoản nào trong hệ thống chưa."""
    ket_noi = None
    try:
        tao_bang_neu_chua_co()
        duong_dan = lay_duong_dan_db()
        ket_noi = sqlite3.connect(duong_dan)
        con_tro = ket_noi.cursor()
        con_tro.execute('SELECT COUNT(*) FROM bang_nguoi_dung')
        so_luong = con_tro.fetchone()[0]
        return so_luong > 0
    except sqlite3.Error as loi:
        print(f'[LOI DATABASE] Loi khi kiem tra nguoi dung: {str(loi)}')
        return False
    finally:
        if ket_noi:
            ket_noi.close()


def xuat_du_lieu_csv():
    """Xuất toàn bộ dữ liệu ra định dạng CSV string."""
    ket_noi = None
    try:
        duong_dan = lay_duong_dan_db()
        ket_noi = sqlite3.connect(duong_dan)
        con_tro = ket_noi.cursor()
        con_tro.execute('SELECT * FROM bang_mat_hang')
        cac_hang = con_tro.fetchall()
        ten_cot = [mo_ta[0] for mo_ta in con_tro.description]
        # Tạo nội dung CSV
        dong_csv = []
        dong_csv.append(','.join(ten_cot))
        for hang in cac_hang:
            cac_gia_tri = []
            for gia_tri in hang:
                if gia_tri is None:
                    cac_gia_tri.append('')
                else:
                    # Escape dấu phẩy và ngoặc kép trong giá trị
                    s = str(gia_tri)
                    if ',' in s or '"' in s or '\n' in s:
                        s = '"' + s.replace('"', '""') + '"'
                    cac_gia_tri.append(s)
            dong_csv.append(','.join(cac_gia_tri))
        return '\n'.join(dong_csv)
    except sqlite3.Error as loi:
        print(f'[LOI DATABASE] Loi khi xuat CSV: {str(loi)}')
        raise
    finally:
        if ket_noi:
            ket_noi.close()