"""
NHÓM 6-7: Tìm kiếm, Sắp xếp, Thống kê
=========================================
Chứa: tim_kiem_san_pham, sap_xep_danh_sach, lay_thong_ke
"""

from django.http import JsonResponse

from . import khoi_tao as _kho


# ============================================================
# NHÓM 6: TÌM KIẾM + SẮP XẾP
# ============================================================

def tim_kiem_san_pham(request):
    """
    API GET /tim-kiem - tìm kiếm nâng cao (tên / mã / loại).

    Query params:
        ?tu_khoa=python&tieu_chi=ten   (hoặc 'ma', 'loai')
        
    [Tương tác JS]: Được gọi bởi hàm `tim_kiem(tu_khoa, tieu_chi)` trong file `goi_du_lieu.js`.
    """
    if _kho.Danh_sach_cua_hang is None:
        _kho.khoi_tao_danh_sach()
    try:
        tu_khoa   = request.GET.get('tu_khoa', '').strip()
        tieu_chi  = request.GET.get('tieu_chi', 'ten').strip()

        if tieu_chi == 'ma':
            ket_qua = []
            sp = _kho.Danh_sach_cua_hang.tim_theo_ma_so(tu_khoa)
            if sp:
                ket_qua.append(sp)
        elif tieu_chi == 'loai':
            ket_qua = _kho.Danh_sach_cua_hang.tim_theo_the_loai(tu_khoa)
        else:
            ket_qua = _kho.Danh_sach_cua_hang.tim_kiem(tu_khoa)

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
    """
    API GET /sap-xep - sắp xếp DSLK bằng Merge Sort (thuật toán O(n log n)).

    Query params:
        ?tieu_chi=gia_ban   (hoặc 'ten_san_pham', 'ton_kho', ...)
        
    [Tương tác JS]: Được gọi bởi hàm `sap_xep(tieu_chi)` trong file `goi_du_lieu.js`.
    """
    if _kho.Danh_sach_cua_hang is None:
        _kho.khoi_tao_danh_sach()
    try:
        tieu_chi  = request.GET.get('tieu_chi', 'gia_ban').strip()
        _kho.Danh_sach_cua_hang.sap_xep_tron(tieu_chi)
        danh_sach = _kho.Danh_sach_cua_hang.chuyen_thanh_danh_sach()
        return JsonResponse({
            'trang_thai': 'thanh_cong',
            'so_luong':   _kho.Danh_sach_cua_hang.so_luong,
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
    """
    API GET /thong-ke - trả về thống kê tổng quan.

    Bao gồm: tổng số lượng, số mặt hàng sắp hết, tổng giá trị kho,
    mặt hàng đắt nhất, rẻ nhất, thống kê theo từng loại.
    
    [Tương tác JS]: Được gọi bởi hàm `lay_thong_ke()` trong file `goi_du_lieu.js`.
    """
    if _kho.Danh_sach_cua_hang is None:
        _kho.khoi_tao_danh_sach()
    try:
        tk = _kho.Danh_sach_cua_hang.thong_ke()
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
