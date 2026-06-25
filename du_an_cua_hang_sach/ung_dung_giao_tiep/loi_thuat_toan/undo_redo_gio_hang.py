"""
Module Undo/Redo sử dụng cấu trúc dữ liệu Stack.
Cho phép hoàn tác và làm lại các thao tác vừa thực hiện.
"""


class NganXep:
    """
    Lớp Ngăn xếp (Stack) - cấu trúc LIFO (Last In, First Out).
    Tự cài đặt bằng danh sách liên kết đơn thay vì dùng list Python.
    """

    class _NodeNganXep:
        def __init__(self, du_lieu, ben_duoi=None):
            self.du_lieu = du_lieu
            self.ben_duoi = ben_duoi

    def __init__(self, gioi_han=50):
        self._dinh = None
        self._so_luong = 0
        self._gioi_han = gioi_han  # Giới hạn kích thước stack

    def day_vao(self, du_lieu):
        """Push - Đẩy phần tử vào đỉnh ngăn xếp."""
        self._dinh = self._NodeNganXep(du_lieu, self._dinh)
        self._so_luong += 1
        # Cắt bớt nếu vượt giới hạn
        if self._so_luong > self._gioi_han:
            self._cat_day()

    def lay_ra(self):
        """Pop - Lấy và xóa phần tử ở đỉnh ngăn xếp."""
        if self.la_rong():
            return None
        du_lieu = self._dinh.du_lieu
        self._dinh = self._dinh.ben_duoi
        self._so_luong -= 1
        return du_lieu

    def nhin_dinh(self):
        """Peek - Xem phần tử ở đỉnh mà không xóa."""
        if self.la_rong():
            return None
        return self._dinh.du_lieu

    def la_rong(self):
        """Kiểm tra ngăn xếp có rỗng không."""
        return self._dinh is None

    def xoa_tat_ca(self):
        """Xóa toàn bộ ngăn xếp."""
        self._dinh = None
        self._so_luong = 0

    def _cat_day(self):
        """Cắt bớt phần tử ở đáy khi vượt giới hạn."""
        node = self._dinh
        dem = 1
        while node is not None and dem < self._gioi_han:
            node = node.ben_duoi
            dem += 1
        if node is not None:
            node.ben_duoi = None
            self._so_luong = self._gioi_han

    @property
    def so_luong(self):
        return self._so_luong


class QuanLyUndoRedo:
    """
    Quản lý chức năng Undo/Redo bằng 2 Stack.
    - Stack Undo: chứa các thao tác đã thực hiện.
    - Stack Redo: chứa các thao tác đã hoàn tác (để làm lại).

    Mỗi thao tác được lưu dưới dạng dict:
    {
        'loai': 'them' | 'xoa' | 'sua',
        'du_lieu_cu': {...},     # Dữ liệu trước khi thay đổi (dùng để undo)
        'du_lieu_moi': {...},    # Dữ liệu sau khi thay đổi (dùng để redo)
    }
    """

    def __init__(self):
        self._ngan_xep_undo = NganXep(gioi_han=50)
        self._ngan_xep_redo = NganXep(gioi_han=50)

    def ghi_thao_tac(self, loai, du_lieu_cu=None, du_lieu_moi=None):
        """
        Ghi nhận một thao tác vào stack Undo.
        Khi có thao tác mới, stack Redo bị xóa (không thể redo nữa).
        """
        thao_tac = {
            'loai': loai,
            'du_lieu_cu': du_lieu_cu,
            'du_lieu_moi': du_lieu_moi
        }
        self._ngan_xep_undo.day_vao(thao_tac)
        self._ngan_xep_redo.xoa_tat_ca()

    def hoan_tac(self):
        """
        Undo - Hoàn tác thao tác gần nhất.
        Trả về thao tác cần hoàn tác, hoặc None nếu không có gì để undo.
        """
        thao_tac = self._ngan_xep_undo.lay_ra()
        if thao_tac is not None:
            self._ngan_xep_redo.day_vao(thao_tac)
        return thao_tac

    def lam_lai(self):
        """
        Redo - Làm lại thao tác đã hoàn tác.
        Trả về thao tác cần làm lại, hoặc None nếu không có gì để redo.
        """
        thao_tac = self._ngan_xep_redo.lay_ra()
        if thao_tac is not None:
            self._ngan_xep_undo.day_vao(thao_tac)
        return thao_tac

    def co_the_hoan_tac(self):
        """Kiểm tra có thể Undo không."""
        return not self._ngan_xep_undo.la_rong()

    def co_the_lam_lai(self):
        """Kiểm tra có thể Redo không."""
        return not self._ngan_xep_redo.la_rong()

    def trang_thai(self):
        """Trả về trạng thái hiện tại (số thao tác Undo/Redo)."""
        return {
            'co_the_undo': self.co_the_hoan_tac(),
            'co_the_redo': self.co_the_lam_lai(),
            'so_undo': self._ngan_xep_undo.so_luong,
            'so_redo': self._ngan_xep_redo.so_luong
        }


class GioHang:
    """
    Lớp Giỏ hàng sử dụng Queue (FIFO) để quản lý các bước thanh toán.
    Áp dụng cấu trúc dữ liệu hàng đợi tự cài đặt.
    """

    class _NodeHangDoi:
        def __init__(self, du_lieu, tiep_theo=None):
            self.du_lieu = du_lieu
            self.tiep_theo = tiep_theo

    def __init__(self):
        self._dau = None     # Đầu hàng đợi (dequeue từ đây)
        self._cuoi = None    # Cuối hàng đợi (enqueue vào đây)
        self._so_luong = 0

    def them_vao_gio(self, ma_so, ten_san_pham, gia_ban, so_luong_mua):
        """Enqueue - Thêm sản phẩm vào giỏ hàng."""
        mon_hang = {
            'ma_so': ma_so,
            'ten_san_pham': ten_san_pham,
            'gia_ban': gia_ban,
            'so_luong_mua': so_luong_mua,
            'thanh_tien': gia_ban * so_luong_mua
        }
        node_moi = self._NodeHangDoi(mon_hang)
        if self._cuoi is None:
            self._dau = node_moi
            self._cuoi = node_moi
        else:
            self._cuoi.tiep_theo = node_moi
            self._cuoi = node_moi
        self._so_luong += 1

    def xoa_khoi_gio(self, ma_so):
        """Xóa một sản phẩm khỏi giỏ hàng theo mã số."""
        truoc = None
        hien_tai = self._dau
        while hien_tai is not None:
            if hien_tai.du_lieu['ma_so'] == ma_so:
                if truoc is None:
                    self._dau = hien_tai.tiep_theo
                    if self._dau is None:
                        self._cuoi = None
                else:
                    truoc.tiep_theo = hien_tai.tiep_theo
                    if hien_tai == self._cuoi:
                        self._cuoi = truoc
                self._so_luong -= 1
                return True
            truoc = hien_tai
            hien_tai = hien_tai.tiep_theo
        return False

    def thanh_toan(self):
        """Dequeue tất cả - Xử lý thanh toán và trả về hóa đơn."""
        if self.la_rong():
            return None
        hoa_don = {
            'cac_mon': [],
            'tong_tien': 0,
            'so_mon': self._so_luong
        }
        while not self.la_rong():
            mon = self._dau.du_lieu
            hoa_don['cac_mon'].append(mon)
            hoa_don['tong_tien'] += mon['thanh_tien']
            self._dau = self._dau.tiep_theo
            self._so_luong -= 1
        self._cuoi = None
        return hoa_don

    def xem_gio_hang(self):
        """Xem toàn bộ giỏ hàng mà không xóa."""
        cac_mon = []
        tong_tien = 0
        node = self._dau
        while node is not None:
            cac_mon.append(node.du_lieu)
            tong_tien += node.du_lieu['thanh_tien']
            node = node.tiep_theo
        return {
            'cac_mon': cac_mon,
            'tong_tien': tong_tien,
            'so_mon': self._so_luong
        }

    def la_rong(self):
        return self._dau is None

    def xoa_gio(self):
        """Xóa toàn bộ giỏ hàng."""
        self._dau = None
        self._cuoi = None
        self._so_luong = 0

    @property
    def so_luong(self):
        return self._so_luong
