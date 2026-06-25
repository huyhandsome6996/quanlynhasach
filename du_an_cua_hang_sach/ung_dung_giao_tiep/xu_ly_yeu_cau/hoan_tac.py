"""
NHÓM 8: Undo / Redo (Stack LIFO)
==================================
Chứa: hoan_tac, lam_lai
"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from . import khoi_tao as _kho


@csrf_exempt
@require_http_methods(['POST'])
def hoan_tac(request):
    """API POST /hoan-tac - hoàn tác thao tác gần nhất (Undo)."""
    if _kho.Danh_sach_cua_hang is None:
        _kho.khoi_tao_danh_sach()
    try:
        thao_tac = _kho.Bo_undoredo['undo'].lay_ra()
        if thao_tac is None:
            return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Không có thao tác nào để hoàn tác.'}, status=400)
        _kho.Bo_undoredo['redo'].day_vao(thao_tac)
        loai = thao_tac['loai']
        if loai == 'them':
            ma_so = thao_tac['du_lieu_moi']['ma_so']
            _kho.Danh_sach_cua_hang.xoa_node(ma_so)
            from ..loi_thuat_toan.ket_noi_sqlite import xoa_mot_san_pham
            xoa_mot_san_pham(ma_so)
            thong_bao = f'Đã hoàn tác: xóa "{thao_tac["du_lieu_moi"]["ten_san_pham"]}".'
        elif loai == 'xoa':
            from ..loi_thuat_toan.lop_doi_tuong import Sach, TapChi, BaoGiay, LuanVan, BanThao
            cu = thao_tac['du_lieu_cu']
            lh = cu['loai_hang']
            if lh == 'Sách': sp = Sach(cu['ma_so'], cu['ten_san_pham'], cu['gia_co_ban'], cu['ton_kho'], cu.get('tac_gia',''), cu.get('nha_xuat_ban',''))
            elif lh == 'Tạp chí': sp = TapChi(cu['ma_so'], cu['ten_san_pham'], cu['gia_co_ban'], cu['ton_kho'], cu.get('so_phat_hanh',''))
            elif lh == 'Báo giấy': sp = BaoGiay(cu['ma_so'], cu['ten_san_pham'], cu['gia_co_ban'], cu['ton_kho'], cu.get('ngay_xuat_ban',''))
            elif lh == 'Luận văn': sp = LuanVan(cu['ma_so'], cu['ten_san_pham'], cu['gia_co_ban'], cu['ton_kho'], cu.get('tac_gia',''), cu.get('truong_dai_hoc',''), '')
            elif lh == 'Bản thảo': sp = BanThao(cu['ma_so'], cu['ten_san_pham'], cu['gia_co_ban'], cu['ton_kho'], cu.get('tac_gia',''), cu.get('tinh_trang',''))
            else: sp = None
            if sp:
                _kho.Danh_sach_cua_hang.them_vao_cuoi(sp)
                from ..loi_thuat_toan.ket_noi_sqlite import luu_mot_san_pham
                luu_mot_san_pham(sp)
            thong_bao = f'Đã hoàn tác: thêm lại "{cu["ten_san_pham"]}".'
        elif loai == 'sua':
            cu = thao_tac['du_lieu_cu']
            ma_so = cu['ma_so']
            dl = {'ten_san_pham': cu['ten_san_pham'], 'gia_co_ban': cu['gia_co_ban'], 'ton_kho': cu['ton_kho']}
            for k in ('tac_gia','nha_xuat_ban','so_phat_hanh','ngay_xuat_ban','truong_dai_hoc','tinh_trang'):
                if k in cu: dl[k] = cu[k]
            sp = _kho.Danh_sach_cua_hang.tim_theo_ma_so(ma_so)
            if sp:
                _kho.Danh_sach_cua_hang.cap_nhat_node(ma_so, dl)
                from ..loi_thuat_toan.ket_noi_sqlite import cap_nhat_san_pham
                cap_nhat_san_pham(sp)
            thong_bao = f'Đã hoàn tác: khôi phục thông tin "{cu["ten_san_pham"]}".'
        else:
            thong_bao = 'Thao tác không xác định.'
        return JsonResponse({'trang_thai': 'thanh_cong', 'thong_bao': thong_bao})
    except Exception as loi:
        return JsonResponse({'trang_thai': 'loi', 'thong_bao': f'Lỗi khi hoàn tác: {str(loi)}'}, status=500)


@csrf_exempt
@require_http_methods(['POST'])
def lam_lai(request):
    """API POST /lam-lai - làm lại thao tác đã hoàn tác (Redo)."""
    if _kho.Danh_sach_cua_hang is None:
        _kho.khoi_tao_danh_sach()
    try:
        thao_tac = _kho.Bo_undoredo['redo'].lay_ra()
        if thao_tac is None:
            return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Không có thao tác nào để làm lại.'}, status=400)
        _kho.Bo_undoredo['undo'].day_vao(thao_tac)
        loai = thao_tac['loai']
        if loai == 'them':
            from ..loi_thuat_toan.lop_doi_tuong import Sach, TapChi, BaoGiay, LuanVan, BanThao
            moi = thao_tac['du_lieu_moi']
            lh = moi['loai_hang']
            if lh == 'Sách': sp = Sach(moi['ma_so'], moi['ten_san_pham'], moi['gia_co_ban'], moi['ton_kho'], moi.get('tac_gia',''), moi.get('nha_xuat_ban',''))
            elif lh == 'Tạp chí': sp = TapChi(moi['ma_so'], moi['ten_san_pham'], moi['gia_co_ban'], moi['ton_kho'], moi.get('so_phat_hanh',''))
            elif lh == 'Báo giấy': sp = BaoGiay(moi['ma_so'], moi['ten_san_pham'], moi['gia_co_ban'], moi['ton_kho'], moi.get('ngay_xuat_ban',''))
            elif lh == 'Luận văn': sp = LuanVan(moi['ma_so'], moi['ten_san_pham'], moi['gia_co_ban'], moi['ton_kho'], moi.get('tac_gia',''), moi.get('truong_dai_hoc',''), '')
            elif lh == 'Bản thảo': sp = BanThao(moi['ma_so'], moi['ten_san_pham'], moi['gia_co_ban'], moi['ton_kho'], moi.get('tac_gia',''), moi.get('tinh_trang',''))
            else: sp = None
            if sp:
                _kho.Danh_sach_cua_hang.them_vao_cuoi(sp)
                from ..loi_thuat_toan.ket_noi_sqlite import luu_mot_san_pham
                luu_mot_san_pham(sp)
            thong_bao = f'Đã làm lại: thêm "{moi["ten_san_pham"]}".'
        elif loai == 'xoa':
            ma_so = thao_tac['du_lieu_cu']['ma_so']
            _kho.Danh_sach_cua_hang.xoa_node(ma_so)
            from ..loi_thuat_toan.ket_noi_sqlite import xoa_mot_san_pham
            xoa_mot_san_pham(ma_so)
            thong_bao = f'Đã làm lại: xóa "{thao_tac["du_lieu_cu"]["ten_san_pham"]}".'
        elif loai == 'sua':
            moi = thao_tac['du_lieu_moi']
            ma_so = moi['ma_so']
            dl = {'ten_san_pham': moi['ten_san_pham'], 'gia_co_ban': moi['gia_co_ban'], 'ton_kho': moi['ton_kho']}
            for k in ('tac_gia','nha_xuat_ban','so_phat_hanh','ngay_xuat_ban','truong_dai_hoc','tinh_trang'):
                if k in moi: dl[k] = moi[k]
            sp = _kho.Danh_sach_cua_hang.tim_theo_ma_so(ma_so)
            if sp:
                _kho.Danh_sach_cua_hang.cap_nhat_node(ma_so, dl)
                from ..loi_thuat_toan.ket_noi_sqlite import cap_nhat_san_pham
                cap_nhat_san_pham(sp)
            thong_bao = f'Đã làm lại: cập nhật "{moi["ten_san_pham"]}".'
        else:
            thong_bao = 'Thao tác không xác định.'
        return JsonResponse({'trang_thai': 'thanh_cong', 'thong_bao': thong_bao})
    except Exception as loi:
        return JsonResponse({'trang_thai': 'loi', 'thong_bao': f'Lỗi khi làm lại: {str(loi)}'}, status=500)
