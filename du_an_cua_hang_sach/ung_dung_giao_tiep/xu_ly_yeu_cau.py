"""
Tệp xử lý yêu cầu từ giao diện (Frontend).
Nhận yêu cầu HTTP, gọi danh sách liên kết, trả dữ liệu JSON về trình duyệt.

Các API endpoint:
    GET  /              → Hiển thị trang chủ.
    GET  /danh-sach     → Lấy toàn bộ danh sách mặt hàng.
    POST /them-san-pham → Thêm sản phẩm mới.
    POST /sua-san-pham  → Sửa thông tin sản phẩm.
    POST /xoa-san-pham  → Xóa sản phẩm.
    GET  /tim-kiem      → Tìm kiếm nâng cao (tên, mã, loại).
    GET  /sap-xep       → Sắp xếp danh sách (Merge Sort).
    GET  /thong-ke      → Thống kê tổng quan.
    POST /them-gio-hang → Thêm vào giỏ hàng.
    GET  /xem-gio-hang  → Xem giỏ hàng.
    POST /xoa-gio-hang  → Xóa khỏi giỏ hàng.
    POST /thanh-toan    → Thanh toán giỏ hàng.
    POST /hoan-tac      → Undo (hoàn tác).
    POST /lam-lai       → Redo (làm lại).

Quy tắc: KHÔNG dùng Django Rest Framework.
Tự xử lý trả về JSON bằng hàm JsonResponse của Django.
"""

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

# ============================================================
# BIẾN TOÀN CỤC
# ============================================================

# Danh sách liên kết đôi - Quản lý toàn bộ mặt hàng trên RAM
Danh_sach_cua_hang = None

# Ngăn xếp Undo/Redo - Lưu lịch sử thao tác
Ngan_xep_hoan_tac = None   # Stack chứa các thao tác cần hoàn tác (Undo)
Ngan_xep_lam_lai = None    # Stack chứa các thao tác cần làm lại (Redo)

# Hàng đợi Giỏ hàng - Quản lý mặt hàng chờ thanh toán
Gio_hang = None


# ============================================================
# KHỞI TẠO HỆ THỐNG
# ============================================================

def khoi_tao_danh_sach():
    """
    Khởi tạo danh sách liên kết đôi và nạp dữ liệu từ SQLite.
    Được gọi khi máy chủ Django bắt đầu chạy hoặc lần đầu truy cập.

    Luồng hoạt động:
        1. Tạo đối tượng DoublyLinkedList rỗng.
        2. Gọi hàm tai_du_lieu() để đọc từ SQLite.
        3. Các bản ghi được biến thành đối tượng OOP và đưa vào Linked List.
        4. Khởi tạo Stack (Undo/Redo) và Queue (Giỏ hàng).
    """
    global Danh_sach_cua_hang, Ngan_xep_hoan_tac, Ngan_xep_lam_lai, Gio_hang

    from .loi_thuat_toan.danh_sach_lien_ket import DoublyLinkedList
    from .loi_thuat_toan.cau_truc_du_lieu import NganXep, HangDoi
    from .loi_thuat_toan.ket_noi_sqlite import tai_du_lieu

    # Khởi tạo danh sách liên kết đôi rỗng
    Danh_sach_cua_hang = DoublyLinkedList()

    # Nạp dữ liệu từ SQLite vào danh sách liên kết đôi
    tai_du_lieu(Danh_sach_cua_hang)

    # Khởi tạo ngăn xếp Undo/Redo
    Ngan_xep_hoan_tac = NganXep()
    Ngan_xep_lam_lai = NganXep()

    # Khởi tạo hàng đợi Giỏ hàng
    Gio_hang = HangDoi()

    print(f"[KHỞI ĐỘNG] Đã nạp {Danh_sach_cua_hang.so_luong} mặt hàng vào danh sách liên kết đôi.")


# ============================================================
# TRANG CHỦ
# ============================================================

def trang_chu(request):
    """
    Xử lý yêu cầu hiển thị trang chủ.

    Tham số:
        request: Đối tượng yêu cầu HTTP từ trình duyệt.

    Trả về:
        HttpResponse chứa trang HTML.
    """
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()

    return render(request, 'trang_chu.html')


# ============================================================
# API: LẤY DANH SÁCH
# ============================================================

def lay_danh_sach(request):
    """
    API GET /danh-sach
    Lấy toàn bộ danh sách mặt hàng hiện có trên RAM và trả về dạng JSON.

    Luồng hoạt động:
        1. Truy cập biến Danh_sach_cua_hang.
        2. Duyệt danh sách liên kết đôi từ head đến cuoi.
        3. Chuyển đổi các đối tượng thành định dạng JSON.
        4. Trả dữ liệu về trình duyệt.
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


# ============================================================
# API: THÊM SẢN PHẨM
# ============================================================

@csrf_exempt
@require_http_methods(["POST"])
def them_san_pham(request):
    """
    API POST /them-san-pham
    Thêm một sản phẩm mới vào danh sách liên kết đôi và lưu vào SQLite.

    Luồng hoạt động:
        1. Nhận thông tin từ biểu mẫu gửi lên.
        2. Kiểm tra tính hợp lệ của dữ liệu.
        3. Kiểm tra trùng mã số.
        4. Tạo đối tượng OOP tương ứng (Sach, TapChi, BaoGiay, LuanVan, BanThao).
        5. Thêm vào danh sách liên kết đôi trên RAM.
        6. Lưu vĩnh viễn vào SQLite.
        7. Lưu thao tác vào Stack Undo.
    """
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()

    try:
        du_lieu = json.loads(request.body)

        # Lấy các thông tin chung
        loai_hang = du_lieu.get('loai_hang', '').strip()
        ma_so = du_lieu.get('ma_so', '').strip()
        ten_san_pham = du_lieu.get('ten_san_pham', '').strip()
        gia_co_ban = float(du_lieu.get('gia_co_ban', 0))
        ton_kho = int(du_lieu.get('ton_kho', 0))

        # ---- Kiểm tra dữ liệu hợp lệ ----
        if not ma_so or not ten_san_pham or not loai_hang:
            return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Vui lòng điền đầy đủ thông tin.'}, status=400)

        if gia_co_ban < 0:
            return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Giá cơ bản không được âm.'}, status=400)

        if ton_kho < 0:
            return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Số lượng tồn kho không được âm.'}, status=400)

        # ---- Kiểm tra trùng mã số ----
        node_ton_tai = Danh_sach_cua_hang.tim_theo_ma(ma_so)
        if node_ton_tai is not None:
            return JsonResponse({'trang_thai': 'loi', 'thong_bao': f'Mã số "{ma_so}" đã tồn tại trong cửa hàng.'}, status=400)

        # ---- Tạo đối tượng OOP tương ứng với loại hàng ----
        from .loi_thuat_toan.lop_doi_tuong import Sach, TapChi, BaoGiay, LuanVan, BanThao

        if loai_hang == 'Sách':
            tac_gia = du_lieu.get('tac_gia', '').strip()
            nha_xuat_ban = du_lieu.get('nha_xuat_ban', '').strip()
            if not tac_gia or not nha_xuat_ban:
                return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Vui lòng nhập tác giả và nhà xuất bản.'}, status=400)
            san_pham_moi = Sach(ma_so, ten_san_pham, gia_co_ban, ton_kho, tac_gia, nha_xuat_ban)

        elif loai_hang == 'Tạp chí':
            so_phat_hanh = du_lieu.get('so_phat_hanh', '').strip()
            if not so_phat_hanh:
                return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Vui lòng nhập số phát hành.'}, status=400)
            san_pham_moi = TapChi(ma_so, ten_san_pham, gia_co_ban, ton_kho, so_phat_hanh)

        elif loai_hang == 'Báo giấy':
            ngay_xuat_ban = du_lieu.get('ngay_xuat_ban', '').strip()
            if not ngay_xuat_ban:
                return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Vui lòng nhập ngày xuất bản.'}, status=400)
            san_pham_moi = BaoGiay(ma_so, ten_san_pham, gia_co_ban, ton_kho, ngay_xuat_ban)

        elif loai_hang == 'Luận văn':
            tac_gia = du_lieu.get('tac_gia', '').strip()
            truong_dai_hoc = du_lieu.get('truong_dai_hoc', '').strip()
            if not tac_gia or not truong_dai_hoc:
                return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Vui lòng nhập tác giả và trường đại học.'}, status=400)
            san_pham_moi = LuanVan(ma_so, ten_san_pham, gia_co_ban, ton_kho, tac_gia, truong_dai_hoc)

        elif loai_hang == 'Bản thảo':
            tac_gia = du_lieu.get('tac_gia', '').strip()
            trang_thai = du_lieu.get('trang_thai', 'Chưa duyệt').strip()
            if not tac_gia:
                return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Vui lòng nhập tác giả.'}, status=400)
            san_pham_moi = BanThao(ma_so, ten_san_pham, gia_co_ban, ton_kho, tac_gia, trang_thai)

        else:
            return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Loại hàng không hợp lệ.'}, status=400)

        # ---- Bước 1: Thêm vào danh sách liên kết đôi trên RAM ----
        Danh_sach_cua_hang.them_vao_cuoi(san_pham_moi)

        # ---- Bước 2: Lưu vĩnh viễn vào SQLite ----
        from .loi_thuat_toan.ket_noi_sqlite import luu_mot_san_pham
        luu_mot_san_pham(san_pham_moi)

        # ---- Bước 3: Lưu thao tác vào Stack Undo ----
        Ngan_xep_hoan_tac.day_vao({
            'thao_tac': 'them',
            'ma_so': ma_so
        })
        # Khi thêm mới, xóa Stack Redo (chuỗi thao tác bị đứt)
        Ngan_xep_lam_lai.xoa_tat_ca()

        return JsonResponse({
            'trang_thai': 'thanh_cong',
            'thong_bao': f'Đã thêm "{ten_san_pham}" vào cửa hàng.'
        })

    except json.JSONDecodeError:
        return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Dữ liệu gửi lên không hợp lệ.'}, status=400)
    except ValueError:
        return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Giá hoặc số lượng phải là số.'}, status=400)


# ============================================================
# API: SỬA SẢN PHẨM
# ============================================================

@csrf_exempt
@require_http_methods(["POST"])
def sua_san_pham(request):
    """
    API POST /sua-san-pham
    Sửa thông tin một sản phẩm trong danh sách liên kết đôi và SQLite.

    Luồng hoạt động:
        1. Nhận thông tin từ biểu mẫu gửi lên.
        2. Tìm sản phẩm theo mã số trong danh sách liên kết đôi.
        3. Lưu dữ liệu cũ vào Stack Undo (để có thể hoàn tác).
        4. Cập nhật thông tin trên RAM.
        5. Cập nhật thông tin trong SQLite.
    """
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()

    try:
        du_lieu = json.loads(request.body)

        ma_so = du_lieu.get('ma_so', '').strip()
        ten_san_pham_moi = du_lieu.get('ten_san_pham', '').strip()
        gia_co_ban_moi = du_lieu.get('gia_co_ban', 0)
        ton_kho_moi = du_lieu.get('ton_kho', 0)

        if not ma_so:
            return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Mã số không được để trống.'}, status=400)

        # ---- Tìm sản phẩm trong danh sách liên kết đôi ----
        san_pham = Danh_sach_cua_hang.tim_theo_ma(ma_so)
        if san_pham is None:
            return JsonResponse({'trang_thai': 'loi', 'thong_bao': f'Không tìm thấy sản phẩm mã {ma_so}.'}, status=404)

        # ---- Lưu dữ liệu cũ vào Stack Undo trước khi sửa ----
        du_lieu_cu = san_pham.chuyen_thanh_dict()
        Ngan_xep_hoan_tac.day_vao({
            'thao_tac': 'sua',
            'du_lieu_cu': du_lieu_cu
        })
        Ngan_xep_lam_lai.xoa_tat_ca()

        # ---- Cập nhật thông tin trên RAM ----
        if ten_san_pham_moi:
            san_pham.ten_san_pham = ten_san_pham_moi
        if gia_co_ban_moi is not None and float(gia_co_ban_moi) >= 0:
            san_pham.gia_co_ban = float(gia_co_ban_moi)
        if ton_kho_moi is not None and int(ton_kho_moi) >= 0:
            san_pham.ton_kho = int(ton_kho_moi)

        # Cập nhật các thuộc tính riêng theo loại hàng
        if san_pham.loai_hang == 'Sách':
            if 'tac_gia' in du_lieu and du_lieu['tac_gia']:
                san_pham.tac_gia = du_lieu['tac_gia'].strip()
            if 'nha_xuat_ban' in du_lieu and du_lieu['nha_xuat_ban']:
                san_pham.nha_xuat_ban = du_lieu['nha_xuat_ban'].strip()

        elif san_pham.loai_hang == 'Tạp chí':
            if 'so_phat_hanh' in du_lieu and du_lieu['so_phat_hanh']:
                san_pham.so_phat_hanh = du_lieu['so_phat_hanh'].strip()

        elif san_pham.loai_hang == 'Báo giấy':
            if 'ngay_xuat_ban' in du_lieu and du_lieu['ngay_xuat_ban']:
                san_pham.ngay_xuat_ban = du_lieu['ngay_xuat_ban'].strip()

        elif san_pham.loai_hang == 'Luận văn':
            if 'tac_gia' in du_lieu and du_lieu['tac_gia']:
                san_pham.tac_gia = du_lieu['tac_gia'].strip()
            if 'truong_dai_hoc' in du_lieu and du_lieu['truong_dai_hoc']:
                san_pham.truong_dai_hoc = du_lieu['truong_dai_hoc'].strip()

        elif san_pham.loai_hang == 'Bản thảo':
            if 'tac_gia' in du_lieu and du_lieu['tac_gia']:
                san_pham.tac_gia = du_lieu['tac_gia'].strip()
            if 'trang_thai' in du_lieu and du_lieu['trang_thai']:
                san_pham.trang_thai = du_lieu['trang_thai'].strip()

        # ---- Cập nhật trong SQLite ----
        from .loi_thuat_toan.ket_noi_sqlite import cap_nhat_san_pham
        cap_nhat_san_pham(san_pham)

        return JsonResponse({
            'trang_thai': 'thanh_cong',
            'thong_bao': f'Đã cập nhật thông tin sản phẩm "{san_pham.ten_san_pham}".'
        })

    except json.JSONDecodeError:
        return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Dữ liệu gửi lên không hợp lệ.'}, status=400)
    except ValueError:
        return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Giá hoặc số lượng phải là số.'}, status=400)


# ============================================================
# API: XÓA SẢN PHẨM
# ============================================================

@csrf_exempt
@require_http_methods(["POST"])
def xoa_san_pham(request):
    """
    API POST /xoa-san-pham
    Xóa một sản phẩm khỏi danh sách liên kết đôi và SQLite.

    Luồng hoạt động:
        1. Nhận mã số sản phẩm cần xóa.
        2. Lưu dữ liệu cũ vào Stack Undo.
        3. Xóa khỏi danh sách liên kết đôi trên RAM.
        4. Xóa khỏi SQLite.
    """
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()

    try:
        du_lieu = json.loads(request.body)
        ma_so = du_lieu.get('ma_so', '').strip()

        if not ma_so:
            return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Mã số không được để trống.'}, status=400)

        # ---- Lưu dữ liệu cũ vào Stack Undo trước khi xóa ----
        san_pham = Danh_sach_cua_hang.tim_theo_ma(ma_so)
        if san_pham is not None:
            du_lieu_cu = san_pham.chuyen_thanh_dict()
            Ngan_xep_hoan_tac.day_vao({
                'thao_tac': 'xoa',
                'du_lieu_cu': du_lieu_cu
            })
            Ngan_xep_lam_lai.xoa_tat_ca()

        # ---- Xóa khỏi danh sách liên kết đôi trên RAM ----
        ket_qua = Danh_sach_cua_hang.xoa_node(ma_so)

        if ket_qua:
            # ---- Xóa khỏi SQLite ----
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


# ============================================================
# API: TÌM KIẾM NÂNG CAO
# ============================================================

def tim_kiem_san_pham(request):
    """
    API GET /tim-kiem?tu_khoa=...&tieu_chi=ten
    Tìm kiếm sản phẩm theo từ khóa với nhiều tiêu chí.

    Tiêu chí tìm kiếm:
        - 'ten':  Tìm trong tên sản phẩm (mặc định).
        - 'ma':   Tìm theo mã số chính xác.
        - 'loai': Tìm theo loại hàng.

    Luồng hoạt động:
        1. Nhận từ khóa và tiêu chí từ yêu cầu GET.
        2. Gọi hàm tim_kiem() của lớp DoublyLinkedList.
        3. Trả về danh sách kết quả.
    """
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()

    tu_khoa = request.GET.get('tu_khoa', '').strip()
    tieu_chi = request.GET.get('tieu_chi', 'ten').strip()

    # Gọi hàm tìm kiếm trên danh sách liên kết đôi
    ket_qua = Danh_sach_cua_hang.tim_kiem(tu_khoa, tieu_chi)

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


# ============================================================
# API: SẮP XẾP
# ============================================================

def sap_xep_danh_sach(request):
    """
    API GET /sap-xep?tieu_chi=gia_ban
    Sắp xếp danh sách mặt hàng bằng thuật toán Merge Sort trên DSLK đôi.

    Tiêu chí sắp xếp:
        - 'gia_ban':      Sắp xếp theo giá bán.
        - 'ten_san_pham': Sắp xếp theo tên sản phẩm.
        - 'ton_kho':      Sắp xếp theo tồn kho.
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


# ============================================================
# API: THỐNG KÊ
# ============================================================

def thong_ke(request):
    """
    API GET /thong-ke
    Thống kê tổng quan về cửa hàng sách.

    Các thống kê:
        - Tổng số lượng mặt hàng.
        - Mặt hàng đắt nhất.
        - Mặt hàng rẻ nhất.
        - Số mặt hàng sắp hết hàng (tồn kho <= 10).
        - Tổng giá trị tồn kho.
        - Thống kê theo loại hàng.
    """
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()

    tong_so_luong = Danh_sach_cua_hang.so_luong

    if tong_so_luong == 0:
        return JsonResponse({
            'trang_thai': 'thanh_cong',
            'thong_ke': {
                'tong_so_luong': 0,
                'mat_hang_dat_nhat': None,
                'mat_hang_re_nhat': None,
                'so_mat_hang_sap_het': 0,
                'tong_gia_tri_ton_kho': 0,
                'thong_ke_theo_loai': {}
            }
        })

    # Duyệt qua danh sách liên kết đôi để tính toán thống kê
    mat_hang_dat_nhat = None
    mat_hang_re_nhat = None
    so_mat_hang_sap_het = 0
    tong_gia_tri_ton_kho = 0
    thong_ke_theo_loai = {}

    node_hien_tai = Danh_sach_cua_hang.head

    while node_hien_tai is not None:
        san_pham = node_hien_tai.data
        gia_ban = san_pham.tinh_gia_ban()

        # Tìm mặt hàng đắt nhất
        if mat_hang_dat_nhat is None or gia_ban > mat_hang_dat_nhat['gia_ban']:
            mat_hang_dat_nhat = san_pham.chuyen_thanh_dict()

        # Tìm mặt hàng rẻ nhất
        if mat_hang_re_nhat is None or gia_ban < mat_hang_re_nhat['gia_ban']:
            mat_hang_re_nhat = san_pham.chuyen_thanh_dict()

        # Đếm mặt hàng sắp hết (tồn kho <= 10)
        if san_pham.ton_kho <= 10:
            so_mat_hang_sap_het += 1

        # Tính tổng giá trị tồn kho
        tong_gia_tri_ton_kho += gia_ban * san_pham.ton_kho

        # Thống kê theo loại hàng
        loai = san_pham.loai_hang
        if loai not in thong_ke_theo_loai:
            thong_ke_theo_loai[loai] = {'so_luong': 0, 'tong_ton_kho': 0}
        thong_ke_theo_loai[loai]['so_luong'] += 1
        thong_ke_theo_loai[loai]['tong_ton_kho'] += san_pham.ton_kho

        node_hien_tai = node_hien_tai.next

    return JsonResponse({
        'trang_thai': 'thanh_cong',
        'thong_ke': {
            'tong_so_luong': tong_so_luong,
            'mat_hang_dat_nhat': mat_hang_dat_nhat,
            'mat_hang_re_nhat': mat_hang_re_nhat,
            'so_mat_hang_sap_het': so_mat_hang_sap_het,
            'tong_gia_tri_ton_kho': tong_gia_tri_ton_kho,
            'thong_ke_theo_loai': thong_ke_theo_loai
        }
    })


# ============================================================
# API: GIỎ HÀNG (Queue)
# ============================================================

@csrf_exempt
@require_http_methods(["POST"])
def them_gio_hang(request):
    """
    API POST /them-gio-hang
    Thêm một mặt hàng vào giỏ hàng (Hàng đợi).

    Luồng hoạt động:
        1. Nhận mã số sản phẩm.
        2. Tìm sản phẩm trong danh sách liên kết đôi.
        3. Thêm vào hàng đợi Giỏ hàng.
    """
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()

    try:
        du_lieu = json.loads(request.body)
        ma_so = du_lieu.get('ma_so', '').strip()

        if not ma_so:
            return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Mã số không được để trống.'}, status=400)

        # Tìm sản phẩm trong danh sách
        san_pham = Danh_sach_cua_hang.tim_theo_ma(ma_so)
        if san_pham is None:
            return JsonResponse({'trang_thai': 'loi', 'thong_bao': f'Không tìm thấy sản phẩm mã {ma_so}.'}, status=404)

        # Kiểm tra đã có trong giỏ hàng chưa
        danh_sach_gio = Gio_hang.xem_danh_sach()
        for sp in danh_sach_gio:
            if sp.get('ma_so') == ma_so:
                return JsonResponse({'trang_thai': 'loi', 'thong_bao': f'Sản phẩm "{san_pham.ten_san_pham}" đã có trong giỏ hàng.'}, status=400)

        # Thêm vào hàng đợi
        Gio_hang.them_vao(san_pham)

        return JsonResponse({
            'trang_thai': 'thanh_cong',
            'thong_bao': f'Đã thêm "{san_pham.ten_san_pham}" vào giỏ hàng.'
        })

    except json.JSONDecodeError:
        return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Dữ liệu gửi lên không hợp lệ.'}, status=400)


def xem_gio_hang(request):
    """
    API GET /xem-gio-hang
    Xem danh sách các mặt hàng trong giỏ hàng.
    """
    if Gio_hang is None:
        khoi_tao_danh_sach()

    danh_sach_gio = Gio_hang.xem_danh_sach()

    # Tính tổng tiền giỏ hàng
    tong_tien = 0
    for sp in danh_sach_gio:
        tong_tien += sp.get('gia_ban', 0)

    return JsonResponse({
        'trang_thai': 'thanh_cong',
        'so_luong': Gio_hang.so_luong,
        'gio_hang': danh_sach_gio,
        'tong_tien': tong_tien
    })


@csrf_exempt
@require_http_methods(["POST"])
def xoa_gio_hang(request):
    """
    API POST /xoa-gio-hang
    Xóa một mặt hàng khỏi giỏ hàng theo mã số.
    """
    if Gio_hang is None:
        khoi_tao_danh_sach()

    try:
        du_lieu = json.loads(request.body)
        ma_so = du_lieu.get('ma_so', '').strip()

        ket_qua = Gio_hang.xoa_theo_ma(ma_so)

        if ket_qua:
            return JsonResponse({'trang_thai': 'thanh_cong', 'thong_bao': f'Đã xóa sản phẩm mã {ma_so} khỏi giỏ hàng.'})
        else:
            return JsonResponse({'trang_thai': 'loi', 'thong_bao': f'Không tìm thấy sản phẩm mã {ma_so} trong giỏ hàng.'}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Dữ liệu gửi lên không hợp lệ.'}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def thanh_toan(request):
    """
    API POST /thanh-toan
    Thanh toán toàn bộ giỏ hàng.

    Luồng hoạt động:
        1. Lấy từng mặt hàng từ hàng đợi (FIFO).
        2. Giảm số lượng tồn kho tương ứng.
        3. Cập nhật vào SQLite.
        4. Xóa giỏ hàng sau khi thanh toán xong.
    """
    if Gio_hang is None:
        khoi_tao_danh_sach()

    if Gio_hang.rong():
        return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Giỏ hàng đang trống.'}, status=400)

    danh_sach_da_mua = []
    tong_tien = 0

    # Lấy từng mặt hàng từ hàng đợi (FIFO)
    while not Gio_hang.rong():
        san_pham = Gio_hang.lay_ra()
        if san_pham is not None:
            # Giảm tồn kho đi 1
            if san_pham.ton_kho > 0:
                san_pham.ton_kho -= 1
                # Cập nhật vào SQLite
                from .loi_thuat_toan.ket_noi_sqlite import cap_nhat_san_pham
                cap_nhat_san_pham(san_pham)

            tong_tien += san_pham.tinh_gia_ban()
            danh_sach_da_mua.append(san_pham.chuyen_thanh_dict())

    return JsonResponse({
        'trang_thai': 'thanh_cong',
        'thong_bao': f'Thanh toán thành công! Tổng tiền: {tong_tien:,.0f}đ',
        'danh_sach_da_mua': danh_sach_da_mua,
        'tong_tien': tong_tien
    })


# ============================================================
# API: UNDO / REDO (Stack)
# ============================================================

@csrf_exempt
@require_http_methods(["POST"])
def hoan_tac(request):
    """
    API POST /hoan-tac
    Hoàn tác thao tác gần nhất (Undo).

    Luồng hoạt động:
        1. Lấy thao tác gần nhất từ Stack Undo.
        2. Tùy loại thao tác (them/sua/xoa) mà hoàn tác tương ứng.
        3. Đẩy thao tác vào Stack Redo.
    """
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()

    thao_tac = Ngan_xep_hoan_tac.lay_ra()

    if thao_tac is None:
        return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Không có thao tác nào để hoàn tác.'}, status=400)

    loai_thao_tac = thao_tac.get('thao_tac', '')

    try:
        if loai_thao_tac == 'them':
            # Hoàn tác thao tác THÊM → Xóa sản phẩm vừa thêm
            ma_so = thao_tac['ma_so']
            san_pham = Danh_sach_cua_hang.tim_theo_ma(ma_so)
            if san_pham:
                du_lieu_cu = san_pham.chuyen_thanh_dict()
                Danh_sach_cua_hang.xoa_node(ma_so)
                from .loi_thuat_toan.ket_noi_sqlite import xoa_mot_san_pham
                xoa_mot_san_pham(ma_so)
                Ngan_xep_lam_lai.day_vao({'thao_tac': 'them', 'du_lieu_cu': du_lieu_cu})
                return JsonResponse({'trang_thai': 'thanh_cong', 'thong_bao': f'Đã hoàn tác: Xóa sản phẩm mã {ma_so}.'})

        elif loai_thao_tac == 'xoa':
            # Hoàn tác thao tác XÓA → Thêm lại sản phẩm đã xóa
            du_lieu_cu = thao_tac['du_lieu_cu']
            from .loi_thuat_toan.lop_doi_tuong import Sach, TapChi, BaoGiay, LuanVan, BanThao

            loai_hang = du_lieu_cu['loai_hang']
            if loai_hang == 'Sách':
                san_pham = Sach(du_lieu_cu['ma_so'], du_lieu_cu['ten_san_pham'],
                                du_lieu_cu['gia_co_ban'], du_lieu_cu['ton_kho'],
                                du_lieu_cu.get('tac_gia', ''), du_lieu_cu.get('nha_xuat_ban', ''))
            elif loai_hang == 'Tạp chí':
                san_pham = TapChi(du_lieu_cu['ma_so'], du_lieu_cu['ten_san_pham'],
                                  du_lieu_cu['gia_co_ban'], du_lieu_cu['ton_kho'],
                                  du_lieu_cu.get('so_phat_hanh', ''))
            elif loai_hang == 'Báo giấy':
                san_pham = BaoGiay(du_lieu_cu['ma_so'], du_lieu_cu['ten_san_pham'],
                                   du_lieu_cu['gia_co_ban'], du_lieu_cu['ton_kho'],
                                   du_lieu_cu.get('ngay_xuat_ban', ''))
            elif loai_hang == 'Luận văn':
                san_pham = LuanVan(du_lieu_cu['ma_so'], du_lieu_cu['ten_san_pham'],
                                   du_lieu_cu['gia_co_ban'], du_lieu_cu['ton_kho'],
                                   du_lieu_cu.get('tac_gia', ''), du_lieu_cu.get('truong_dai_hoc', ''))
            elif loai_hang == 'Bản thảo':
                san_pham = BanThao(du_lieu_cu['ma_so'], du_lieu_cu['ten_san_pham'],
                                   du_lieu_cu['gia_co_ban'], du_lieu_cu['ton_kho'],
                                   du_lieu_cu.get('tac_gia', ''), du_lieu_cu.get('trang_thai', 'Chưa duyệt'))
            else:
                return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Không thể hoàn tác: loại hàng không xác định.'}, status=400)

            Danh_sach_cua_hang.them_vao_cuoi(san_pham)
            from .loi_thuat_toan.ket_noi_sqlite import luu_mot_san_pham
            luu_mot_san_pham(san_pham)
            Ngan_xep_lam_lai.day_vao({'thao_tac': 'xoa', 'ma_so': du_lieu_cu['ma_so']})
            return JsonResponse({'trang_thai': 'thanh_cong', 'thong_bao': f'Đã hoàn tác: Thêm lại sản phẩm "{du_lieu_cu["ten_san_pham"]}".'})

        elif loai_thao_tac == 'sua':
            # Hoàn tác thao tác SỬA → Khôi phục dữ liệu cũ
            du_lieu_cu = thao_tac['du_lieu_cu']
            san_pham = Danh_sach_cua_hang.tim_theo_ma(du_lieu_cu['ma_so'])
            if san_pham:
                # Lưu dữ liệu hiện tại vào Stack Redo trước khi khôi phục
                du_lieu_hien_tai = san_pham.chuyen_thanh_dict()
                Ngan_xep_lam_lai.day_vao({'thao_tac': 'sua', 'du_lieu_cu': du_lieu_hien_tai})

                # Khôi phục dữ liệu cũ
                san_pham.ten_san_pham = du_lieu_cu['ten_san_pham']
                san_pham.gia_co_ban = du_lieu_cu['gia_co_ban']
                san_pham.ton_kho = du_lieu_cu['ton_kho']

                # Khôi phục thuộc tính riêng
                if san_pham.loai_hang == 'Sách':
                    san_pham.tac_gia = du_lieu_cu.get('tac_gia', '')
                    san_pham.nha_xuat_ban = du_lieu_cu.get('nha_xuat_ban', '')
                elif san_pham.loai_hang == 'Tạp chí':
                    san_pham.so_phat_hanh = du_lieu_cu.get('so_phat_hanh', '')
                elif san_pham.loai_hang == 'Báo giấy':
                    san_pham.ngay_xuat_ban = du_lieu_cu.get('ngay_xuat_ban', '')
                elif san_pham.loai_hang == 'Luận văn':
                    san_pham.tac_gia = du_lieu_cu.get('tac_gia', '')
                    san_pham.truong_dai_hoc = du_lieu_cu.get('truong_dai_hoc', '')
                elif san_pham.loai_hang == 'Bản thảo':
                    san_pham.tac_gia = du_lieu_cu.get('tac_gia', '')
                    san_pham.trang_thai = du_lieu_cu.get('trang_thai', 'Chưa duyệt')

                from .loi_thuat_toan.ket_noi_sqlite import cap_nhat_san_pham
                cap_nhat_san_pham(san_pham)
                return JsonResponse({'trang_thai': 'thanh_cong', 'thong_bao': f'Đã hoàn tác: Khôi phục thông tin "{san_pham.ten_san_pham}".'})

        return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Không thể hoàn tác thao tác này.'}, status=400)

    except Exception as loi:
        return JsonResponse({'trang_thai': 'loi', 'thong_bao': f'Lỗi khi hoàn tác: {str(loi)}'}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def lam_lai(request):
    """
    API POST /lam-lai
    Làm lại thao tác vừa hoàn tác (Redo).

    Luồng hoạt động:
        1. Lấy thao tác gần nhất từ Stack Redo.
        2. Thực hiện lại thao tác đó.
        3. Đẩy thao tác vào Stack Undo.
    """
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()

    thao_tac = Ngan_xep_lam_lai.lay_ra()

    if thao_tac is None:
        return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Không có thao tác nào để làm lại.'}, status=400)

    loai_thao_tac = thao_tac.get('thao_tac', '')

    try:
        if loai_thao_tac == 'them':
            # Làm lại thao tác THÊM
            du_lieu_cu = thao_tac['du_lieu_cu']
            from .loi_thuat_toan.lop_doi_tuong import Sach, TapChi, BaoGiay, LuanVan, BanThao

            loai_hang = du_lieu_cu['loai_hang']
            if loai_hang == 'Sách':
                san_pham = Sach(du_lieu_cu['ma_so'], du_lieu_cu['ten_san_pham'],
                                du_lieu_cu['gia_co_ban'], du_lieu_cu['ton_kho'],
                                du_lieu_cu.get('tac_gia', ''), du_lieu_cu.get('nha_xuat_ban', ''))
            elif loai_hang == 'Tạp chí':
                san_pham = TapChi(du_lieu_cu['ma_so'], du_lieu_cu['ten_san_pham'],
                                  du_lieu_cu['gia_co_ban'], du_lieu_cu['ton_kho'],
                                  du_lieu_cu.get('so_phat_hanh', ''))
            elif loai_hang == 'Báo giấy':
                san_pham = BaoGiay(du_lieu_cu['ma_so'], du_lieu_cu['ten_san_pham'],
                                   du_lieu_cu['gia_co_ban'], du_lieu_cu['ton_kho'],
                                   du_lieu_cu.get('ngay_xuat_ban', ''))
            elif loai_hang == 'Luận văn':
                san_pham = LuanVan(du_lieu_cu['ma_so'], du_lieu_cu['ten_san_pham'],
                                   du_lieu_cu['gia_co_ban'], du_lieu_cu['ton_kho'],
                                   du_lieu_cu.get('tac_gia', ''), du_lieu_cu.get('truong_dai_hoc', ''))
            elif loai_hang == 'Bản thảo':
                san_pham = BanThao(du_lieu_cu['ma_so'], du_lieu_cu['ten_san_pham'],
                                   du_lieu_cu['gia_co_ban'], du_lieu_cu['ton_kho'],
                                   du_lieu_cu.get('tac_gia', ''), du_lieu_cu.get('trang_thai', 'Chưa duyệt'))
            else:
                return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Không thể làm lại.'}, status=400)

            Danh_sach_cua_hang.them_vao_cuoi(san_pham)
            from .loi_thuat_toan.ket_noi_sqlite import luu_mot_san_pham
            luu_mot_san_pham(san_pham)
            Ngan_xep_hoan_tac.day_vao({'thao_tac': 'them', 'ma_so': du_lieu_cu['ma_so']})
            return JsonResponse({'trang_thai': 'thanh_cong', 'thong_bao': f'Đã làm lại: Thêm sản phẩm "{du_lieu_cu["ten_san_pham"]}".'})

        elif loai_thao_tac == 'xoa':
            # Làm lại thao tác XÓA
            ma_so = thao_tac['ma_so']
            san_pham = Danh_sach_cua_hang.tim_theo_ma(ma_so)
            if san_pham:
                du_lieu_cu = san_pham.chuyen_thanh_dict()
                Danh_sach_cua_hang.xoa_node(ma_so)
                from .loi_thuat_toan.ket_noi_sqlite import xoa_mot_san_pham
                xoa_mot_san_pham(ma_so)
                Ngan_xep_hoan_tac.day_vao({'thao_tac': 'xoa', 'du_lieu_cu': du_lieu_cu})
                return JsonResponse({'trang_thai': 'thanh_cong', 'thong_bao': f'Đã làm lại: Xóa sản phẩm mã {ma_so}.'})

        elif loai_thao_tac == 'sua':
            # Làm lại thao tác SỬA
            du_lieu_cu = thao_tac['du_lieu_cu']
            san_pham = Danh_sach_cua_hang.tim_theo_ma(du_lieu_cu['ma_so'])
            if san_pham:
                du_lieu_hien_tai = san_pham.chuyen_thanh_dict()
                Ngan_xep_hoan_tac.day_vao({'thao_tac': 'sua', 'du_lieu_cu': du_lieu_hien_tai})

                san_pham.ten_san_pham = du_lieu_cu['ten_san_pham']
                san_pham.gia_co_ban = du_lieu_cu['gia_co_ban']
                san_pham.ton_kho = du_lieu_cu['ton_kho']

                if san_pham.loai_hang == 'Sách':
                    san_pham.tac_gia = du_lieu_cu.get('tac_gia', '')
                    san_pham.nha_xuat_ban = du_lieu_cu.get('nha_xuat_ban', '')
                elif san_pham.loai_hang == 'Tạp chí':
                    san_pham.so_phat_hanh = du_lieu_cu.get('so_phat_hanh', '')
                elif san_pham.loai_hang == 'Báo giấy':
                    san_pham.ngay_xuat_ban = du_lieu_cu.get('ngay_xuat_ban', '')
                elif san_pham.loai_hang == 'Luận văn':
                    san_pham.tac_gia = du_lieu_cu.get('tac_gia', '')
                    san_pham.truong_dai_hoc = du_lieu_cu.get('truong_dai_hoc', '')
                elif san_pham.loai_hang == 'Bản thảo':
                    san_pham.tac_gia = du_lieu_cu.get('tac_gia', '')
                    san_pham.trang_thai = du_lieu_cu.get('trang_thai', 'Chưa duyệt')

                from .loi_thuat_toan.ket_noi_sqlite import cap_nhat_san_pham
                cap_nhat_san_pham(san_pham)
                return JsonResponse({'trang_thai': 'thanh_cong', 'thong_bao': f'Đã làm lại: Cập nhật thông tin "{san_pham.ten_san_pham}".'})

        return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Không thể làm lại thao tác này.'}, status=400)

    except Exception as loi:
        return JsonResponse({'trang_thai': 'loi', 'thong_bao': f'Lỗi khi làm lại: {str(loi)}'}, status=500)
