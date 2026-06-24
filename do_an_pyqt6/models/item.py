# Lớp cha: Mặt hàng (Item)
class MatHang:
    def __init__(self, ma_so, ten, gia_ban, so_luong):
        self.ma_so = ma_so
        self.ten = ten
        self.gia_ban = float(gia_ban)
        self.so_luong = int(so_luong)

    # Đa hình: Phương thức tinh_gia_ban có thể được ghi đè ở lớp con nếu cần
    def tinh_gia_ban(self):
        return self.gia_ban

    def to_dict(self):
        return {
            "loai": "MatHang",
            "ma_so": self.ma_so,
            "ten": self.ten,
            "gia_ban": self.gia_ban,
            "so_luong": self.so_luong
        }

    # Đa hình: Ghi đè phương thức hiển thị chuỗi
    def __str__(self):
        return f"[{self.ma_so}] {self.ten} - Giá: {self.gia_ban} - SL: {self.so_luong}"
