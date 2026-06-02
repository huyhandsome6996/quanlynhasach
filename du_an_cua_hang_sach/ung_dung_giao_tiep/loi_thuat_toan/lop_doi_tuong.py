"""
Tệp chứa các lớp đối tượng (OOP) cho hệ thống quản lý cửa hàng sách.
Bao gồm lớp cha trừu tượng MatHang và các lớp con Sach, TapChi, BaoGiay.

Quy tắc: Tên biến, tên hàm, chú thích sử dụng tiếng Việt.
Ngoại lệ: Các từ khóa cốt lõi của cấu trúc dữ liệu (Node, DoublyLinkedList, head, next, data).
"""

from abc import ABC, abstractmethod


class MatHang(ABC):
    """
    Lớp cha trừu tượng MatHang - Đại diện cho một mặt hàng trong cửa hàng.
    Các lớp con phải kế thừa và ghi đè phương thức tinh_gia_ban().

    Thuộc tính:
        ma_so (str): Mã định danh duy nhất của mặt hàng.
        loai_hang (str): Loại mặt hàng (Sách, Tạp chí, Báo giấy).
        ten_san_pham (str): Tên sản phẩm.
        gia_co_ban (float): Giá cơ bản (Không được âm).
        ton_kho (int): Số lượng tồn kho.
    """

    def __init__(self, ma_so, ten_san_pham, gia_co_ban, ton_kho):
        """
        Khởi tạo một mặt hàng mới.

        Tham số:
            ma_so (str): Mã định danh duy nhất.
            ten_san_pham (str): Tên sản phẩm.
            gia_co_ban (float): Giá cơ bản (phải >= 0).
            ton_kho (int): Số lượng tồn kho (phải >= 0).
        """
        self.ma_so = ma_so
        self.loai_hang = ""  # Sẽ được ghi đè bởi các lớp con
        self.ten_san_pham = ten_san_pham

        # Kiểm tra giá cơ bản không được âm
        if gia_co_ban < 0:
            raise ValueError("Giá cơ bản không được âm.")
        self.gia_co_ban = gia_co_ban

        # Kiểm tra tồn kho không được âm
        if ton_kho < 0:
            raise ValueError("Số lượng tồn kho không được âm.")
        self.ton_kho = ton_kho

    @abstractmethod
    def tinh_gia_ban(self):
        """
        Phương thức trừu tượng tính giá bán.
        Mỗi lớp con phải ghi đè phương thức này (Tính đa hình).

        Trả về:
            float: Giá bán sau khi áp dụng thuế.
        """
        pass

    def chuyen_thanh_dict(self):
        """
        Chuyển đổi đối tượng mặt hàng thành từ điển (dict) Python
        để dễ dàng serialize thành JSON gửi về giao diện.

        Trả về:
            dict: Từ điển chứa thông tin mặt hàng.
        """
        return {
            'ma_so': self.ma_so,
            'loai_hang': self.loai_hang,
            'ten_san_pham': self.ten_san_pham,
            'gia_co_ban': self.gia_co_ban,
            'ton_kho': self.ton_kho,
            'gia_ban': self.tinh_gia_ban()
        }

    def __str__(self):
        """
        Trả về chuỗi mô tả mặt hàng.

        Trả về:
            str: Chuỗi mô tả ngắn gọn.
        """
        return f"[{self.ma_so}] {self.loai_hang} - {self.ten_san_pham} | Giá bán: {self.tinh_gia_ban():.0f}đ | Tồn kho: {self.ton_kho}"


class Sach(MatHang):
    """
    Lớp Sach (Sách) - Kế thừa từ MatHang.
    Thuộc tính riêng: tac_gia (Tác giả), nha_xuat_ban (Nhà xuất bản).
    Ghi đè tinh_gia_ban() = gia_co_ban * 1.1 (Cộng 10% thuế).
    """

    def __init__(self, ma_so, ten_san_pham, gia_co_ban, ton_kho, tac_gia, nha_xuat_ban):
        """
        Khởi tạo một cuốn sách mới.

        Tham số:
            ma_so (str): Mã định danh duy nhất.
            ten_san_pham (str): Tên sách.
            gia_co_ban (float): Giá cơ bản (phải >= 0).
            ton_kho (int): Số lượng tồn kho (phải >= 0).
            tac_gia (str): Tên tác giả.
            nha_xuat_ban (str): Tên nhà xuất bản.
        """
        super().__init__(ma_so, ten_san_pham, gia_co_ban, ton_kho)
        self.loai_hang = "Sách"
        self.tac_gia = tac_gia
        self.nha_xuat_ban = nha_xuat_ban

    def tinh_gia_ban(self):
        """
        Tính giá bán của sách.
        Công thức: gia_co_ban * 1.1 (Cộng 10% thuế).

        Trả về:
            float: Giá bán sau thuế.
        """
        return self.gia_co_ban * 1.1

    def chuyen_thanh_dict(self):
        """
        Chuyển đổi đối tượng sách thành từ điển, bao gồm các thuộc tính riêng.

        Trả về:
            dict: Từ điển chứa thông tin sách.
        """
        dict_co_ban = super().chuyen_thanh_dict()
        dict_co_ban['tac_gia'] = self.tac_gia
        dict_co_ban['nha_xuat_ban'] = self.nha_xuat_ban
        return dict_co_ban


class TapChi(MatHang):
    """
    Lớp TapChi (Tạp chí) - Kế thừa từ MatHang.
    Thuộc tính riêng: so_phat_hanh (Số phát hành).
    Ghi đè tinh_gia_ban() = gia_co_ban * 1.05 (Cộng 5% thuế).
    """

    def __init__(self, ma_so, ten_san_pham, gia_co_ban, ton_kho, so_phat_hanh):
        """
        Khởi tạo một cuốn tạp chí mới.

        Tham số:
            ma_so (str): Mã định danh duy nhất.
            ten_san_pham (str): Tên tạp chí.
            gia_co_ban (float): Giá cơ bản (phải >= 0).
            ton_kho (int): Số lượng tồn kho (phải >= 0).
            so_phat_hanh (str): Số phát hành.
        """
        super().__init__(ma_so, ten_san_pham, gia_co_ban, ton_kho)
        self.loai_hang = "Tạp chí"
        self.so_phat_hanh = so_phat_hanh

    def tinh_gia_ban(self):
        """
        Tính giá bán của tạp chí.
        Công thức: gia_co_ban * 1.05 (Cộng 5% thuế).

        Trả về:
            float: Giá bán sau thuế.
        """
        return self.gia_co_ban * 1.05

    def chuyen_thanh_dict(self):
        """
        Chuyển đổi đối tượng tạp chí thành từ điển, bao gồm thuộc tính riêng.

        Trả về:
            dict: Từ điển chứa thông tin tạp chí.
        """
        dict_co_ban = super().chuyen_thanh_dict()
        dict_co_ban['so_phat_hanh'] = self.so_phat_hanh
        return dict_co_ban


class BaoGiay(MatHang):
    """
    Lớp BaoGiay (Báo giấy) - Kế thừa từ MatHang.
    Thuộc tính riêng: ngay_xuat_ban (Ngày xuất bản).
    Ghi đè tinh_gia_ban() = gia_co_ban (Không cộng thuế).
    """

    def __init__(self, ma_so, ten_san_pham, gia_co_ban, ton_kho, ngay_xuat_ban):
        """
        Khởi tạo một tờ báo giấy mới.

        Tham số:
            ma_so (str): Mã định danh duy nhất.
            ten_san_pham (str): Tên báo.
            gia_co_ban (float): Giá cơ bản (phải >= 0).
            ton_kho (int): Số lượng tồn kho (phải >= 0).
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
        Chuyển đổi đối tượng báo giấy thành từ điển, bao gồm thuộc tính riêng.

        Trả về:
            dict: Từ điển chứa thông tin báo giấy.
        """
        dict_co_ban = super().chuyen_thanh_dict()
        dict_co_ban['ngay_xuat_ban'] = self.ngay_xuat_ban
        return dict_co_ban
