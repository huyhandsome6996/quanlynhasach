"""
Tệp chứa 2 cấu trúc dữ liệu tự cài đặt: Ngăn xếp (Stack) và Hàng đợi (Queue).
===========================================================================

Bao gồm:
    1. NganXep (Stack):  Dùng cho tính năng Undo/Redo.
    2. HangDoi (Queue):  Dùng cho tính năng Giỏ hàng.

Cả hai cấu trúc đều TỰ CÀI ĐẶT (dùng lớp Node liên kết qua con trỏ),
KHÔNG dùng list Python thay thế — để đúng tinh thần môn Lập trình Nâng cao.
"""

# ============================================================
# NGĂN XẾP (STACK) - Dùng cho Undo/Redo
# ============================================================

class NodeNganXep:
    """
    Lớp NodeNganXep — một mắt xích trong Ngăn xếp.

    Mỗi Node chứa:
        data: Dữ liệu (ở đây là thông tin thao tác cần hoàn tác/làm lại).
        duoi: Con trỏ trỏ đến Node ngay phía dưới trong ngăn xếp.

    Minh họa Stack (LIFO - Last In First Out):
        [Node C]  ← Đỉnh (top)    ← Lấy ra đầu tiên
        [Node B]
        [Node A]  ← Đáy           ← Lấy ra cuối cùng
    """

    def __init__(self, data):
        """Khởi tạo một Node mới với dữ liệu truyền vào, duoi = None."""
        self.data = data        # Lưu dữ liệu của Node (thường là dict thao tác).
        self.duoi = None        # Chưa trỏ đến Node nào (sẽ gán khi push).


class NganXep:
    """
    Lớp NganXep (Stack - Ngăn xếp) — tự cài đặt theo nguyên lý LIFO.

    Nguyên lý LIFO (Last In First Out):
      - Phần tử ĐẨY VÀO cuối cùng sẽ được LẤY RA đầu tiên.
      - Giống như xếp đĩa: đĩa xếp sau cùng nằm trên cùng → lấy ra trước.

    Ứng dụng: Lưu lịch sử thao tác để Undo (lấy từ đỉnh undo)
              và Redo (chuyển sang đỉnh redo).

    Thuộc tính:
        dinh:     Trỏ đến Node trên cùng của ngăn xếp (hoặc None nếu rỗng).
        so_luong: Số Node hiện có trong ngăn xếp.
    """

    def __init__(self):
        """Khởi tạo một ngăn xếp rỗng: đỉnh = None, số lượng = 0."""
        self.dinh = None        # Chưa có Node nào → đỉnh là None.
        self.so_luong = 0       # Đếm số phần tử để hiển thị / kiểm tra nhanh.

    def day_vao(self, data):
        """
        Push — đẩy một phần tử mới lên ĐỈNH ngăn xếp.

        Tham số: data — dữ liệu cần lưu (thường là dict chứa
                 'loai' thao tác, 'du_lieu_cu', 'du_lieu_moi').
        """
        node_moi = NodeNganXep(data)    # Bọc dữ liệu vào một Node mới.
        node_moi.duoi = self.dinh       # Node mới trỏ xuống Node đỉnh cũ.
        self.dinh = node_moi            # Cập nhật đỉnh = Node mới.
        self.so_luong += 1              # Tăng bộ đếm.

    def lay_ra(self):
        """
        Pop — lấy phần tử trên ĐỈNH ngăn xếp ra (và xóa nó khỏi stack).

        Trả về: dữ liệu của Node đỉnh, hoặc None nếu ngăn xếp rỗng.
        """
        if self.dinh is None:           # Trường hợp ngăn xếp rỗng.
            return None
        data = self.dinh.data           # Lưu dữ liệu đỉnh trước khi gỡ.
        self.dinh = self.dinh.duoi      # Hạ đỉnh xuống Node phía dưới.
        self.so_luong -= 1              # Giảm bộ đếm.
        return data                     # Trả về dữ liệu đã gỡ.

    def xem_dinh(self):
        """
        Peek — xem dữ liệu đỉnh mà KHÔNG lấy ra (không thay đổi stack).

        Trả về: dữ liệu của Node đỉnh, hoặc None nếu rỗng.
        """
        if self.dinh is None:
            return None
        return self.dinh.data

    def rong(self):
        """Kiểm tra ngăn xếp có rỗng không. Trả về True/False."""
        return self.dinh is None

    def xoa_tat_ca(self):
        """Clear — xóa toàn bộ Node trong ngăn xếp (chỉ cần cắt đỉnh)."""
        self.dinh = None                # Cắt liên kết → Python GC sẽ dọn Node.
        self.so_luong = 0


# ============================================================
# HÀNG ĐỢI (QUEUE) - Dùng cho Giỏ hàng
# ============================================================

class NodeHangDoi:
    """
    Lớp NodeHangDoi — một mắt xích trong Hàng đợi.

    Mỗi Node chứa:
        data: Dữ liệu (ở đây là mặt hàng trong giỏ).
        sau:  Con trỏ trỏ đến Node phía sau (Node tiếp theo trong hàng).

    Minh họa Queue (FIFO - First In First Out):
        Đầu → [A] → [B] → [C] ← Cuối
        (A vào trước → A ra trước)
    """

    def __init__(self, data):
        """Khởi tạo Node mới với dữ liệu truyền vào, sau = None."""
        self.data = data        # Lưu mặt hàng (đối tượng Sach/TapChi/...).
        self.sau = None         # Chưa trỏ đến Node kế tiếp.


class HangDoi:
    """
    Lớp HangDoi (Queue - Hàng đợi) — tự cài đặt theo nguyên lý FIFO.

    Nguyên lý FIFO (First In First Out):
      - Phần tử THÊM VÀO đầu tiên sẽ được LẤY RA đầu tiên.
      - Giống như xếp hàng mua vé: người đến trước được phục vụ trước.

    Ứng dụng: Quản lý giỏ hàng — mặt hàng thêm trước sẽ thanh toán trước.

    Thuộc tính:
        dau:       Trỏ đến Node đầu hàng (lấy ra ở đây khi thanh toán).
        cuoi_hang: Trỏ đến Node cuối hàng (thêm mới vào đây).
        so_luong:  Số Node hiện có.
    """

    def __init__(self):
        """Khởi tạo hàng đợi rỗng: đầu = cuối = None, số lượng = 0."""
        self.dau = None
        self.cuoi_hang = None
        self.so_luong = 0

    def them_vao(self, data):
        """Enqueue — thêm một phần tử vào CUỐI hàng đợi."""
        node_moi = NodeHangDoi(data)        # Bọc dữ liệu vào Node mới.

        if self.dau is None:                # Trường hợp hàng đang rỗng.
            self.dau = node_moi             # Node mới là cả đầu lẫn cuối.
            self.cuoi_hang = node_moi
        else:                               # Trường hợp đã có phần tử.
            self.cuoi_hang.sau = node_moi   # Nối Node mới sau Node cuối.
            self.cuoi_hang = node_moi       # Cập nhật cuối = Node mới.

        self.so_luong += 1

    def lay_ra(self):
        """
        Dequeue — lấy phần tử ở ĐẦU hàng đợi ra (và xóa nó).

        Trả về: dữ liệu của Node đầu, hoặc None nếu rỗng.
        """
        if self.dau is None:
            return None

        data = self.dau.data                # Lưu dữ liệu đầu.
        self.dau = self.dau.sau             # Dịch đầu sang Node kế tiếp.

        if self.dau is None:                # Nếu sau khi dịch mà rỗng →
            self.cuoi_hang = None           # phải reset cả cuối_hang.

        self.so_luong -= 1
        return data

    def xem_danh_sach(self):
        """
        Trả về danh sách Python chứa toàn bộ phần tử từ đầu đến cuối,
        dùng để frontend hiển thị giỏ hàng. KHÔNG lấy phần tử ra.
        """
        ket_qua = []                            # Danh sách kết quả.
        node_hien_tai = self.dau                # Bắt đầu duyệt từ đầu.
        while node_hien_tai is not None:        # Lặp đến khi hết Node.
            if hasattr(node_hien_tai.data, 'chuyen_thanh_dict'):
                # Nếu data là đối tượng có hàm chuyen_thanh_dict → gọi để ra dict.
                ket_qua.append(node_hien_tai.data.chuyen_thanh_dict())
            else:
                # Nếu data đã là dict/kiểu cơ bản → giữ nguyên.
                ket_qua.append(node_hien_tai.data)
            node_hien_tai = node_hien_tai.sau   # Tiến sang Node kế.
        return ket_qua

    def rong(self):
        """Kiểm tra hàng đợi có rỗng không. Trả về True/False."""
        return self.dau is None

    def xoa_tat_ca(self):
        """Clear — xóa toàn bộ giỏ hàng (dùng khi thanh toán xong)."""
        self.dau = None
        self.cuoi_hang = None
        self.so_luong = 0

    def xoa_theo_ma(self, ma_so):
        """
        Xóa một phần tử BẤT KỲ trong hàng đợi theo mã số
        (vì khách có thể đổi ý, muốn bỏ 1 món khỏi giỏ).

        Hỗ trợ 2 kiểu dữ liệu trong Node:
            - Đối tượng có thuộc tính `ma_so` (MatHang + lớp con).
            - Dict có key 'ma_so' (dùng khi giỏ hàng lưu dict thay vì object).

        Tham số: ma_so — mã sản phẩm cần bỏ.
        Trả về: True nếu xóa được, False nếu không tìm thấy.
        """
        if self.dau is None:                    # Hàng rỗng.
            return False

        # Hàm nội bộ: lấy ma_so từ data (hỗ trợ cả object + dict).
        def _lay_ma(d):
            if hasattr(d, 'ma_so'):             # Object có attribute.
                return d.ma_so
            if isinstance(d, dict):             # Dict có key.
                return d.get('ma_so')
            return None

        # Trường hợp 1: Node cần xóa chính là Node đầu.
        if _lay_ma(self.dau.data) == ma_so:
            self.dau = self.dau.sau             # Bỏ qua Node đầu.
            if self.dau is None:                # Nếu hàng chỉ có 1 Node.
                self.cuoi_hang = None
            self.so_luong -= 1
            return True

        # Trường hợp 2: Node cần xóa nằm ở giữa hoặc cuối → duyệt tìm.
        node_hien_tai = self.dau
        while node_hien_tai.sau is not None:
            # Nếu Node kế tiếp (node_hien_tai.sau) là Node cần xóa.
            if _lay_ma(node_hien_tai.sau.data) == ma_so:
                # Nếu Node cần xóa là Node cuối → cập nhật lại cuối_hang.
                if node_hien_tai.sau == self.cuoi_hang:
                    self.cuoi_hang = node_hien_tai
                # Bỏ qua Node cần xóa: trỏ `.sau` của Node hiện tại sang Node sau nữa.
                node_hien_tai.sau = node_hien_tai.sau.sau
                self.so_luong -= 1
                return True
            node_hien_tai = node_hien_tai.sau   # Tiếp tục duyệt.

        return False                            # Không tìm thấy mã.
