from models.item import MatHang

# Lớp Con 1: Sách (Book)
class Sach(MatHang):
    def __init__(self, ma_so, ten, gia_ban, so_luong, tac_gia, nha_xuat_ban):
        super().__init__(ma_so, ten, gia_ban, so_luong) # Gọi __init__ của lớp cha
        self.tac_gia = tac_gia
        self.nha_xuat_ban = nha_xuat_ban

    def to_dict(self):
        data = super().to_dict()
        data["loai"] = "Sach"
        data["tac_gia"] = self.tac_gia
        data["nha_xuat_ban"] = self.nha_xuat_ban
        return data

# Lớp Con 2: Tạp Chí (Magazines)
class TapChi(MatHang):
    def __init__(self, ma_so, ten, gia_ban, so_luong, so_phat_hanh):
        super().__init__(ma_so, ten, gia_ban, so_luong)
        self.so_phat_hanh = so_phat_hanh

    def to_dict(self):
        data = super().to_dict()
        data["loai"] = "TapChi"
        data["so_phat_hanh"] = self.so_phat_hanh
        return data

# Lớp Con 3: Báo (Newspapers)
class Bao(MatHang):
    def __init__(self, ma_so, ten, gia_ban, so_luong, ngay_phat_hanh):
        super().__init__(ma_so, ten, gia_ban, so_luong)
        self.ngay_phat_hanh = ngay_phat_hanh

    def to_dict(self):
        data = super().to_dict()
        data["loai"] = "Bao"
        data["ngay_phat_hanh"] = self.ngay_phat_hanh
        return data

# Lớp Con 4: Luận Văn (Theses)
class LuanVan(MatHang):
    def __init__(self, ma_so, ten, gia_ban, so_luong, truong_dai_hoc):
        super().__init__(ma_so, ten, gia_ban, so_luong)
        self.truong_dai_hoc = truong_dai_hoc

    def to_dict(self):
        data = super().to_dict()
        data["loai"] = "LuanVan"
        data["truong_dai_hoc"] = self.truong_dai_hoc
        return data

# Lớp Con 5: Bản Thảo (Manuscripts)
class BanThao(MatHang):
    def __init__(self, ma_so, ten, gia_ban, so_luong, tinh_trang):
        super().__init__(ma_so, ten, gia_ban, so_luong)
        self.tinh_trang = tinh_trang

    def to_dict(self):
        data = super().to_dict()
        data["loai"] = "BanThao"
        data["tinh_trang"] = self.tinh_trang
        return data
