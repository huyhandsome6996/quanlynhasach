from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
Danh_sach_cua_hang = None

def khoi_tao_danh_sach():
    global Danh_sach_cua_hang
    from .loi_thuat_toan.danh_sach_lien_ket import DoublyLinkedList
    from .loi_thuat_toan.ket_noi_sqlite import tai_du_lieu
    Danh_sach_cua_hang = DoublyLinkedList()
    tai_du_lieu(Danh_sach_cua_hang)
    try:
        print(f'[KHOI DONG] Da nap {Danh_sach_cua_hang.so_luong} mat hang vao danh sach lien ket doi.')
    except UnicodeEncodeError:
        print(f'[KHOI DONG] Da nap {Danh_sach_cua_hang.so_luong} mat hang.')

def trang_chu(request):
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()
    return render(request, 'trang_chu.html')

def lay_danh_sach(request):
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()
    danh_sach = Danh_sach_cua_hang.chuyen_thanh_danh_sach()
    return JsonResponse({'trang_thai': 'thanh_cong', 'so_luong': Danh_sach_cua_hang.so_luong, 'danh_sach': danh_sach})

@csrf_exempt
@require_http_methods(['POST'])
def them_san_pham(request):
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()
    try:
        du_lieu = json.loads(request.body)
        loai_hang = du_lieu.get('loai_hang', '').strip()
        ma_so = du_lieu.get('ma_so', '').strip()
        ten_san_pham = du_lieu.get('ten_san_pham', '').strip()
        gia_co_ban = float(du_lieu.get('gia_co_ban', 0))
        ton_kho = int(du_lieu.get('ton_kho', 0))
        if not ma_so or not ten_san_pham or (not loai_hang):
            return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Vui lòng điền đầy đủ thông tin.'}, status=400)
        if gia_co_ban < 0:
            return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Giá cơ bản không được âm.'}, status=400)
        if ton_kho < 0:
            return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Số lượng tồn kho không được âm.'}, status=400)
        node_hien_tai = Danh_sach_cua_hang.head
        while node_hien_tai is not None:
            if node_hien_tai.data.ma_so == ma_so:
                return JsonResponse({'trang_thai': 'loi', 'thong_bao': f'Mã số "{ma_so}" đã tồn tại trong cửa hàng.'}, status=400)
            node_hien_tai = node_hien_tai.next
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
        Danh_sach_cua_hang.them_vao_cuoi(san_pham_moi)
        from .loi_thuat_toan.ket_noi_sqlite import luu_mot_san_pham
        luu_mot_san_pham(san_pham_moi)
        return JsonResponse({'trang_thai': 'thanh_cong', 'thong_bao': f'Đã thêm "{ten_san_pham}" vào cửa hàng.'})
    except json.JSONDecodeError:
        return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Dữ liệu gửi lên không hợp lệ.'}, status=400)
    except ValueError:
        return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Giá hoặc số lượng phải là số.'}, status=400)

@csrf_exempt
@require_http_methods(['POST'])
def xoa_san_pham(request):
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()
    try:
        du_lieu = json.loads(request.body)
        ma_so = du_lieu.get('ma_so', '').strip()
        if not ma_so:
            return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Mã số không được để trống.'}, status=400)
        ket_qua = Danh_sach_cua_hang.xoa_node(ma_so)
        if ket_qua:
            from .loi_thuat_toan.ket_noi_sqlite import xoa_mot_san_pham
            xoa_mot_san_pham(ma_so)
            return JsonResponse({'trang_thai': 'thanh_cong', 'thong_bao': f'Đã xóa sản phẩm mã {ma_so}.'})
        else:
            return JsonResponse({'trang_thai': 'loi', 'thong_bao': f'Không tìm thấy sản phẩm mã {ma_so}.'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Dữ liệu gửi lên không hợp lệ.'}, status=400)

def tim_kiem_san_pham(request):
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()
    tu_khoa = request.GET.get('tu_khoa', '').strip()
    ket_qua = Danh_sach_cua_hang.tim_kiem(tu_khoa)
    danh_sach_ket_qua = []
    for mat_hang in ket_qua:
        if hasattr(mat_hang, 'chuyen_thanh_dict'):
            danh_sach_ket_qua.append(mat_hang.chuyen_thanh_dict())
    return JsonResponse({'trang_thai': 'thanh_cong', 'so_luong': len(danh_sach_ket_qua), 'danh_sach': danh_sach_ket_qua})

def sap_xep_danh_sach(request):
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()
    tieu_chi = request.GET.get('tieu_chi', 'gia_ban').strip()
    Danh_sach_cua_hang.sap_xep_tron(tieu_chi)
    danh_sach = Danh_sach_cua_hang.chuyen_thanh_danh_sach()
    return JsonResponse({'trang_thai': 'thanh_cong', 'so_luong': Danh_sach_cua_hang.so_luong, 'danh_sach': danh_sach})

