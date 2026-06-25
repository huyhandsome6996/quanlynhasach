"""
Tệp danh_sach_lien_ket.py — Cài đặt Danh sách liên kết ĐÔI (Doubly Linked List)
=============================================================================

Tự cài đặt (KHÔNG dùng list Python) để hiểu sâu về con trỏ/tham chiếu,
đúng yêu cầu của môn Lập trình Nâng cao.

Mỗi Node có 2 con trỏ:
    truoc : trỏ tới Node phía trước.
    next  : trỏ tới Node phía sau.

→ Có thể duyệt tiến/lùi, chèn/xóa O(1) khi đã có Node tham chiếu.

Bao gồm:
    - Lớp Node
    - Lớp DoublyLinkedList với:
        * them_vao_cuoi, xoa_node, cap_nhat_node  (CRUD)
        * tim_theo_ma_so, tim_kiem, tim_theo_the_loai, tim_kiem_nang_cao
        * thong_ke
        * sap_xep_tron (Merge Sort O(n log n))
        * chuyen_thanh_danh_sach (đổi sang list Python để trả JSON)
"""


class Node:
    """
    Lớp Node — đơn vị cơ bản của danh sách liên kết đôi.

    Mỗi Node chứa:
        data   : Dữ liệu thực tế (thường là đối tượng MatHang).
        truoc  : Con trỏ tới Node phía trước (Python gọi là tham chiếu).
        next   : Con trỏ tới Node phía sau.

    Minh họa:
        None ← [Node A] ⇄ [Node B] ⇄ [Node C] → None
                head                         cuoi
    """

    def __init__(self, data):
        """Khởi tạo Node với data truyền vào, truoc = next = None."""
        self.data = data        # Dữ liệu (đối tượng sản phẩm).
        self.truoc = None       # Chưa liên kết Node trước.
        self.next = None        # Chưa liên kết Node sau.

    def __str__(self):
        """In Node → in dữ liệu bên trong (gọi str(data))."""
        return str(self.data)


class DoublyLinkedList:
    """
    Lớp DoublyLinkedList — quản lý toàn bộ danh sách liên kết đôi.

    Thuộc tính:
        head      : Trỏ tới Node đầu danh sách (None nếu rỗng).
        cuoi      : Trỏ tới Node cuối danh sách (None nếu rỗng).
        so_luong  : Số Node hiện có (để tránh phải duyệt mỗi lần đếm).

    Phương thức chính (xem docstring từng hàm):
        them_vao_cuoi, xoa_node, cap_nhat_node, tim_theo_ma_so, tim_kiem,
        tim_theo_the_loai, tim_kiem_nang_cao, thong_ke, sap_xep_tron,
        chuyen_thanh_danh_sach.
    """

    def __init__(self):
        """Khởi tạo danh sách rỗng."""
        self.head = None        # Chưa có Node đầu.
        self.cuoi = None        # Chưa có Node cuối.
        self.so_luong = 0       # Đếm số phần tử.

    # ============================================================
    # THÊM PHẦN TỬ
    # ============================================================

    def them_vao_cuoi(self, data):
        """
        Thêm một phần tử mới vào CUỐI danh sách.

        Độ phức tạp: O(1) nhờ duy trì sẵn con trỏ `cuoi`.
        Nếu chỉ có `head` mà không có `cuoi`, sẽ phải duyệt O(n) để tìm cuối.
        """
        node_moi = Node(data)               # Bọc dữ liệu vào Node.

        if self.head is None:               # Trường hợp danh sách rỗng.
            self.head = node_moi            # Node mới là đầu.
            self.cuoi = node_moi            # Đồng thời cũng là cuối.
        else:                               # Trường hợp đã có phần tử.
            self.cuoi.next = node_moi       # Nối Node mới sau Node cuối.
            node_moi.truoc = self.cuoi      # Node mới trỏ ngược lại.
            self.cuoi = node_moi            # Cập nhật lại cuối.

        self.so_luong += 1                  # Tăng bộ đếm.

    # ============================================================
    # XÓA PHẦN TỬ
    # ============================================================

    def xoa_node(self, ma_so):
        """
        Xóa Node đầu tiên có data.ma_so == ma_so.

        Trả về: True nếu xóa được, False nếu không tìm thấy.
        Độ phức tạp: O(n) do phải duyệt tìm.
        """
        node_hien_tai = self.head                       # Bắt đầu từ đầu.
        while node_hien_tai is not None:                # Lặp đến hết.
            # Kiểm tra Node hiện tại có data.ma_so khớp không.
            if hasattr(node_hien_tai.data, 'ma_so') and node_hien_tai.data.ma_so == ma_so:

                # Trường hợp 1: Node cần xóa chính là Node đầu.
                if node_hien_tai == self.head:
                    self.head = node_hien_tai.next      # Đẩy head sang Node kế.
                    if self.head is not None:
                        self.head.truoc = None          # Node đầu mới không có truoc.
                    else:
                        self.cuoi = None                # Nếu rỗng → reset cả cuoi.

                # Trường hợp 2: Node cần xóa là Node cuối.
                elif node_hien_tai == self.cuoi:
                    self.cuoi = node_hien_tai.truoc     # Lùi cuoi về Node trước.
                    self.cuoi.next = None               # Cắt liên kết tới Node bị xóa.

                # Trường hợp 3: Node ở giữa → nối prev và next bỏ qua Node hiện tại.
                else:
                    node_hien_tai.truoc.next = node_hien_tai.next
                    node_hien_tai.next.truoc = node_hien_tai.truoc

                self.so_luong -= 1
                return True

            node_hien_tai = node_hien_tai.next          # Tiến sang Node kế.
        return False                                   # Duyệt hết mà không thấy.

    # ============================================================
    # TÌM KIẾM
    # ============================================================

    def tim_theo_ma_so(self, ma_so):
        """Tìm chính xác theo Mã số. Trả về đối tượng hoặc None. O(n)."""
        node_hien_tai = self.head
        while node_hien_tai is not None:
            if hasattr(node_hien_tai.data, 'ma_so') and node_hien_tai.data.ma_so == ma_so:
                return node_hien_tai.data
            node_hien_tai = node_hien_tai.next
        return None

    def tim_kiem(self, tu_khoa):
        """
        Tìm kiếm theo Tên sản phẩm — so khớp CHỨA (substring),
        không phân biệt HOA/thường.
        """
        ket_qua = []
        node_hien_tai = self.head
        tu_khoa_chu_thuong = tu_khoa.lower()           # Chuẩn hoá từ khóa.
        while node_hien_tai is not None:
            if hasattr(node_hien_tai.data, 'ten_san_pham'):
                ten_chu_thuong = node_hien_tai.data.ten_san_pham.lower()
                if tu_khoa_chu_thuong in ten_chu_thuong:
                    ket_qua.append(node_hien_tai.data)
            node_hien_tai = node_hien_tai.next
        return ket_qua

    def tim_theo_the_loai(self, the_loai):
        """Tìm theo loại hàng (Sách/Tạp chí/...). Trả về list các đối tượng."""
        ket_qua = []
        node_hien_tai = self.head
        the_loai_chu_thuong = the_loai.lower()
        while node_hien_tai is not None:
            if hasattr(node_hien_tai.data, 'loai_hang'):
                if the_loai_chu_thuong in node_hien_tai.data.loai_hang.lower():
                    ket_qua.append(node_hien_tai.data)
            node_hien_tai = node_hien_tai.next
        return ket_qua

    def tim_kiem_nang_cao(self, tu_khoa):
        """
        Tìm kiếm nâng cao: tìm đồng thời theo MÃ SỐ, TÊN, và LOẠI HÀNG.
        Sử dụng set để tránh trùng lặp kết quả.
        """
        ket_qua = []
        ma_da_them = set()                             # Set các mã đã thêm.
        node_hien_tai = self.head
        tu_khoa_lower = tu_khoa.lower()
        while node_hien_tai is not None:
            data = node_hien_tai.data
            da_khop = False
            # Kiểm tra khớp theo mã số.
            if hasattr(data, 'ma_so') and tu_khoa_lower in data.ma_so.lower():
                da_khop = True
            # Nếu chưa khớp → kiểm tra theo tên.
            if not da_khop and hasattr(data, 'ten_san_pham') and tu_khoa_lower in data.ten_san_pham.lower():
                da_khop = True
            # Nếu vẫn chưa khớp → kiểm tra theo loại hàng.
            if not da_khop and hasattr(data, 'loai_hang') and tu_khoa_lower in data.loai_hang.lower():
                da_khop = True
            # Nếu khớp và chưa thêm → thêm vào kết quả.
            if da_khop and data.ma_so not in ma_da_them:
                ket_qua.append(data)
                ma_da_them.add(data.ma_so)
            node_hien_tai = node_hien_tai.next
        return ket_qua

    # ============================================================
    # CẬP NHẬT
    # ============================================================

    def cap_nhat_node(self, ma_so, du_lieu_moi):
        """
        Cập nhật các trường của Node có ma_so tương ứng.
        du_lieu_moi là dict {ten_truong: gia_tri_moi}.
        Trả về đối tượng đã cập nhật, hoặc None nếu không tìm thấy.
        """
        node_hien_tai = self.head
        while node_hien_tai is not None:
            if hasattr(node_hien_tai.data, 'ma_so') and node_hien_tai.data.ma_so == ma_so:
                doi_tuong = node_hien_tai.data
                # Lặp từng cặp (tên_trường, giá_trị) trong dict và gán vào đối tượng.
                for thuoc_tinh, gia_tri in du_lieu_moi.items():
                    if hasattr(doi_tuong, thuoc_tinh):
                        setattr(doi_tuong, thuoc_tinh, gia_tri)
                return doi_tuong
            node_hien_tai = node_hien_tai.next
        return None

    # ============================================================
    # THỐNG KÊ
    # ============================================================

    def thong_ke(self):
        """
        Thống kê toàn bộ danh sách:
            - tong_so            : tổng số mặt hàng
            - dat_nhat / re_nhat : mặt hàng có giá bán cao/thấp nhất
            - sap_het_hang       : danh sách hàng tồn kho ≤ 5
            - theo_loai          : số lượng + tổng tồn kho theo từng loại
            - tong_gia_tri_kho   : tổng giá trị hàng trong kho
            - tong_ton_kho       : tổng số sản phẩm tồn
        """
        if self.so_luong == 0:                         # Trường hợp danh sách rỗng.
            return {
                'tong_so': 0,
                'dat_nhat': None,
                're_nhat': None,
                'sap_het_hang': [],
                'theo_loai': {},
                'tong_gia_tri_kho': 0,
                'tong_ton_kho': 0
            }

        # Khởi tạo các biến tích lũy.
        dat_nhat = None
        re_nhat = None
        gia_cao_nhat = -1                                # Khởi tạo âm để mọi giá đều lớn hơn.
        gia_thap_nhat = float('inf')                     # Vô cực để mọi giá đều nhỏ hơn.
        sap_het_hang = []
        theo_loai = {}
        tong_gia_tri_kho = 0
        tong_ton_kho = 0

        # Duyệt qua từng Node để tích lũy thống kê.
        node_hien_tai = self.head
        while node_hien_tai is not None:
            data = node_hien_tai.data
            if hasattr(data, 'tinh_gia_ban'):
                gia_ban = data.tinh_gia_ban()
                # Cập nhật đắt nhất.
                if gia_ban > gia_cao_nhat:
                    gia_cao_nhat = gia_ban
                    dat_nhat = data
                # Cập nhật rẻ nhất.
                if gia_ban < gia_thap_nhat:
                    gia_thap_nhat = gia_ban
                    re_nhat = data

            if hasattr(data, 'ton_kho'):
                tong_ton_kho += data.ton_kho
                tong_gia_tri_kho += data.gia_co_ban * data.ton_kho
                # Cảnh báo hàng sắp hết khi tồn kho ≤ 5.
                if data.ton_kho <= 5:
                    sap_het_hang.append(data)

            if hasattr(data, 'loai_hang'):
                loai = data.loai_hang
                # Nếu loại chưa có trong dict → khởi tạo.
                if loai not in theo_loai:
                    theo_loai[loai] = {'so_luong': 0, 'tong_ton': 0}
                theo_loai[loai]['so_luong'] += 1
                theo_loai[loai]['tong_ton'] += data.ton_kho

            node_hien_tai = node_hien_tai.next

        # Trả về dict kết quả — các đối tượng được chuyển thành dict để JSON hóa.
        return {
            'tong_so': self.so_luong,
            'dat_nhat': dat_nhat.chuyen_thanh_dict() if dat_nhat else None,
            're_nhat': re_nhat.chuyen_thanh_dict() if re_nhat else None,
            'sap_het_hang': [item.chuyen_thanh_dict() for item in sap_het_hang],
            'theo_loai': theo_loai,
            'tong_gia_tri_kho': tong_gia_tri_kho,
            'tong_ton_kho': tong_ton_kho
        }

    # ============================================================
    # SẮP XẾP - THUẬT TOÁN MERGE SORT (ĐỆ QUY)
    # ============================================================

    def sap_xep_tron(self, tieu_chi='gia_ban'):
        """
        Sắp xếp danh sách bằng thuật toán Merge Sort — O(n log n).

        Ý tưởng Merge Sort:
          1. Chia danh sách làm 2 nửa (chia để trị).
          2. Đệ quy sắp xếp từng nửa.
          3. Trộn 2 nửa đã sắp xếp thành danh sách kết quả.

        Hỗ trợ 3 tiêu chí: 'gia_ban', 'ten_san_pham', 'ton_kho'.
        """
        # Điều kiện dừng: 0 hoặc 1 phần tử → đã "sắp xếp" sẵn.
        if self.head is None or self.head.next is None:
            return

        # 1. Chia đôi danh sách thành 2 nửa.
        nua_dau, nua_sau = self._chia_doi()

        # 2. Bọc nửa đầu thành DoublyLinkedList để đệ quy.
        ds_nua_dau = DoublyLinkedList()
        ds_nua_dau.head = nua_dau
        # Tìm Node cuối của nửa đầu (vì _chia_doi chỉ trả head).
        node_cuoi_dau = nua_dau
        while node_cuoi_dau.next is not None:
            node_cuoi_dau = node_cuoi_dau.next
        ds_nua_dau.cuoi = node_cuoi_dau
        ds_nua_dau.so_luong = self._dem_node(nua_dau)

        # Tương tự cho nửa sau.
        ds_nua_sau = DoublyLinkedList()
        ds_nua_sau.head = nua_sau
        node_cuoi_sau = nua_sau
        while node_cuoi_sau.next is not None:
            node_cuoi_sau = node_cuoi_sau.next
        ds_nua_sau.cuoi = node_cuoi_sau
        ds_nua_sau.so_luong = self._dem_node(nua_sau)

        # Đệ quy sắp xếp từng nửa.
        ds_nua_dau.sap_xep_tron(tieu_chi)
        ds_nua_sau.sap_xep_tron(tieu_chi)

        # 3. Trộn 2 nửa đã sắp xếp vào lại self.
        self._tron(ds_nua_dau, ds_nua_sau, tieu_chi)

    def _chia_doi(self):
        """
        Chia danh sách thành 2 nửa bằng kỹ thuật Fast/Slow pointer:
            - con_tro_cham  đi 1 bước mỗi lần.
            - con_tro_nhanh đi 2 bước mỗi lần.
        Khi con_tro_nhanh tới cuối → con_tro_cham đang ở giữa.
        """
        con_tro_cham = self.head
        con_tro_nhanh = self.head
        # Lưu ý: kiểm tra next.next để không bị vượt quá cuối.
        while con_tro_nhanh.next is not None and con_tro_nhanh.next.next is not None:
            con_tro_cham = con_tro_cham.next
            con_tro_nhanh = con_tro_nhanh.next.next
        # Tách 2 nửa.
        nua_dau = self.head
        nua_sau = con_tro_cham.next
        con_tro_cham.next = None                # Cắt liên kết nửa đầu ↔ nửa sau.
        if nua_sau is not None:
            nua_sau.truoc = None                # Nửa sau không còn prev.
        return (nua_dau, nua_sau)

    def _tron(self, ds_a, ds_b, tieu_chi):
        """
        Trộn 2 danh sách A và B (đã sắp xếp) thành 1 danh sách cũng sắp xếp.

        Dùng Node tạm (Node(None)) làm điểm xuất phát, sau đó so sánh từng
        cặp Node đầu của A và B để lấy Node nhỏ hơn gắn vào kết quả.
        """
        node_tam = Node(None)                   # Node giả để dễ code.
        hien_tai = node_tam                     # Con trỏ xây danh sách kết quả.
        node_a = ds_a.head
        node_b = ds_b.head

        # So sánh từng cặp Node đầu của A và B.
        while node_a is not None and node_b is not None:
            gia_tri_a = self._lay_gia_tri(node_a.data, tieu_chi)
            gia_tri_b = self._lay_gia_tri(node_b.data, tieu_chi)
            # Lấy Node có giá trị nhỏ hơn gắn vào kết quả.
            if gia_tri_a <= gia_tri_b:
                hien_tai.next = node_a
                node_a.truoc = hien_tai
                node_a = node_a.next
            else:
                hien_tai.next = node_b
                node_b.truoc = hien_tai
                node_b = node_b.next
            hien_tai = hien_tai.next

        # Một trong hai danh sách còn sót → gắn toàn bộ vào cuối kết quả.
        if node_a is not None:
            hien_tai.next = node_a
            node_a.truoc = hien_tai
            self.cuoi = ds_a.cuoi               # Cập nhật cuối của danh sách ghép.
        if node_b is not None:
            hien_tai.next = node_b
            node_b.truoc = hien_tai
            self.cuoi = ds_b.cuoi

        # Bỏ Node tạm và đặt lại head mới.
        self.head = node_tam.next
        if self.head is not None:
            self.head.truoc = None              # Head mới không có prev.

    def _lay_gia_tri(self, doi_tuong, tieu_chi):
        """Lấy giá trị để so sánh theo tiêu chí (gia_ban / ten_san_pham / ton_kho)."""
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
        """Đếm số Node từ node_dau đến cuối (dùng khi chia đôi)."""
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
        Đổi danh sách liên kết thành list Python các dict —
        dùng khi trả về JSON cho frontend.
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
        """In danh sách theo dạng: A <-> B <-> C."""
        danh_sach = []
        node_hien_tai = self.head
        while node_hien_tai is not None:
            danh_sach.append(str(node_hien_tai.data))
            node_hien_tai = node_hien_tai.next
        return ' <-> '.join(danh_sach)

    def __len__(self):
        """Cho phép dùng len(ds) — trả về so_luong."""
        return self.so_luong
