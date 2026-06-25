"""
Tệp undo_redo_gio_hang.py — Bổ sung phiên bản Stack + Queue + quản lý Undo/Redo.
=================================================================================

File này cung cấp các lớp TIỆN ÍCH BỔ SUNG cho chức năng Undo/Redo và Giỏ hàng
với giới hạn kích thước, đầy đủ getter/setter theo phong cách Lập trình Nâng cao.

Lớp chính:
    - NganXep            : Stack LIFO có giới hạn kích thước (50 thao tác).
    - QuanLyUndoRedo     : Quản lý 2 Stack (Undo + Redo).
    - GioHang            : Queue FIFO cho giỏ hàng + thanh toán.

Lưu ý: File cau_truc_du_lieu.py đã có NganXep/HangDoi đơn giản hơn;
file này là PHIÊN BẢN NÂNG CAO phục vụ mục đích học tập nâng cao.
"""


class NganXep:
    """
    Lớp Ngăn xếp (Stack) - cấu trúc LIFO (Last In, First Out).

    Tự cài đặt bằng DSLK đơn (không dùng list Python) — mỗi Node có 1 con trỏ
    trỏ xuống Node bên dưới.

    Có giới hạn kích thước để tránh tràn RAM khi người dùng thao tác quá nhiều.
    """

    # Lớp _NodeNganXep lồng trong NganXep (private — dấu gạch dưới).
    class _NodeNganXep:
        def __init__(self, du_lieu, ben_duoi=None):
            self.du_lieu = du_lieu          # Dữ liệu thao tác.
            self.ben_duoi = ben_duoi        # Trỏ xuống Node dưới (có thể None).

    def __init__(self, gioi_han=50):
        # Khởi tạo stack rỗng với giới hạn số phần tử.
        self._dinh = None                   # Đỉnh stack (None = rỗng).
        self._so_luong = 0                  # Số phần tử hiện có.
        self._gioi_han = gioi_han           # Giới hạn tối đa (mặc định 50).

    def day_vao(self, du_lieu):
        """Push — đẩy một phần tử lên đỉnh ngăn xếp."""
        # Tạo Node mới, trỏ xuống đỉnh cũ.
        self._dinh = self._NodeNganXep(du_lieu, self._dinh)
        self._so_luong += 1
        # Nếu vượt giới hạn → cắt bớt Node ở đáy.
        if self._so_luong > self._gioi_han:
            self._cat_day()

    def lay_ra(self):
        """Pop — lấy phần tử ở đỉnh (và xóa nó). Trả về None nếu rỗng."""
        if self.la_rong():
            return None
        du_lieu = self._dinh.du_lieu        # Lưu dữ liệu đỉnh.
        self._dinh = self._dinh.ben_duoi    # Hạ đỉnh xuống Node dưới.
        self._so_luong -= 1
        return du_lieu

    def nhin_dinh(self):
        """Peek — xem dữ liệu đỉnh mà KHÔNG lấy ra."""
        if self.la_rong():
            return None
        return self._dinh.du_lieu

    def la_rong(self):
        """Kiểm tra stack có rỗng không."""
        return self._dinh is None

    def xoa_tat_ca(self):
        """Clear — xóa toàn bộ stack (chỉ cần cắt đỉnh)."""
        self._dinh = None
        self._so_luong = 0

    def _cat_day(self):
        """Hàm nội bộ — cắt bớt Node ở đáy khi stack vượt giới hạn."""
        node = self._dinh
        dem = 1
        # Duyệt đến Node thứ `gioi_han` (tính từ đỉnh).
        while node is not None and dem < self._gioi_han:
            node = node.ben_duoi
            dem += 1
        # Cắt liên kết → các Node bên dưới sẽ bị GC dọn.
        if node is not None:
            node.ben_duoi = None
            self._so_luong = self._gioi_han

    # @property cho phép truy cập `obj.so_luong` như thuộc tính, không cần gọi hàm.
    @property
    def so_luong(self):
        """Getter — trả về số phần tử hiện có."""
        return self._so_luong


class QuanLyUndoRedo:
    """
    Quản lý Undo/Redo bằng 2 Stack.

    Nguyên lý:
      - Khi người dùng THỰC HIỆN thao tác → đẩy vào stack Undo, XÓA stack Redo.
      - Khi người dùng UNDO → lấy 1 thao tác từ đỉnh Undo → đẩy sang Redo.
      - Khi người dùng REDO → lấy 1 thao tác từ đỉnh Redo → đẩy ngược về Undo.

    Mỗi thao tác lưu dưới dạng dict:
        {
            'loai'       : 'them' | 'xoa' | 'sua',
            'du_lieu_cu' : {...} hoặc None,   # Trạng thái trước khi đổi (dùng cho undo)
            'du_lieu_moi': {...} hoặc None    # Trạng thái sau khi đổi   (dùng cho redo)
        }
    """

    def __init__(self):
        # Khởi tạo 2 stack Undo + Redo, mỗi stack giới hạn 50 thao tác.
        self._ngan_xep_undo = NganXep(gioi_han=50)
        self._ngan_xep_redo = NganXep(gioi_han=50)

    def ghi_thao_tac(self, loai, du_lieu_cu=None, du_lieu_moi=None):
        """
        Ghi nhận một thao tác vừa thực hiện.

        Tham số:
            loai        : 'them' | 'xoa' | 'sua'
            du_lieu_cu  : Dữ liệu trước khi đổi (dùng để undo).
            du_lieu_moi : Dữ liệu sau khi đổi (dùng để redo).
        """
        thao_tac = {
            'loai':        loai,
            'du_lieu_cu':  du_lieu_cu,
            'du_lieu_moi': du_lieu_moi
        }
        # Đẩy vào stack Undo.
        self._ngan_xep_undo.day_vao(thao_tac)
        # Có thao tác mới → không thể redo các thao tác cũ nữa → xóa Redo.
        self._ngan_xep_redo.xoa_tat_ca()

    def hoan_tac(self):
        """
        Undo — hoàn tác thao tác gần nhất.
        Trả về dict thao tác để view biết phải đảo ngược thế nào.
        Trả về None nếu không có gì để undo.
        """
        thao_tac = self._ngan_xep_undo.lay_ra()
        if thao_tac is not None:
            # Đẩy sang Redo để có thể redo lại.
            self._ngan_xep_redo.day_vao(thao_tac)
        return thao_tac

    def lam_lai(self):
        """
        Redo — làm lại thao tác đã undo.
        Trả về dict thao tác, hoặc None nếu không có gì để redo.
        """
        thao_tac = self._ngan_xep_redo.lay_ra()
        if thao_tac is not None:
            # Đẩy ngược về Undo để tiếp tục undo được.
            self._ngan_xep_undo.day_vao(thao_tac)
        return thao_tac

    def co_the_hoan_tac(self):
        """Kiểm tra có thao tác nào để Undo không."""
        return not self._ngan_xep_undo.la_rong()

    def co_the_lam_lai(self):
        """Kiểm tra có thao tác nào để Redo không."""
        return not self._ngan_xep_redo.la_rong()

    def trang_thai(self):
        """Trả về trạng thái hiện tại của Undo/Redo (dùng cho UI hiển thị)."""
        return {
            'co_the_undo': self.co_the_hoan_tac(),
            'co_the_redo': self.co_the_lam_lai(),
            'so_undo':     self._ngan_xep_undo.so_luong,
            'so_redo':     self._ngan_xep_redo.so_luong
        }


class GioHang:
    """
    Lớp Giỏ hàng dùng Queue FIFO.

    Tự cài đặt bằng DSLK đơn: mỗi Node trỏ tới Node kế tiếp (`tiep_theo`).

    Ứng dụng thực tế:
        - Khách thêm món A rồi thêm món B → khi thanh toán, A được xử lý trước.
        - Queue FIFO đảm bảo thứ tự công bằng.
    """

    # Lớp Node nội bộ (private).
    class _NodeHangDoi:
        def __init__(self, du_lieu, tiep_theo=None):
            self.du_lieu = du_lieu
            self.tiep_theo = tiep_theo

    def __init__(self):
        # Khởi tạo hàng đợi rỗng.
        self._dau = None      # Đầu hàng (dequeue từ đây).
        self._cuoi = None     # Cuối hàng (enqueue vào đây).
        self._so_luong = 0

    def them_vao_gio(self, ma_so, ten_san_pham, gia_ban, so_luong_mua):
        """Enqueue — thêm một sản phẩm vào CUỐI giỏ hàng."""
        # Tạo dict chứa thông tin món hàng + thành tiền = giá × số lượng.
        mon_hang = {
            'ma_so':         ma_so,
            'ten_san_pham':  ten_san_pham,
            'gia_ban':       gia_ban,
            'so_luong_mua':  so_luong_mua,
            'thanh_tien':    gia_ban * so_luong_mua
        }
        node_moi = self._NodeHangDoi(mon_hang)

        # Trường hợp giỏ rỗng → Node mới là cả đầu lẫn cuối.
        if self._cuoi is None:
            self._dau = node_moi
            self._cuoi = node_moi
        else:
            # Nối Node mới sau Node cuối, cập nhật cuối.
            self._cuoi.tiep_theo = node_moi
            self._cuoi = node_moi

        self._so_luong += 1

    def xoa_khoi_gio(self, ma_so):
        """
        Xóa 1 sản phẩm khỏi giỏ theo mã số (có thể ở giữa hàng).
        Trả về True nếu xóa được, False nếu không tìm thấy.
        """
        truoc = None                  # Node ngay trước Node hiện tại.
        hien_tai = self._dau
        while hien_tai is not None:
            if hien_tai.du_lieu['ma_so'] == ma_so:
                # Trường hợp Node cần xóa là Node đầu.
                if truoc is None:
                    self._dau = hien_tai.tiep_theo
                    if self._dau is None:
                        self._cuoi = None     # Hàng chỉ có 1 Node → reset cuối.
                else:
                    # Bỏ qua Node hiện tại.
                    truoc.tiep_theo = hien_tai.tiep_theo
                    # Nếu Node cần xóa là Node cuối → cập nhật cuối.
                    if hien_tai == self._cuoi:
                        self._cuoi = truoc
                self._so_luong -= 1
                return True
            truoc = hien_tai
            hien_tai = hien_tai.tiep_theo
        return False

    def thanh_toan(self):
        """
        Dequeue toàn bộ — xử lý thanh toán và trả về hóa đơn.

        Trả về: dict hóa đơn chứa danh sách món + tổng tiền, hoặc None nếu giỏ rỗng.
        """
        if self.la_rong():
            return None

        hoa_don = {
            'cac_mon':   [],
            'tong_tien': 0,
            'so_mon':    self._so_luong
        }

        # Lần lượt lấy từng món từ ĐẦU hàng (theo FIFO) → đưa vào hóa đơn.
        while not self.la_rong():
            mon = self._dau.du_lieu
            hoa_don['cac_mon'].append(mon)
            hoa_don['tong_tien'] += mon['thanh_tien']
            self._dau = self._dau.tiep_theo
            self._so_luong -= 1

        # Sau khi thanh toán xong, giỏ rỗng → reset cuối.
        self._cuoi = None
        return hoa_don

    def xem_gio_hang(self):
        """Xem toàn bộ giỏ hàng mà KHÔNG xóa (peek all)."""
        cac_mon = []
        tong_tien = 0
        node = self._dau
        while node is not None:
            cac_mon.append(node.du_lieu)
            tong_tien += node.du_lieu['thanh_tien']
            node = node.tiep_theo
        return {
            'cac_mon':   cac_mon,
            'tong_tien': tong_tien,
            'so_mon':    self._so_luong
        }

    def la_rong(self):
        """Kiểm tra giỏ có rỗng không."""
        return self._dau is None

    def xoa_gio(self):
        """Clear — xóa toàn bộ giỏ hàng (không thanh toán)."""
        self._dau = None
        self._cuoi = None
        self._so_luong = 0

    @property
    def so_luong(self):
        """Getter — số món hiện có trong giỏ."""
        return self._so_luong
