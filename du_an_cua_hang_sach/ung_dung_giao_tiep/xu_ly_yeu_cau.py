"""
Tệp xử lý yêu cầu HTTP (Views) cho ứng dụng Django.

Tất cả endpoint được tổ chức thành 7 nhóm theo barem chấm điểm:
    1) Đăng nhập / Đăng xuất / Phân quyền  (Admin / Nhân viên)
    2) Đọc danh sách                        (GET /danh-sach)
    3) Thêm sản phẩm                        (POST /them-san-pham)
    4) Sửa sản phẩm                         (POST /sua-san-pham)
    5) Xóa sản phẩm                         (POST /xoa-san-pham)   ← CHỈ ADMIN
    6) Tìm kiếm + Sắp xếp                   (GET /tim-kiem, /sap-xep)
    7) Thống kê                             (GET /thong-ke)
    8) Undo/Redo  (Stack LIFO)              (POST /hoan-tac, /lam-lai)
    9) Giỏ hàng  (Queue FIFO)               (POST /them-gio-hang, /xem-gio-hang,
                                              /xoa-gio-hang, /thanh-toan)

Mỗi nhóm đều bọc try/except để bắt lỗi theo yêu cầu của barem.
"""

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

# Biến toàn cục giữ Danh sách liên kết đôi + Undo/Redo + Giỏ hàng
Danh_sach_cua_hang = None
Bo_undoredo        = None
Gio_hang_hien_tai  = None


# ============================================================
# KHỞI TẠO HỆ THỐNG
# ============================================================

def khoi_tao_danh_sach():
    """Khởi tạo DSLK đôi + Undo/Redo + Giỏ hàng; nạp dữ liệu từ SQLite."""
    global Danh_sach_cua_hang, Bo_undoredo, Gio_hang_hien_tai
    from .loi_thuat_toan.danh_sach_lien_ket import DoublyLinkedList
    from .loi_thuat_toan.cau_truc_du_lieu import NganXep, HangDoi
    from .loi_thuat_toan.ket_noi_sqlite import tai_du_lieu, tao_du_lieu_mau_neu_rong
    from .loi_thuat_toan.nguoi_dung import khoi_tao_nguoi_dung_mac_dinh

    # Bảng SQLite + dữ liệu mẫu + tài khoản mẫu (chỉ tạo lần đầu)
    tao_du_lieu_mau_neu_rong()

    Danh_sach_cua_hang = DoublyLinkedList()
    tai_du_lieu(Danh_sach_cua_hang)

    # 2 Stack cho Undo/Redo
    ngan_xep_undo = NganXep()
    ngan_xep_redo = NganXep()
    Bo_undoredo = {'undo': ngan_xep_undo, 'redo': ngan_xep_redo}

    # 1 Queue cho Giỏ hàng
    Gio_hang_hien_tai = HangDoi()

    # Tạo 2 tài khoản mẫu nếu chưa có
    khoi_tao_nguoi_dung_mac_dinh()

    try:
        print(f'[KHOI DONG] Da nap {Danh_sach_cua_hang.so_luong} mat hang vao danh sach lien ket doi.')
    except UnicodeEncodeError:
        print(f'[KHOI DONG] Da nap {Danh_sach_cua_hang.so_luong} mat hang.')


# ============================================================
# NHÓM 1: ĐĂNG NHẬP / ĐĂNG XUẤT / PHÂN QUYỀN
# ============================================================

def trang_chu(request):
    """Trang chủ - nếu chưa đăng nhập thì chuyển sang trang đăng nhập."""
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()
    # Nếu chưa đăng nhập → chuyển tới trang đăng nhập
    if 'ten_dang_nhap' not in request.session:
        return redirect('/dang-nhap')
    # Lưu thông tin người dùng để template dùng
    request.session['nguoi_dung'] = {
        'ten_dang_nhap': request.session.get('ten_dang_nhap'),
        'ho_ten':        request.session.get('ho_ten', ''),
        'vai_tro':       request.session.get('vai_tro', 'nhan_vien'),
        'la_admin':      request.session.get('vai_tro', 'nhan_vien') == 'admin'
    }
    return render(request, 'trang_chu.html')


def trang_dang_nhap(request):
    """Hiển thị form đăng nhập."""
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()
    # Nếu đã đăng nhập rồi thì về trang chủ
    if 'ten_dang_nhap' in request.session:
        return redirect('/')
    return render(request, 'dang_nhap.html')


@csrf_exempt
@require_http_methods(['POST'])
def xu_ly_dang_nhap(request):
    """API POST /dang-nhap - kiểm tra tài khoản và lưu session."""
    try:
        du_lieu = json.loads(request.body)
        ten_dang_nhap = du_lieu.get('ten_dang_nhap', '').strip()
        mat_khau      = du_lieu.get('mat_khau', '').strip()

        if not ten_dang_nhap or not mat_khau:
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': 'Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.'},
                status=400
            )

        from .loi_thuat_toan.nguoi_dung import kiem_tra_dang_nhap
        nguoi_dung = kiem_tra_dang_nhap(ten_dang_nhap, mat_khau)

        if nguoi_dung is None:
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': 'Sai tên đăng nhập hoặc mật khẩu.'},
                status=401
            )

        # Lưu thông tin vào session
        request.session['ten_dang_nhap'] = nguoi_dung.ten_dang_nhap
        request.session['ho_ten']        = nguoi_dung.ho_ten
        request.session['vai_tro']       = nguoi_dung.vai_tro

        return JsonResponse({
            'trang_thai': 'thanh_cong',
            'thong_bao':  f'Chào mừng {nguoi_dung.ho_ten}!',
            'nguoi_dung': nguoi_dung.chuyen_thanh_dict()
        })
    except json.JSONDecodeError:
        return JsonResponse(
            {'trang_thai': 'loi', 'thong_bao': 'Dữ liệu gửi lên không hợp lệ.'},
            status=400
        )
    except Exception as loi:
        return JsonResponse(
            {'trang_thai': 'loi', 'thong_bao': f'Lỗi máy chủ: {str(loi)}'},
            status=500
        )


@csrf_exempt
@require_http_methods(['POST', 'GET'])
def xu_ly_dang_xuat(request):
    """API /dang-xuat - xóa session và quay về trang đăng nhập."""
    try:
        # Xóa toàn bộ session
        request.session.flush()
        if request.method == 'GET':
            return redirect('/dang-nhap')
        return JsonResponse({
            'trang_thai': 'thanh_cong',
            'thong_bao':  'Đã đăng xuất thành công.'
        })
    except Exception as loi:
        return JsonResponse(
            {'trang_thai': 'loi', 'thong_bao': f'Lỗi khi đăng xuất: {str(loi)}'},
            status=500
        )


def thong_tin_nguoi_dung(request):
    """API GET /nguoi-dung - trả về thông tin người dùng đang đăng nhập."""
    try:
        if 'ten_dang_nhap' not in request.session:
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': 'Chưa đăng nhập.'},
                status=401
            )
        return JsonResponse({
            'trang_thai': 'thanh_cong',
            'nguoi_dung': {
                'ten_dang_nhap': request.session.get('ten_dang_nhap'),
                'ho_ten':        request.session.get('ho_ten', ''),
                'vai_tro':       request.session.get('vai_tro', 'nhan_vien'),
                'la_admin':      request.session.get('vai_tro', 'nhan_vien') == 'admin'
            }
        })
    except Exception as loi:
        return JsonResponse(
            {'trang_thai': 'loi', 'thong_bao': f'Lỗi máy chủ: {str(loi)}'},
            status=500
        )


def la_admin(request):
    """Hàm tiện ích - kiểm tra request hiện tại có phải admin không."""
    return request.session.get('vai_tro', 'nhan_vien') == 'admin'


# ============================================================
# NHÓM 2: ĐỌC DANH SÁCH
# ============================================================

def lay_danh_sach(request):
    """API GET /danh-sach - trả về toàn bộ mặt hàng dưới dạng JSON."""
    try:
        if Danh_sach_cua_hang is None:
            khoi_tao_danh_sach()
        danh_sach = Danh_sach_cua_hang.chuyen_thanh_danh_sach()
        return JsonResponse({
            'trang_thai': 'thanh_cong',
            'so_luong':   Danh_sach_cua_hang.so_luong,
            'danh_sach':  danh_sach
        })
    except Exception as loi:
        return JsonResponse(
            {'trang_thai': 'loi', 'thong_bao': f'Lỗi khi tải danh sách: {str(loi)}'},
            status=500
        )


# ============================================================
# NHÓM 3: THÊM SẢN PHẨM
# ============================================================

@csrf_exempt
@require_http_methods(['POST'])
def them_san_pham(request):
    """API POST /them-san-pham - thêm một sản phẩm mới (hỗ trợ 5 loại)."""
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()
    try:
        du_lieu        = json.loads(request.body)
        loai_hang      = du_lieu.get('loai_hang', '').strip()
        ma_so          = du_lieu.get('ma_so', '').strip()
        ten_san_pham   = du_lieu.get('ten_san_pham', '').strip()
        gia_co_ban     = float(du_lieu.get('gia_co_ban', 0))
        ton_kho        = int(du_lieu.get('ton_kho', 0))

        # --- Validate dữ liệu ---
        if not ma_so or not ten_san_pham or not loai_hang:
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': 'Vui lòng điền đầy đủ thông tin.'},
                status=400
            )
        if gia_co_ban < 0:
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': 'Giá cơ bản không được âm.'},
                status=400
            )
        if ton_kho < 0:
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': 'Số lượng tồn kho không được âm.'},
                status=400
            )

        # --- Kiểm tra trùng mã ---
        if Danh_sach_cua_hang.tim_theo_ma_so(ma_so) is not None:
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': f'Mã số "{ma_so}" đã tồn tại.'},
                status=400
            )

        # --- Tạo đối tượng theo loại hàng (đa hình OOP) ---
        from .loi_thuat_toan.lop_doi_tuong import Sach, TapChi, BaoGiay, LuanVan, BanThao

        if loai_hang == 'Sách':
            tac_gia       = du_lieu.get('tac_gia', '').strip()
            nha_xuat_ban  = du_lieu.get('nha_xuat_ban', '').strip()
            if not tac_gia or not nha_xuat_ban:
                return JsonResponse(
                    {'trang_thai': 'loi', 'thong_bao': 'Vui lòng nhập tác giả và nhà xuất bản.'},
                    status=400
                )
            san_pham_moi = Sach(ma_so, ten_san_pham, gia_co_ban, ton_kho, tac_gia, nha_xuat_ban)

        elif loai_hang == 'Tạp chí':
            so_phat_hanh = du_lieu.get('so_phat_hanh', '').strip()
            if not so_phat_hanh:
                return JsonResponse(
                    {'trang_thai': 'loi', 'thong_bao': 'Vui lòng nhập số phát hành.'},
                    status=400
                )
            san_pham_moi = TapChi(ma_so, ten_san_pham, gia_co_ban, ton_kho, so_phat_hanh)

        elif loai_hang == 'Báo giấy':
            ngay_xuat_ban = du_lieu.get('ngay_xuat_ban', '').strip()
            if not ngay_xuat_ban:
                return JsonResponse(
                    {'trang_thai': 'loi', 'thong_bao': 'Vui lòng nhập ngày xuất bản.'},
                    status=400
                )
            san_pham_moi = BaoGiay(ma_so, ten_san_pham, gia_co_ban, ton_kho, ngay_xuat_ban)

        elif loai_hang == 'Luận văn':
            tac_gia        = du_lieu.get('tac_gia', '').strip()
            truong_dai_hoc = du_lieu.get('truong_dai_hoc', '').strip()
            if not tac_gia or not truong_dai_hoc:
                return JsonResponse(
                    {'trang_thai': 'loi', 'thong_bao': 'Vui lòng nhập tác giả và trường đại học.'},
                    status=400
                )
            san_pham_moi = LuanVan(ma_so, ten_san_pham, gia_co_ban, ton_kho,
                                   tac_gia, truong_dai_hoc, '')
        elif loai_hang == 'Bản thảo':
            tac_gia    = du_lieu.get('tac_gia', '').strip()
            trang_thai = du_lieu.get('trang_thai', 'Chưa duyệt').strip()
            if not tac_gia:
                return JsonResponse(
                    {'trang_thai': 'loi', 'thong_bao': 'Vui lòng nhập tác giả.'},
                    status=400
                )
            san_pham_moi = BanThao(ma_so, ten_san_pham, gia_co_ban, ton_kho,
                                   tac_gia, trang_thai)
        else:
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': 'Loại hàng không hợp lệ.'},
                status=400
            )

        # --- Thêm vào DSLK + SQLite ---
        Danh_sach_cua_hang.them_vao_cuoi(san_pham_moi)
        from .loi_thuat_toan.ket_noi_sqlite import luu_mot_san_pham
        luu_mot_san_pham(san_pham_moi)

        # --- Ghi vào Stack Undo ---
        Bo_undoredo['undo'].day_vao({
            'loai':        'them',
            'du_lieu_cu':  None,
            'du_lieu_moi': san_pham_moi.chuyen_thanh_dict()
        })
        Bo_undoredo['redo'].xoa_tat_ca()  # Có thao tác mới → xóa Redo

        return JsonResponse({
            'trang_thai': 'thanh_cong',
            'thong_bao':  f'Đã thêm "{ten_san_pham}" vào cửa hàng.'
        })

    except json.JSONDecodeError:
        return JsonResponse(
            {'trang_thai': 'loi', 'thong_bao': 'Dữ liệu gửi lên không hợp lệ.'},
            status=400
        )
    except ValueError:
        return JsonResponse(
            {'trang_thai': 'loi', 'thong_bao': 'Giá hoặc số lượng phải là số.'},
            status=400
        )
    except Exception as loi:
        return JsonResponse(
            {'trang_thai': 'loi', 'thong_bao': f'Lỗi máy chủ: {str(loi)}'},
            status=500
        )


# ============================================================
# NHÓM 4: SỬA SẢN PHẨM
# ============================================================

@csrf_exempt
@require_http_methods(['POST'])
def sua_san_pham(request):
    """API POST /sua-san-pham - cập nhật thông tin sản phẩm."""
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()
    try:
        du_lieu      = json.loads(request.body)
        ma_so        = du_lieu.get('ma_so', '').strip()
        ten_san_pham = du_lieu.get('ten_san_pham', '').strip()
        gia_co_ban   = float(du_lieu.get('gia_co_ban', 0))
        ton_kho      = int(du_lieu.get('ton_kho', 0))

        if not ma_so:
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': 'Mã số không được để trống.'},
                status=400
            )

        # Tìm sản phẩm hiện tại để lưu dữ liệu cũ (cho Undo)
        san_pham_cu = Danh_sach_cua_hang.tim_theo_ma_so(ma_so)
        if san_pham_cu is None:
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': f'Không tìm thấy sản phẩm mã {ma_so}.'},
                status=404
            )

        du_lieu_cu = san_pham_cu.chuyen_thanh_dict()

        # Cập nhật các trường chung
        du_lieu_moi = {
            'ten_san_pham': ten_san_pham,
            'gia_co_ban':   gia_co_ban,
            'ton_kho':      ton_kho
        }

        # Cập nhật các trường riêng theo loại
        loai_hang = san_pham_cu.loai_hang
        if loai_hang == 'Sách':
            du_lieu_moi['tac_gia']       = du_lieu.get('tac_gia', '').strip()
            du_lieu_moi['nha_xuat_ban']  = du_lieu.get('nha_xuat_ban', '').strip()
        elif loai_hang == 'Tạp chí':
            du_lieu_moi['so_phat_hanh']  = du_lieu.get('so_phat_hanh', '').strip()
        elif loai_hang == 'Báo giấy':
            du_lieu_moi['ngay_xuat_ban'] = du_lieu.get('ngay_xuat_ban', '').strip()
        elif loai_hang == 'Luận văn':
            du_lieu_moi['tac_gia']        = du_lieu.get('tac_gia', '').strip()
            du_lieu_moi['truong_dai_hoc'] = du_lieu.get('truong_dai_hoc', '').strip()
        elif loai_hang == 'Bản thảo':
            du_lieu_moi['tac_gia']    = du_lieu.get('tac_gia', '').strip()
            du_lieu_moi['tinh_trang'] = du_lieu.get('trang_thai', '').strip()

        Danh_sach_cua_hang.cap_nhat_node(ma_so, du_lieu_moi)
        from .loi_thuat_toan.ket_noi_sqlite import cap_nhat_san_pham
        cap_nhat_san_pham(san_pham_cu)

        # Ghi Undo
        Bo_undoredo['undo'].day_vao({
            'loai':        'sua',
            'du_lieu_cu':  du_lieu_cu,
            'du_lieu_moi': san_pham_cu.chuyen_thanh_dict()
        })
        Bo_undoredo['redo'].xoa_tat_ca()

        return JsonResponse({
            'trang_thai': 'thanh_cong',
            'thong_bao':  f'Đã cập nhật sản phẩm "{ten_san_pham}".'
        })

    except json.JSONDecodeError:
        return JsonResponse(
            {'trang_thai': 'loi', 'thong_bao': 'Dữ liệu gửi lên không hợp lệ.'},
            status=400
        )
    except ValueError:
        return JsonResponse(
            {'trang_thai': 'loi', 'thong_bao': 'Giá hoặc số lượng phải là số.'},
            status=400
        )
    except Exception as loi:
        return JsonResponse(
            {'trang_thai': 'loi', 'thong_bao': f'Lỗi máy chủ: {str(loi)}'},
            status=500
        )


# ============================================================
# NHÓM 5: XÓA SẢN PHẨM (CHỈ ADMIN)
# ============================================================

@csrf_exempt
@require_http_methods(['POST'])
def xoa_san_pham(request):
    """API POST /xoa-san-pham - xóa sản phẩm. CHỈ ADMIN mới được xóa."""
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()

    # --- Kiểm tra phân quyền ---
    if not la_admin(request):
        return JsonResponse(
            {'trang_thai': 'loi', 'thong_bao': 'BẠN LÀ NHÂN VIÊN - KHÔNG ĐƯỢC PHÉP XÓA SẢN PHẨM.'},
            status=403
        )

    try:
        du_lieu = json.loads(request.body)
        ma_so   = du_lieu.get('ma_so', '').strip()
        if not ma_so:
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': 'Mã số không được để trống.'},
                status=400
            )

        # Lưu dữ liệu cũ trước khi xóa (để Undo)
        san_pham_cu = Danh_sach_cua_hang.tim_theo_ma_so(ma_so)
        if san_pham_cu is None:
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': f'Không tìm thấy sản phẩm mã {ma_so}.'},
                status=404
            )
        du_lieu_cu = san_pham_cu.chuyen_thanh_dict()

        # Xóa khỏi DSLK + SQLite
        ket_qua = Danh_sach_cua_hang.xoa_node(ma_so)
        if ket_qua:
            from .loi_thuat_toan.ket_noi_sqlite import xoa_mot_san_pham
            xoa_mot_san_pham(ma_so)

            # Ghi Undo
            Bo_undoredo['undo'].day_vao({
                'loai':       'xoa',
                'du_lieu_cu': du_lieu_cu,
                'du_lieu_moi': None
            })
            Bo_undoredo['redo'].xoa_tat_ca()

            return JsonResponse({
                'trang_thai': 'thanh_cong',
                'thong_bao':  f'Đã xóa sản phẩm mã {ma_so}.'
            })
        else:
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': f'Không tìm thấy sản phẩm mã {ma_so}.'},
                status=404
            )

    except json.JSONDecodeError:
        return JsonResponse(
            {'trang_thai': 'loi', 'thong_bao': 'Dữ liệu gửi lên không hợp lệ.'},
            status=400
        )
    except Exception as loi:
        return JsonResponse(
            {'trang_thai': 'loi', 'thong_bao': f'Lỗi máy chủ: {str(loi)}'},
            status=500
        )


# ============================================================
# NHÓM 6: TÌM KIẾM + SẮP XẾP
# ============================================================

def tim_kiem_san_pham(request):
    """API GET /tim-kiem - tìm kiếm nâng cao (tên / mã / loại)."""
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()
    try:
        tu_khoa   = request.GET.get('tu_khoa', '').strip()
        tieu_chi  = request.GET.get('tieu_chi', 'ten').strip()

        if tieu_chi == 'ma':
            ket_qua = []
            sp = Danh_sach_cua_hang.tim_theo_ma_so(tu_khoa)
            if sp:
                ket_qua.append(sp)
        elif tieu_chi == 'loai':
            ket_qua = Danh_sach_cua_hang.tim_theo_the_loai(tu_khoa)
        else:  # mặc định: 'ten'
            ket_qua = Danh_sach_cua_hang.tim_kiem(tu_khoa)

        danh_sach_ket_qua = []
        for mat_hang in ket_qua:
            if hasattr(mat_hang, 'chuyen_thanh_dict'):
                danh_sach_ket_qua.append(mat_hang.chuyen_thanh_dict())

        return JsonResponse({
            'trang_thai': 'thanh_cong',
            'so_luong':   len(danh_sach_ket_qua),
            'danh_sach':  danh_sach_ket_qua
        })
    except Exception as loi:
        return JsonResponse(
            {'trang_thai': 'loi', 'thong_bao': f'Lỗi khi tìm kiếm: {str(loi)}'},
            status=500
        )


def sap_xep_danh_sach(request):
    """API GET /sap-xep - sắp xếp DSLK bằng Merge Sort."""
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()
    try:
        tieu_chi  = request.GET.get('tieu_chi', 'gia_ban').strip()
        Danh_sach_cua_hang.sap_xep_tron(tieu_chi)
        danh_sach = Danh_sach_cua_hang.chuyen_thanh_danh_sach()
        return JsonResponse({
            'trang_thai': 'thanh_cong',
            'so_luong':   Danh_sach_cua_hang.so_luong,
            'danh_sach':  danh_sach
        })
    except Exception as loi:
        return JsonResponse(
            {'trang_thai': 'loi', 'thong_bao': f'Lỗi khi sắp xếp: {str(loi)}'},
            status=500
        )


# ============================================================
# NHÓM 7: THỐNG KÊ
# ============================================================

def lay_thong_ke(request):
    """API GET /thong-ke - trả về thống kê tổng quan."""
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()
    try:
        tk = Danh_sach_cua_hang.thong_ke()
        # Đổi tên key cho khớp với JS
        return JsonResponse({
            'trang_thai': 'thanh_cong',
            'thong_ke': {
                'tong_so_luong':         tk['tong_so'],
                'so_mat_hang_sap_het':   len(tk['sap_het_hang']),
                'tong_gia_tri_ton_kho':  tk['tong_gia_tri_kho'],
                'mat_hang_dat_nhat':     tk['dat_nhat'],
                'mat_hang_re_nhat':      tk['re_nhat'],
                'thong_ke_theo_loai':    tk['theo_loai']
            }
        })
    except Exception as loi:
        return JsonResponse(
            {'trang_thai': 'loi', 'thong_bao': f'Lỗi khi thống kê: {str(loi)}'},
            status=500
        )


# ============================================================
# NHÓM 8: UNDO / REDO (STACK LIFO)
# ============================================================

@csrf_exempt
@require_http_methods(['POST'])
def hoan_tac(request):
    """API POST /hoan-tac - hoàn tác thao tác gần nhất (Undo)."""
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()
    try:
        thao_tac = Bo_undoredo['undo'].lay_ra()
        if thao_tac is None:
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': 'Không có thao tác nào để hoàn tác.'},
                status=400
            )

        # Đẩy sang Redo để có thể làm lại
        Bo_undoredo['redo'].day_vao(thao_tac)

        # Thực hiện đảo ngược thao tác
        loai = thao_tac['loai']
        if loai == 'them':
            # Undo thao tác THÊM → Xóa sản phẩm đó đi
            ma_so = thao_tac['du_lieu_moi']['ma_so']
            Danh_sach_cua_hang.xoa_node(ma_so)
            from .loi_thuat_toan.ket_noi_sqlite import xoa_mot_san_pham
            xoa_mot_san_pham(ma_so)
            thong_bao = f'Đã hoàn tác: xóa "{thao_tac["du_lieu_moi"]["ten_san_pham"]}".'

        elif loai == 'xoa':
            # Undo thao tác XÓA → Thêm lại sản phẩm cũ
            from .loi_thuat_toan.lop_doi_tuong import Sach, TapChi, BaoGiay, LuanVan, BanThao
            cu = thao_tac['du_lieu_cu']
            loai_hang = cu['loai_hang']
            if loai_hang == 'Sách':
                sp = Sach(cu['ma_so'], cu['ten_san_pham'], cu['gia_co_ban'], cu['ton_kho'],
                          cu.get('tac_gia', ''), cu.get('nha_xuat_ban', ''))
            elif loai_hang == 'Tạp chí':
                sp = TapChi(cu['ma_so'], cu['ten_san_pham'], cu['gia_co_ban'], cu['ton_kho'],
                            cu.get('so_phat_hanh', ''))
            elif loai_hang == 'Báo giấy':
                sp = BaoGiay(cu['ma_so'], cu['ten_san_pham'], cu['gia_co_ban'], cu['ton_kho'],
                             cu.get('ngay_xuat_ban', ''))
            elif loai_hang == 'Luận văn':
                sp = LuanVan(cu['ma_so'], cu['ten_san_pham'], cu['gia_co_ban'], cu['ton_kho'],
                             cu.get('tac_gia', ''), cu.get('truong_dai_hoc', ''), '')
            elif loai_hang == 'Bản thảo':
                sp = BanThao(cu['ma_so'], cu['ten_san_pham'], cu['gia_co_ban'], cu['ton_kho'],
                             cu.get('tac_gia', ''), cu.get('tinh_trang', ''))
            else:
                sp = None
            if sp:
                Danh_sach_cua_hang.them_vao_cuoi(sp)
                from .loi_thuat_toan.ket_noi_sqlite import luu_mot_san_pham
                luu_mot_san_pham(sp)
            thong_bao = f'Đã hoàn tác: thêm lại "{cu["ten_san_pham"]}".'

        elif loai == 'sua':
            # Undo thao tác SỬA → Đặt lại dữ liệu cũ
            cu = thao_tac['du_lieu_cu']
            ma_so = cu['ma_so']
            du_lieu_cu = {
                'ten_san_pham': cu['ten_san_pham'],
                'gia_co_ban':   cu['gia_co_ban'],
                'ton_kho':      cu['ton_kho']
            }
            if 'tac_gia' in cu:            du_lieu_cu['tac_gia'] = cu['tac_gia']
            if 'nha_xuat_ban' in cu:       du_lieu_cu['nha_xuat_ban'] = cu['nha_xuat_ban']
            if 'so_phat_hanh' in cu:       du_lieu_cu['so_phat_hanh'] = cu['so_phat_hanh']
            if 'ngay_xuat_ban' in cu:      du_lieu_cu['ngay_xuat_ban'] = cu['ngay_xuat_ban']
            if 'truong_dai_hoc' in cu:     du_lieu_cu['truong_dai_hoc'] = cu['truong_dai_hoc']
            if 'tinh_trang' in cu:         du_lieu_cu['tinh_trang'] = cu['tinh_trang']

            sp = Danh_sach_cua_hang.tim_theo_ma_so(ma_so)
            if sp:
                Danh_sach_cua_hang.cap_nhat_node(ma_so, du_lieu_cu)
                from .loi_thuat_toan.ket_noi_sqlite import cap_nhat_san_pham
                cap_nhat_san_pham(sp)
            thong_bao = f'Đã hoàn tác: khôi phục thông tin "{cu["ten_san_pham"]}".'

        else:
            thong_bao = 'Thao tác không xác định.'

        return JsonResponse({
            'trang_thai': 'thanh_cong',
            'thong_bao':  thong_bao
        })

    except Exception as loi:
        return JsonResponse(
            {'trang_thai': 'loi', 'thong_bao': f'Lỗi khi hoàn tác: {str(loi)}'},
            status=500
        )


@csrf_exempt
@require_http_methods(['POST'])
def lam_lai(request):
    """API POST /lam-lai - làm lại thao tác đã hoàn tác (Redo)."""
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()
    try:
        thao_tac = Bo_undoredo['redo'].lay_ra()
        if thao_tac is None:
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': 'Không có thao tác nào để làm lại.'},
                status=400
            )

        # Đẩy lại sang Undo
        Bo_undoredo['undo'].day_vao(thao_tac)

        # Thực hiện lại thao tác
        loai = thao_tac['loai']
        if loai == 'them':
            # Redo THÊM → thêm lại
            from .loi_thuat_toan.lop_doi_tuong import Sach, TapChi, BaoGiay, LuanVan, BanThao
            moi = thao_tac['du_lieu_moi']
            loai_hang = moi['loai_hang']
            if loai_hang == 'Sách':
                sp = Sach(moi['ma_so'], moi['ten_san_pham'], moi['gia_co_ban'], moi['ton_kho'],
                          moi.get('tac_gia', ''), moi.get('nha_xuat_ban', ''))
            elif loai_hang == 'Tạp chí':
                sp = TapChi(moi['ma_so'], moi['ten_san_pham'], moi['gia_co_ban'], moi['ton_kho'],
                            moi.get('so_phat_hanh', ''))
            elif loai_hang == 'Báo giấy':
                sp = BaoGiay(moi['ma_so'], moi['ten_san_pham'], moi['gia_co_ban'], moi['ton_kho'],
                             moi.get('ngay_xuat_ban', ''))
            elif loai_hang == 'Luận văn':
                sp = LuanVan(moi['ma_so'], moi['ten_san_pham'], moi['gia_co_ban'], moi['ton_kho'],
                             moi.get('tac_gia', ''), moi.get('truong_dai_hoc', ''), '')
            elif loai_hang == 'Bản thảo':
                sp = BanThao(moi['ma_so'], moi['ten_san_pham'], moi['gia_co_ban'], moi['ton_kho'],
                             moi.get('tac_gia', ''), moi.get('tinh_trang', ''))
            else:
                sp = None
            if sp:
                Danh_sach_cua_hang.them_vao_cuoi(sp)
                from .loi_thuat_toan.ket_noi_sqlite import luu_mot_san_pham
                luu_mot_san_pham(sp)
            thong_bao = f'Đã làm lại: thêm "{moi["ten_san_pham"]}".'

        elif loai == 'xoa':
            # Redo XÓA → xóa lại
            ma_so = thao_tac['du_lieu_cu']['ma_so']
            Danh_sach_cua_hang.xoa_node(ma_so)
            from .loi_thuat_toan.ket_noi_sqlite import xoa_mot_san_pham
            xoa_mot_san_pham(ma_so)
            thong_bao = f'Đã làm lại: xóa "{thao_tac["du_lieu_cu"]["ten_san_pham"]}".'

        elif loai == 'sua':
            # Redo SỬA → áp dụng lại dữ liệu mới
            moi = thao_tac['du_lieu_moi']
            ma_so = moi['ma_so']
            du_lieu_moi = {
                'ten_san_pham': moi['ten_san_pham'],
                'gia_co_ban':   moi['gia_co_ban'],
                'ton_kho':      moi['ton_kho']
            }
            if 'tac_gia' in moi:            du_lieu_moi['tac_gia'] = moi['tac_gia']
            if 'nha_xuat_ban' in moi:       du_lieu_moi['nha_xuat_ban'] = moi['nha_xuat_ban']
            if 'so_phat_hanh' in moi:       du_lieu_moi['so_phat_hanh'] = moi['so_phat_hanh']
            if 'ngay_xuat_ban' in moi:      du_lieu_moi['ngay_xuat_ban'] = moi['ngay_xuat_ban']
            if 'truong_dai_hoc' in moi:     du_lieu_moi['truong_dai_hoc'] = moi['truong_dai_hoc']
            if 'tinh_trang' in moi:         du_lieu_moi['tinh_trang'] = moi['tinh_trang']

            sp = Danh_sach_cua_hang.tim_theo_ma_so(ma_so)
            if sp:
                Danh_sach_cua_hang.cap_nhat_node(ma_so, du_lieu_moi)
                from .loi_thuat_toan.ket_noi_sqlite import cap_nhat_san_pham
                cap_nhat_san_pham(sp)
            thong_bao = f'Đã làm lại: cập nhật "{moi["ten_san_pham"]}".'

        else:
            thong_bao = 'Thao tác không xác định.'

        return JsonResponse({
            'trang_thai': 'thanh_cong',
            'thong_bao':  thong_bao
        })

    except Exception as loi:
        return JsonResponse(
            {'trang_thai': 'loi', 'thong_bao': f'Lỗi khi làm lại: {str(loi)}'},
            status=500
        )


# ============================================================
# NHÓM 9: GIỎ HÀNG (QUEUE FIFO)
# ============================================================

@csrf_exempt
@require_http_methods(['POST'])
def them_vao_gio_hang(request):
    """API POST /them-gio-hang - thêm sản phẩm vào giỏ (Enqueue)."""
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()
    try:
        du_lieu = json.loads(request.body)
        ma_so   = du_lieu.get('ma_so', '').strip()
        if not ma_so:
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': 'Mã số không được để trống.'},
                status=400
            )

        san_pham = Danh_sach_cua_hang.tim_theo_ma_so(ma_so)
        if san_pham is None:
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': f'Không tìm thấy sản phẩm mã {ma_so}.'},
                status=404
            )

        # Đóng gói thành dict và enqueue
        mon_hang = {
            'ma_so':        san_pham.ma_so,
            'ten_san_pham': san_pham.ten_san_pham,
            'gia_ban':      san_pham.tinh_gia_ban(),
            'loai_hang':    san_pham.loai_hang
        }
        Gio_hang_hien_tai.them_vao(mon_hang)

        return JsonResponse({
            'trang_thai': 'thanh_cong',
            'thong_bao':  f'Đã thêm "{san_pham.ten_san_pham}" vào giỏ hàng.',
            'so_luong':   Gio_hang_hien_tai.so_luong
        })

    except json.JSONDecodeError:
        return JsonResponse(
            {'trang_thai': 'loi', 'thong_bao': 'Dữ liệu gửi lên không hợp lệ.'},
            status=400
        )
    except Exception as loi:
        return JsonResponse(
            {'trang_thai': 'loi', 'thong_bao': f'Lỗi máy chủ: {str(loi)}'},
            status=500
        )


def xem_gio_hang(request):
    """API GET /xem-gio-hang - xem toàn bộ giỏ hàng."""
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()
    try:
        danh_sach = Gio_hang_hien_tai.xem_danh_sach()
        tong_tien = sum(mon.get('gia_ban', 0) for mon in danh_sach)
        return JsonResponse({
            'trang_thai': 'thanh_cong',
            'so_luong':   Gio_hang_hien_tai.so_luong,
            'tong_tien':  tong_tien,
            'gio_hang':   danh_sach
        })
    except Exception as loi:
        return JsonResponse(
            {'trang_thai': 'loi', 'thong_bao': f'Lỗi khi xem giỏ hàng: {str(loi)}'},
            status=500
        )


@csrf_exempt
@require_http_methods(['POST'])
def xoa_khoi_gio_hang(request):
    """API POST /xoa-gio-hang - xóa 1 mặt hàng khỏi giỏ."""
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()
    try:
        du_lieu = json.loads(request.body)
        ma_so   = du_lieu.get('ma_so', '').strip()
        if not ma_so:
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': 'Mã số không được để trống.'},
                status=400
            )

        ket_qua = Gio_hang_hien_tai.xoa_theo_ma(ma_so)
        if ket_qua:
            return JsonResponse({
                'trang_thai': 'thanh_cong',
                'thong_bao':  f'Đã xóa "{ma_so}" khỏi giỏ hàng.'
            })
        else:
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': f'Không có "{ma_so}" trong giỏ.'},
                status=404
            )
    except json.JSONDecodeError:
        return JsonResponse(
            {'trang_thai': 'loi', 'thong_bao': 'Dữ liệu gửi lên không hợp lệ.'},
            status=400
        )
    except Exception as loi:
        return JsonResponse(
            {'trang_thai': 'loi', 'thong_bao': f'Lỗi máy chủ: {str(loi)}'},
            status=500
        )


@csrf_exempt
@require_http_methods(['POST'])
def thanh_toan(request):
    """API POST /thanh-toan - thanh toán toàn bộ giỏ hàng (Dequeue all)."""
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()
    try:
        if Gio_hang_hien_tai.rong():
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': 'Giỏ hàng đang trống.'},
                status=400
            )

        # Lấy toàn bộ ra theo FIFO
        cac_mon = []
        tong_tien = 0
        while not Gio_hang_hien_tai.rong():
            mon = Gio_hang_hien_tai.lay_ra()
            cac_mon.append(mon)
            tong_tien += mon.get('gia_ban', 0)

        return JsonResponse({
            'trang_thai': 'thanh_cong',
            'thong_bao':  f'Đã thanh toán {len(cac_mon)} mặt hàng, tổng {tong_tien:,.0f}đ.',
            'hoa_don': {
                'cac_mon':  cac_mon,
                'tong_tien': tong_tien,
                'so_mon':   len(cac_mon)
            }
        })
    except Exception as loi:
        return JsonResponse(
            {'trang_thai': 'loi', 'thong_bao': f'Lỗi khi thanh toán: {str(loi)}'},
            status=500
        )
