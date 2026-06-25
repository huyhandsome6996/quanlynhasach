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
    """
    API POST /hoan-tac - hoàn tác thao tác gần nhất (Undo).
    
    [Tương tác JS]: Được gọi bởi hàm `hoan_tac()` trong file `goi_du_lieu.js`.

    """
    # [NGUYÊN LÝ ĐỒ ÁN - ĐỌC KỸ TRƯỚC KHI LÊN BẢNG]
    # Đảm bảo danh sách liên kết đã được nạp vào RAM. Nếu chưa có thì khởi tạo.
    # Nguồn: Biến `Danh_sach_cua_hang` và hàm `khoi_tao_danh_sach()` được lấy từ file `khoi_tao.py`.
    if _kho.Danh_sach_cua_hang is None:
        _kho.khoi_tao_danh_sach()
        
    try:
        # [NGUYÊN LÝ STACK - LIFO] (Vào sau ra trước)
        # BƯỚC 1: Gọi lệnh POP (lay_ra) để bốc hành động cuối cùng trên đỉnh của Ngăn xếp Undo.
        # Nguồn: Biến `Bo_undoredo['undo']` là một đối tượng thuộc class `Stack` được tạo sẵn từ file `khoi_tao.py`.
        # Tác động đồ án: Chứng minh bạn biết cách lấy phần tử ra khỏi Stack.
        thao_tac = _kho.Bo_undoredo['undo'].lay_ra()
        
        # Nếu rỗng (chưa có thao tác nào để undo), trả về lỗi 400.
        if thao_tac is None:
            return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Không có thao tác nào để hoàn tác.'}, status=400)
            
        # [NGUYÊN LÝ STACK - LIFO]
        # BƯỚC 2: Gọi lệnh PUSH (day_vao) để ném thẳng cái thao tác vừa POP sang Ngăn xếp Redo.
        # Tác động đồ án: Để dự phòng, lỡ người dùng bấm "Làm lại" thì ta lại POP từ Redo ra.
        _kho.Bo_undoredo['redo'].day_vao(thao_tac)
        
        # Lấy thông tin xem người dùng vừa làm cái trò gì (them, xoa, hay sua).
        loai = thao_tac['loai']
        
        # [NGUYÊN LÝ NGHỊCH ĐẢO HÀNH ĐỘNG] - Nếu cũ là "Thêm" thì hoàn tác phải là "XÓA".
        if loai == 'them':
            ma_so = thao_tac['du_lieu_moi']['ma_so'] # Lấy mã sách vừa thêm
            
            # [NGUYÊN LÝ ĐỒNG BỘ TẦNG 1: TRÊN RAM]
            # Tác động đồ án: Chạy thuật toán xóa node trên cấu trúc Danh Sách Liên Kết, cho tốc độ cực nhanh.
            _kho.Danh_sach_cua_hang.xoa_node(ma_so)
            
            # [NGUYÊN LÝ ĐỒNG BỘ TẦNG 2: XUỐNG Ổ CỨNG]
            # Nguồn: Hàm `xoa_mot_san_pham` được import từ file `loi_thuat_toan/ket_noi_sqlite.py`.
            # Tác dụng: Thực thi câu lệnh SQL DELETE để xóa dữ liệu cứng dưới Database.
            # Tác động đồ án: Xóa luôn dưới Database SQLite để lúc tắt Server mở lại không bị mất dữ liệu.
            from ..loi_thuat_toan.ket_noi_sqlite import xoa_mot_san_pham
            xoa_mot_san_pham(ma_so)
            
            thong_bao = f'Đã hoàn tác: xóa "{thao_tac["du_lieu_moi"]["ten_san_pham"]}".'
            
        # [NGUYÊN LÝ NGHỊCH ĐẢO] - Nếu cũ lỡ tay "Xóa", thì hoàn tác phải "THÊM LẠI" y hệt.
        elif loai == 'xoa':
            # Nguồn: Import các Class từ file `loi_thuat_toan/lop_doi_tuong.py`.
            # Tác dụng: Cung cấp bản thiết kế OOP để ta đúc lại đối tượng sách bị xóa.
            from ..loi_thuat_toan.lop_doi_tuong import Sach, TapChi, BaoGiay, LuanVan, BanThao
            cu = thao_tac['du_lieu_cu'] # Lấy nguyên cục dữ liệu cũ của quyển sách đã xóa
            lh = cu['loai_hang']
            
            # [NGUYÊN LÝ TÍNH ĐA HÌNH TRONG OOP (Polymorphism)]
            # Tác động đồ án: Kiểm tra xem loại sách là gì để dùng đúng Class con (Sach, TapChi...) tạo lại Object.
            if lh == 'Sách': sp = Sach(cu['ma_so'], cu['ten_san_pham'], cu['gia_co_ban'], cu['ton_kho'], cu.get('tac_gia',''), cu.get('nha_xuat_ban',''))
            elif lh == 'Tạp chí': sp = TapChi(cu['ma_so'], cu['ten_san_pham'], cu['gia_co_ban'], cu['ton_kho'], cu.get('so_phat_hanh',''))
            elif lh == 'Báo giấy': sp = BaoGiay(cu['ma_so'], cu['ten_san_pham'], cu['gia_co_ban'], cu['ton_kho'], cu.get('ngay_xuat_ban',''))
            elif lh == 'Luận văn': sp = LuanVan(cu['ma_so'], cu['ten_san_pham'], cu['gia_co_ban'], cu['ton_kho'], cu.get('tac_gia',''), cu.get('truong_dai_hoc',''), '')
            elif lh == 'Bản thảo': sp = BanThao(cu['ma_so'], cu['ten_san_pham'], cu['gia_co_ban'], cu['ton_kho'], cu.get('tac_gia',''), cu.get('tinh_trang',''))
            else: sp = None
            
            if sp:
                # [ĐỒNG BỘ TẦNG 1: RAM] Phục hồi nó lại vào đuôi Danh Sách Liên Kết.
                _kho.Danh_sach_cua_hang.them_vao_cuoi(sp)
                
                # [ĐỒNG BỘ TẦNG 2: Ổ CỨNG] Cập nhật lại vào SQLite để bảo lưu lâu dài.
                # Nguồn: Hàm `luu_mot_san_pham` import từ file `loi_thuat_toan/ket_noi_sqlite.py`.
                # Tác dụng: Chạy câu lệnh SQL INSERT để nhét đối tượng sách này vào lại Database.
                from ..loi_thuat_toan.ket_noi_sqlite import luu_mot_san_pham
                luu_mot_san_pham(sp)
                
            thong_bao = f'Đã hoàn tác: thêm lại "{cu["ten_san_pham"]}".'
            
        # [NGUYÊN LÝ NGHỊCH ĐẢO] - Nếu cũ sửa sai, thì lấy dữ liệu trước khi sửa đè ngược lại.
        elif loai == 'sua':
            cu = thao_tac['du_lieu_cu'] # Đây là dữ liệu gốc trước khi người dùng bậy bạ
            ma_so = cu['ma_so']
            
            # Lọc ra các trường cần cập nhật
            dl = {'ten_san_pham': cu['ten_san_pham'], 'gia_co_ban': cu['gia_co_ban'], 'ton_kho': cu['ton_kho']}
            for k in ('tac_gia','nha_xuat_ban','so_phat_hanh','ngay_xuat_ban','truong_dai_hoc','tinh_trang'):
                if k in cu: dl[k] = cu[k]
                
            # Móc quyển sách đó ra khỏi Danh Sách Liên Kết
            sp = _kho.Danh_sach_cua_hang.tim_theo_ma_so(ma_so)
            if sp:
                # [ĐỒNG BỘ TẦNG 1: RAM] Gọi hàm cập nhật node trong Danh sách liên kết đè thông tin cũ vào.
                _kho.Danh_sach_cua_hang.cap_nhat_node(ma_so, dl)
                
                # [ĐỒNG BỘ TẦNG 2: Ổ CỨNG] Gọi hàm cập nhật SQLite để đè thông tin cũ xuống DB.
                # Nguồn: Hàm `cap_nhat_san_pham` import từ file `loi_thuat_toan/ket_noi_sqlite.py`.
                # Tác dụng: Chạy câu lệnh SQL UPDATE để sửa lại dữ liệu bảng SanPham.
                from ..loi_thuat_toan.ket_noi_sqlite import cap_nhat_san_pham
                cap_nhat_san_pham(sp)
                
            thong_bao = f'Đã hoàn tác: khôi phục thông tin "{cu["ten_san_pham"]}".'
            
        else:
            thong_bao = 'Thao tác không xác định.'
            
        # Gửi cục JSON này về cho Javascript để hiện thông báo Toast màu xanh lá cây
        return JsonResponse({'trang_thai': 'thanh_cong', 'thong_bao': thong_bao})
        
    except Exception as loi:
        # Nếu có exception (bị crash), bắt lấy và trả về JSON báo lỗi màu đỏ.
        return JsonResponse({'trang_thai': 'loi', 'thong_bao': f'Lỗi khi hoàn tác: {str(loi)}'}, status=500)


@csrf_exempt
@require_http_methods(['POST'])
def lam_lai(request):
    """
    API POST /lam-lai - làm lại thao tác đã hoàn tác (Redo).
    
    [Tương tác JS]: Được gọi bởi hàm `lam_lai()` trong file `goi_du_lieu.js`.
    """
    # [NGUYÊN LÝ ĐỒ ÁN - ĐỌC KỸ TRƯỚC KHI LÊN BẢNG]
    # Đảm bảo danh sách liên kết đã được nạp vào RAM.
    # Nguồn: Biến `Danh_sach_cua_hang` và hàm `khoi_tao_danh_sach()` được lấy từ file `khoi_tao.py`.
    if _kho.Danh_sach_cua_hang is None:
        _kho.khoi_tao_danh_sach()
        
    try:
        # [NGUYÊN LÝ STACK - LIFO] (Vào sau ra trước)
        # BƯỚC 1: Lần này, ta gọi lệnh POP (lay_ra) nhưng là bốc từ đỉnh của Ngăn xếp Redo.
        # Nguồn: Biến `Bo_undoredo['redo']` là một đối tượng thuộc class `Stack` tạo sẵn từ file `khoi_tao.py`.
        # Tác động đồ án: Chứng minh bạn hiểu sự tương tác luân phiên giữa 2 Stack (Undo và Redo).
        thao_tac = _kho.Bo_undoredo['redo'].lay_ra()
        
        # Nếu rỗng (tức là user chưa từng Undo cái gì cả), thì lấy đâu ra mà Redo. Báo lỗi 400.
        if thao_tac is None:
            return JsonResponse({'trang_thai': 'loi', 'thong_bao': 'Không có thao tác nào để làm lại.'}, status=400)
            
        # [NGUYÊN LÝ STACK - LIFO]
        # BƯỚC 2: Gọi lệnh PUSH (day_vao) ném thao tác này TRỞ VỀ lại Ngăn xếp Undo.
        # Tác động đồ án: Để user có thể lật bánh xèo, Redo xong lại Undo tiếp vô hạn lần.
        _kho.Bo_undoredo['undo'].day_vao(thao_tac)
        
        # Lấy thông tin loại thao tác (them, xoa, sua).
        loai = thao_tac['loai']
        
        # [NGUYÊN LÝ PHỤC HỒI HÀNH ĐỘNG] - Nếu hành động gốc là "Thêm", thì Redo là "THÊM LẠI LẦN NỮA".
        if loai == 'them':
            # Nguồn: Import các Class từ file `loi_thuat_toan/lop_doi_tuong.py`.
            # Tác dụng: Lấy khuôn (Class) để đúc lại đối tượng sách mới y hệt lúc user tạo.
            from ..loi_thuat_toan.lop_doi_tuong import Sach, TapChi, BaoGiay, LuanVan, BanThao
            moi = thao_tac['du_lieu_moi']
            lh = moi['loai_hang']
            
            # [NGUYÊN LÝ TÍNH ĐA HÌNH TRONG OOP (Polymorphism)]
            # Tác động đồ án: Đúc đúng đối tượng con (Sach hay TapChi...) dựa vào `loai_hang`.
            if lh == 'Sách': sp = Sach(moi['ma_so'], moi['ten_san_pham'], moi['gia_co_ban'], moi['ton_kho'], moi.get('tac_gia',''), moi.get('nha_xuat_ban',''))
            elif lh == 'Tạp chí': sp = TapChi(moi['ma_so'], moi['ten_san_pham'], moi['gia_co_ban'], moi['ton_kho'], moi.get('so_phat_hanh',''))
            elif lh == 'Báo giấy': sp = BaoGiay(moi['ma_so'], moi['ten_san_pham'], moi['gia_co_ban'], moi['ton_kho'], moi.get('ngay_xuat_ban',''))
            elif lh == 'Luận văn': sp = LuanVan(moi['ma_so'], moi['ten_san_pham'], moi['gia_co_ban'], moi['ton_kho'], moi.get('tac_gia',''), moi.get('truong_dai_hoc',''), '')
            elif lh == 'Bản thảo': sp = BanThao(moi['ma_so'], moi['ten_san_pham'], moi['gia_co_ban'], moi['ton_kho'], moi.get('tac_gia',''), moi.get('tinh_trang',''))
            else: sp = None
            
            if sp:
                # [ĐỒNG BỘ TẦNG 1: RAM] Thêm đối tượng vào đuôi Danh Sách Liên Kết.
                _kho.Danh_sach_cua_hang.them_vao_cuoi(sp)
                
                # [ĐỒNG BỘ TẦNG 2: Ổ CỨNG] Lưu xuống Database SQLite.
                # Nguồn: Hàm `luu_mot_san_pham` import từ file `loi_thuat_toan/ket_noi_sqlite.py`.
                # Tác dụng: Chạy lệnh SQL INSERT.
                from ..loi_thuat_toan.ket_noi_sqlite import luu_mot_san_pham
                luu_mot_san_pham(sp)
                
            thong_bao = f'Đã làm lại: thêm "{moi["ten_san_pham"]}".'
            
        # [NGUYÊN LÝ PHỤC HỒI HÀNH ĐỘNG] - Nếu hành động gốc là "Xóa", thì Redo là "XÓA LẦN NỮA".
        elif loai == 'xoa':
            ma_so = thao_tac['du_lieu_cu']['ma_so'] # Chỉ cần mã số là đủ để sát sinh.
            
            # [ĐỒNG BỘ TẦNG 1: RAM] Gọi hàm xóa node trên Danh sách liên kết.
            _kho.Danh_sach_cua_hang.xoa_node(ma_so)
            
            # [ĐỒNG BỘ TẦNG 2: Ổ CỨNG] Gọi hàm xóa dưới DB.
            # Nguồn: Hàm `xoa_mot_san_pham` import từ file `loi_thuat_toan/ket_noi_sqlite.py`.
            # Tác dụng: Chạy lệnh SQL DELETE.
            from ..loi_thuat_toan.ket_noi_sqlite import xoa_mot_san_pham
            xoa_mot_san_pham(ma_so)
            
            thong_bao = f'Đã làm lại: xóa "{thao_tac["du_lieu_cu"]["ten_san_pham"]}".'
            
        # [NGUYÊN LÝ PHỤC HỒI HÀNH ĐỘNG] - Nếu hành động gốc là "Sửa", thì Redo là "SỬA LẠI THEO DỮ LIỆU MỚI".
        elif loai == 'sua':
            moi = thao_tac['du_lieu_moi'] # Ở Redo, ta dùng `du_lieu_moi` thay vì `du_lieu_cu` như bên Undo.
            ma_so = moi['ma_so']
            
            # Chuẩn bị Dictionary dữ liệu cập nhật
            dl = {'ten_san_pham': moi['ten_san_pham'], 'gia_co_ban': moi['gia_co_ban'], 'ton_kho': moi['ton_kho']}
            for k in ('tac_gia','nha_xuat_ban','so_phat_hanh','ngay_xuat_ban','truong_dai_hoc','tinh_trang'):
                if k in moi: dl[k] = moi[k]
                
            # Móc quyển sách cần sửa khỏi Danh sách trên RAM
            sp = _kho.Danh_sach_cua_hang.tim_theo_ma_so(ma_so)
            if sp:
                # [ĐỒNG BỘ TẦNG 1: RAM] Đè dữ liệu mới vào Node trên Danh Sách Liên Kết.
                _kho.Danh_sach_cua_hang.cap_nhat_node(ma_so, dl)
                
                # [ĐỒNG BỘ TẦNG 2: Ổ CỨNG] Đè dữ liệu mới xuống DB.
                # Nguồn: Hàm `cap_nhat_san_pham` import từ file `loi_thuat_toan/ket_noi_sqlite.py`.
                # Tác dụng: Chạy lệnh SQL UPDATE.
                from ..loi_thuat_toan.ket_noi_sqlite import cap_nhat_san_pham
                cap_nhat_san_pham(sp)
                
            thong_bao = f'Đã làm lại: cập nhật "{moi["ten_san_pham"]}".'
            
        else:
            thong_bao = 'Thao tác không xác định.'
            
        # Gửi thông báo xanh lá cho Front-end
        return JsonResponse({'trang_thai': 'thanh_cong', 'thong_bao': thong_bao})
        
    except Exception as loi:
        # Bắt lỗi sập server
        return JsonResponse({'trang_thai': 'loi', 'thong_bao': f'Lỗi khi làm lại: {str(loi)}'}, status=500)
