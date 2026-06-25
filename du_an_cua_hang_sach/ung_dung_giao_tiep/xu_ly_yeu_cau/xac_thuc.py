"""
NHÓM 1: Đăng nhập / Đăng xuất / Phân quyền
=============================================
Chứa: trang_chu, trang_dang_nhap, xu_ly_dang_nhap, xu_ly_dang_xuat,
       thong_tin_nguoi_dung, la_admin
"""

import json

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from . import khoi_tao as _kho


# ============================================================
# NHÓM 1: ĐĂNG NHẬP / ĐĂNG XUẤT / PHÂN QUYỀN
# ============================================================

def trang_chu(request):
    """
    Trang chủ - nếu chưa đăng nhập thì chuyển sang trang đăng nhập.

    URL: GET /
    
    [Tương tác JS]: File này sẽ load file `tuong_tac.js` và `goi_du_lieu.js` lên trình duyệt.
    """
    if _kho.Danh_sach_cua_hang is None:
        _kho.khoi_tao_danh_sach()
    if 'ten_dang_nhap' not in request.session:
        return redirect('/dang-nhap')
    request.session['nguoi_dung'] = {
        'ten_dang_nhap': request.session.get('ten_dang_nhap'),
        'ho_ten':        request.session.get('ho_ten', ''),
        'vai_tro':       request.session.get('vai_tro', 'nhan_vien'),
        'la_admin':      request.session.get('vai_tro', 'nhan_vien') == 'admin'
    }
    return render(request, 'trang_chu.html')


def trang_dang_nhap(request):
    """
    Hiển thị form đăng nhập.

    URL: GET /dang-nhap
    """
    if _kho.Danh_sach_cua_hang is None:
        _kho.khoi_tao_danh_sach()
    if 'ten_dang_nhap' in request.session:
        return redirect('/')
    return render(request, 'dang_nhap.html')


@csrf_exempt
@require_http_methods(['POST'])
def xu_ly_dang_nhap(request):
    """
    API POST /dang-nhap - kiểm tra tài khoản và lưu session.

    Frontend gửi JSON: {"ten_dang_nhap": "...", "mat_khau": "..."}
    Trả về JSON: {"trang_thai": "thanh_cong", "nguoi_dung": {...}}
    
    [Tương tác JS]: Được gọi bởi đoạn mã JS nội tuyến (inline JS) chứa `fetch('/api/dang-nhap')` 
    nằm trực tiếp trong file `dang_nhap.html`.
    """
    try:
        du_lieu = json.loads(request.body)
        ten_dang_nhap = du_lieu.get('ten_dang_nhap', '').strip()
        mat_khau      = du_lieu.get('mat_khau', '').strip()

        if not ten_dang_nhap or not mat_khau:
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': 'Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.'},
                status=400
            )

        from ..loi_thuat_toan.nguoi_dung import kiem_tra_dang_nhap
        nguoi_dung = kiem_tra_dang_nhap(ten_dang_nhap, mat_khau)

        if nguoi_dung is None:
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': 'Sai tên đăng nhập hoặc mật khẩu.'},
                status=401
            )

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
    """
    API /dang-xuat - xóa session và quay về trang đăng nhập.
    
    [Tương tác JS]: Được gọi khi người dùng bấm nút Đăng xuất trên `dau_trang.html`.
    """
    try:
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
    """
    API GET /nguoi-dung - trả về thông tin người dùng đang đăng nhập.
    Frontend dùng để hiển thị tên + vai trò trên thanh đầu trang.
    
    [Tương tác JS]: Được gọi bởi hàm `tai_thong_tin_nguoi_dung()` trong file `tuong_tac.js`.
    """
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
    """
    Hàm tiện ích - kiểm tra request hiện tại có phải admin không.
    Trả về True nếu session có vai_tro = 'admin', ngược lại False.
    Dùng để chặn các view CHỈ ADMIN mới được dùng (ví dụ: xóa sản phẩm).
    """
    return request.session.get('vai_tro', 'nhan_vien') == 'admin'
