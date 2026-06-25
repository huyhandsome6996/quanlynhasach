"""
NHÓM 2-5: Quản lý sản phẩm (CRUD)
====================================
Chứa: lay_danh_sach, them_san_pham, sua_san_pham, xoa_san_pham
"""

import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from . import khoi_tao as _kho
from .xac_thuc import la_admin


# ============================================================
# NHÓM 2: ĐỌC DANH SÁCH
# ============================================================

def lay_danh_sach(request):
    """
    API GET /danh-sach - trả về toàn bộ mặt hàng dưới dạng JSON.
    Frontend gọi khi load trang để fill vào bảng dữ liệu.
    
    [Tương tác JS]: Được gọi bởi hàm `lay_danh_sach()` trong file `goi_du_lieu.js`.
    """
    try:
        if _kho.Danh_sach_cua_hang is None:
            _kho.khoi_tao_danh_sach()
        danh_sach = _kho.Danh_sach_cua_hang.chuyen_thanh_danh_sach()
        return JsonResponse({
            'trang_thai': 'thanh_cong',
            'so_luong':   _kho.Danh_sach_cua_hang.so_luong,
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
    """
    API POST /them-san-pham - thêm một sản phẩm mới (hỗ trợ 5 loại).

    5 loại: Sách, Tạp chí, Báo giấy, Luận văn, Bản thảo.
    Mỗi loại có các trường dữ liệu riêng (tac_gia, so_phat_hanh, ...).
    
    [Tương tác JS]: Được gọi bởi hàm `them_san_pham()` trong file `goi_du_lieu.js` 
    (khi bấm submit trên form thêm).
    """
    if _kho.Danh_sach_cua_hang is None:
        _kho.khoi_tao_danh_sach()
    try:
        du_lieu        = json.loads(request.body)
        loai_hang      = du_lieu.get('loai_hang', '').strip()
        ma_so          = du_lieu.get('ma_so', '').strip()
        ten_san_pham   = du_lieu.get('ten_san_pham', '').strip()
        gia_co_ban     = float(du_lieu.get('gia_co_ban', 0))
        ton_kho        = int(du_lieu.get('ton_kho', 0))

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

        if _kho.Danh_sach_cua_hang.tim_theo_ma_so(ma_so) is not None:
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': f'Mã số "{ma_so}" đã tồn tại.'},
                status=400
            )

        from ..loi_thuat_toan.lop_doi_tuong import Sach, TapChi, BaoGiay, LuanVan, BanThao

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

        _kho.Danh_sach_cua_hang.them_vao_cuoi(san_pham_moi)
        from ..loi_thuat_toan.ket_noi_sqlite import luu_mot_san_pham
        luu_mot_san_pham(san_pham_moi)

        _kho.Bo_undoredo['undo'].day_vao({
            'loai':        'them',
            'du_lieu_cu':  None,
            'du_lieu_moi': san_pham_moi.chuyen_thanh_dict()
        })
        _kho.Bo_undoredo['redo'].xoa_tat_ca()

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
    """
    API POST /sua-san-pham - cập nhật thông tin sản phẩm.

    Frontend gửi mã sản phẩm cần sửa + các trường mới → view cập nhật
    trong DSLK + SQLite, đồng thời ghi stack Undo để có thể hoàn tác.
    
    [Tương tác JS]: Được gọi bởi hàm `sua_san_pham()` trong file `goi_du_lieu.js` 
    (khi bấm submit trên form sửa).
    """
    if _kho.Danh_sach_cua_hang is None:
        _kho.khoi_tao_danh_sach()
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

        san_pham_cu = _kho.Danh_sach_cua_hang.tim_theo_ma_so(ma_so)
        if san_pham_cu is None:
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': f'Không tìm thấy sản phẩm mã {ma_so}.'},
                status=404
            )

        du_lieu_cu = san_pham_cu.chuyen_thanh_dict()

        du_lieu_moi = {
            'ten_san_pham': ten_san_pham,
            'gia_co_ban':   gia_co_ban,
            'ton_kho':      ton_kho
        }

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

        _kho.Danh_sach_cua_hang.cap_nhat_node(ma_so, du_lieu_moi)
        from ..loi_thuat_toan.ket_noi_sqlite import cap_nhat_san_pham
        cap_nhat_san_pham(san_pham_cu)

        _kho.Bo_undoredo['undo'].day_vao({
            'loai':        'sua',
            'du_lieu_cu':  du_lieu_cu,
            'du_lieu_moi': san_pham_cu.chuyen_thanh_dict()
        })
        _kho.Bo_undoredo['redo'].xoa_tat_ca()

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
    """
    API POST /xoa-san-pham - xóa sản phẩm. CHỈ ADMIN mới được xóa.

    Phân quyền: nhân viên gọi endpoint này sẽ bị từ chối với lỗi 403.
    
    [Tương tác JS]: Được gọi bởi hàm `xoa_san_pham()` trong file `goi_du_lieu.js` 
    (khi admin bấm nút "Xóa" trên bảng).
    """
    if _kho.Danh_sach_cua_hang is None:
        _kho.khoi_tao_danh_sach()

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

        san_pham_cu = _kho.Danh_sach_cua_hang.tim_theo_ma_so(ma_so)
        if san_pham_cu is None:
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': f'Không tìm thấy sản phẩm mã {ma_so}.'},
                status=404
            )
        du_lieu_cu = san_pham_cu.chuyen_thanh_dict()

        ket_qua = _kho.Danh_sach_cua_hang.xoa_node(ma_so)
        if ket_qua:
            from ..loi_thuat_toan.ket_noi_sqlite import xoa_mot_san_pham
            xoa_mot_san_pham(ma_so)

            _kho.Bo_undoredo['undo'].day_vao({
                'loai':       'xoa',
                'du_lieu_cu': du_lieu_cu,
                'du_lieu_moi': None
            })
            _kho.Bo_undoredo['redo'].xoa_tat_ca()

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
