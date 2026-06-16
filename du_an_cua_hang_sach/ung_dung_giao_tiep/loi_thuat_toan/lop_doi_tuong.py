"""
Tệp chứa các lớp đối tượng (OOP) cho hệ thống quản lý cửa hàng sách.

Cấu trúc kế thừa:
    MatHang (Lớp cha trừu tượng)
      ├── Sach (Sách)
      ├── TapChi (Tạp chí)
      ├── BaoGiay (Báo giấy)
      ├── LuanVan (Luận văn)
      └── BanThao (Bản thảo)

Tính đa hình: Mỗi lớp con ghi đè phương thức tinh_gia_ban()
với công thức tính thuế khác nhau.

Quy ước: Tên biến, tên hàm, chú thích sử dụng tiếng Việt.
Ngoại lệ: Các từ khóa cốt lõi (ABC, abstractmethod, super, v.v.).
"""

from abc import ABC, abstractmethod


# ============================================================
# LỚP CHA TRỪU TƯỢNG
# ============================================================

class MatHang(ABC):
    """
    Lớp cha trừu tượng MatHang (Mặt hàng).

    Đại diện cho một mặt hàng bất kỳ trong cửa hàng sách.
    Chứa các thuộc tính chung cho TẤT CẢ các loại mặt hàng.
    Các lớp con BẮT BUỘC phải ghi đè phương thức tinh_gia_ban().

    Thuộc tính chung:
        ma_so (str):       Mã định danh duy nhất (VD: "MH001").
        loai_hang (str):   Loại mặt hàng (VD: "Sách", "Tạp chí").
        ten_san_pham (str): Tên sản phẩm (VD: "Lập trình Python").
        gia_co_ban (float): Giá cơ bản, phải >= 0.
        ton_kho (int):     Số lượng tồn kho, phải >= 0.
    """

    def __init__(self, ma_so, ten_san_pham, gia_co_ban, ton_kho):
        """
        Khởi tạo một mặt hàng mới.

        Tham số:
            ma_so (str):       Mã định danh duy nhất.
            ten_san_pham (str): Tên sản phẩm.
            gia_co_ban (float): Giá cơ bản (phải >= 0).
            ton_kho (int):     Số lượng tồn kho (phải >= 0).

        Ngoại lệ:
            ValueError: Nếu giá cơ bản hoặc tồn kho bị âm.
        """
        self.ma_so = ma_so
        self.loai_hang = ""  # Sẽ được ghi đè bởi từng lớp con
        self.ten_san_pham = ten_san_pham

        # ---- Kiểm tra giá cơ bản không được âm ----
        if gia_co_ban < 0:
            raise ValueError("Giá cơ bản không được âm.")
        self.gia_co_ban = gia_co_ban

        # ---- Kiểm tra tồn kho không được âm ----
        if ton_kho < 0:
            raise ValueError("Số lượng tồn kho không được âm.")
        self.ton_kho = ton_kho

    @abstractmethod
    def tinh_gia_ban(self):
        """
        Phương thức trừu tượng - Tính giá bán sau thuế.

        Mỗi lớp con phải ghi đè phương thức này với công thức riêng.
        Đây chính là tính ĐA HÌNH (Polymorphism) trong OOP.

        Trả về:
            float: Giá bán sau khi áp dụng thuế.
        """
        pass

    def chuyen_thanh_dict(self):
        """
        Chuyển đối tượng thành từ điển (dict) để gửi JSON về trình duyệt.

        Trả về:
            dict: Từ điển chứa thông tin cơ bản của mặt hàng.
        """
        return {
            'ma_so': self.ma_so,
            'loai_hang': self.loai_hang,
            'ten_san_pham': self.ten_san_pham,
            'gia_co_ban': self.gia_co_ban,
            'ton_kho': self.ton_kho,
            'gia_ban': self.tinh_gia_ban()  # Gọi phương thức đa hình
        }

    def __str__(self):
        """
        Trả về chuỗi mô tả mặt hàng (dùng khi in ra màn hình).

        Trả về:
            str: Chuỗi mô tả ngắn gọn.
        """
        return f"[{self.ma_so}] {self.loai_hang} - {self.ten_san_pham} | Giá bán: {self.tinh_gia_ban():.0f}đ | Tồn kho: {self.ton_kho}"


# ============================================================
# CÁC LỚP CON - KẾ THỪA TỪ MatHang
# ============================================================

class Sach(MatHang):
    """
    Lớp Sach (Sách) - Kế thừa từ MatHang.

    Thuộc tính riêng:
        tac_gia (str):       Tên tác giả.
        nha_xuat_ban (str):  Tên nhà xuất bản.

    Công thức tính giá bán: gia_co_ban × 1.10 (Cộng 10% thuế).
    """

    def __init__(self, ma_so, ten_san_pham, gia_co_ban, ton_kho, tac_gia, nha_xuat_ban):
        """
        Khởi tạo một cuốn sách mới.

        Tham số:
            ma_so (str):       Mã định danh duy nhất.
            ten_san_pham (str): Tên sách.
            gia_co_ban (float): Giá cơ bản (phải >= 0).
            ton_kho (int):     Số lượng tồn kho (phải >= 0).
            tac_gia (str):     Tên tác giả.
            nha_xuat_ban (str): Tên nhà xuất bản.
        """
        # Gọi hàm khởi tạo của lớp cha
        super().__init__(ma_so, ten_san_pham, gia_co_ban, ton_kho)
        self.loai_hang = "Sách"
        self.tac_gia = tac_gia
        self.nha_xuat_ban = nha_xuat_ban

    def tinh_gia_ban(self):
        """
        Tính giá bán của sách.
        Công thức: gia_co_ban × 1.10 (Cộng 10% thuế).

        Trả về:
            float: Giá bán sau thuế.
        """
        return self.gia_co_ban * 1.10

    def chuyen_thanh_dict(self):
        """
        Chuyển đối tượng sách thành từ điển, bao gồm thuộc tính riêng.

        Trả về:
            dict: Từ điển chứa toàn bộ thông tin sách.
        """
        dict_co_ban = super().chuyen_thanh_dict()
        dict_co_ban['tac_gia'] = self.tac_gia
        dict_co_ban['nha_xuat_ban'] = self.nha_xuat_ban
        return dict_co_ban


class TapChi(MatHang):
    """
    Lớp TapChi (Tạp chí) - Kế thừa từ MatHang.

    Thuộc tính riêng:
        so_phat_hanh (str): Số phát hành (VD: "Số 123").

    Công thức tính giá bán: gia_co_ban × 1.05 (Cộng 5% thuế).
    """

    def __init__(self, ma_so, ten_san_pham, gia_co_ban, ton_kho, so_phat_hanh):
        """
        Khởi tạo một cuốn tạp chí mới.

        Tham số:
            ma_so (str):       Mã định danh duy nhất.
            ten_san_pham (str): Tên tạp chí.
            gia_co_ban (float): Giá cơ bản (phải >= 0).
            ton_kho (int):     Số lượng tồn kho (phải >= 0).
            so_phat_hanh (str): Số phát hành.
        """
        super().__init__(ma_so, ten_san_pham, gia_co_ban, ton_kho)
        self.loai_hang = "Tạp chí"
        self.so_phat_hanh = so_phat_hanh

    def tinh_gia_ban(self):
        """
        Tính giá bán của tạp chí.
        Công thức: gia_co_ban × 1.05 (Cộng 5% thuế).

        Trả về:
            float: Giá bán sau thuế.
        """
        return self.gia_co_ban * 1.05

    def chuyen_thanh_dict(self):
        """
        Chuyển đối tượng tạp chí thành từ điển, bao gồm thuộc tính riêng.

        Trả về:
            dict: Từ điển chứa toàn bộ thông tin tạp chí.
        """
        dict_co_ban = super().chuyen_thanh_dict()
        dict_co_ban['so_phat_hanh'] = self.so_phat_hanh
        return dict_co_ban


class BaoGiay(MatHang):
    """
    Lớp BaoGiay (Báo giấy) - Kế thừa từ MatHang.

    Thuộc tính riêng:
        ngay_xuat_ban (str): Ngày xuất bản (VD: "15/06/2025").

    Công thức tính giá bán: gia_co_ban (Không cộng thuế).
    """

    def __init__(self, ma_so, ten_san_pham, gia_co_ban, ton_kho, ngay_xuat_ban):
        """
        Khởi tạo một tờ báo giấy mới.

        Tham số:
            ma_so (str):       Mã định danh duy nhất.
            ten_san_pham (str): Tên báo.
            gia_co_ban (float): Giá cơ bản (phải >= 0).
            ton_kho (int):     Số lượng tồn kho (phải >= 0).
            ngay_xuat_ban (str): Ngày xuất bản (định dạng dd/mm/yyyy).
        """
        super().__init__(ma_so, ten_san_pham, gia_co_ban, ton_kho)
        self.loai_hang = "Báo giấy"
        self.ngay_xuat_ban = ngay_xuat_ban

    def tinh_gia_ban(self):
        """
        Tính giá bán của báo giấy.
        Công thức: gia_co_ban (Không cộng thuế).

        Trả về:
            float: Giá bán bằng đúng giá cơ bản.
        """
        return self.gia_co_ban

    def chuyen_thanh_dict(self):
        """
        Chuyển đối tượng báo giấy thành từ điển, bao gồm thuộc tính riêng.

        Trả về:
            dict: Từ điển chứa toàn bộ thông tin báo giấy.
        """
        dict_co_ban = super().chuyen_thanh_dict()
        dict_co_ban['ngay_xuat_ban'] = self.ngay_xuat_ban
        return dict_co_ban


class LuanVan(MatHang):
    """
    Lớp LuanVan (Luận văn) - Kế thừa từ MatHang.

    Thuộc tính riêng:
        tac_gia (str):      Tên tác giả (sinh viên/nghiên cứu sinh).
        truong_dai_hoc (str): Tên trường đại học.

    Công thức tính giá bán: gia_co_ban × 1.15 (Cộng 15% thuế).
    """

    def __init__(self, ma_so, ten_san_pham, gia_co_ban, ton_kho, tac_gia, truong_dai_hoc):
        """
        Khởi tạo một luận văn mới.

        Tham số:
            ma_so (str):       Mã định danh duy nhất.
            ten_san_pham (str): Tên luận văn.
            gia_co_ban (float): Giá cơ bản (phải >= 0).
            ton_kho (int):     Số lượng tồn kho (phải >= 0).
            tac_gia (str):     Tên tác giả.
            truong_dai_hoc (str): Tên trường đại học.
        """
        super().__init__(ma_so, ten_san_pham, gia_co_ban, ton_kho)
        self.loai_hang = "Luận văn"
        self.tac_gia = tac_gia
        self.truong_dai_hoc = truong_dai_hoc

    def tinh_gia_ban(self):
        """
        Tính giá bán của luận văn.
        Công thức: gia_co_ban × 1.15 (Cộng 15% thuế).

        Trả về:
            float: Giá bán sau thuế.
        """
        return self.gia_co_ban * 1.15

    def chuyen_thanh_dict(self):
        """
        Chuyển đối tượng luận văn thành từ điển, bao gồm thuộc tính riêng.

        Trả về:
            dict: Từ điển chứa toàn bộ thông tin luận văn.
        """
        dict_co_ban = super().chuyen_thanh_dict()
        dict_co_ban['tac_gia'] = self.tac_gia
        dict_co_ban['truong_dai_hoc'] = self.truong_dai_hoc
        return dict_co_ban


class BanThao(MatHang):
    """
    Lớp BanThao (Bản thảo) - Kế thừa từ MatHang.

    Thuộc tính riêng:
        tac_gia (str):    Tên tác giả.
        trang_thai (str): Trạng thái bản thảo (VD: "Chưa duyệt", "Đã duyệt").

    Công thức tính giá bán: gia_co_ban × 1.08 (Cộng 8% thuế).
    """

    def __init__(self, ma_so, ten_san_pham, gia_co_ban, ton_kho, tac_gia, trang_thai):
        """
        Khởi tạo một bản thảo mới.

        Tham số:
            ma_so (str):       Mã định danh duy nhất.
            ten_san_pham (str): Tên bản thảo.
            gia_co_ban (float): Giá cơ bản (phải >= 0).
            ton_kho (int):     Số lượng tồn kho (phải >= 0).
            tac_gia (str):     Tên tác giả.
            trang_thai (str):  Trạng thái bản thảo.
        """
        super().__init__(ma_so, ten_san_pham, gia_co_ban, ton_kho)
        self.loai_hang = "Bản thảo"
        self.tac_gia = tac_gia
        self.trang_thai = trang_thai

    def tinh_gia_ban(self):
        """
        Tính giá bán của bản thảo.
        Công thức: gia_co_ban × 1.08 (Cộng 8% thuế).

        Trả về:
            float: Giá bán sau thuế.
        """
        return self.gia_co_ban * 1.08

    def chuyen_thanh_dict(self):
        """
        Chuyển đối tượng bản thảo thành từ điển, bao gồm thuộc tính riêng.

        Trả về:
            dict: Từ điển chứa toàn bộ thông tin bản thảo.
        """
        dict_co_ban = super().chuyen_thanh_dict()
        dict_co_ban['tac_gia'] = self.tac_gia
        dict_co_ban['trang_thai'] = self.trang_thai
        return dict_co_ban
