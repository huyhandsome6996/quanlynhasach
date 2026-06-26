"""
Tệp kiem_thu.py — KIỂM THỬ Danh sách liên kết đôi + thuật toán Merge Sort.
=========================================================================

Chạy:   python -m ung_dung_giao_tiep.loi_thuat_toan.kiem_thu
  (hoặc: cd du_an_cua_hang_sach && python -m ung_dung_giao_tiep.loi_thuat_toan.kiem_thu)

Tự động tạo 5 mặt hàng giả, rồi test lần lượt:
  [1] Thêm phần tử
  [2] Chuyển DSLK thành list Python
  [3] Xóa phần tử tồn tại
  [4] Xóa phần tử KHÔNG tồn tại
  [5] Tìm kiếm theo tên (substring)
  [6] Sắp xếp theo giá bán bằng Merge Sort
"""

# Nhập Node và DoublyLinkedList từ module cùng thư mục.
# Dấu `.` nghĩa là "module trong cùng package".
from loi_thuat_toan.danh_sach_lien_ket import Node, DoublyLinkedList


# Lớp MatHangGia — một mặt hàng ĐƠN GIẢN chỉ phục vụ kiểm thử.
# (Khác với lop_doi_tuong.py, lớp này không kế thừa ABC, không phân loại —
# chỉ cần đủ 4 thuộc tính để DoublyLinkedList có thể thao tác.)
class MatHangGia:

    def __init__(self, ma_so, ten_san_pham, gia_co_ban):
        # Khởi tạo 3 trường tối thiểu cần cho test.
        self.ma_so = ma_so
        self.ten_san_pham = ten_san_pham
        self.gia_co_ban = gia_co_ban

    def tinh_gia_ban(self):
        """Giá bán = giá cơ bản (không phụ thu) — đủ để Merge Sort chạy."""
        return self.gia_co_ban

    def chuyen_thanh_dict(self):
        """Trả về dict để in/in kết quả test dưới dạng JSON-like."""
        return {
            'ma_so':         self.ma_so,
            'ten_san_pham':  self.ten_san_pham,
            'gia_co_ban':    self.gia_co_ban,
            'gia_ban':       self.tinh_gia_ban()
        }

    def __str__(self):
        """In mặt hàng: [MH001] Tên - 120000đ."""
        return f'[{self.ma_so}] {self.ten_san_pham} - {self.gia_co_ban}đ'


def tao_du_lieu_gia():
    """Tạo DSLK chứa 5 mặt hàng mẫu để test."""
    ds = DoublyLinkedList()
    ds.them_vao_cuoi(MatHangGia('MH001', 'Sách Lập trình Python',  120000))
    ds.them_vao_cuoi(MatHangGia('MH002', 'Tạp chí Khoa học',        45000))
    ds.them_vao_cuoi(MatHangGia('MH003', 'Báo Nhân dân',              8000))
    ds.them_vao_cuoi(MatHangGia('MH004', 'Sách Cấu trúc dữ liệu',   95000))
    ds.them_vao_cuoi(MatHangGia('MH005', 'Tạp chí Công nghệ',       55000))
    return ds


def kiem_thu_co_ban():
    """Hàm chính — chạy 6 test case và in kết quả ra màn hình."""

    # In tiêu đề báo cáo.
    print('=' * 60)
    print('KIỂM THỬ DANH SÁCH LIÊN KẾT ĐÔI')
    print('=' * 60)

    # [1] Test thêm phần tử.
    ds = tao_du_lieu_gia()
    print(f'\n[1] Thêm phần tử: Số lượng = {ds.so_luong}')
    print(f'    Nội dung: {ds}')

    # [2] Test chuyển DSLK → list Python.
    danh_sach = ds.chuyen_thanh_danh_sach()
    print(f'\n[2] Chuyển thành danh sách dict: {danh_sach}')

    # [3] Test xóa phần tử TỒN TẠI.
    ket_qua_xoa = ds.xoa_node('MH003')
    print(f"\n[3] Xóa MH003: {('Thành công' if ket_qua_xoa else 'Thất bại')}")
    print(f'    Số lượng sau xóa = {ds.so_luong}')
    print(f'    Nội dung: {ds}')

    # [4] Test xóa phần tử KHÔNG TỒN TẠI → phải báo False.
    ket_qua_xoa_2 = ds.xoa_node('MH999')
    print(f"\n[4] Xóa MH999 (không tồn tại): {('Thành công' if ket_qua_xoa_2 else 'Thất bại')}")
    print(f'    Số lượng = {ds.so_luong}')

    # [5] Test tìm kiếm theo tên (substring, không phân biệt hoa thường).
    ds2 = tao_du_lieu_gia()
    ket_qua_tim = ds2.tim_kiem('sách')   # Mong đợi 2 kết quả: "Sách Lập trình..." và "Sách Cấu trúc..."
    print(f"\n[5] Tìm kiếm 'sách': Tìm thấy {len(ket_qua_tim)} kết quả")
    for mh in ket_qua_tim:
        print(f'    - {mh}')

    # [6] Test Merge Sort theo giá bán (tăng dần).
    ds3 = tao_du_lieu_gia()
    print(f'\n[6] Sắp xếp theo giá bán:')
    print(f'    Trước: {ds3}')
    ds3.sap_xep_tron('gia_ban')
    print(f'    Sau:   {ds3}')

    # In kết thúc.
    print('\n' + '=' * 60)
    print('HOÀN THÀNH KIỂM THỬ!')
    print('=' * 60)


# Điểm vào khi chạy trực tiếp: `python -m ung_dung_giao_tiep.loi_thuat_toan.kiem_thu`.
# Lưu ý: phải dùng `python -m` (chạy như module) thay vì `python kiem_thu.py`
# vì file có dùng `from loi_thuat_toan.danh_sach_lien_ket import ...` (relative import).
if __name__ == '__main__':
    kiem_thu_co_ban()
