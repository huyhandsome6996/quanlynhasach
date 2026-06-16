"""
Tệp chứa cấu trúc dữ liệu Danh sách liên kết đôi (DoublyLinkedList)
và lớp Node (Mắt xích).

Đây là cấu trúc dữ liệu chính quản lý toàn bộ mặt hàng trên RAM.
KHÔNG sử dụng list Python để thay thế - Tự cài đặt hoàn toàn.

Cấu trúc:
    Node:        Mỗi phần tử chứa data + 2 con trỏ (truoc, next).
    DoublyLinkedList: Quản lý danh sách, cung cấp các thao tác:
        - them_vao_cuoi():      Thêm phần tử vào cuối.
        - xoa_node():           Xóa phần tử theo mã số.
        - tim_theo_ma():        Tìm kiếm theo mã số (ID).
        - tim_kiem():           Tìm kiếm theo từ khóa (tên, loại).
        - sap_xep_tron():       Sắp xếp bằng thuật toán Merge Sort.

Quy ước: Tên biến, tên hàm, chú thích sử dụng tiếng Việt.
Ngoại lệ: Các từ khóa cốt lõi (Node, DoublyLinkedList, head, next, data).
"""


class Node:
    """
    Lớp Node (Mắt xích) - Đại diện cho một phần tử trong danh sách liên kết đôi.

    Mỗi Node chứa:
        data:  Dữ liệu (đối tượng Sách, Tạp chí, Báo giấy...).
        truoc: Con trỏ trỏ về Node phía trước (None nếu là Node đầu).
        next:  Con trỏ trỏ đến Node phía sau (None nếu là Node cuối).

    Hình minh họa:
        None <-- [Node A] <--> [Node B] <--> [Node C] --> None
                   head                           cuoi
    """

    def __init__(self, data):
        """
        Khởi tạo một Node mới.

        Tham số:
            data: Đối tượng dữ liệu cần lưu trữ trong Node.
        """
        self.data = data
        self.truoc = None   # Con trỏ về Node trước
        self.next = None    # Con trỏ đến Node sau

    def __str__(self):
        """Trả về chuỗi mô tả dữ liệu của Node."""
        return str(self.data)


class DoublyLinkedList:
    """
    Lớp DoublyLinkedList (Danh sách liên kết đôi).

    Cấu trúc dữ liệu chính quản lý toàn bộ mặt hàng trong cửa hàng trên RAM.
    Duyệt được theo hai chiều: từ đầu đến cuối (next) và từ cuối về đầu (truoc).

    Thuộc tính:
        head:     Trỏ đến Node đầu tiên (None nếu danh sách rỗng).
        cuoi:     Trỏ đến Node cuối cùng (None nếu danh sách rỗng).
        so_luong: Số lượng phần tử hiện có.
    """

    def __init__(self):
        """Khởi tạo danh sách liên kết đôi rỗng."""
        self.head = None
        self.cuoi = None
        self.so_luong = 0

    # ============================================================
    # THÊM PHẦN TỬ
    # ============================================================

    def them_vao_cuoi(self, data):
        """
        Thêm một phần tử mới vào CUỐI danh sách liên kết đôi.

        Các bước thực hiện:
            1. Tạo Node mới chứa dữ liệu.
            2. Nếu danh sách rỗng → Node mới là cả head và cuoi.
            3. Nếu danh sách có phần tử → Nối Node mới sau Node cuoi.

        Tham số:
            data: Đối tượng dữ liệu cần thêm vào danh sách.
        """
        node_moi = Node(data)

        # Trường hợp 1: Danh sách đang rỗng
        if self.head is None:
            self.head = node_moi
            self.cuoi = node_moi
        else:
            # Trường hợp 2: Danh sách đã có phần tử
            # Nối Node mới vào sau Node cuối hiện tại
            self.cuoi.next = node_moi      # Node cuối trỏ next đến Node mới
            node_moi.truoc = self.cuoi      # Node mới trỏ truoc về Node cuối
            self.cuoi = node_moi            # Cập nhật Node cuối thành Node mới

        self.so_luong += 1

    # ============================================================
    # XÓA PHẦN TỬ
    # ============================================================

    def xoa_node(self, ma_so):
        """
        Xóa một Node khỏi danh sách dựa trên mã số mặt hàng.

        Các bước thực hiện:
            1. Duyệt từ head đến cuối, tìm Node có ma_so khớp.
            2. Nếu tìm thấy, xử lý 3 trường hợp:
               a. Node cần xóa là head
               b. Node cần xóa là cuoi
               c. Node cần xóa nằm ở giữa

        Tham số:
            ma_so (str): Mã số định danh duy nhất của mặt hàng cần xóa.

        Trả về:
            True:  Xóa thành công.
            False: Không tìm thấy Node cần xóa.
        """
        node_hien_tai = self.head

        while node_hien_tai is not None:
            # So sánh mã số của dữ liệu trong Node với mã số cần tìm
            if hasattr(node_hien_tai.data, 'ma_so') and node_hien_tai.data.ma_so == ma_so:

                # Trường hợp A: Node cần xóa là Node ĐẦU TIÊN
                if node_hien_tai == self.head:
                    self.head = node_hien_tai.next
                    if self.head is not None:
                        self.head.truoc = None  # Node đầu mới không có truoc
                    else:
                        # Danh sách chỉ có 1 phần tử → sau khi xóa thì rỗng
                        self.cuoi = None

                # Trường hợp B: Node cần xóa là Node CUỐI CÙNG
                elif node_hien_tai == self.cuoi:
                    self.cuoi = node_hien_tai.truoc
                    self.cuoi.next = None  # Node cuối mới không có next

                # Trường hợp C: Node cần xóa nằm Ở GIỮA danh sách
                else:
                    # Bỏ qua Node hiện tại bằng cách nối Node trước và Node sau
                    node_hien_tai.truoc.next = node_hien_tai.next
                    node_hien_tai.next.truoc = node_hien_tai.truoc

                self.so_luong -= 1
                return True

            # Chưa tìm thấy → di chuyển đến Node tiếp theo
            node_hien_tai = node_hien_tai.next

        return False  # Không tìm thấy

    # ============================================================
    # TÌM KIẾM
    # ============================================================

    def tim_theo_ma(self, ma_so):
        """
        Tìm kiếm mặt hàng theo MÃ SỐ (ID).

        Duyệt tuần tự qua từng Node, so sánh thuộc tính ma_so.
        Dừng lại ngay khi tìm thấy Node đầu tiên khớp.

        Tham số:
            ma_so (str): Mã số cần tìm.

        Trả về:
            Đối tượng dữ liệu nếu tìm thấy, None nếu không tìm thấy.
        """
        node_hien_tai = self.head

        while node_hien_tai is not None:
            if hasattr(node_hien_tai.data, 'ma_so') and node_hien_tai.data.ma_so == ma_so:
                return node_hien_tai.data
            node_hien_tai = node_hien_tai.next

        return None  # Không tìm thấy

    def tim_kiem(self, tu_khoa, tieu_chi='ten'):
        """
        Tìm kiếm nâng cao theo từ khóa với nhiều tiêu chí.

        Duyệt qua tất cả Node, kiểm tra từ khóa theo tiêu chí chọn:
            - 'ten': Tìm trong tên sản phẩm (mặc định).
            - 'ma':  Tìm theo mã số chính xác.
            - 'loai': Tìm theo loại hàng chính xác.

        Tham số:
            tu_khoa (str):    Từ khóa cần tìm (không phân biệt hoa/thường).
            tieu_chi (str):   Tiêu chí tìm kiếm ('ten', 'ma', 'loai').

        Trả về:
            list: Danh sách các đối tượng dữ liệu thỏa mãn điều kiện.
        """
        ket_qua = []
        node_hien_tai = self.head
        tu_khoa_thuong = tu_khoa.lower()

        while node_hien_tai is not None:
            du_lieu = node_hien_tai.data

            if tieu_chi == 'ma':
                # Tìm theo mã số (chính xác, không phân biệt hoa/thường)
                if hasattr(du_lieu, 'ma_so'):
                    if du_lieu.ma_so.lower() == tu_khoa_thuong:
                        ket_qua.append(du_lieu)

            elif tieu_chi == 'loai':
                # Tìm theo loại hàng (chính xác, không phân biệt hoa/thường)
                if hasattr(du_lieu, 'loai_hang'):
                    if du_lieu.loai_hang.lower() == tu_khoa_thuong:
                        ket_qua.append(du_lieu)

            else:
                # Tìm theo tên sản phẩm (chứa từ khóa, không phân biệt hoa/thường)
                if hasattr(du_lieu, 'ten_san_pham'):
                    ten_thuong = du_lieu.ten_san_pham.lower()
                    if tu_khoa_thuong in ten_thuong:
                        ket_qua.append(du_lieu)

            node_hien_tai = node_hien_tai.next

        return ket_qua

    # ============================================================
    # SẮP XẾP - THUẬT TOÁN MERGE SORT
    # ============================================================

    def sap_xep_tron(self, tieu_chi='gia_ban'):
        """
        Sắp xếp danh sách liên kết đôi bằng thuật toán Sắp xếp trộn (Merge Sort).

        Thuật toán Merge Sort trên Danh sách liên kết đôi:
            Bước 1: Chia đôi danh sách thành hai nửa (dùng con trỏ nhanh/chậm).
            Bước 2: Gọi đệ quy sắp xếp từng nửa.
            Bước 3: Trộn hai nửa đã sắp xếp thành một danh sách duy nhất.

        Ưu điểm: Độ phức tạp O(n log n), ổn định, không cần mảng phụ.

        Tham số:
            tieu_chi (str): Tiêu chí sắp xếp ('gia_ban', 'ten_san_pham', 'ton_kho').
        """
        # Danh sách rỗng hoặc chỉ có 1 phần tử → không cần sắp xếp
        if self.head is None or self.head.next is None:
            return

        # ---- Bước 1: Chia danh sách thành hai nửa ----
        nua_dau, nua_sau = self._chia_doi()

        # ---- Bước 2: Đưa mỗi nửa vào DoublyLinkedList tạm để gọi đệ quy ----
        ds_nua_dau = DoublyLinkedList()
        ds_nua_dau.head = nua_dau
        # Tìm Node cuối của nửa đầu
        node_cuoi_dau = nua_dau
        while node_cuoi_dau.next is not None:
            node_cuoi_dau = node_cuoi_dau.next
        ds_nua_dau.cuoi = node_cuoi_dau
        ds_nua_dau.so_luong = self._dem_node(nua_dau)

        ds_nua_sau = DoublyLinkedList()
        ds_nua_sau.head = nua_sau
        # Tìm Node cuối của nửa sau
        node_cuoi_sau = nua_sau
        while node_cuoi_sau.next is not None:
            node_cuoi_sau = node_cuoi_sau.next
        ds_nua_sau.cuoi = node_cuoi_sau
        ds_nua_sau.so_luong = self._dem_node(nua_sau)

        # ---- Gọi đệ quy sắp xếp từng nửa ----
        ds_nua_dau.sap_xep_tron(tieu_chi)
        ds_nua_sau.sap_xep_tron(tieu_chi)

        # ---- Bước 3: Trộn hai nửa đã sắp xếp ----
        self._tron(ds_nua_dau, ds_nua_sau, tieu_chi)

    def _chia_doi(self):
        """
        Chia danh sách liên kết đôi thành hai nửa bằng kỹ thuật con trỏ nhanh/chậm.

        Nguyên lý:
            - Con trỏ CHẬM di chuyển 1 bước mỗi lần.
            - Con trỏ NHANH di chuyển 2 bước mỗi lần.
            - Khi con trỏ nhanh đến cuối, con trỏ chạm ở giữa danh sách.

        Trả về:
            tuple: (nua_dau, nua_sau) - Node đầu của mỗi nửa.
        """
        con_tro_cham = self.head
        con_tro_nhanh = self.head

        while con_tro_nhanh.next is not None and con_tro_nhanh.next.next is not None:
            con_tro_cham = con_tro_cham.next          # Di chuyển 1 bước
            con_tro_nhanh = con_tro_nhanh.next.next    # Di chuyển 2 bước

        # Cắt đôi danh sách tại vị trí con trỏ chậm
        nua_dau = self.head
        nua_sau = con_tro_cham.next
        con_tro_cham.next = None   # Cắt liên kết giữa hai nửa
        if nua_sau is not None:
            nua_sau.truoc = None   # Nửa sau không có Node trước

        return nua_dau, nua_sau

    def _tron(self, ds_a, ds_b, tieu_chi):
        """
        Trộn hai danh sách liên kết đôi đã sắp xếp thành một danh sách duy nhất.

        Nguyên lý:
            - So sánh Node đầu của ds_a và ds_b.
            - Node có giá trị nhỏ hơn được nối vào kết quả.
            - Lặp lại cho đến khi một danh sách hết phần tử.
            - Nối phần còn lại của danh sách kia vào cuối.

        Tham số:
            ds_a:       Danh sách liên kết đôi thứ nhất đã sắp xếp.
            ds_b:       Danh sách liên kết đôi thứ hai đã sắp xếp.
            tieu_chi:   Tiêu chí so sánh khi trộn.
        """
        node_tam = Node(None)  # Node tạm để dễ thao tác
        hien_tai = node_tam

        node_a = ds_a.head
        node_b = ds_b.head

        while node_a is not None and node_b is not None:
            # Lấy giá trị để so sánh
            gia_tri_a = self._lay_gia_tri(node_a.data, tieu_chi)
            gia_tri_b = self._lay_gia_tri(node_b.data, tieu_chi)

            # Node nào có giá trị nhỏ hơn thì được chọn
            if gia_tri_a <= gia_tri_b:
                hien_tai.next = node_a
                node_a.truoc = hien_tai
                node_a = node_a.next
            else:
                hien_tai.next = node_b
                node_b.truoc = hien_tai
                node_b = node_b.next

            hien_tai = hien_tai.next

        # Nối phần còn lại của danh sách A (nếu còn)
        if node_a is not None:
            hien_tai.next = node_a
            node_a.truoc = hien_tai
            self.cuoi = ds_a.cuoi

        # Nối phần còn lại của danh sách B (nếu còn)
        if node_b is not None:
            hien_tai.next = node_b
            node_b.truoc = hien_tai
            self.cuoi = ds_b.cuoi

        # Cập nhật head và bỏ liên kết của Node tạm
        self.head = node_tam.next
        if self.head is not None:
            self.head.truoc = None

    def _lay_gia_tri(self, doi_tuong, tieu_chi):
        """
        Lấy giá trị của đối tượng theo tiêu chí tương ứng để so sánh.

        Tham số:
            doi_tuong:  Đối tượng mặt hàng cần lấy giá trị.
            tieu_chi:   Chuỗi tiêu chí ('gia_ban', 'ten_san_pham', 'ton_kho').

        Trả về:
            Giá trị tương ứng với tiêu chí (số hoặc chuỗi).
        """
        if tieu_chi == 'gia_ban':
            if hasattr(doi_tuong, 'tinh_gia_ban'):
                return doi_tuong.tinh_gia_ban()
            return getattr(doi_tuong, 'gia_co_ban', 0)
        elif tieu_chi == 'ten_san_pham':
            return getattr(doi_tuong, 'ten_san_pham', '')
        elif tieu_chi == 'ton_kho':
            return getattr(doi_tuong, 'ton_kho', 0)
        return 0

    def _dem_node(self, node_dau):
        """
        Đếm số lượng Node từ một Node đầu tiên cho trước.

        Tham số:
            node_dau: Node bắt đầu đếm.

        Trả về:
            int: Số lượng Node đếm được.
        """
        dem = 0
        node_hien_tai = node_dau
        while node_hien_tai is not None:
            dem += 1
            node_hien_tai = node_hien_tai.next
        return dem

    # ============================================================
    # TIỆN ÍCH
    # ============================================================

    def chuyen_thanh_danh_sach(self):
        """
        Chuyển đổi danh sách liên kết đôi thành danh sách (list) Python
        để dễ dàng serialize thành JSON gửi về giao diện.

        Trả về:
            list: Danh sách chứa các từ điển (dict) mô tả từng mặt hàng.
        """
        ket_qua = []
        node_hien_tai = self.head

        while node_hien_tai is not None:
            du_lieu = node_hien_tai.data
            if hasattr(du_lieu, 'chuyen_thanh_dict'):
                ket_qua.append(du_lieu.chuyen_thanh_dict())
            else:
                ket_qua.append(str(du_lieu))
            node_hien_tai = node_hien_tai.next

        return ket_qua

    def __str__(self):
        """Trả về chuỗi mô tả toàn bộ danh sách."""
        danh_sach = []
        node_hien_tai = self.head
        while node_hien_tai is not None:
            danh_sach.append(str(node_hien_tai.data))
            node_hien_tai = node_hien_tai.next
        return ' <-> '.join(danh_sach)
