"""
Tệp chứa các cấu trúc dữ liệu bổ sung cho hệ thống quản lý cửa hàng sách.

Bao gồm:
    1. NganXep (Stack):  Dùng cho tính năng Undo/Redo.
    2. HangDoi (Queue):  Dùng cho tính năng Giỏ hàng.

Cả hai cấu trúc đều tự cài đặt, KHÔNG dùng list Python thay thế.

Quy ước: Tên biến, tên hàm, chú thích sử dụng tiếng Việt.
Ngoại lệ: Các từ khóa cốt lõi (Stack, Queue, Node, v.v.).
"""


# ============================================================
# NGĂN XẾP (STACK) - Dùng cho Undo/Redo
# ============================================================

class NodeNganXep:
    """
    Lớp NodeNganXep (Mắt xích của Ngăn xếp).

    Mỗi Node chứa:
        data: Dữ liệu (thao tác cần hoàn tác/làm lại).
        duoi: Con trỏ trỏ đến Node phía dưới (Node trước đó trong ngăn xếp).

    Hình minh họa (Stack):
        [Node C]  ← Đỉnh (top)
        [Node B]
        [Node A]  ← Đáy
    """

    def __init__(self, data):
        """
        Khởi tạo một NodeNganXep mới.

        Tham số:
            data: Dữ liệu cần lưu trữ (VD: thông tin thao tác).
        """
        self.data = data
        self.duoi = None  # Con trỏ trỏ đến Node phía dưới


class NganXep:
    """
    Lớp NganXep (Stack - Ngăn xếp).

    Nguyên lý hoạt động: LIFO (Last In, First Out).
    - Phần tử vào CUỐI CÙNG sẽ ra ĐẦU TIÊN.
    - Giống như xếp đĩa: đĩa xếp sau cùng lấy ra trước.

    Ứng dụng: Lưu lịch sử thao tác để thực hiện Undo/Redo.

    Thuộc tính:
        dinh:    Trỏ đến Node trên cùng của ngăn xếp.
        so_luong: Số lượng phần tử hiện có.
    """

    def __init__(self):
        """Khởi tạo ngăn xếp rỗng."""
        self.dinh = None
        self.so_luong = 0

    def day_vao(self, data):
        """
        Đẩy một phần tử vào ĐỈNH ngăn xếp (Push).

        Các bước thực hiện:
            1. Tạo Node mới chứa dữ liệu.
            2. Node mới trỏ duoi đến Node đỉnh hiện tại.
            3. Cập nhật đỉnh thành Node mới.

        Tham số:
            data: Dữ liệu cần đẩy vào ngăn xếp.
        """
        node_moi = NodeNganXep(data)
        node_moi.duoi = self.dinh  # Node mới trỏ xuống Node đỉnh cũ
        self.dinh = node_moi        # Cập nhật đỉnh thành Node mới
        self.so_luong += 1

    def lay_ra(self):
        """
        Lấy phần tử khỏi ĐỈNH ngăn xếp (Pop).

        Các bước thực hiện:
            1. Nếu ngăn xếp rỗng → trả về None.
            2. Lưu dữ liệu của Node đỉnh.
            3. Cập nhật đỉnh xuống Node phía dưới.
            4. Trả về dữ liệu đã lưu.

        Trả về:
            Dữ liệu của Node đỉnh, hoặc None nếu ngăn xếp rỗng.
        """
        if self.dinh is None:
            return None

        data = self.dinh.data
        self.dinh = self.dinh.duoi  # Đỉnh trỏ xuống Node dưới
        self.so_luong -= 1
        return data

    def xem_dinh(self):
        """
        Xem dữ liệu tại đỉnh ngăn xếp mà KHÔNG lấy ra (Peek).

        Trả về:
            Dữ liệu của Node đỉnh, hoặc None nếu ngăn xếp rỗng.
        """
        if self.dinh is None:
            return None
        return self.dinh.data

    def rong(self):
        """
        Kiểm tra ngăn xếp có rỗng không.

        Trả về:
            True: Ngăn xếp rỗng. False: Ngăn xếp có phần tử.
        """
        return self.dinh is None

    def xoa_tat_ca(self):
        """Xóa toàn bộ phần tử trong ngăn xếp."""
        self.dinh = None
        self.so_luong = 0


# ============================================================
# HÀNG ĐỢI (QUEUE) - Dùng cho Giỏ hàng
# ============================================================

class NodeHangDoi:
    """
    Lớp NodeHangDoi (Mắt xích của Hàng đợi).

    Mỗi Node chứa:
        data: Dữ liệu (mặt hàng trong giỏ hàng).
        sau:  Con trỏ trỏ đến Node phía sau (Node tiếp theo trong hàng đợi).

    Hình minh họa (Queue):
        Đầu → [Node A] → [Node B] → [Node C] ← Cuối
    """

    def __init__(self, data):
        """
        Khởi tạo một NodeHangDoi mới.

        Tham số:
            data: Dữ liệu cần lưu trữ.
        """
        self.data = data
        self.sau = None  # Con trỏ trỏ đến Node phía sau


class HangDoi:
    """
    Lớp HangDoi (Queue - Hàng đợi).

    Nguyên lý hoạt động: FIFO (First In, First Out).
    - Phần tử vào ĐẦU TIÊN sẽ ra ĐẦU TIÊN.
    - Giống như xếp hàng mua vé: người đến trước được phục vụ trước.

    Ứng dụng: Quản lý giỏ hàng - mặt hàng thêm trước sẽ thanh toán trước.

    Thuộc tính:
        dau:      Trỏ đến Node đầu hàng đợi (lấy ra ở đây).
        cuoi_hang: Trỏ đến Node cuối hàng đợi (thêm vào ở đây).
        so_luong: Số lượng phần tử hiện có.
    """

    def __init__(self):
        """Khởi tạo hàng đợi rỗng."""
        self.dau = None
        self.cuoi_hang = None
        self.so_luong = 0

    def them_vao(self, data):
        """
        Thêm một phần tử vào CUỐI hàng đợi (Enqueue).

        Các bước thực hiện:
            1. Tạo Node mới chứa dữ liệu.
            2. Nếu hàng đợi rỗng → Node mới là cả đầu và cuối.
            3. Nếu đã có phần tử → Nối Node mới sau Node cuối.

        Tham số:
            data: Dữ liệu cần thêm vào hàng đợi.
        """
        node_moi = NodeHangDoi(data)

        # Trường hợp 1: Hàng đợi rỗng
        if self.dau is None:
            self.dau = node_moi
            self.cuoi_hang = node_moi
        else:
            # Trường hợp 2: Hàng đợi đã có phần tử
            self.cuoi_hang.sau = node_moi
            self.cuoi_hang = node_moi

        self.so_luong += 1

    def lay_ra(self):
        """
        Lấy phần tử khỏi ĐẦU hàng đợi (Dequeue).

        Các bước thực hiện:
            1. Nếu hàng đợi rỗng → trả về None.
            2. Lưu dữ liệu của Node đầu.
            3. Cập nhật đầu sang Node tiếp theo.
            4. Trả về dữ liệu đã lưu.

        Trả về:
            Dữ liệu của Node đầu, hoặc None nếu hàng đợi rỗng.
        """
        if self.dau is None:
            return None

        data = self.dau.data
        self.dau = self.dau.sau  # Dịch đầu sang Node sau

        # Nếu hàng đợi chỉ còn 1 phần tử, cập nhật lại cuối
        if self.dau is None:
            self.cuoi_hang = None

        self.so_luong -= 1
        return data

    def xem_danh_sach(self):
        """
        Xem toàn bộ phần tử trong hàng đợi mà KHÔNG lấy ra.

        Trả về:
            list: Danh sách dữ liệu từ đầu đến cuối hàng đợi.
        """
        ket_qua = []
        node_hien_tai = self.dau
        while node_hien_tai is not None:
            if hasattr(node_hien_tai.data, 'chuyen_thanh_dict'):
                ket_qua.append(node_hien_tai.data.chuyen_thanh_dict())
            else:
                ket_qua.append(node_hien_tai.data)
            node_hien_tai = node_hien_tai.sau
        return ket_qua

    def rong(self):
        """
        Kiểm tra hàng đợi có rỗng không.

        Trả về:
            True: Hàng đợi rỗng. False: Hàng đợi có phần tử.
        """
        return self.dau is None

    def xoa_tat_ca(self):
        """Xóa toàn bộ phần tử trong hàng đợi."""
        self.dau = None
        self.cuoi_hang = None
        self.so_luong = 0

    def xoa_theo_ma(self, ma_so):
        """
        Xóa một phần tử trong hàng đợi theo mã số.

        Tham số:
            ma_so (str): Mã số của mặt hàng cần xóa khỏi giỏ.

        Trả về:
            True: Xóa thành công. False: Không tìm thấy.
        """
        if self.dau is None:
            return False

        # Trường hợp Node đầu là Node cần xóa
        if hasattr(self.dau.data, 'ma_so') and self.dau.data.ma_so == ma_so:
            self.dau = self.dau.sau
            if self.dau is None:
                self.cuoi_hang = None
            self.so_luong -= 1
            return True

        # Duyệt tìm Node cần xóa
        node_hien_tai = self.dau
        while node_hien_tai.sau is not None:
            if hasattr(node_hien_tai.sau.data, 'ma_so') and node_hien_tai.sau.data.ma_so == ma_so:
                # Bỏ qua Node cần xóa
                if node_hien_tai.sau == self.cuoi_hang:
                    self.cuoi_hang = node_hien_tai
                node_hien_tai.sau = node_hien_tai.sau.sau
                self.so_luong -= 1
                return True
            node_hien_tai = node_hien_tai.sau

        return False
