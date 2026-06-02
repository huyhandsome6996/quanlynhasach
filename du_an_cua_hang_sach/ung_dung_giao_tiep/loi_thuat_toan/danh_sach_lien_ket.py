"""
Tệp chứa cấu trúc dữ liệu Danh sách liên kết đôi (DoublyLinkedList)
và lớp Node (Mắt xích).

Quy tắc: Tên biến, tên hàm, chú thích sử dụng tiếng Việt.
Ngoại lệ: Các từ khóa cốt lõi của cấu trúc dữ liệu gồm Node, DoublyLinkedList, head, next, data.
"""


class Node:
    """
    Lớp Node (Mắt xích) - Đại diện cho một phần tử trong danh sách liên kết đôi.

    Thuộc tính:
        data: Biến lưu trữ đối tượng sản phẩm (Sách, Tạp chí, Báo giấy...).
        truoc: Con trỏ trỏ về Node phía trước nó.
        next: Con trỏ trỏ đến Node phía sau nó.
    """

    def __init__(self, data):
        """
        Khởi tạo một Node mới.

        Tham số:
            data: Đối tượng dữ liệu cần lưu trữ trong Node.
        """
        self.data = data
        self.truoc = None
        self.next = None

    def __str__(self):
        """Trả về chuỗi mô tả dữ liệu của Node."""
        return str(self.data)


class DoublyLinkedList:
    """
    Lớp DoublyLinkedList (Danh sách liên kết đôi) - Cấu trúc dữ liệu chính
    quản lý toàn bộ mặt hàng trong cửa hàng trên bộ nhớ RAM.

    Thuộc tính:
        head: Trỏ đến Node đầu tiên trong danh sách.
        cuoi: Trỏ đến Node cuối cùng trong danh sách.
        so_luong: Số lượng phần tử hiện có trong danh sách.
    """

    def __init__(self):
        """Khởi tạo danh sách liên kết đôi rỗng."""
        self.head = None
        self.cuoi = None
        self.so_luong = 0

    def them_vao_cuoi(self, data):
        """
        Thêm một phần tử mới vào cuối danh sách liên kết đôi.

        Tham số:
            data: Đối tượng dữ liệu cần thêm vào danh sách.
        """
        node_moi = Node(data)

        # Trường hợp danh sách đang rỗng
        if self.head is None:
            self.head = node_moi
            self.cuoi = node_moi
        else:
            # Nối Node mới vào sau Node cuối hiện tại
            self.cuoi.next = node_moi
            node_moi.truoc = self.cuoi
            self.cuoi = node_moi

        self.so_luong += 1

    def xoa_node(self, ma_so):
        """
        Xóa một Node khỏi danh sách dựa trên mã số mặt hàng.

        Tham số:
            ma_so: Mã số định danh duy nhất của mặt hàng cần xóa.

        Trả về:
            True nếu xóa thành công, False nếu không tìm thấy Node cần xóa.
        """
        node_hien_tai = self.head

        while node_hien_tai is not None:
            # So sánh mã số của dữ liệu trong Node với mã số cần tìm
            if hasattr(node_hien_tai.data, 'ma_so') and node_hien_tai.data.ma_so == ma_so:
                # Trường hợp Node cần xóa là Node đầu tiên
                if node_hien_tai == self.head:
                    self.head = node_hien_tai.next
                    if self.head is not None:
                        self.head.truoc = None
                    else:
                        # Danh sách chỉ có 1 phần tử, sau khi xóa thì danh sách rỗng
                        self.cuoi = None

                # Trường hợp Node cần xóa là Node cuối cùng
                elif node_hien_tai == self.cuoi:
                    self.cuoi = node_hien_tai.truoc
                    self.cuoi.next = None

                # Trường hợp Node cần xóa nằm ở giữa danh sách
                else:
                    node_hien_tai.truoc.next = node_hien_tai.next
                    node_hien_tai.next.truoc = node_hien_tai.truoc

                self.so_luong -= 1
                return True

            node_hien_tai = node_hien_tai.next

        return False

    def tim_kiem(self, tu_khoa):
        """
        Tìm kiếm các mặt hàng chứa từ khóa trong tên sản phẩm.
        Duyệt tuần tự qua các Node bằng con trỏ next.

        Tham số:
            tu_khoa: Chuỗi từ khóa cần tìm kiếm (không phân biệt hoa/thường).

        Trả về:
            Danh sách (list Python) các đối tượng dữ liệu thỏa mãn điều kiện.
        """
        ket_qua = []
        node_hien_tai = self.head
        tu_khoa_chu_thuong = tu_khoa.lower()

        while node_hien_tai is not None:
            # Tìm kiếm trong tên sản phẩm (không phân biệt hoa/thường)
            if hasattr(node_hien_tai.data, 'ten_san_pham'):
                ten_chu_thuong = node_hien_tai.data.ten_san_pham.lower()
                if tu_khoa_chu_thuong in ten_chu_thuong:
                    ket_qua.append(node_hien_tai.data)

            node_hien_tai = node_hien_tai.next

        return ket_qua

    def sap_xep_tron(self, tieu_chi='gia_ban'):
        """
        Sắp xếp danh sách liên kết đôi bằng thuật toán Sắp xếp trộn (Merge Sort).
        Thao tác trực tiếp trên các con trỏ next, truoc - KHÔNG dùng list.sort().

        Tham số:
            tieu_chi: Tiêu chí sắp xếp. Mặc định là 'gia_ban' (sắp xếp theo giá bán).
        """
        if self.head is None or self.head.next is None:
            return

        # Bước 1: Chia danh sách thành hai nửa
        nua_dau, nua_sau = self._chia_doi()

        # Bước 2: Đưa mỗi nửa vào một DoublyLinkedList tạm để gọi đệ quy
        ds_nua_dau = DoublyLinkedList()
        ds_nua_dau.head = nua_dau
        node_cuoi_dau = nua_dau
        while node_cuoi_dau.next is not None:
            node_cuoi_dau = node_cuoi_dau.next
        ds_nua_dau.cuoi = node_cuoi_dau
        ds_nua_dau.so_luong = self._dem_node(nua_dau)

        ds_nua_sau = DoublyLinkedList()
        ds_nua_sau.head = nua_sau
        node_cuoi_sau = nua_sau
        while node_cuoi_sau.next is not None:
            node_cuoi_sau = node_cuoi_sau.next
        ds_nua_sau.cuoi = node_cuoi_sau
        ds_nua_sau.so_luong = self._dem_node(nua_sau)

        # Bước 3: Gọi đệ quy sắp xếp từng nửa
        ds_nua_dau.sap_xep_tron(tieu_chi)
        ds_nua_sau.sap_xep_tron(tieu_chi)

        # Bước 4: Trộn hai nửa đã sắp xếp
        self._tron(ds_nua_dau, ds_nua_sau, tieu_chi)

    def _chia_doi(self):
        """
        Chia danh sách liên kết đôi thành hai nửa bằng kỹ thuật con trỏ nhanh/chậm.

        Trả về:
            Tuple (nua_dau, nua_sau) - Node đầu của mỗi nửa.
        """
        con_tro_cham = self.head
        con_tro_nhanh = self.head

        while con_tro_nhanh.next is not None and con_tro_nhanh.next.next is not None:
            con_tro_cham = con_tro_cham.next
            con_tro_nhanh = con_tro_nhanh.next.next

        # Cắt đôi danh sách
        nua_dau = self.head
        nua_sau = con_tro_cham.next
        con_tro_cham.next = None
        if nua_sau is not None:
            nua_sau.truoc = None

        return nua_dau, nua_sau

    def _tron(self, ds_a, ds_b, tieu_chi):
        """
        Trộn hai danh sách liên kết đôi đã sắp xếp thành một danh sách duy nhất.
        Thao tác trực tiếp trên các con trỏ next, truoc.

        Tham số:
            ds_a: Danh sách liên kết đôi thứ nhất đã sắp xếp.
            ds_b: Danh sách liên kết đôi thứ hai đã sắp xếp.
            tieu_chi: Tiêu chí so sánh khi trộn.
        """
        node_tam = Node(None)  # Node tạm thời để dễ thao tác
        hien_tai = node_tam

        node_a = ds_a.head
        node_b = ds_b.head

        while node_a is not None and node_b is not None:
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

        # Nối phần còn lại của danh sách A
        if node_a is not None:
            hien_tai.next = node_a
            node_a.truoc = hien_tai
            self.cuoi = ds_a.cuoi

        # Nối phần còn lại của danh sách B
        if node_b is not None:
            hien_tai.next = node_b
            node_b.truoc = hien_tai
            self.cuoi = ds_b.cuoi

        # Cập nhật head và xóa liên kết của Node tạm
        self.head = node_tam.next
        if self.head is not None:
            self.head.truoc = None

    def _lay_gia_tri(self, doi_tuong, tieu_chi):
        """
        Lấy giá trị của đối tượng theo tiêu chí tương ứng để so sánh.

        Tham số:
            doi_tuong: Đối tượng mặt hàng cần lấy giá trị.
            tieu_chi: Chuỗi tiêu chí ('gia_ban', 'ten_san_pham', 'ton_kho').

        Trả về:
            Giá trị tương ứng với tiêu chí.
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
            Số lượng Node đếm được.
        """
        dem = 0
        node_hien_tai = node_dau
        while node_hien_tai is not None:
            dem += 1
            node_hien_tai = node_hien_tai.next
        return dem

    def chuyen_thanh_danh_sach(self):
        """
        Chuyển đổi danh sách liên kết đôi thành danh sách (list) Python
        để dễ dàng serialize thành JSON gửi về giao diện.

        Trả về:
            Danh sách (list) chứa các từ điển (dict) mô tả từng mặt hàng.
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
