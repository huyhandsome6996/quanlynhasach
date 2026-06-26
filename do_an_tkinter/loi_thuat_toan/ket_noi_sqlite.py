"""
Tệp ket_noi_sqlite.py — KẾT NỐI CƠ SỞ DỮ LIỆU SQLite.
=====================================================

Lưu trữ dữ liệu bền vững: khi tắt server và bật lại, dữ liệu vẫn còn.

Có 2 bảng chính:
    bang_mat_hang   : Lưu 5 loại mặt hàng (Sách/Tạp chí/Báo giấy/Luận văn/Bản thảo).
    bang_nguoi_dung : Lưu tài khoản đăng nhập + phân quyền.

Tất cả hàm đều bọc try-except-finally để:
    - Bắt lỗi sqlite3.Error không làm sập server.
    - Đảm bảo đóng kết nối (finally) để không rò rỉ tài nguyên.
"""

# sqlite3: thư viện chuẩn của Python để làm việc với SQLite.
import sqlite3

# os: dùng để thao tác đường dẫn file độc lập hệ điều hành.
import os


def lay_duong_dan_db():
    """
    Trả về đường dẫn TUYỆT ĐỐI tới file database SQLite.

    Cách tính:
        __file__                             = .../loi_thuat_toan/ket_noi_sqlite.py
        dirname(abspath(__file__))           = .../loi_thuat_toan/
        dirname(dirname(...))                = .../ung_dung_giao_tiep/
        dirname(dirname(dirname(...)))       = .../du_an_cua_hang_sach/   ← BASE_DIR
    → file DB nằm ở: .../du_an_cua_hang_sach/db.sqlite3
    """
    thu_muc_hien_tai = os.path.dirname(os.path.abspath(__file__))
    duong_dan_du_an = os.path.dirname(os.path.dirname(thu_muc_hien_tai))
    return os.path.join(duong_dan_du_an, 'db.sqlite3')


def tao_bang_neu_chua_co():
    """
    Tạo 2 bảng bang_mat_hang + bang_nguoi_dung nếu chưa tồn tại.
    Dùng "CREATE TABLE IF NOT EXISTS" để không lỗi nếu bảng đã có sẵn.

    Áp dụng try-except-finally.
    """
    ket_noi = None                                   # Khởi tạo trước để finally có thể truy cập.
    try:
        duong_dan = lay_duong_dan_db()
        ket_noi = sqlite3.connect(duong_dan)         # Mở kết nối tới file DB.
        con_tro = ket_noi.cursor()                   # Tạo con trỏ để thực thi SQL.

        # Bảng mặt hàng — chứa tất cả 5 loại với các trường dùng chung + trường riêng.
        # Các trường riêng (tac_gia, so_phat_hanh, ...) có thể NULL vì không phải
        # loại hàng nào cũng có (VD: Báo giấy không có tác giả).
        con_tro.execute('''
            CREATE TABLE IF NOT EXISTS bang_mat_hang (
                ma_so         TEXT PRIMARY KEY,      -- Khóa chính, duy nhất.
                loai_hang     TEXT NOT NULL,          -- 'Sách' | 'Tạp chí' | ...
                ten_san_pham  TEXT NOT NULL,          -- Tên sản phẩm.
                gia_co_ban    REAL NOT NULL,          -- Giá nhập (số thực).
                ton_kho       INTEGER NOT NULL,       -- Số lượng tồn (số nguyên).
                tac_gia       TEXT,                   -- Riêng cho Sách/Luận văn/Bản thảo.
                nha_xuat_ban  TEXT,                   -- Riêng cho Sách.
                so_phat_hanh  TEXT,                   -- Riêng cho Tạp chí.
                ngay_xuat_ban TEXT,                   -- Riêng cho Báo giấy.
                truong_dai_hoc TEXT,                  -- Riêng cho Luận văn.
                nam_bao_ve    TEXT,                   -- Riêng cho Luận văn.
                tinh_trang    TEXT                    -- Riêng cho Bản thảo.
            )
        ''')

        # Bảng người dùng — lưu tài khoản đăng nhập + vai trò phân quyền.
        con_tro.execute('''
            CREATE TABLE IF NOT EXISTS bang_nguoi_dung (
                ten_dang_nhap  TEXT PRIMARY KEY,      -- Khóa chính.
                mat_khau_hash  TEXT NOT NULL,         -- Mật khẩu (đã băm hoặc plaintext).
                ho_ten         TEXT NOT NULL,         -- Tên hiển thị.
                vai_tro        TEXT NOT NULL DEFAULT 'nhan_vien'   -- Mặc định là nhân viên.
            )
        ''')

        ket_noi.commit()                             # Lưu thay đổi xuống file.
    except sqlite3.Error as loi:
        print(f'[LOI DATABASE] Loi khi tao bang: {str(loi)}')
        raise                                        # Ném lỗi lên để view xử lý.
    finally:
        # Dù thành công hay lỗi, đều phải đóng kết nối để giải phóng tài nguyên.
        if ket_noi:
            ket_noi.close()


def tai_du_lieu(danh_sach_lien_ket):
    """
    Nạp toàn bộ dữ liệu từ bảng bang_mat_hang vào DoublyLinkedList
    để dùng trong bộ nhớ (in-memory) — giúp thao tác CRUD nhanh hơn.

    Tham số:
        danh_sach_lien_ket : Đối tượng DoublyLinkedList đã khởi tạo.
    """
    # Lazy import để tránh phụ thuộc vòng.
    from loi_thuat_toan.lop_doi_tuong import Sach, TapChi, BaoGiay, LuanVan, BanThao
    tao_bang_neu_chua_co()                           # Đảm bảo bảng đã tồn tại.
    ket_noi = None
    try:
        duong_dan = lay_duong_dan_db()
        ket_noi = sqlite3.connect(duong_dan)
        con_tro = ket_noi.cursor()
        # Lấy tất cả hàng từ bảng.
        con_tro.execute('SELECT * FROM bang_mat_hang')
        cac_hang = con_tro.fetchall()                # Trả về list các tuple.

        # Lấy tên cột từ con_tro.description để truy cập theo tên (dễ đọc hơn index).
        ten_cot = [mo_ta[0] for mo_ta in con_tro.description]

        # Duyệt từng hàng → tạo đối tượng OOP tương ứng → thêm vào DSLK.
        for hang in cac_hang:
            du_lieu = dict(zip(ten_cot, hang))       # Ép tuple → dict {cot: gia_tri}.
            ma_so = du_lieu['ma_so']
            loai_hang = du_lieu['loai_hang']
            ten_san_pham = du_lieu['ten_san_pham']
            gia_co_ban = du_lieu['gia_co_ban']
            ton_kho = du_lieu['ton_kho']

            # Tùy loại hàng → khởi tạo đối tượng lớp con tương ứng.
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
                continue                              # Loại lạ → bỏ qua.

            danh_sach_lien_ket.them_vao_cuoi(san_pham)

    except sqlite3.Error as loi:
        print(f'[LOI DATABASE] Loi khi tai du lieu: {str(loi)}')
        raise
    finally:
        if ket_noi:
            ket_noi.close()


def luu_mot_san_pham(san_pham):
    """
    Lưu một sản phẩm mới vào bảng bang_mat_hang.

    Sử dụng PARAMETERIZED QUERY (dấu ? thay vì nối chuỗi) để CHỐNG SQL INJECTION.
    """
    ket_noi = None
    try:
        duong_dan = lay_duong_dan_db()
        ket_noi = sqlite3.connect(duong_dan)
        con_tro = ket_noi.cursor()
        # Câu SQL có 12 dấu ? tương ứng 12 giá trị — SQLite tự thay thế an toàn.
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
            # getattr(obj, attr, default) — trả về default nếu đối tượng không có thuộc tính.
            # Cần vì không phải lớp con nào cũng có tất cả các trường riêng.
            getattr(san_pham, 'tac_gia', None),
            getattr(san_pham, 'nha_xuat_ban', None),
            getattr(san_pham, 'so_phat_hanh', None),
            getattr(san_pham, 'ngay_xuat_ban', None),
            getattr(san_pham, 'truong_dai_hoc', None),
            getattr(san_pham, 'nam_bao_ve', None),
            getattr(san_pham, 'tinh_trang', None)
        ))
        ket_noi.commit()                             # Lưu xuống file.
    except sqlite3.IntegrityError as loi:
        # IntegrityError thường do trùng khóa chính (ma_so đã tồn tại).
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
    Cập nhật thông tin sản phẩm trong SQLite theo ma_so.

    Trả về: True nếu tìm thấy và cập nhật, False nếu không tìm thấy.
    """
    ket_noi = None
    try:
        duong_dan = lay_duong_dan_db()
        ket_noi = sqlite3.connect(duong_dan)
        con_tro = ket_noi.cursor()
        # Dùng UPDATE ... SET ... WHERE ma_so = ?
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
            san_pham.ma_so                            # Điều kiện WHERE.
        ))
        ket_noi.commit()
        # rowcount = số hàng bị ảnh hưởng (1 = cập nhật thành công, 0 = không thấy).
        return con_tro.rowcount > 0
    except sqlite3.Error as loi:
        print(f'[LOI DATABASE] Loi khi cap nhat: {str(loi)}')
        raise
    finally:
        if ket_noi:
            ket_noi.close()


def xoa_mot_san_pham(ma_so):
    """
    Xóa một sản phẩm khỏi SQLite theo ma_so.
    Trả về True nếu xóa được, False nếu không tìm thấy.
    """
    ket_noi = None
    try:
        duong_dan = lay_duong_dan_db()
        ket_noi = sqlite3.connect(duong_dan)
        con_tro = ket_noi.cursor()
        # Cần truyền tuple (ma_so,) — dấu phẩy để Python hiểu là tuple 1 phần tử.
        con_tro.execute('DELETE FROM bang_mat_hang WHERE ma_so = ?', (ma_so,))
        ket_noi.commit()
        return con_tro.rowcount > 0
    except sqlite3.Error as loi:
        print(f'[LOI DATABASE] Loi khi xoa: {str(loi)}')
        raise
    finally:
        if ket_noi:
            ket_noi.close()


# ============================================================
# QUẢN LÝ NGƯỜI DÙNG (CRUD tài khoản)
# ============================================================

def tao_nguoi_dung(ten_dang_nhap, mat_khau_hash, ho_ten, vai_tro='nhan_vien'):
    """
    Tạo tài khoản người dùng mới.
    Trả về True nếu thành công, False nếu tên đăng nhập đã tồn tại.
    """
    ket_noi = None
    try:
        tao_bang_neu_chua_co()                       # Đảm bảo bảng đã có.
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
        # Trùng khóa chính → tên đăng nhập đã có.
        return False
    except sqlite3.Error as loi:
        print(f'[LOI DATABASE] Loi khi tao nguoi dung: {str(loi)}')
        raise
    finally:
        if ket_noi:
            ket_noi.close()


def xac_thuc_nguoi_dung(ten_dang_nhap):
    """
    Lấy thông tin người dùng theo ten_dang_nhap để kiểm tra đăng nhập.
    Trả về dict thông tin hoặc None nếu tên đăng nhập không tồn tại.
    """
    ket_noi = None
    try:
        tao_bang_neu_chua_co()
        duong_dan = lay_duong_dan_db()
        ket_noi = sqlite3.connect(duong_dan)
        con_tro = ket_noi.cursor()
        con_tro.execute('SELECT * FROM bang_nguoi_dung WHERE ten_dang_nhap = ?', (ten_dang_nhap,))
        ket_qua = con_tro.fetchone()                 # Lấy 1 hàng đầu tiên (hoặc None).
        if ket_qua:
            # Ép tuple → dict để dễ truy cập theo tên.
            return {
                'ten_dang_nhap': ket_qua[0],
                'mat_khau_hash': ket_qua[1],
                'ho_ten':        ket_qua[2],
                'vai_tro':       ket_qua[3]
            }
        return None
    except sqlite3.Error as loi:
        print(f'[LOI DATABASE] Loi khi xac thuc: {str(loi)}')
        raise
    finally:
        if ket_noi:
            ket_noi.close()


def co_nguoi_dung_nao_chua():
    """
    Kiểm tra bảng bang_nguoi_dung có tài khoản nào chưa.
    Dùng để quyết định có cần tạo 2 tài khoản mẫu (admin/nhanvien) hay không.
    """
    ket_noi = None
    try:
        tao_bang_neu_chua_co()
        duong_dan = lay_duong_dan_db()
        ket_noi = sqlite3.connect(duong_dan)
        con_tro = ket_noi.cursor()
        con_tro.execute('SELECT COUNT(*) FROM bang_nguoi_dung')
        so_luong = con_tro.fetchone()[0]             # [0] để lấy giá trị COUNT.
        return so_luong > 0
    except sqlite3.Error as loi:
        print(f'[LOI DATABASE] Loi khi kiem tra nguoi dung: {str(loi)}')
        return False
    finally:
        if ket_noi:
            ket_noi.close()


def tao_du_lieu_mau_neu_rong():
    """
    Nếu bảng bang_mat_hang còn trống → thêm 5 sản phẩm mẫu (mỗi loại 1 cái).

    Mục đích: khi người dùng clone dự án về chạy lần đầu tiên, có ngay dữ liệu
    để test mà không phải tự thêm từng sản phẩm.
    """
    ket_noi = None
    try:
        tao_bang_neu_chua_co()
        duong_dan = lay_duong_dan_db()
        ket_noi = sqlite3.connect(duong_dan)
        con_tro = ket_noi.cursor()
        con_tro.execute('SELECT COUNT(*) FROM bang_mat_hang')
        so_luong = con_tro.fetchone()[0]
        if so_luong > 0:
            return                                   # Đã có dữ liệu → không thêm nữa.

        # 5 sản phẩm mẫu (mã, loại, tên, giá, tồn, tac_gia, nha_xuat_ban,
        #                so_phat_hanh, ngay_xuat_ban, truong_dai_hoc, nam_bao_ve, tinh_trang)
        san_pham_mau = [
            ('MH001', 'Sách',      'Truyện Kiều',           50000, 20, 'Nguyễn Du',  'NXB Văn học',  None, None,         None,           None,   None),
            ('MH002', 'Tạp chí',   'Tạp chí Khoa học 06/25', 30000, 15, None,         None,           'Số 120', None,        None,           None,   None),
            ('MH003', 'Báo giấy',  'Báo Tuổi Trẻ 25/06',      5000, 50, None,         None,           None,    '2025-06-25', None,           None,   None),
            ('MH004', 'Luận văn',  'Luận văn Tốt nghiệp',  120000,  3, 'Trần Thị B', None,           None,    None,        'ĐH Bách Khoa', '2024', None),
            ('MH005', 'Bản thảo',  'Bản thảo Tiểu thuyết', 200000,  1, 'Lê Văn C',   None,           None,    None,        None,           None,   'Chưa duyệt'),
        ]
        for sp in san_pham_mau:
            con_tro.execute('''
                INSERT INTO bang_mat_hang (ma_so, loai_hang, ten_san_pham, gia_co_ban, ton_kho,
                                            tac_gia, nha_xuat_ban, so_phat_hanh, ngay_xuat_ban,
                                            truong_dai_hoc, nam_bao_ve, tinh_trang)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', sp)
        ket_noi.commit()
        print('[KHOI TAO] Da them 5 san pham mau vao database.')
    except sqlite3.Error as loi:
        print(f'[LOI DATABASE] Loi khi tao du lieu mau: {str(loi)}')
    finally:
        if ket_noi:
            ket_noi.close()


def xuat_du_lieu_csv():
    """
    Xuất toàn bộ dữ liệu bảng bang_mat_hang ra chuỗi CSV (Comma-Separated Values).
    Dùng khi cần backup hoặc mở bằng Excel.
    """
    ket_noi = None
    try:
        duong_dan = lay_duong_dan_db()
        ket_noi = sqlite3.connect(duong_dan)
        con_tro = ket_noi.cursor()
        con_tro.execute('SELECT * FROM bang_mat_hang')
        cac_hang = con_tro.fetchall()
        ten_cot = [mo_ta[0] for mo_ta in con_tro.description]

        # Tạo nội dung CSV: dòng đầu là tên cột, các dòng sau là dữ liệu.
        dong_csv = []
        dong_csv.append(','.join(ten_cot))           # Dòng tiêu đề.
        for hang in cac_hang:
            cac_gia_tri = []
            for gia_tri in hang:
                if gia_tri is None:
                    cac_gia_tri.append('')           # NULL → chuỗi rỗng.
                else:
                    s = str(gia_tri)
                    # Nếu giá trị chứa dấu phẩy / ngoặc kép / xuống dòng → bọc trong "".
                    if ',' in s or '"' in s or '\n' in s:
                        s = '"' + s.replace('"', '""') + '"'   # Escape "" thành "".
                    cac_gia_tri.append(s)
            dong_csv.append(','.join(cac_gia_tri))
        return '\n'.join(dong_csv)                   # Nối các dòng bằng xuống dòng.
    except sqlite3.Error as loi:
        print(f'[LOI DATABASE] Loi khi xuat CSV: {str(loi)}')
        raise
    finally:
        if ket_noi:
            ket_noi.close()
