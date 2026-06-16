"""
Tệp chứa dữ liệu giả (mock data) để kiểm thử danh sách liên kết đôi
và các cấu trúc dữ liệu khác (Stack, Queue).

Chạy tệp này trực tiếp để xác minh các thao tác cơ bản.

Cách chạy:
    cd du_an_cua_hang_sach
    python -m ung_dung_giao_tiep.loi_thuat_toan.kiem_thu
"""

from .danh_sach_lien_ket import Node, DoublyLinkedList
from .cau_truc_du_lieu import NganXep, HangDoi
from .lop_doi_tuong import Sach, TapChi, BaoGiay, LuanVan, BanThao


def tao_du_lieu_gia():
    """
    Tạo danh sách liên kết đôi với dữ liệu giả để kiểm thử.

    Trả về:
        Đối tượng DoublyLinkedList đã nạp sẵn dữ liệu.
    """
    ds = DoublyLinkedList()

    # Thêm các mặt hàng giả vào danh sách
    ds.them_vao_cuoi(Sach("MH001", "Sách Lập trình Python", 120000, 50, "Nguyễn Văn A", "NXB Giáo dục"))
    ds.them_vao_cuoi(TapChi("MH002", "Tạp chí Khoa học", 45000, 30, "Số 123"))
    ds.them_vao_cuoi(BaoGiay("MH003", "Báo Nhân dân", 8000, 100, "15/06/2025"))
    ds.them_vao_cuoi(Sach("MH004", "Sách Cấu trúc dữ liệu", 95000, 15, "Trần Thị B", "NXB Đại học"))
    ds.them_vao_cuoi(TapChi("MH005", "Tạp chí Công nghệ", 55000, 8, "Số 456"))
    ds.them_vao_cuoi(LuanVan("MH006", "Luận văn AI trong Y tế", 200000, 5, "Lê Văn C", "ĐH Bách Khoa"))
    ds.them_vao_cuoi(BanThao("MH007", "Bản thảo Tiểu thuyết", 80000, 3, "Phạm Thị D", "Chưa duyệt"))

    return ds


def kiem_thu_danh_sach_lien_ket():
    """Kiểm thử các thao tác cơ bản trên danh sách liên kết đôi."""
    print("=" * 60)
    print("KIỂM THỬ DANH SÁCH LIÊN KẾT ĐÔI")
    print("=" * 60)

    # 1. Thêm phần tử
    ds = tao_du_lieu_gia()
    print(f"\n[1] Thêm phần tử: Số lượng = {ds.so_luong}")
    print(f"    Nội dung: {ds}")

    # 2. Tìm theo mã số
    ket_qua = ds.tim_theo_ma("MH004")
    print(f"\n[2] Tìm theo mã số MH004: {ket_qua}")

    # 3. Tìm kiếm theo tên
    ket_qua_ten = ds.tim_kiem("sách", "ten")
    print(f"\n[3] Tìm kiếm 'sách' (theo tên): {len(ket_qua_ten)} kết quả")
    for mh in ket_qua_ten:
        print(f"    - {mh}")

    # 4. Tìm kiếm theo loại
    ket_qua_loai = ds.tim_kiem("tạp chí", "loai")
    print(f"\n[4] Tìm kiếm 'tạp chí' (theo loại): {len(ket_qua_loai)} kết quả")
    for mh in ket_qua_loai:
        print(f"    - {mh}")

    # 5. Xóa phần tử
    ket_qua_xoa = ds.xoa_node("MH003")
    print(f"\n[5] Xóa MH003: {'Thành công' if ket_qua_xoa else 'Thất bại'}")
    print(f"    Số lượng sau xóa = {ds.so_luong}")

    # 6. Xóa phần tử không tồn tại
    ket_qua_xoa_2 = ds.xoa_node("MH999")
    print(f"\n[6] Xóa MH999 (không tồn tại): {'Thành công' if ket_qua_xoa_2 else 'Thất bại'}")

    # 7. Sắp xếp theo giá bán
    ds3 = tao_du_lieu_gia()
    print(f"\n[7] Sắp xếp theo giá bán:")
    print(f"    Trước: {ds3}")
    ds3.sap_xep_tron('gia_ban')
    print(f"    Sau:   {ds3}")

    # 8. Đa hình - Tính giá bán
    print(f"\n[8] Kiểm tra đa hình (tinh_gia_ban):")
    ds4 = tao_du_lieu_gia()
    node = ds4.head
    while node is not None:
        sp = node.data
        print(f"    {sp.loai_hang} '{sp.ten_san_pham}': Giá cơ bản={sp.gia_co_ban:,.0f}đ → Giá bán={sp.tinh_gia_ban():,.0f}đ")
        node = node.next


def kiem_thu_ngan_xep():
    """Kiểm thử cấu trúc Ngăn xếp (Stack) dùng cho Undo/Redo."""
    print("\n" + "=" * 60)
    print("KIỂM THỬ NGĂN XẾP (STACK) - Undo/Redo")
    print("=" * 60)

    stack = NganXep()

    # Đẩy các thao tác vào ngăn xếp
    stack.day_vao({'thao_tac': 'them', 'ma_so': 'MH001'})
    stack.day_vao({'thao_tac': 'sua', 'ma_so': 'MH002'})
    stack.day_vao({'thao_tac': 'xoa', 'ma_so': 'MH003'})

    print(f"\n[1] Đẩy 3 thao tác vào ngăn xếp: Số lượng = {stack.so_luong}")

    # Lấy ra (LIFO - phần tử cuối cùng vào sẽ ra đầu tiên)
    thao_tac = stack.lay_ra()
    print(f"\n[2] Lấy ra (Pop): {thao_tac}")
    print(f"    Số lượng còn lại = {stack.so_luong}")

    thao_tac = stack.lay_ra()
    print(f"\n[3] Lấy ra (Pop): {thao_tac}")

    # Xem đỉnh
    print(f"\n[4] Xem đỉnh (Peek): {stack.xem_dinh()}")


def kiem_thu_hang_doi():
    """Kiểm thử cấu trúc Hàng đợi (Queue) dùng cho Giỏ hàng."""
    print("\n" + "=" * 60)
    print("KIỂM THỬ HÀNG ĐỢI (QUEUE) - Giỏ hàng")
    print("=" * 60)

    queue = HangDoi()

    # Thêm mặt hàng vào hàng đợi
    s1 = Sach("MH001", "Sách Python", 120000, 50, "Tác giả A", "NXB")
    s2 = TapChi("MH002", "Tạp chí KH", 45000, 30, "Số 1")
    s3 = BaoGiay("MH003", "Báo ND", 8000, 100, "15/06/2025")

    queue.them_vao(s1)
    queue.them_vao(s2)
    queue.them_vao(s3)

    print(f"\n[1] Thêm 3 mặt hàng vào hàng đợi: Số lượng = {queue.so_luong}")

    # Xem danh sách
    ds = queue.xem_danh_sach()
    print(f"\n[2] Xem danh sách giỏ hàng:")
    for sp in ds:
        print(f"    - {sp['ten_san_pham']} ({sp['loai_hang']}): {sp['gia_ban']:,.0f}đ")

    # Lấy ra (FIFO - phần tử đầu tiên vào sẽ ra đầu tiên)
    sp_ra = queue.lay_ra()
    print(f"\n[3] Lấy ra (Dequeue): {sp_ra}")
    print(f"    Số lượng còn lại = {queue.so_luong}")

    # Xóa theo mã
    queue.xoa_theo_ma("MH002")
    print(f"\n[4] Xóa MH002 khỏi hàng đợi: Số lượng = {queue.so_luong}")


def kiem_thu_co_ban():
    """Chạy tất cả các bài kiểm thử."""
    kiem_thu_danh_sach_lien_ket()
    kiem_thu_ngan_xep()
    kiem_thu_hang_doi()

    print("\n" + "=" * 60)
    print("HOÀN THÀNH KIỂM THỬ!")
    print("=" * 60)


if __name__ == "__main__":
    kiem_thu_co_ban()
