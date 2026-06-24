# ====================================================================
# HÀNG ĐỢI (QUEUE) - Cấu trúc FIFO: Vào trước, ra trước
# --------------------------------------------------------------------
# Tưởng tượng như XẾP HÀNG MUA VÉ: người đến trước được phục vụ trước.
# Ứng dụng: dùng để làm GIỎ HÀNG trong phần mềm.
# ====================================================================


class NutHangDoi:
    """Mỗi mắt xích trong hàng đợi (giống như 1 người đang xếp hàng)."""

    def __init__(self, du_lieu):
        self.du_lieu = du_lieu  # Dữ liệu chứa trong mắt xích
        self.sau = None          # Trỏ tới mắt xích đứng sau mình


class HangDoi:
    """
    Hàng đợi (Queue) - FIFO: First In, First Out.
    - Phần tử vào đầu tiên sẽ được lấy ra đầu tiên.
    - Giống như xếp hàng mua vé: người đến trước được phục vụ trước.
    """

    def __init__(self):
        self.dau = None      # Phần tử đầu hàng (lấy ra ở đây)
        self.cuoi = None     # Phần tử cuối hàng (thêm vào ở đây)
        self.so_luong = 0    # Số phần tử đang có

    def them_vao(self, du_lieu):
        """
        Thêm một phần tử vào CUỐI hàng đợi (Enqueue).
        - Tạo mắt xích mới.
        - Nếu hàng rỗng: phần tử mới là vừa đầu vừa cuối.
        - Nếu không rỗng: phần tử cuối hiện tại trỏ tới phần tử mới.
        """
        nut_moi = NutHangDoi(du_lieu)
        if self.cuoi is None:
            # Hàng đợi đang rỗng → phần tử mới là vừa đầu vừa cuối
            self.dau = nut_moi
            self.cuoi = nut_moi
        else:
            self.cuoi.sau = nut_moi  # Nối phần tử cũ với phần tử mới
            self.cuoi = nut_moi       # Cập nhật lại phần tử cuối
        self.so_luong += 1

    def lay_ra(self):
        """
        Lấy phần tử ở ĐẦU hàng đợi ra (Dequeue).
        - Nếu rỗng: trả về None.
        - Nếu không rỗng: trả về dữ liệu đầu, đầu mới = phần tử đứng sau.
        """
        if self.dau is None:
            return None
        nut_lay = self.dau
        self.dau = self.dau.sau  # Đầu mới = phần tử đứng sau
        if self.dau is None:
            # Hàng đợi rỗng sau khi lấy ra
            self.cuoi = None
        self.so_luong -= 1
        return nut_lay.du_lieu

    def xem_danh_sach(self):
        """Trả về list Python chứa tất cả phần tử (KHÔNG xóa khỏi hàng đợi)."""
        ket_qua = []
        hien_tai = self.dau
        while hien_tai is not None:
            ket_qua.append(hien_tai.du_lieu)
            hien_tai = hien_tai.sau
        return ket_qua

    def xoa_theo_ma(self, ma_so):
        """
        Xóa 1 phần tử theo mã số (dùng để BỎ 1 món khỏi giỏ hàng).
        Trả về True nếu xóa được, False nếu không tìm thấy.
        """
        hien_tai = self.dau
        truoc = None
        while hien_tai is not None:
            if hien_tai.du_lieu.ma_so == ma_so:
                if truoc is None:
                    # Xóa phần tử ĐẦU tiên
                    self.dau = hien_tai.sau
                    if self.dau is None:
                        self.cuoi = None  # Hàng rỗng sau khi xóa
                else:
                    truoc.sau = hien_tai.sau
                    if hien_tai == self.cuoi:
                        self.cuoi = truoc  # Xóa phần tử cuối
                self.so_luong -= 1
                return True
            truoc = hien_tai
            hien_tai = hien_tai.sau
        return False

    def rong(self):
        """Kiểm tra hàng đợi có rỗng không."""
        return self.dau is None

    def xoa_tat_ca(self):
        """Xóa sạch toàn bộ hàng đợi."""
        self.dau = None
        self.cuoi = None
        self.so_luong = 0
