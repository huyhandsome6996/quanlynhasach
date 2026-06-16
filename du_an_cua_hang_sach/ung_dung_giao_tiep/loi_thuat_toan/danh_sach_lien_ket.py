"""
Module cấu trúc dữ liệu Danh sách liên kết đôi (Doubly Linked List).
Tự cài đặt thay vì dùng list có sẵn của Python để hiểu sâu về con trỏ/tham chiếu.
"""


class Node:
    """
    Lớp Node - đơn vị cơ bản của danh sách liên kết đôi.
    Chứa dữ liệu (đối tượng sản phẩm) và hai liên kết next, prev.
    """

    def __init__(self, data):
        self.data = data
        self.truoc = None  # Con trỏ tới node trước (prev)
        self.next = None   # Con trỏ tới node sau (next)

    def __str__(self):
        return str(self.data)


class DoublyLinkedList:
    """
    Lớp Danh sách liên kết đôi - quản lý dữ liệu thay cho list Python.
    Cài đặt các phương thức: insert_tail, remove_node, search_by_id, sort_list.
    """

    def __init__(self):
        self.head = None    # Con trỏ đầu danh sách
        self.cuoi = None    # Con trỏ cuối danh sách
        self.so_luong = 0   # Đếm số phần tử

    # ==================== THÊM PHẦN TỬ ====================

    # ============================================================
    # THÊM PHẦN TỬ
    # ============================================================

    def them_vao_cuoi(self, data):
        """
        insert_tail() - Thêm một phần tử mới vào cuối danh sách.
        Độ phức tạp: O(1) nhờ duy trì con trỏ cuối.
        """
        node_moi = Node(data)
        if self.head is None:
            self.head = node_moi
            self.cuoi = node_moi
        else:
            self.cuoi.next = node_moi
            node_moi.truoc = self.cuoi
            self.cuoi = node_moi
        self.so_luong += 1

    # ==================== XÓA PHẦN TỬ ====================

    def xoa_node(self, ma_so):
        """
        remove_node() - Xóa một node theo mã số.
        Duyệt tuần tự và cập nhật liên kết prev/next.
        Trả về True nếu xóa thành công, False nếu không tìm thấy.
        """
        node_hien_tai = self.head
        while node_hien_tai is not None:
            if hasattr(node_hien_tai.data, 'ma_so') and node_hien_tai.data.ma_so == ma_so:
                if node_hien_tai == self.head:
                    self.head = node_hien_tai.next
                    if self.head is not None:
                        self.head.truoc = None  # Node đầu mới không có truoc
                    else:
                        self.cuoi = None
                elif node_hien_tai == self.cuoi:
                    self.cuoi = node_hien_tai.truoc
                    self.cuoi.next = None
                else:
                    # Bỏ qua Node hiện tại bằng cách nối Node trước và Node sau
                    node_hien_tai.truoc.next = node_hien_tai.next
                    node_hien_tai.next.truoc = node_hien_tai.truoc
                self.so_luong -= 1
                return True
            node_hien_tai = node_hien_tai.next
        return False

    # ==================== TÌM KIẾM ====================

    def tim_theo_ma_so(self, ma_so):
        """
        search_by_id() - Tìm kiếm một sản phẩm theo Mã số (ID).
        Trả về đối tượng sản phẩm nếu tìm thấy, None nếu không.
        Độ phức tạp: O(n).
        """
        node_hien_tai = self.head
        while node_hien_tai is not None:
            if hasattr(node_hien_tai.data, 'ma_so') and node_hien_tai.data.ma_so == ma_so:
                return node_hien_tai.data
            node_hien_tai = node_hien_tai.next
        return None

    def tim_kiem(self, tu_khoa):
        """
        Tìm kiếm theo Tên sản phẩm (substring match, case-insensitive).
        Trả về danh sách (list) các đối tượng phù hợp.
        """
        ket_qua = []
        node_hien_tai = self.head
        tu_khoa_chu_thuong = tu_khoa.lower()
        while node_hien_tai is not None:
            if hasattr(node_hien_tai.data, 'ten_san_pham'):
                ten_chu_thuong = node_hien_tai.data.ten_san_pham.lower()
                if tu_khoa_chu_thuong in ten_chu_thuong:
                    ket_qua.append(node_hien_tai.data)
            node_hien_tai = node_hien_tai.next
        return ket_qua

    def tim_theo_the_loai(self, the_loai):
        """
        Tìm kiếm theo Thể loại (loại hàng).
        Trả về danh sách các sản phẩm thuộc thể loại được chỉ định.
        """
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
        Tìm kiếm nâng cao: tìm đồng thời theo Mã số, Tên, và Thể loại.
        Trả về danh sách kết quả không trùng lặp.
        """
        ket_qua = []
        ma_da_them = set()
        node_hien_tai = self.head
        tu_khoa_lower = tu_khoa.lower()
        while node_hien_tai is not None:
            data = node_hien_tai.data
            da_khop = False
            if hasattr(data, 'ma_so') and tu_khoa_lower in data.ma_so.lower():
                da_khop = True
            if not da_khop and hasattr(data, 'ten_san_pham') and tu_khoa_lower in data.ten_san_pham.lower():
                da_khop = True
            if not da_khop and hasattr(data, 'loai_hang') and tu_khoa_lower in data.loai_hang.lower():
                da_khop = True
            if da_khop and data.ma_so not in ma_da_them:
                ket_qua.append(data)
                ma_da_them.add(data.ma_so)
            node_hien_tai = node_hien_tai.next
        return ket_qua

    # ==================== CẬP NHẬT ====================

    def cap_nhat_node(self, ma_so, du_lieu_moi):
        """
        Cập nhật thông tin một node theo mã số.
        du_lieu_moi là dict chứa các trường cần cập nhật.
        Trả về đối tượng đã cập nhật nếu thành công, None nếu không tìm thấy.
        """
        node_hien_tai = self.head
        while node_hien_tai is not None:
            if hasattr(node_hien_tai.data, 'ma_so') and node_hien_tai.data.ma_so == ma_so:
                doi_tuong = node_hien_tai.data
                for thuoc_tinh, gia_tri in du_lieu_moi.items():
                    if hasattr(doi_tuong, thuoc_tinh):
                        setattr(doi_tuong, thuoc_tinh, gia_tri)
                return doi_tuong
            node_hien_tai = node_hien_tai.next
        return None

    # ==================== THỐNG KÊ ====================

    def thong_ke(self):
        """
        Thống kê dữ liệu: tổng số lượng, mặt hàng đắt nhất/rẻ nhất,
        cảnh báo hàng sắp hết (tồn kho <= 5), thống kê theo loại hàng.
        Trả về dict chứa tất cả thông tin thống kê.
        """
        if self.so_luong == 0:
            return {
                'tong_so': 0,
                'dat_nhat': None,
                're_nhat': None,
                'sap_het_hang': [],
                'theo_loai': {},
                'tong_gia_tri_kho': 0,
                'tong_ton_kho': 0
            }

        dat_nhat = None
        re_nhat = None
        gia_cao_nhat = -1
        gia_thap_nhat = float('inf')
        sap_het_hang = []
        theo_loai = {}
        tong_gia_tri_kho = 0
        tong_ton_kho = 0

        node_hien_tai = self.head
        while node_hien_tai is not None:
            data = node_hien_tai.data
            if hasattr(data, 'tinh_gia_ban'):
                gia_ban = data.tinh_gia_ban()
                if gia_ban > gia_cao_nhat:
                    gia_cao_nhat = gia_ban
                    dat_nhat = data
                if gia_ban < gia_thap_nhat:
                    gia_thap_nhat = gia_ban
                    re_nhat = data

            if hasattr(data, 'ton_kho'):
                tong_ton_kho += data.ton_kho
                tong_gia_tri_kho += data.gia_co_ban * data.ton_kho
                if data.ton_kho <= 5:
                    sap_het_hang.append(data)

            if hasattr(data, 'loai_hang'):
                loai = data.loai_hang
                if loai not in theo_loai:
                    theo_loai[loai] = {'so_luong': 0, 'tong_ton': 0}
                theo_loai[loai]['so_luong'] += 1
                theo_loai[loai]['tong_ton'] += data.ton_kho

            node_hien_tai = node_hien_tai.next

        return {
            'tong_so': self.so_luong,
            'dat_nhat': dat_nhat.chuyen_thanh_dict() if dat_nhat else None,
            're_nhat': re_nhat.chuyen_thanh_dict() if re_nhat else None,
            'sap_het_hang': [item.chuyen_thanh_dict() for item in sap_het_hang],
            'theo_loai': theo_loai,
            'tong_gia_tri_kho': tong_gia_tri_kho,
            'tong_ton_kho': tong_ton_kho
        }

    # ==================== SẮP XẾP (MERGE SORT) ====================

    # ============================================================
    # SẮP XẾP - THUẬT TOÁN MERGE SORT
    # ============================================================

    def sap_xep_tron(self, tieu_chi='gia_ban'):
        """
        sort_list() - Sắp xếp danh sách liên kết bằng thuật toán Merge Sort.
        Hỗ trợ sắp xếp theo: gia_ban, ten_san_pham, ton_kho.
        Độ phức tạp: O(n log n).
        """
        # Danh sách rỗng hoặc chỉ có 1 phần tử → không cần sắp xếp
        if self.head is None or self.head.next is None:
            return
        nua_dau, nua_sau = self._chia_doi()
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
        ds_nua_dau.sap_xep_tron(tieu_chi)
        ds_nua_sau.sap_xep_tron(tieu_chi)
        self._tron(ds_nua_dau, ds_nua_sau, tieu_chi)

    def _chia_doi(self):
        """Chia danh sách liên kết thành 2 nửa bằng kỹ thuật fast/slow pointer."""
        con_tro_cham = self.head
        con_tro_nhanh = self.head
        while con_tro_nhanh.next is not None and con_tro_nhanh.next.next is not None:
            con_tro_cham = con_tro_cham.next
            con_tro_nhanh = con_tro_nhanh.next.next
        nua_dau = self.head
        nua_sau = con_tro_cham.next
        con_tro_cham.next = None   # Cắt liên kết giữa hai nửa
        if nua_sau is not None:
            nua_sau.truoc = None
        return (nua_dau, nua_sau)

    def _tron(self, ds_a, ds_b, tieu_chi):
        """Trộn hai danh sách đã sắp xếp thành một danh sách có thứ tự."""
        node_tam = Node(None)
        hien_tai = node_tam
        node_a = ds_a.head
        node_b = ds_b.head
        while node_a is not None and node_b is not None:
            # Lấy giá trị để so sánh
            gia_tri_a = self._lay_gia_tri(node_a.data, tieu_chi)
            gia_tri_b = self._lay_gia_tri(node_b.data, tieu_chi)
            if gia_tri_a <= gia_tri_b:
                hien_tai.next = node_a
                node_a.truoc = hien_tai
                node_a = node_a.next
            else:
                hien_tai.next = node_b
                node_b.truoc = hien_tai
                node_b = node_b.next
            hien_tai = hien_tai.next
        if node_a is not None:
            hien_tai.next = node_a
            node_a.truoc = hien_tai
            self.cuoi = ds_a.cuoi
        if node_b is not None:
            hien_tai.next = node_b
            node_b.truoc = hien_tai
            self.cuoi = ds_b.cuoi
        self.head = node_tam.next
        if self.head is not None:
            self.head.truoc = None

    def _lay_gia_tri(self, doi_tuong, tieu_chi):
        """Lấy giá trị so sánh từ đối tượng theo tiêu chí sắp xếp."""
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
        """Đếm số node từ node_dau đến cuối."""
        dem = 0
        node_hien_tai = node_dau
        while node_hien_tai is not None:
            dem += 1
            node_hien_tai = node_hien_tai.next
        return dem

    # ==================== TIỆN ÍCH ====================

    def chuyen_thanh_danh_sach(self):
        """Chuyển toàn bộ danh sách liên kết thành mảng dict để trả về JSON."""
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
        danh_sach = []
        node_hien_tai = self.head
        while node_hien_tai is not None:
            danh_sach.append(str(node_hien_tai.data))
            node_hien_tai = node_hien_tai.next
        return ' <-> '.join(danh_sach)

    def __len__(self):
        return self.so_luong