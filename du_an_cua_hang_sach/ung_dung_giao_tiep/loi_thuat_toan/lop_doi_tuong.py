from abc import ABC, abstractmethod

class MatHang(ABC):
    """
    Lớp cha trừu tượng đại diện cho một mặt hàng trong cửa hàng sách.
    Thuộc tính chung: Mã số, Tên sản phẩm, Giá cơ bản, Số lượng tồn kho.
    Áp dụng tính đóng gói (encapsulation) và trừu tượng (abstraction).
    """

    def __init__(self, ma_so, ten_san_pham, gia_co_ban, ton_kho):
        self.ma_so = ma_so
        self.loai_hang = ''
        self.ten_san_pham = ten_san_pham
        if gia_co_ban < 0:
            raise ValueError('Giá cơ bản không được âm.')
        self.gia_co_ban = gia_co_ban
        if ton_kho < 0:
            raise ValueError('Số lượng tồn kho không được âm.')
        self.ton_kho = ton_kho

    @abstractmethod
    def tinh_gia_ban(self):
        """Phương thức trừu tượng - tính giá bán tùy theo loại mặt hàng (đa hình)."""
        pass

    def chuyen_thanh_dict(self):
        """Chuyển đối tượng thành dictionary để trả về JSON."""
        return {
            'ma_so': self.ma_so,
            'loai_hang': self.loai_hang,
            'ten_san_pham': self.ten_san_pham,
            'gia_co_ban': self.gia_co_ban,
            'ton_kho': self.ton_kho,
            'gia_ban': self.tinh_gia_ban()
        }

    def __str__(self):
        """Ghi đè __str__ - tính đa hình khi in đối tượng."""
        return f'[{self.ma_so}] {self.loai_hang} - {self.ten_san_pham} | Giá bán: {self.tinh_gia_ban():.0f}đ | Tồn kho: {self.ton_kho}'


class Sach(MatHang):
    """
    Lớp Sách (Book) - kế thừa từ MatHang.
    Thuộc tính riêng: Tác giả, Nhà xuất bản.
    Giá bán = Giá cơ bản * 1.10 (phụ thu 10% bản quyền).
    """

    def __init__(self, ma_so, ten_san_pham, gia_co_ban, ton_kho, tac_gia, nha_xuat_ban):
        super().__init__(ma_so, ten_san_pham, gia_co_ban, ton_kho)
        self.loai_hang = 'Sách'
        self.tac_gia = tac_gia
        self.nha_xuat_ban = nha_xuat_ban

    def tinh_gia_ban(self):
        """Đa hình: Sách có phụ thu 10% bản quyền."""
        return self.gia_co_ban * 1.1

    def chuyen_thanh_dict(self):
        dict_co_ban = super().chuyen_thanh_dict()
        dict_co_ban['tac_gia'] = self.tac_gia
        dict_co_ban['nha_xuat_ban'] = self.nha_xuat_ban
        return dict_co_ban


class TapChi(MatHang):
    """
    Lớp Tạp chí (Magazines) - kế thừa từ MatHang.
    Thuộc tính riêng: Số phát hành.
    Giá bán = Giá cơ bản * 1.05 (phụ thu 5%).
    """

    def __init__(self, ma_so, ten_san_pham, gia_co_ban, ton_kho, so_phat_hanh):
        super().__init__(ma_so, ten_san_pham, gia_co_ban, ton_kho)
        self.loai_hang = 'Tạp chí'
        self.so_phat_hanh = so_phat_hanh

    def tinh_gia_ban(self):
        """Đa hình: Tạp chí phụ thu 5%."""
        return self.gia_co_ban * 1.05

    def chuyen_thanh_dict(self):
        dict_co_ban = super().chuyen_thanh_dict()
        dict_co_ban['so_phat_hanh'] = self.so_phat_hanh
        return dict_co_ban


class BaoGiay(MatHang):
    """
    Lớp Báo giấy (Newspapers) - kế thừa từ MatHang.
    Thuộc tính riêng: Ngày xuất bản.
    Giá bán = Giá cơ bản (không phụ thu).
    """

    def __init__(self, ma_so, ten_san_pham, gia_co_ban, ton_kho, ngay_xuat_ban):
        super().__init__(ma_so, ten_san_pham, gia_co_ban, ton_kho)
        self.loai_hang = 'Báo giấy'
        self.ngay_xuat_ban = ngay_xuat_ban

    def tinh_gia_ban(self):
        """Đa hình: Báo giấy không phụ thu."""
        return self.gia_co_ban

    def chuyen_thanh_dict(self):
        dict_co_ban = super().chuyen_thanh_dict()
        dict_co_ban['ngay_xuat_ban'] = self.ngay_xuat_ban
        return dict_co_ban


class LuanVan(MatHang):
    """
    Lớp Luận văn (Theses) - kế thừa từ MatHang.
    Thuộc tính riêng: Tác giả, Trường đại học, Năm bảo vệ.
    Giá bán = Giá cơ bản * 1.20 (phụ thu 20% giá trị học thuật).
    """

    def __init__(self, ma_so, ten_san_pham, gia_co_ban, ton_kho, tac_gia, truong_dai_hoc, nam_bao_ve):
        super().__init__(ma_so, ten_san_pham, gia_co_ban, ton_kho)
        self.loai_hang = 'Luận văn'
        self.tac_gia = tac_gia
        self.truong_dai_hoc = truong_dai_hoc
        self.nam_bao_ve = nam_bao_ve

    def tinh_gia_ban(self):
        """Đa hình: Luận văn phụ thu 20% giá trị học thuật."""
        return self.gia_co_ban * 1.2

    def chuyen_thanh_dict(self):
        dict_co_ban = super().chuyen_thanh_dict()
        dict_co_ban['tac_gia'] = self.tac_gia
        dict_co_ban['truong_dai_hoc'] = self.truong_dai_hoc
        dict_co_ban['nam_bao_ve'] = self.nam_bao_ve
        return dict_co_ban


class BanThao(MatHang):
    """
    Lớp Bản thảo (Manuscripts) - kế thừa từ MatHang.
    Thuộc tính riêng: Tác giả, Tình trạng (nháp, chỉnh sửa, hoàn thiện).
    Giá bán = Giá cơ bản * 1.15 (phụ thu 15% cho tài liệu gốc).
    """

    def __init__(self, ma_so, ten_san_pham, gia_co_ban, ton_kho, tac_gia, tinh_trang):
        super().__init__(ma_so, ten_san_pham, gia_co_ban, ton_kho)
        self.loai_hang = 'Bản thảo'
        self.tac_gia = tac_gia
        self.tinh_trang = tinh_trang

    def tinh_gia_ban(self):
        """Đa hình: Bản thảo phụ thu 15% cho tài liệu gốc."""
        return self.gia_co_ban * 1.15

    def chuyen_thanh_dict(self):
        dict_co_ban = super().chuyen_thanh_dict()
        dict_co_ban['tac_gia'] = self.tac_gia
        dict_co_ban['tinh_trang'] = self.tinh_trang
        return dict_co_ban