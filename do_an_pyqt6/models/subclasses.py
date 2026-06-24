from models.item import MatHang

# ====================================================================
# CÁC LỚP CON: Kế thừa từ MatHang và ghi đè tinh_gia_ban() để thể hiện
# TÍNH ĐA HÌNH (Polymorphism) theo yêu cầu đề bài.
# ====================================================================


# Lớp Con 1: Sách (Book) — cộng thêm 20% vào giá cơ bản
class Sach(MatHang):
    def __init__(self, ma_so, ten, gia_co_ban, so_luong, tac_gia, nha_xuat_ban):
        super().__init__(ma_so, ten, gia_co_ban, so_luong)  # Gọi __init__ lớp cha
        self.tac_gia = tac_gia
        self.nha_xuat_ban = nha_xuat_ban

    # GHI ĐÈ: Sách có giá bán = giá cơ bản + 20%
    def tinh_gia_ban(self):
        return self.gia_co_ban * 1.20

    def to_dict(self):
        data = super().to_dict()
        data["loai"] = "Sach"
        data["tac_gia"] = self.tac_gia
        data["nha_xuat_ban"] = self.nha_xuat_ban
        return data


# Lớp Con 2: Tạp chí (Magazines) — giảm 10% so với giá cơ bản
class TapChi(MatHang):
    def __init__(self, ma_so, ten, gia_co_ban, so_luong, so_phat_hanh):
        super().__init__(ma_so, ten, gia_co_ban, so_luong)
        self.so_phat_hanh = so_phat_hanh

    # GHI ĐÈ: Tạp chí cũ nên giảm giá 10%
    def tinh_gia_ban(self):
        return self.gia_co_ban * 0.90

    def to_dict(self):
        data = super().to_dict()
        data["loai"] = "TapChi"
        data["so_phat_hanh"] = self.so_phat_hanh
        return data


# Lớp Con 3: Báo (Newspapers) — giữ nguyên giá cơ bản
class Bao(MatHang):
    def __init__(self, ma_so, ten, gia_co_ban, so_luong, ngay_phat_hanh):
        super().__init__(ma_so, ten, gia_co_ban, so_luong)
        self.ngay_phat_hanh = ngay_phat_hanh

    # GHI ĐÈ: Báo bán theo giá gốc (không cộng không trừ)
    def tinh_gia_ban(self):
        return self.gia_co_ban

    def to_dict(self):
        data = super().to_dict()
        data["loai"] = "Bao"
        data["ngay_phat_hanh"] = self.ngay_phat_hanh
        return data


# Lớp Con 4: Luận văn (Theses) — cộng 30% vì là tài liệu đặc biệt
class LuanVan(MatHang):
    def __init__(self, ma_so, ten, gia_co_ban, so_luong, truong_dai_hoc):
        super().__init__(ma_so, ten, gia_co_ban, so_luong)
        self.truong_dai_hoc = truong_dai_hoc

    # GHI ĐÈ: Luận văn tài liệu hiếm nên cộng 30%
    def tinh_gia_ban(self):
        return self.gia_co_ban * 1.30

    def to_dict(self):
        data = super().to_dict()
        data["loai"] = "LuanVan"
        data["truong_dai_hoc"] = self.truong_dai_hoc
        return data


# Lớp Con 5: Bản thảo (Manuscripts) — cộng 50% vì là bản gốc
class BanThao(MatHang):
    def __init__(self, ma_so, ten, gia_co_ban, so_luong, tinh_trang):
        super().__init__(ma_so, ten, gia_co_ban, so_luong)
        self.tinh_trang = tinh_trang  # "mới" hoặc "cũ"

    # GHI ĐÈ: Bản thảo mới +50%, bản thảo cũ +20%
    def tinh_gia_ban(self):
        if self.tinh_trang.lower() == "mới":
            return self.gia_co_ban * 1.50
        else:
            return self.gia_co_ban * 1.20

    def to_dict(self):
        data = super().to_dict()
        data["loai"] = "BanThao"
        data["tinh_trang"] = self.tinh_trang
        return data
