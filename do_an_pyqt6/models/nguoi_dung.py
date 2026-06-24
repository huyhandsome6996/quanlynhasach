# ====================================================================
# NGƯỜI DÙNG & PHÂN QUYỀN (Admin / Nhân viên)
# --------------------------------------------------------------------
# Mỗi người dùng có: tên đăng nhập, mật khẩu, vai trò (quyen).
# - "admin":  QUYỀN ĐẦY ĐỦ (xem + thêm + sửa + xóa + thống kê + giỏ hàng)
# - "nhan_vien": KHÔNG ĐƯỢC XÓA (chỉ xem + thêm + sửa + thống kê + giỏ hàng)
# ====================================================================


class NguoiDung:
    """Lớp mô tả một tài khoản người dùng."""

    def __init__(self, ten_dang_nhap, mat_khau, quyen):
        self.ten_dang_nhap = ten_dang_nhap   # Tên đăng nhập (vd: "admin")
        self.mat_khau = mat_khau             # Mật khẩu
        # quyen chỉ có 2 giá trị: "admin" hoặc "nhan_vien"
        self.quyen = quyen

    def la_admin(self):
        """Trả về True nếu đây là tài khoản Admin."""
        return self.quyen == "admin"

    def la_nhan_vien(self):
        """Trả về True nếu đây là tài khoản Nhân viên."""
        return self.quyen == "nhan_vien"


# ====================================================================
# DANH SÁCH TÀI KHOẢN MẶC ĐỊNH
# --------------------------------------------------------------------
# Trong thực tế tài khoản sẽ lưu trong CSDL, nhưng để đơn giản
# (đến thằng ngu cũng hiểu) thì mình lưu sẵn 2 tài khoản mẫu:
#    - admin / 123     : toàn quyền
#    - nhanvien / 123  : không được xóa
# ====================================================================
DANH_SACH_TAI_KHOAN = [
    NguoiDung("admin",    "123", "admin"),
    NguoiDung("nhanvien", "123", "nhan_vien"),
]


def kiem_tra_dang_nhap(ten_dang_nhap, mat_khau):
    """
    Kiểm tra xem cặp (tên đăng nhập + mật khẩu) có đúng không.
    - Nếu đúng: trả về đối tượng NguoiDung.
    - Nếu sai : trả về None.
    """
    for nguoi in DANH_SACH_TAI_KHOAN:
        if (nguoi.ten_dang_nhap == ten_dang_nhap
                and nguoi.mat_khau == mat_khau):
            return nguoi
    return None
