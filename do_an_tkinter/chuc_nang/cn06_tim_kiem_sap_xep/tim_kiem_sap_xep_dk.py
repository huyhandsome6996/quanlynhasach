"""
Tệp tim_kiem_sap_xep_dk.py — ĐIỀU KHIỂN cho Tìm kiếm + Sắp xếp
================================================================

Cầu nối giữa UI (ThanhTimKiemSapXepUI) và Thuật toán (tim_kiem, sap_xep).
Điều khiển luồng:
    - Nút "Tìm"       → gọi tim_kiem → đổ kết quả vào bảng.
    - Nút "Làm mới"   → nạp lại toàn bộ danh sách.
    - Nút "Sắp xếp"   → gọi sap_xep → đổ kết quả vào bảng.
"""

# Import thuật toán tìm + sắp xếp.
from .tim_kiem_sap_xep_tt import tim_kiem, sap_xep
# Import thuật toán đọc danh sách (dùng cho nút Làm mới).
from chuc_nang.cn02_doc_danh_sach.doc_danh_sach_tt import lay_danh_sach


class DieuKhienTimKiemSapXep:
    """Lớp điều khiển Tìm kiếm + Sắp xếp."""

    def __init__(self, ui_thanh, danh_sach, ui_bang):
        """
        Khởi tạo điều khiển.

        Tham số:
            ui_thanh : đối tượng ThanhTimKiemSapXepUI.
            danh_sach : DSLK đôi toàn cục.
            ui_bang   : đối tượng BangSanPhamUI (để đổ kết quả).
        """
        self.ui = ui_thanh
        self.danh_sach = danh_sach
        self.ui_bang = ui_bang

    # ----------------------------------------------------------------
    # GẮN SỰ KIỆN CHO CÁC NÚT
    # ----------------------------------------------------------------
    def gan_su_kien(self):
        """Gắn command cho các nút trên thanh UI."""
        # Nút Tìm → hàm xu_ly_tim.
        self.ui.btn_tim.config(command=self.xu_ly_tim)
        # Nút Làm mới → hàm xu_ly_lam_moi.
        self.ui.btn_lam_moi.config(command=self.xu_ly_lam_moi)
        # Nút Sắp xếp → hàm xu_ly_sap_xep.
        self.ui.btn_sap_xep.config(command=self.xu_ly_sap_xep)
        # Phím Enter trong ô từ khóa → cũng gọi tìm.
        self.ui.bind_enter_tim(self.xu_ly_tim)

    # ----------------------------------------------------------------
    # XỬ LÝ TÌM KIẾM
    # ----------------------------------------------------------------
    def xu_ly_tim(self):
        """Đọc từ khóa + tiêu chí → gọi thuật toán → đổ kết quả vào bảng.
        -bước 1: Lấy thông tin từ khoá và tiêu chí từ UI
        -Bước 2: Gọi thuật toán tim_kiem từ _tt
        -Bước 3: xoá hết dữ liệu trong bảng UI
        -bước4: duyệt và lấy all sản phẩm đúng tiêu chí và thêm vào bảng UI
        """
        tu_khoa = self.ui.lay_tu_khoa() #Lấy từ khoá
        tieu_chi = self.ui.lay_tieu_chi_tim() #lấy tiêu chí tìm cho từ khoá
        # Gọi thuật toán tìm từ file _tt
        kq = tim_kiem(self.danh_sach, tu_khoa, tieu_chi) 
        # Đổ vào bảng.
        self.ui_bang.xoa_tat_ca_dong() #Xoá hết những gì đang có trong bảng
        for sp in kq: #duyệt danh sách
            self.ui_bang.them_dong(sp) #thêm vào bảng những sản phảm đúng tiêu chí
        # Trả về số kết quả để caller hiển thị thanh trạng thái.
        return len(kq)

    # ----------------------------------------------------------------
    # XỬ LÝ LÀM MỚI
    # ----------------------------------------------------------------
    def xu_ly_lam_moi(self):
        """Tải lại toàn bộ danh sách từ DSLK."""
        ds = lay_danh_sach(self.danh_sach)
        self.ui_bang.xoa_tat_ca_dong()
        for sp in ds:
            self.ui_bang.them_dong(sp)
        return len(ds)

    # ----------------------------------------------------------------
    # XỬ LÝ SẮP XẾP
    # ----------------------------------------------------------------
    def xu_ly_sap_xep(self):
        """Sắp xếp DSLK theo tiêu chí → đổ kết quả vào bảng.
        -bước 1: lấy tiêu chí sắp xếp từ UI
        -bước 2: gọi thuật toán sap_xep từ _tt
        -bước 3: xoá hết dữ liệu trong bảng UI
        -bước 4: duyệt và lấy all dữ liệu đúng tiêu chí và thêm vào bảng UI
        """
        tieu_chi = self.ui.lay_tieu_chi_sap_xep() #Lấy tiêu chí sắp xếp từ UI
        # Gọi thuật toán (sửa thứ tự DSLK trong RAM).
        kq = sap_xep(self.danh_sach, tieu_chi) #Gọi thuật toán sắp xếp
        # Đổ vào bảng.
        self.ui_bang.xoa_tat_ca_dong() #Xoá hết dữ liệu trong bảng
        for sp in kq: #Duyệt, và lấy all dữ liệu đúng tiêu chí và đổ vào bảng
            self.ui_bang.them_dong(sp)
        return len(kq)
