"""
Tệp nguoi_dung.py — Quản lý người dùng + phân quyền (Admin / Nhân viên).
========================================================================

Hỗ trợ 2 vai trò:
    - 'admin'     : Quản trị viên — có toàn quyền (xem + thêm + sửa + xóa + giỏ hàng).
    - 'nhan_vien' : Nhân viên    — bị hạn chế (KHÔNG được xóa sản phẩm).

Lớp NguoiDung đóng gói thông tin đăng nhập + hàm la_admin() để kiểm tra
quyền nhanh chóng từ view hoặc template.
"""


# ============================================================
# LỚP NGƯỜI DÙNG
# ============================================================

class NguoiDung:
    """
    Lớp NguoiDung — đại diện cho một tài khoản đăng nhập hệ thống.

    Thuộc tính:
        ten_dang_nhap (str): Tên đăng nhập (duy nhất, PRIMARY KEY trong DB).
        mat_khau      (str): Mật khẩu. Ở đây dùng plaintext cho đơn giản —
                             trong thực tế PHẢI băm bằng hashlib/bcrypt.
        ho_ten        (str): Họ tên đầy đủ để hiển thị trên UI.
        vai_tro       (str): 'admin' hoặc 'nhan_vien'.
    """

    def __init__(self, ten_dang_nhap, mat_khau, ho_ten, vai_tro='nhan_vien'):
        # Mặc định vai_tro = 'nhan_vien' nếu không truyền vào.
        self.ten_dang_nhap = ten_dang_nhap
        self.mat_khau = mat_khau
        self.ho_ten = ho_ten
        self.vai_tro = vai_tro

    def la_admin(self):
        """
        Kiểm tra người dùng có phải là admin không.
        Trả về True nếu vai_tro == 'admin', ngược lại False.
        """
        return self.vai_tro == 'admin'

    def chuyen_thanh_dict(self):
        """
        Chuyển đối tượng thành dict để trả về JSON.
        LƯU Ý: KHÔNG trả mật khẩu ra ngoài — tránh lộ thông tin nhạy cảm.
        """
        return {
            'ten_dang_nhap': self.ten_dang_nhap,
            'ho_ten':        self.ho_ten,
            'vai_tro':       self.vai_tro,
            'la_admin':      self.la_admin()       # Tiện cho frontend kiểm tra nhanh.
        }


# ============================================================
# DANH SÁCH NGƯỜI DÙNG MẪU (Tạo sẵn khi khởi động lần đầu)
# ============================================================

# 2 tài khoản mẫu — được nạp vào SQLite khi hệ thống chạy lần đầu.
DANH_SACH_NGUOI_DUNG_MAC_DINH = [
    NguoiDung('admin',    '123', 'Quản trị viên hệ thống', 'admin'),
    NguoiDung('nhanvien', '123', 'Nhân viên bán hàng',     'nhan_vien'),
]


def khoi_tao_nguoi_dung_mac_dinh():
    """
    Tạo 2 tài khoản mẫu vào SQLite nếu bảng người dùng còn trống.
    - admin/123    : toàn quyền (xem + thêm + sửa + xóa).
    - nhanvien/123 : hạn chế (không được xóa).

    Áp dụng try-except để không làm sập chương trình khi DB lỗi.
    """
    try:
        # Import lười (lazy import) để tránh phụ thuộc vòng.
        from .ket_noi_sqlite import co_nguoi_dung_nao_chua, tao_nguoi_dung
        # Nếu DB chưa có ai → chèn 2 tài khoản mẫu.
        if not co_nguoi_dung_nao_chua():
            for nguoi in DANH_SACH_NGUOI_DUNG_MAC_DINH:
                tao_nguoi_dung(
                    ten_dang_nhap=nguoi.ten_dang_nhap,
                    mat_khau_hash=nguoi.mat_khau,    # plaintext làm "hash" cho đơn giản.
                    ho_ten=nguoi.ho_ten,
                    vai_tro=nguoi.vai_tro
                )
            print('[KHOI TAO] Da tao 2 tai khoan mac dinh: admin/123 va nhanvien/123')
    except Exception as loi:
        # Bắt lỗi để in ra console nhưng KHÔNG làm sập server.
        print(f'[LOI] Khong the khoi tao nguoi dung mac dinh: {str(loi)}')


def kiem_tra_dang_nhap(ten_dang_nhap, mat_khau):
    """
    Kiểm tra thông tin đăng nhập.

    Tham số:
        ten_dang_nhap : Tên đăng nhập người dùng nhập.
        mat_khau      : Mật khẩu người dùng nhập.

    Trả về:
        NguoiDung nếu đăng nhập đúng.
        None      nếu sai tên đăng nhập hoặc mật khẩu.

    Áp dụng try-except để bắt lỗi DB.
    """
    try:
        from .ket_noi_sqlite import xac_thuc_nguoi_dung
        thong_tin = xac_thuc_nguoi_dung(ten_dang_nhap)
        if thong_tin is None:
            return None                                  # Sai tên đăng nhập.
        if thong_tin['mat_khau_hash'] != mat_khau:
            return None                                  # Sai mật khẩu.
        # Tất cả đúng → trả về đối tượng NguoiDung.
        return NguoiDung(
            ten_dang_nhap=thong_tin['ten_dang_nhap'],
            mat_khau=thong_tin['mat_khau_hash'],
            ho_ten=thong_tin['ho_ten'],
            vai_tro=thong_tin['vai_tro']
        )
    except Exception as loi:
        print(f'[LOI] Loi khi kiem tra dang nhap: {str(loi)}')
        return None
