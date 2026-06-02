"""
Tệp chứa dữ liệu giả (mock data) để kiểm thử danh sách liên kết đôi.
Chạy tệp này trực tiếp để xác minh các thao tác cơ bản trên DoublyLinkedList.
"""

from .danh_sach_lien_ket import Node, DoublyLinkedList


class MatHangGia:
    """
    Lớp mặt hàng giả dùng để kiểm thử danh sách liên kết đôi
    trước khi tích hợp với các lớp OOP chính thức.
    """

    def __init__(self, ma_so, ten_san_pham, gia_co_ban):
        self.ma_so = ma_so
        self.ten_san_pham = ten_san_pham
        self.gia_co_ban = gia_co_ban

    def tinh_gia_ban(self):
        return self.gia_co_ban

    def chuyen_thanh_dict(self):
        return {
            'ma_so': self.ma_so,
            'ten_san_pham': self.ten_san_pham,
            'gia_co_ban': self.gia_co_ban,
            'gia_ban': self.tinh_gia_ban()
        }

    def __str__(self):
        return f"[{self.ma_so}] {self.ten_san_pham} - {self.gia_co_ban}đ"


def tao_du_lieu_gia():
    """
    Tạo danh sách liên kết đôi với dữ liệu giả để kiểm thử.

    Trả về:
        Đối tượng DoublyLinkedList đã nạp sẵn dữ liệu.
    """
    ds = DoublyLinkedList()

    # Thêm các mặt hàng giả vào danh sách
    ds.them_vao_cuoi(MatHangGia("MH001", "Sách Lập trình Python", 120000))
    ds.them_vao_cuoi(MatHangGia("MH002", "Tạp chí Khoa học", 45000))
    ds.them_vao_cuoi(MatHangGia("MH003", "Báo Nhân dân", 8000))
    ds.them_vao_cuoi(MatHangGia("MH004", "Sách Cấu trúc dữ liệu", 95000))
    ds.them_vao_cuoi(MatHangGia("MH005", "Tạp chí Công nghệ", 55000))

    return ds


def kiem_thu_co_ban():
    """Hàm kiểm thử các thao tác cơ bản trên danh sách liên kết đôi."""
    print("=" * 60)
    print("KIỂM THỬ DANH SÁCH LIÊN KẾT ĐÔI")
    print("=" * 60)

    # Kiểm tra thêm phần tử
    ds = tao_du_lieu_gia()
    print(f"\n[1] Thêm phần tử: Số lượng = {ds.so_luong}")
    print(f"    Nội dung: {ds}")

    # Kiểm tra chuyển thành danh sách
    danh_sach = ds.chuyen_thanh_danh_sach()
    print(f"\n[2] Chuyển thành danh sách dict: {danh_sach}")

    # Kiểm tra xóa phần tử
    ket_qua_xoa = ds.xoa_node("MH003")
    print(f"\n[3] Xóa MH003: {'Thành công' if ket_qua_xoa else 'Thất bại'}")
    print(f"    Số lượng sau xóa = {ds.so_luong}")
    print(f"    Nội dung: {ds}")

    # Kiểm tra xóa phần tử không tồn tại
    ket_qua_xoa_2 = ds.xoa_node("MH999")
    print(f"\n[4] Xóa MH999 (không tồn tại): {'Thành công' if ket_qua_xoa_2 else 'Thất bại'}")
    print(f"    Số lượng = {ds.so_luong}")

    # Kiểm tra tìm kiếm
    ds2 = tao_du_lieu_gia()
    ket_qua_tim = ds2.tim_kiem("sách")
    print(f"\n[5] Tìm kiếm 'sách': Tìm thấy {len(ket_qua_tim)} kết quả")
    for mh in ket_qua_tim:
        print(f"    - {mh}")

    # Kiểm tra sắp xếp
    ds3 = tao_du_lieu_gia()
    print(f"\n[6] Sắp xếp theo giá bán:")
    print(f"    Trước: {ds3}")
    ds3.sap_xep_tron('gia_ban')
    print(f"    Sau:   {ds3}")

    print("\n" + "=" * 60)
    print("HOÀN THÀNH KIỂM THỬ!")
    print("=" * 60)


if __name__ == "__main__":
    kiem_thu_co_ban()
