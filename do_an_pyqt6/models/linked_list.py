# ================================================================
# 👤 PHỤ TRÁCH: HỒ QUANG HUY
# ----------------------------------------------------------------
# 📚 KIẾN THỨC CẦN HỌC ĐI THI:
#    1. Danh sách liên kết ĐÔI (Doubly Linked List) - con trỏ trước/sau
#    2. Thao tác: thêm cuối, xóa theo mã, tìm kiếm, duyệt
#    3. Thuật toán MERGE SORT (đệ quy) trên Linked List
#    4. Kỹ thuật 2 con trỏ (nhanh/chậm) để tìm điểm giữa
# ----------------------------------------------------------------
# 📝 NỘI DUNG FILE:
#    Cài đặt cấu trúc Node + lớp DanhSachLienKetDoi. Đây là xương
#    sống của chương trình: mọi sản phẩm đều được lưu trong cấu trúc
#    này trên RAM trước khi ghi xuống SQLite.
# ================================================================

# Cài đặt cấu trúc Node cho Danh sách liên kết đôi
class Nut:
    def __init__(self, du_lieu):
        self.du_lieu = du_lieu
        self.truoc = None # Con trỏ trỏ về nút trước
        self.sau = None   # Con trỏ trỏ tới nút sau

# Cài đặt Danh sách liên kết đôi (Doubly Linked List)
class DanhSachLienKetDoi:
    def __init__(self):
        self.dau = None # Head
        self.cuoi = None # Tail
        self.so_luong = 0

    def them_vao_cuoi(self, du_lieu):
        nut_moi = Nut(du_lieu)
        if self.dau is None: # Danh sách trống
            self.dau = nut_moi
            self.cuoi = nut_moi
        else:
            self.cuoi.sau = nut_moi
            nut_moi.truoc = self.cuoi
            self.cuoi = nut_moi
        self.so_luong += 1

    def xoa_nut_theo_ma(self, ma_so):
        hien_tai = self.dau
        while hien_tai is not None:
            if hien_tai.du_lieu.ma_so == ma_so:
                # Xóa nút hiện tại khỏi liên kết
                if hien_tai.truoc is not None:
                    hien_tai.truoc.sau = hien_tai.sau
                else: # Nếu nó là nút đầu
                    self.dau = hien_tai.sau

                if hien_tai.sau is not None:
                    hien_tai.sau.truoc = hien_tai.truoc
                else: # Nếu nó là nút cuối
                    self.cuoi = hien_tai.truoc
                
                self.so_luong -= 1
                return True
            hien_tai = hien_tai.sau
        return False

    def tim_kiem_theo_ma(self, ma_so):
        hien_tai = self.dau
        while hien_tai is not None:
            if hien_tai.du_lieu.ma_so.lower() == ma_so.lower():
                return hien_tai.du_lieu
            hien_tai = hien_tai.sau
        return None

    def duyet_danh_sach(self):
        """Trả về một list Python thông thường ĐỂ HIỂN THỊ LÊN GIAO DIỆN"""
        ket_qua = []
        hien_tai = self.dau
        while hien_tai is not None:
            ket_qua.append(hien_tai.du_lieu)
            hien_tai = hien_tai.sau
        return ket_qua

    def xoa_tat_ca(self):
        self.dau = None
        self.cuoi = None
        self.so_luong = 0

    # ========================================================
    # THUẬT TOÁN MERGE SORT TRÊN DANH SÁCH LIÊN KẾT ĐÔI
    # ========================================================
    def sap_xep(self, tieu_chi="gia_ban", tang_dan=True):
        if self.dau is None or self.dau.sau is None:
            return # Không cần sắp xếp nếu mảng có 0 hoặc 1 phần tử
        
        self.dau = self._merge_sort(self.dau, tieu_chi, tang_dan)
        
        # Cập nhật lại con trỏ `cuoi` (tail)
        hien_tai = self.dau
        while hien_tai is not None and hien_tai.sau is not None:
            hien_tai = hien_tai.sau
        self.cuoi = hien_tai

    def _chia_doi(self, dau):
        # Kỹ thuật dùng 2 con trỏ (nhanh và chậm) để tìm điểm giữa
        nhanh = dau
        cham = dau
        while nhanh.sau is not None and nhanh.sau.sau is not None:
            nhanh = nhanh.sau.sau
            cham = cham.sau
        
        giua = cham.sau
        cham.sau = None # Cắt đôi danh sách
        return giua

    def _merge_sort(self, dau, tieu_chi, tang_dan):
        # Điều kiện dừng
        if dau is None or dau.sau is None:
            return dau

        # Chia
        giua = self._chia_doi(dau)
        
        # Gọi đệ quy
        trai = self._merge_sort(dau, tieu_chi, tang_dan)
        phai = self._merge_sort(giua, tieu_chi, tang_dan)

        # Trộn
        return self._tron(trai, phai, tieu_chi, tang_dan)

    def _tron(self, trai, phai, tieu_chi, tang_dan):
        if trai is None: return phai
        if phai is None: return trai

        # Lấy giá trị để so sánh bằng hàm getattr
        gt_trai = getattr(trai.du_lieu, tieu_chi)
        gt_phai = getattr(phai.du_lieu, tieu_chi)

        # Tránh lỗi phân biệt chữ hoa / chữ thường khi xếp theo tên
        if isinstance(gt_trai, str): gt_trai = gt_trai.lower()
        if isinstance(gt_phai, str): gt_phai = gt_phai.lower()

        if tang_dan:
            dk = gt_trai <= gt_phai
        else:
            dk = gt_trai >= gt_phai

        if dk:
            ket_qua = trai
            ket_qua.sau = self._tron(trai.sau, phai, tieu_chi, tang_dan)
            if ket_qua.sau:
                ket_qua.sau.truoc = ket_qua
            ket_qua.truoc = None
            return ket_qua
        else:
            ket_qua = phai
            ket_qua.sau = self._tron(trai, phai.sau, tieu_chi, tang_dan)
            if ket_qua.sau:
                ket_qua.sau.truoc = ket_qua
            ket_qua.truoc = None
            return ket_qua
