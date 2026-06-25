"""
NHÓM 9: Giỏ hàng (Queue FIFO)
================================
Chứa: them_vao_gio_hang, xem_gio_hang, xoa_khoi_gio_hang, thanh_toan
"""

import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from . import khoi_tao as _kho


@csrf_exempt
@require_http_methods(['POST'])
def them_vao_gio_hang(request):
    """
    API POST /them-gio-hang - thêm sản phẩm vào giỏ (Enqueue).
    
    [Tương tác JS]: Được gọi bởi hàm `them_vao_gio_hang()` trong file `goi_du_lieu.js`.
    """
    # [NGUYÊN LÝ ĐỒ ÁN - ĐỌC KỸ]
    # Đảm bảo CSDL được nạp vào RAM.
    # Nguồn: Biến `Danh_sach_cua_hang` và hàm `khoi_tao_danh_sach()` lấy từ `khoi_tao.py`.
    if _kho.Danh_sach_cua_hang is None:
        _kho.khoi_tao_danh_sach()
    try:
        du_lieu = json.loads(request.body)
        ma_so   = du_lieu.get('ma_so', '').strip()
        if not ma_so:
            return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Mã số không được để trống.'}, status=400)
        san_pham = _kho.Danh_sach_cua_hang.tim_theo_ma_so(ma_so)
        if san_pham is None:
            return JsonResponse({'trang_thai': 'loi', 'thong_bao': f'Không tìm thấy sản phẩm mã {ma_so}.'}, status=404)
        # Tạo một Dictionary để gói gọn thông tin cuốn sách.
        mon_hang = {
            'ma_so':        san_pham.ma_so,
            'ten_san_pham': san_pham.ten_san_pham,
            'gia_ban':      san_pham.tinh_gia_ban(),
            'loai_hang':    san_pham.loai_hang
        }
        
        # [NGUYÊN LÝ QUEUE - FIFO] (Vào trước ra trước)
        # BƯỚC 1: Gọi hàm ENQUEUE (them_vao) để nhét món hàng vào ĐUÔI của Hàng Đợi.
        # Nguồn: Biến `Gio_hang_hien_tai` là một đối tượng thuộc class Queue (Hàng đợi) tạo từ `khoi_tao.py`.
        # Tác động đồ án: Chứng minh bạn biết ứng dụng Queue làm giỏ hàng (ai chọn trước thì tính tiền trước).
        _kho.Gio_hang_hien_tai.them_vao(mon_hang)
        return JsonResponse({
            'trang_thai': 'thanh_cong',
            'thong_bao':  f'Đã thêm "{san_pham.ten_san_pham}" vào giỏ hàng.',
            'so_luong':   _kho.Gio_hang_hien_tai.so_luong
        })
    except json.JSONDecodeError:
        return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Dữ liệu gửi lên không hợp lệ.'}, status=400)
    except Exception as loi:
        return JsonResponse({'trang_thai': 'loi', 'thong_bao': f'Lỗi máy chủ: {str(loi)}'}, status=500)


def xem_gio_hang(request):
    """
    API GET /xem-gio-hang - xem toàn bộ giỏ hàng (peek all, không xóa).
    
    [Tương tác JS]: Được gọi bởi hàm `xem_gio_hang()` trong file `goi_du_lieu.js`.
    """
    if _kho.Danh_sach_cua_hang is None:
        _kho.khoi_tao_danh_sach()
    try:
        danh_sach = _kho.Gio_hang_hien_tai.xem_danh_sach()
        tong_tien = sum(mon.get('gia_ban', 0) for mon in danh_sach)
        return JsonResponse({
            'trang_thai': 'thanh_cong',
            'so_luong':   _kho.Gio_hang_hien_tai.so_luong,
            'tong_tien':  tong_tien,
            'gio_hang':   danh_sach
        })
    except Exception as loi:
        return JsonResponse({'trang_thai': 'loi', 'thong_bao': f'Lỗi khi xem giỏ hàng: {str(loi)}'}, status=500)


@csrf_exempt
@require_http_methods(['POST'])
def xoa_khoi_gio_hang(request):
    """
    API POST /xoa-gio-hang - xóa 1 mặt hàng khỏi giỏ (theo mã số).
    
    [Tương tác JS]: Được gọi bởi hàm `xoa_khoi_gio_hang()` trong file `goi_du_lieu.js`.
    """
    if _kho.Danh_sach_cua_hang is None:
        _kho.khoi_tao_danh_sach()
    try:
        du_lieu = json.loads(request.body)
        ma_so   = du_lieu.get('ma_so', '').strip()
        if not ma_so:
            return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Mã số không được để trống.'}, status=400)
        ket_qua = _kho.Gio_hang_hien_tai.xoa_theo_ma(ma_so)
        if ket_qua:
            return JsonResponse({'trang_thai': 'thanh_cong', 'thong_bao': f'Đã xóa "{ma_so}" khỏi giỏ hàng.'})
        else:
            return JsonResponse({'trang_thai': 'loi', 'thong_bao': f'Không có "{ma_so}" trong giỏ.'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Dữ liệu gửi lên không hợp lệ.'}, status=400)
    except Exception as loi:
        return JsonResponse({'trang_thai': 'loi', 'thong_bao': f'Lỗi máy chủ: {str(loi)}'}, status=500)


@csrf_exempt
@require_http_methods(['POST'])
def thanh_toan(request):
    """
    API POST /thanh-toan - thanh toán toàn bộ giỏ hàng (Dequeue all).
    
    [Tương tác JS]: Được gọi bởi hàm `thanh_toan_gio_hang()` trong file `goi_du_lieu.js`.
    """
    if _kho.Danh_sach_cua_hang is None:
        _kho.khoi_tao_danh_sach()
    try:
        if _kho.Gio_hang_hien_tai.rong():
            return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Giỏ hàng đang trống.'}, status=400)
        # Chuẩn bị một danh sách rỗng để chứa các món ăn ra.
        cac_mon = []
        tong_tien = 0
        
        # [NGUYÊN LÝ QUEUE - FIFO] (Vào trước ra trước)
        # Vòng lặp: Lặp cho đến khi Giỏ hàng (Hàng đợi) rỗng.
        while not _kho.Gio_hang_hien_tai.rong():
            # BƯỚC 2: Gọi lệnh DEQUEUE (lay_ra) để bốc món hàng ở ĐẦU hàng đợi ra tính tiền.
            # Tác động đồ án: Chứng minh cách xả toàn bộ Queue theo đúng thứ tự FIFO.
            mon = _kho.Gio_hang_hien_tai.lay_ra()
            
            cac_mon.append(mon) # Lưu tạm vào hóa đơn
            tong_tien += mon.get('gia_ban', 0) # Cộng dồn tiền
        return JsonResponse({
            'trang_thai': 'thanh_cong',
            'thong_bao':  f'Đã thanh toán {len(cac_mon)} mặt hàng, tổng {tong_tien:,.0f}đ.',
            'hoa_don': {'cac_mon': cac_mon, 'tong_tien': tong_tien, 'so_mon': len(cac_mon)}
        })
    except Exception as loi:
        return JsonResponse({'trang_thai': 'loi', 'thong_bao': f'Lỗi khi thanh toán: {str(loi)}'}, status=500)
