"""
Tệp xử lý yêu cầu từ giao diện (Frontend).
Nhận yêu cầu HTTP, gọi danh sách liên kết, trả dữ liệu JSON về trình duyệt.

Quy tắc: KHÔNG dùng Django Rest Framework.
Tự xử lý trả về JSON bằng hàm JsonResponse của Django.
"""

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

# Biến toàn cục - Danh sách liên kết đôi quản lý toàn bộ mặt hàng trên RAM
# Sẽ được khởi tạo khi máy chủ bật (xem hàm khoi_tao_danh_sach ở dưới)
Danh_sach_cua_hang = None


def khoi_tao_danh_sach():
    """
    Khởi tạo danh sách liên kết đôi và nạp dữ liệu từ SQLite.
    Được gọi khi máy chủ Django bắt đầu chạy.

    Luồng hoạt động:
        1. Tạo đối tượng DoublyLinkedList rỗng.
        2. Gọi hàm tai_du_lieu() để đọc từ SQLite.
        3. Các bản ghi được biến thành đối tượng OOP và đưa vào Linked List.
    """
    global Danh_sach_cua_hang

    from .loi_thuat_toan.danh_sach_lien_ket import DoublyLinkedList
    from .loi_thuat_toan.ket_noi_sqlite import tai_du_lieu

    # Khởi tạo danh sách liên kết đôi rỗng
    Danh_sach_cua_hang = DoublyLinkedList()

    # Nạp dữ liệu từ SQLite vào danh sách liên kết đôi
    tai_du_lieu(Danh_sach_cua_hang)

    print(f"[KHỞI ĐỘNG] Đã nạp {Danh_sach_cua_hang.so_luong} mặt hàng vào danh sách liên kết đôi.")


def trang_chu(request):
    """
    Xử lý yêu cầu hiển thị trang chủ.
    Trả về tệp HTML trang_chu.html từ thư mục giao_dien.

    Tham số:
        request: Đối tượng yêu cầu HTTP từ trình duyệt.

    Trả về:
        Đối tượng HttpResponse chứa trang HTML.
    """
    # Khởi tạo danh sách nếu chưa có
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()

    return render(request, 'trang_chu.html')


def lay_danh_sach(request):
    """
    API GET /danh-sach
    Lấy toàn bộ danh sách mặt hàng hiện có trên RAM và trả về dạng JSON.

    Luồng hoạt động:
        1. Truy cập vào biến Danh_sach_cua_hang.
        2. Duyệt danh sách liên kết đôi từ head đến cuoi.
        3. Chuyển đổi các đối tượng thành định dạng JSON.
        4. Trả dữ liệu về trình duyệt.

    Tham số:
        request: Đối tượng yêu cầu HTTP từ trình duyệt.

    Trả về:
        JsonResponse chứa danh sách mặt hàng.
    """
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()

    # Chuyển danh sách liên kết đôi thành danh sách Python (list of dicts)
    danh_sach = Danh_sach_cua_hang.chuyen_thanh_danh_sach()

    return JsonResponse({
        'trang_thai': 'thanh_cong',
        'so_luong': Danh_sach_cua_hang.so_luong,
        'danh_sach': danh_sach
    })


@csrf_exempt
@require_http_methods(["POST"])
def them_san_pham(request):
    """
    API POST /them-san-pham
    Thêm một sản phẩm mới vào danh sách liên kết đôi và lưu vào SQLite.

    Luồng hoạt động:
        1. Nhận thông tin từ biểu mẫu gửi lên.
        2. Tạo đối tượng mới (Sach, TapChi, hoặc BaoGiay).
        3. Bước 1 (Xử lý thuật toán): Gọi hàm them_vao_cuoi().
        4. Bước 2 (Lưu trữ): Chạy lệnh SQL INSERT INTO.
        5. Báo thành công về trình duyệt.

    Tham số:
        request: Đối tượng yêu cầu HTTP chứa dữ liệu form.

    Trả về:
        JsonResponse báo thành công hoặc thất bại.
    """
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()

    try:
        # Phân tích dữ liệu JSON từ yêu cầu
        du_lieu = json.loads(request.body)

        # Lấy các thông tin từ dữ liệu gửi lên
        loai_hang = du_lieu.get('loai_hang', '').strip()
        ma_so = du_lieu.get('ma_so', '').strip()
        ten_san_pham = du_lieu.get('ten_san_pham', '').strip()
        gia_co_ban = float(du_lieu.get('gia_co_ban', 0))
        ton_kho = int(du_lieu.get('ton_kho', 0))

        # Kiểm tra dữ liệu hợp lệ
        if not ma_so or not ten_san_pham or not loai_hang:
            return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Vui lòng điền đầy đủ thông tin.'}, status=400)

        if gia_co_ban < 0:
            return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Giá cơ bản không được âm.'}, status=400)

        if ton_kho < 0:
            return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Số lượng tồn kho không được âm.'}, status=400)

        # Tạo đối tượng OOP tương ứng với loại hàng
        from .loi_thuat_toan.lop_doi_tuong import Sach, TapChi, BaoGiay

        if loai_hang == 'Sách':
            tac_gia = du_lieu.get('tac_gia', '').strip()
            nha_xuat_ban = du_lieu.get('nha_xuat_ban', '').strip()
            san_pham_moi = Sach(ma_so, ten_san_pham, gia_co_ban, ton_kho, tac_gia, nha_xuat_ban)

        elif loai_hang == 'Tạp chí':
            so_phat_hanh = du_lieu.get('so_phat_hanh', '').strip()
            san_pham_moi = TapChi(ma_so, ten_san_pham, gia_co_ban, ton_kho, so_phat_hanh)

        elif loai_hang == 'Báo giấy':
            ngay_xuat_ban = du_lieu.get('ngay_xuat_ban', '').strip()
            san_pham_moi = BaoGiay(ma_so, ten_san_pham, gia_co_ban, ton_kho, ngay_xuat_ban)

        else:
            return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Loại hàng không hợp lệ.'}, status=400)

        # Bước 1: Thêm vào danh sách liên kết đôi trên RAM
        Danh_sach_cua_hang.them_vao_cuoi(san_pham_moi)

        # Bước 2: Lưu vĩnh viễn vào SQLite
        from .loi_thuat_toan.ket_noi_sqlite import luu_mot_san_pham
        luu_mot_san_pham(san_pham_moi)

        return JsonResponse({
            'trang_thai': 'thanh_cong',
            'thong_bao': f'Đã thêm "{ten_san_pham}" vào cửa hàng.'
        })

    except json.JSONDecodeError:
        return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Dữ liệu gửi lên không hợp lệ.'}, status=400)
    except ValueError:
        return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Giá hoặc số lượng phải là số.'}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def xoa_san_pham(request):
    """
    API POST /xoa-san-pham
    Xóa một sản phẩm khỏi danh sách liên kết đôi và SQLite.

    Tham số:
        request: Đối tượng yêu cầu HTTP chứa mã số sản phẩm cần xóa.

    Trả về:
        JsonResponse báo thành công hoặc thất bại.
    """
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()

    try:
        du_lieu = json.loads(request.body)
        ma_so = du_lieu.get('ma_so', '').strip()

        if not ma_so:
            return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Mã số không được để trống.'}, status=400)

        # Bước 1: Xóa khỏi danh sách liên kết đôi trên RAM
        ket_qua = Danh_sach_cua_hang.xoa_node(ma_so)

        if ket_qua:
            # Bước 2: Xóa khỏi SQLite
            from .loi_thuat_toan.ket_noi_sqlite import xoa_mot_san_pham
            xoa_mot_san_pham(ma_so)

            return JsonResponse({
                'trang_thai': 'thanh_cong',
                'thong_bao': f'Đã xóa sản phẩm mã {ma_so}.'
            })
        else:
            return JsonResponse({
                'trang_thai': 'loi',
                'thong_bao': f'Không tìm thấy sản phẩm mã {ma_so}.'
            }, status=404)

    except json.JSONDecodeError:
        return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Dữ liệu gửi lên không hợp lệ.'}, status=400)


def tim_kiem_san_pham(request):
    """
    API GET /tim-kiem?tu_khoa=...
    Tìm kiếm sản phẩm theo từ khóa bằng cách duyệt qua danh sách liên kết đôi.

    Luồng hoạt động:
        1. Nhận từ khóa từ yêu cầu GET.
        2. Gọi hàm tim_kiem() của lớp DoublyLinkedList.
        3. Hàm tự chạy vòng lặp qua các Node bằng con trỏ next.
        4. Trả về danh sách kết quả.

    Tham số:
        request: Đối tượng yêu cầu HTTP chứa tham số tu_khoa.

    Trả về:
        JsonResponse chứa danh sách sản phẩm tìm thấy.
    """
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()

    tu_khoa = request.GET.get('tu_khoa', '').strip()

    # Gọi hàm tìm kiếm trên danh sách liên kết đôi (duyệt tuần tự qua các Node)
    ket_qua = Danh_sach_cua_hang.tim_kiem(tu_khoa)

    # Chuyển kết quả thành danh sách dict
    danh_sach_ket_qua = []
    for mat_hang in ket_qua:
        if hasattr(mat_hang, 'chuyen_thanh_dict'):
            danh_sach_ket_qua.append(mat_hang.chuyen_thanh_dict())

    return JsonResponse({
        'trang_thai': 'thanh_cong',
        'so_luong': len(danh_sach_ket_qua),
        'danh_sach': danh_sach_ket_qua
    })


def sap_xep_danh_sach(request):
    """
    API GET /sap-xep?tieu_chi=gia_ban
    Sắp xếp danh sách mặt hàng bằng thuật toán Merge Sort trên danh sách liên kết đôi.

    Luồng hoạt động:
        1. Nhận tiêu chí sắp xếp từ yêu cầu GET.
        2. Gọi hàm sap_xep_tron() của lớp DoublyLinkedList.
        3. Thuật toán tự đổi chỗ các con trỏ next, truoc trong RAM.
        4. Trả về danh sách đã sắp xếp.

    Tham số:
        request: Đối tượng yêu cầu HTTP chứa tham số tieu_chi.

    Trả về:
        JsonResponse chứa danh sách sản phẩm đã sắp xếp.
    """
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()

    tieu_chi = request.GET.get('tieu_chi', 'gia_ban').strip()

    # Gọi hàm sắp xếp trộn (Merge Sort) trên danh sách liên kết đôi
    Danh_sach_cua_hang.sap_xep_tron(tieu_chi)

    # Chuyển danh sách đã sắp xếp thành danh sách dict
    danh_sach = Danh_sach_cua_hang.chuyen_thanh_danh_sach()

    return JsonResponse({
        'trang_thai': 'thanh_cong',
        'so_luong': Danh_sach_cua_hang.so_luong,
        'danh_sach': danh_sach
    })
