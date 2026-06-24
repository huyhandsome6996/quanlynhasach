# Lớp cha: Mặt hàng (Item)
# Chứa các thuộc tính chung cho mọi loại mặt hàng.
class MatHang:
    def __init__(self, ma_so, ten, gia_co_ban, so_luong):
        # Ép kiểu an toàn để tránh lỗi nhập liệu
        self.ma_so = str(ma_so).strip()
        self.ten = str(ten).strip()
        self.gia_co_ban = float(gia_co_ban)
        self.so_luong = int(so_luong)

    # ----- TÍNH ĐA HÌNH -----
    # Phương thức này sẽ được CÁC LỚP CON GHI ĐÈ.
    # Mỗi loại mặt hàng có một cách tính giá bán riêng (ví dụ: Sách +20%, Tạp chí -10%...).
    # Đây chính là tính đa hình (polymorphism) mà đề bài yêu cầu.
    def tinh_gia_ban(self):
        # Mặc định: giá bán = giá cơ bản (nếu lớp con không ghi đè)
        return self.gia_co_ban

    # Chuyển đối tượng thành dictionary để lưu vào CSDL SQLite / JSON
    def to_dict(self):
        return {
            "loai": "MatHang",
            "ma_so": self.ma_so,
            "ten": self.ten,
            "gia_co_ban": self.gia_co_ban,
            "so_luong": self.so_luong
        }

    # Đa hình: Ghi đè phương thức hiển thị chuỗi để in ra cho dễ đọc
    def __str__(self):
        return f"[{self.ma_so}] {self.ten} - Giá bán: {self.tinh_gia_ban():,.0f}đ - SL: {self.so_luong}"
