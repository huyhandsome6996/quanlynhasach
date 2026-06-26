"""
Tệp lop_doi_tuong.py — Định nghĩa 5 lớp OOP cho 5 loại mặt hàng.
=================================================================

Cấu trúc kế thừa:
    MatHang (ABC, trừu tượng)
        ├── Sach       (Sách)
        ├── TapChi     (Tạp chí)
        ├── BaoGiay    (Báo giấy)
        ├── LuanVan    (Luận văn)
        └── BanThao    (Bản thảo)

Mỗi lớp con GHI ĐÈ (override) phương thức tinh_gia_ban() với công thức
riêng → đó chính là ĐA HÌNH (polymorphism) theo yêu cầu barem.
"""

# ABC = Abstract Base Class (lớp trừu tượng) — không thể khởi tạo trực tiếp.
# abstractmethod = bộ trang trí ép lớp con PHẢI ghi đè phương thức.
from abc import ABC, abstractmethod


class MatHang(ABC):
    """
    Lớp CHA trừu tượng đại diện cho một mặt hàng trong cửa hàng sách.

    Thuộc tính chung (mọi loại mặt hàng đều có):
        ma_so         : Mã số duy nhất (PRIMARY KEY).
        loai_hang     : Tên loại ('Sách', 'Tạp chí', ...) — do lớp con gán.
        ten_san_pham  : Tên sản phẩm hiển thị.
        gia_co_ban    : Giá nhập (chưa tính phụ thu).
        ton_kho       : Số lượng hiện có trong kho.

    Áp dụng:
        - Đóng gói (encapsulation): dữ liệu gói trong đối tượng.
        - Trừu tượng (abstraction):  lớp này không thể dùng trực tiếp.
        - Đa hình (polymorphism):   mỗi lớp con có tinh_gia_ban() riêng.
    """

    def __init__(self, ma_so, ten_san_pham, gia_co_ban, ton_kho):
        # Gán trực tiếp — ma_so là định danh duy nhất, không kiểm tra trùng
        # ở đây (việc đó do DoublyLinkedList và SQLite đảm nhiệm).
        self.ma_so = ma_so

        # Loại hàng mặc định rỗng; lớp con sẽ ghi đè trong __init__ của nó.
        self.loai_hang = ''

        self.ten_san_pham = ten_san_pham

        # Validate giá: không được âm — nếu sai raise ValueError.
        if gia_co_ban < 0:
            raise ValueError('Giá cơ bản không được âm.')
        self.gia_co_ban = gia_co_ban

        # Validate tồn kho: cũng không được âm.
        if ton_kho < 0:
            raise ValueError('Số lượng tồn kho không được âm.')
        self.ton_kho = ton_kho

    @abstractmethod
    def tinh_gia_ban(self):
        """
        Phương thức trừu tượng — BẮT BUỘC mỗi lớp con phải ghi đè.

        Mỗi loại mặt hàng có công thức tính giá bán riêng (đa hình):
            Sách      = giá × 1.10  (phụ thu 10% bản quyền)
            Tạp chí   = giá × 1.05  (phụ thu 5%)
            Báo giấy  = giá × 1.00  (không phụ thu)
            Luận văn  = giá × 1.20  (phụ thu 20% học thuật)
            Bản thảo  = giá × 1.15  (phụ thu 15% tài liệu gốc)
        """
        pass    # Chỉ khai báo chữ ký, không có thân — do con override.

    def chuyen_thanh_dict(self):
        """
        Chuyển đối tượng thành dictionary để JsonResponse trả về cho
        frontend dưới dạng JSON.

        Gia_ban được tính bằng cách GỌI self.tinh_gia_ban() — đây chính là
        lúc đa hình phát huy: cùng một lệnh nhưng ra kết quả khác nhau
        tuỳ loại đối tượng.
        """
        return {
            'ma_so':         self.ma_so,
            'loai_hang':     self.loai_hang,
            'ten_san_pham':  self.ten_san_pham,
            'gia_co_ban':    self.gia_co_ban,
            'ton_kho':       self.ton_kho,
            'gia_ban':       self.tinh_gia_ban()   # ← ĐA HÌNH ở đây!
        }

    def __str__(self):
        """
        Ghi đè __str__ để khi print(san_pham) ra chuỗi dễ đọc.
        Đây cũng là một dạng đa hình (override phương thức mặc định của object).
        """
        return (f'[{self.ma_so}] {self.loai_hang} - {self.ten_san_pham} | '
                f'Giá bán: {self.tinh_gia_ban():.0f}đ | Tồn kho: {self.ton_kho}')


# ============================================================
# CÁC LỚP CON - KẾ THỪA TỪ MatHang
# ============================================================

class Sach(MatHang):
    """
    Lớp Sách — kế thừa từ MatHang.

    Thuộc tính riêng:
        tac_gia        : Tên tác giả.
        nha_xuat_ban   : Nhà xuất bản.

    Công thức giá bán:  gia_co_ban × 1.10 (phụ thu 10% bản quyền).
    """

    def __init__(self, ma_so, ten_san_pham, gia_co_ban, ton_kho, tac_gia, nha_xuat_ban):
        # Gọi __init__ của lớp cha để gán các trường chung.
        super().__init__(ma_so, ten_san_pham, gia_co_ban, ton_kho)

        # Gán nhãn loại hàng — dùng để frontend hiển thị và lọc.
        self.loai_hang = 'Sách'

        # Gán 2 trường riêng của Sách.
        self.tac_gia = tac_gia
        self.nha_xuat_ban = nha_xuat_ban

    def tinh_gia_ban(self):
        """Override — Sách phụ thu 10% bản quyền."""
        return self.gia_co_ban * 1.1

    def chuyen_thanh_dict(self):
        """Ghi đè để bổ sung 2 trường riêng (tac_gia, nha_xuat_ban)."""
        dict_co_ban = super().chuyen_thanh_dict()   # Lấy dict của cha.
        dict_co_ban['tac_gia']       = self.tac_gia
        dict_co_ban['nha_xuat_ban']  = self.nha_xuat_ban
        return dict_co_ban


class TapChi(MatHang):
    """
    Lớp Tạp chí — kế thừa từ MatHang.

    Thuộc tính riêng:
        so_phat_hanh : Số phát hành (VD: 'Số 120').

    Công thức giá bán:  gia_co_ban × 1.05 (phụ thu 5%).
    """

    def __init__(self, ma_so, ten_san_pham, gia_co_ban, ton_kho, so_phat_hanh):
        super().__init__(ma_so, ten_san_pham, gia_co_ban, ton_kho)
        self.loai_hang = 'Tạp chí'
        self.so_phat_hanh = so_phat_hanh

    def tinh_gia_ban(self):
        """Override — Tạp chí phụ thu 5%."""
        return self.gia_co_ban * 1.05

    def chuyen_thanh_dict(self):
        """Bổ sung trường so_phat_hanh vào dict JSON."""
        dict_co_ban = super().chuyen_thanh_dict()
        dict_co_ban['so_phat_hanh'] = self.so_phat_hanh
        return dict_co_ban


class BaoGiay(MatHang):
    """
    Lớp Báo giấy — kế thừa từ MatHang.

    Thuộc tính riêng:
        ngay_xuat_ban : Ngày phát hành (VD: '2025-06-25').

    Công thức giá bán:  gia_co_ban × 1.00 (không phụ thu, báo là hàng nhanh).
    """

    def __init__(self, ma_so, ten_san_pham, gia_co_ban, ton_kho, ngay_xuat_ban):
        super().__init__(ma_so, ten_san_pham, gia_co_ban, ton_kho)
        self.loai_hang = 'Báo giấy'
        self.ngay_xuat_ban = ngay_xuat_ban

    def tinh_gia_ban(self):
        """Override — Báo giấy không phụ thu."""
        return self.gia_co_ban

    def chuyen_thanh_dict(self):
        """Bổ sung trường ngay_xuat_ban vào dict JSON."""
        dict_co_ban = super().chuyen_thanh_dict()
        dict_co_ban['ngay_xuat_ban'] = self.ngay_xuat_ban
        return dict_co_ban


class LuanVan(MatHang):
    """
    Lớp Luận văn — kế thừa từ MatHang.

    Thuộc tính riêng:
        tac_gia         : Sinh viên/tác giả luận văn.
        truong_dai_hoc  : Trường đại học.
        nam_bao_ve      : Năm bảo vệ thành công.

    Công thức giá bán:  gia_co_ban × 1.20 (phụ thu 20% giá trị học thuật).
    """

    def __init__(self, ma_so, ten_san_pham, gia_co_ban, ton_kho, tac_gia, truong_dai_hoc, nam_bao_ve):
        super().__init__(ma_so, ten_san_pham, gia_co_ban, ton_kho)
        self.loai_hang = 'Luận văn'
        self.tac_gia = tac_gia
        self.truong_dai_hoc = truong_dai_hoc
        self.nam_bao_ve = nam_bao_ve

    def tinh_gia_ban(self):
        """Override — Luận văn phụ thu 20%."""
        return self.gia_co_ban * 1.2

    def chuyen_thanh_dict(self):
        """Bổ sung 3 trường riêng của Luận văn."""
        dict_co_ban = super().chuyen_thanh_dict()
        dict_co_ban['tac_gia']        = self.tac_gia
        dict_co_ban['truong_dai_hoc'] = self.truong_dai_hoc
        dict_co_ban['nam_bao_ve']     = self.nam_bao_ve
        return dict_co_ban


class BanThao(MatHang):
    """
    Lớp Bản thảo — kế thừa từ MatHang.

    Thuộc tính riêng:
        tac_gia      : Tác giả bản thảo.
        tinh_trang   : Tình trạng ('Chưa duyệt' / 'Đã duyệt').

    Công thức giá bán:  gia_co_ban × 1.15 (phụ thu 15% cho tài liệu gốc).
    """

    def __init__(self, ma_so, ten_san_pham, gia_co_ban, ton_kho, tac_gia, tinh_trang):
        super().__init__(ma_so, ten_san_pham, gia_co_ban, ton_kho)
        self.loai_hang = 'Bản thảo'
        self.tac_gia = tac_gia
        self.tinh_trang = tinh_trang

    def tinh_gia_ban(self):
        """Override — Bản thảo phụ thu 15%."""
        return self.gia_co_ban * 1.15

    def chuyen_thanh_dict(self):
        """Bổ sung 2 trường riêng của Bản thảo."""
        dict_co_ban = super().chuyen_thanh_dict()
        dict_co_ban['tac_gia']     = self.tac_gia
        dict_co_ban['tinh_trang']  = self.tinh_trang
        return dict_co_ban
