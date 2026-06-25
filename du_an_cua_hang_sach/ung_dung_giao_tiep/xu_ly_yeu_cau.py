"""
Tệp xử lý yêu cầu HTTP (Views) cho ứng dụng Django.
==================================================================

File này đóng vai trò là BỘ NÃO của ứng dụng — nhận mọi yêu cầu HTTP
từ trình duyệt (frontend), xử lý, rồi trả về kết quả (JSON hoặc trang HTML).

Tất cả endpoint được tổ chức thành 9 nhóm theo barem chấm điểm:
    1) Đăng nhập / Đăng xuất / Phân quyền  (Admin / Nhân viên)
    2) Đọc danh sách                        (GET /danh-sach)
    3) Thêm sản phẩm                        (POST /them-san-pham)
    4) Sửa sản phẩm                         (POST /sua-san-pham)
    5) Xóa sản phẩm                         (POST /xoa-san-pham)   <- CHỈ ADMIN
    6) Tìm kiếm + Sắp xếp                   (GET /tim-kiem, /sap-xep)
    7) Thống kê                             (GET /thong-ke)
    8) Undo/Redo  (Stack LIFO)              (POST /hoan-tac, /lam-lai)
    9) Giỏ hàng  (Queue FIFO)               (POST /them-gio-hang, /xem-gio-hang,
                                              /xoa-gio-hang, /thanh-toan)

Mỗi nhóm đều bọc try/except để bắt lỗi theo yêu cầu của barem.
"""

# Nhập lớp JsonResponse từ django.http: dùng để trả về dữ liệu dạng JSON cho frontend.
from django.http import JsonResponse, HttpResponse
# Nhập hàm render (trả trang HTML + dữ liệu) và redirect (chuyển hướng URL) từ django.shortcuts.
from django.shortcuts import render, redirect
# csrf_exempt: tắt kiểm tra token CSRF (anti-forgery) cho API POST — cần thiết vì
# frontend gọi API bằng fetch thuần, không kèm token Django generate ra.
from django.views.decorators.csrf import csrf_exempt
# require_http_methods: giới hạn view chỉ chấp nhận các method HTTP được liệt kê
# (ví dụ: ['POST'] => từ chối GET, PUT, DELETE...).
from django.views.decorators.http import require_http_methods
# json: thư viện chuẩn của Python để parse (đọc) và dumps (ghi) chuỗi JSON.
import json

# ============================================================
# BIẾN TOÀN CỤC — Giữ trạng thái ứng dụng khi server đang chạy
# ============================================================
# Danh_sach_cua_hang: đối tượng DoublyLinkedList (DSLK đôi) chứa mọi mặt hàng.
#                      None nghĩa là chưa khởi tạo (sẽ tạo trong khoi_tao_danh_sach).
Danh_sach_cua_hang = None
# Bo_undoredo: dict chứa 2 Stack — 'undo' (hoàn tác) và 'redo' (làm lại).
Bo_undoredo        = None
# Gio_hang_hien_tai: đối tượng HangDoi (Queue) — giỏ hàng chung của phiên làm việc.
Gio_hang_hien_tai  = None


# ============================================================
# KHỞI TẠO HỆ THỐNG
# ============================================================

def khoi_tao_danh_sach():
    """
    Khởi tạo DSLK đôi + Undo/Redo + Giỏ hàng; nạp dữ liệu từ SQLite.

    Hàm này chạy 1 lần đầu tiên khi có request đến mà biến toàn cục còn None.
    Sau đó các biến toàn cục được giữ nguyên trong RAM suốt vòng đời server.
    """
    # Khai báo dùng biến toàn cục (global) để có thể GÁN giá trị mới cho chúng.
    global Danh_sach_cua_hang, Bo_undoredo, Gio_hang_hien_tai
    # Import DoublyLinkedList (DSLK đôi) từ module danh_sach_lien_ket.py
    # trong cùng package loi_thuat_toan.
    from .loi_thuat_toan.danh_sach_lien_ket import DoublyLinkedList
    # Import 2 lớp cấu trúc dữ liệu tự cài đặt: NganXep (Stack) + HangDoi (Queue).
    from .loi_thuat_toan.cau_truc_du_lieu import NganXep, HangDoi
    # Import hàm tải dữ liệu từ SQLite + hàm tạo dữ liệu mẫu nếu DB rỗng.
    from .loi_thuat_toan.ket_noi_sqlite import tai_du_lieu, tao_du_lieu_mau_neu_rong
    # Import hàm tạo 2 tài khoản mặc định (admin + nhân viên) nếu chưa có.
    from .loi_thuat_toan.nguoi_dung import khoi_tao_nguoi_dung_mac_dinh

    # Bảng SQLite + dữ liệu mẫu + tài khoản mẫu (chỉ tạo lần đầu).
    tao_du_lieu_mau_neu_rong()

    # Tạo đối tượng DSLK đôi RỖNG (chưa có node nào).
    Danh_sach_cua_hang = DoublyLinkedList()
    # Tải toàn bộ sản phẩm trong SQLite ra và nhét từng cái vào DSLK đôi.
    tai_du_lieu(Danh_sach_cua_hang)

    # Tạo 2 Stack dùng cho tính năng Undo (hoàn tác) + Redo (làm lại).
    ngan_xep_undo = NganXep()
    ngan_xep_redo = NganXep()
    # Bọc 2 stack vào 1 dict để dễ tham chiếu theo tên.
    Bo_undoredo = {'undo': ngan_xep_undo, 'redo': ngan_xep_redo}

    # Tạo 1 Queue dùng cho giỏ hàng (theo nguyên lý FIFO — vào trước ra trước).
    Gio_hang_hien_tai = HangDoi()

    # Tạo 2 tài khoản mẫu (admin/admin123 và nhanvien/nv123) nếu chưa có.
    khoi_tao_nguoi_dung_mac_dinh()

    # Bọc trong try/except vì một số terminal Windows không in được dấu tiếng Việt.
    try:
        # In thông báo đã nạp bao nhiêu mặt hàng vào DSLK (log ra console server).
        print(f'[KHOI DONG] Da nap {Danh_sach_cua_hang.so_luong} mat hang vao danh sach lien ket doi.')
    # Bắt lỗi UnicodeEncodeError: terminal không hỗ trợ Unicode → in bản không dấu.
    except UnicodeEncodeError:
        print(f'[KHOI DONG] Da nap {Danh_sach_cua_hang.so_luong} mat hang.')


# ============================================================
# NHÓM 1: ĐĂNG NHẬP / ĐĂNG XUẤT / PHÂN QUYỀN
# ============================================================

def trang_chu(request):
    """
    Trang chủ - nếu chưa đăng nhập thì chuyển sang trang đăng nhập.

    URL: GET /
    """
    # Nếu DSLK chưa được khởi tạo (server vừa khởi động) → tạo ngay.
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()
    # Nếu session KHÔNG CÓ key 'ten_dang_nhap' => người dùng chưa đăng nhập.
    if 'ten_dang_nhap' not in request.session:
        # Chuyển hướng (HTTP 302) về trang /dang-nhap để bắt đăng nhập.
        return redirect('/dang-nhap')
    # Lưu thông tin người dùng vào session để TEMPLATE (HTML) có thể đọc được.
    request.session['nguoi_dung'] = {
        'ten_dang_nhap': request.session.get('ten_dang_nhap'),       # Tên đăng nhập.
        'ho_ten':        request.session.get('ho_ten', ''),           # Họ tên đầy đủ.
        'vai_tro':       request.session.get('vai_tro', 'nhan_vien'),# admin hoặc nhan_vien.
        'la_admin':      request.session.get('vai_tro', 'nhan_vien') == 'admin'  # True/False.
    }
    # Render (kết xuất) trang HTML trang_chu.html và trả về client.
    return render(request, 'trang_chu.html')


def trang_dang_nhap(request):
    """
    Hiển thị form đăng nhập.

    URL: GET /dang-nhap
    """
    # Đảm bảo hệ thống đã khởi tạo (tránh lỗi khi người dùng vào thẳng /dang-nhap).
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()
    # Nếu người dùng ĐÃ đăng nhập rồi → không cần đăng nhập nữa → chuyển về trang chủ.
    if 'ten_dang_nhap' in request.session:
        return redirect('/')
    # Trả về trang HTML dang_nhap.html (form nhập tên + mật khẩu).
    return render(request, 'dang_nhap.html')


# Decorator @csrf_exempt: tắt kiểm tra token CSRF cho view này
# (vì frontend gửi JSON bằng fetch, không kèm form Django).
@csrf_exempt
# Decorator @require_http_methods: chỉ cho phép method POST (không cho GET/PUT/DELETE).
@require_http_methods(['POST'])
def xu_ly_dang_nhap(request):
    """
    API POST /dang-nhap - kiểm tra tài khoản và lưu session.

    Frontend gửi JSON: {"ten_dang_nhap": "...", "mat_khau": "..."}
    Trả về JSON: {"trang_thai": "thanh_cong", "nguoi_dung": {...}}
    """
    try:
        # Parse (chuyển) body của request từ chuỗi JSON thành dict Python.
        du_lieu = json.loads(request.body)
        # Lấy 'ten_dang_nhap', nếu thiếu thì mặc định ''. .strip() xoá khoảng trắng 2 đầu.
        ten_dang_nhap = du_lieu.get('ten_dang_nhap', '').strip()
        # Lấy 'mat_khau' tương tự.
        mat_khau      = du_lieu.get('mat_khau', '').strip()

        # Nếu thiếu tên đăng nhập HOẶC thiếu mật khẩu → trả lỗi 400 (Bad Request).
        if not ten_dang_nhap or not mat_khau:
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': 'Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.'},
                status=400
            )

        # Import hàm kiem_tra_dang_nhap từ module nguoi_dung (chỉ import khi cần).
        from .loi_thuat_toan.nguoi_dung import kiem_tra_dang_nhap
        # Gọi hàm kiểm tra — trả về đối tượng NguoiDung nếu đúng, None nếu sai.
        nguoi_dung = kiem_tra_dang_nhap(ten_dang_nhap, mat_khau)

        # Nếu hàm trả về None => sai tài khoản hoặc mật khẩu → trả lỗi 401 (Unauthorized).
        if nguoi_dung is None:
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': 'Sai tên đăng nhập hoặc mật khẩu.'},
                status=401
            )

        # Đăng nhập thành công → Lưu thông tin vào SESSION (cookie phiên làm việc).
        # Session được Django tự động mã hóa và lưu ở server, client chỉ giữ ID.
        request.session['ten_dang_nhap'] = nguoi_dung.ten_dang_nhap
        request.session['ho_ten']        = nguoi_dung.ho_ten
        request.session['vai_tro']       = nguoi_dung.vai_tro

        # Trả về JSON báo thành công + thông tin người dùng (để frontend hiển thị).
        return JsonResponse({
            'trang_thai': 'thanh_cong',
            'thong_bao':  f'Chào mừng {nguoi_dung.ho_ten}!',
            'nguoi_dung': nguoi_dung.chuyen_thanh_dict()
        })
    # Nếu body gửi lên không phải JSON hợp lệ → bắt JSONDecodeError → trả 400.
    except json.JSONDecodeError:
        return JsonResponse(
            {'trang_thai': 'loi', 'thong_bao': 'Dữ liệu gửi lên không hợp lệ.'},
            status=400
        )
    # Bất kỳ lỗi nào khác (lỗi DB, lỗi code...) → bắt Exception chung → trả 500.
    except Exception as loi:
        return JsonResponse(
            {'trang_thai': 'loi', 'thong_bao': f'Lỗi máy chủ: {str(loi)}'},
            status=500
        )


# Tắt CSRF cho endpoint đăng xuất (POST không cần token).
@csrf_exempt
# Cho phép cả POST (gọi từ JS) lẫn GET (khi user gõ URL trực tiếp).
@require_http_methods(['POST', 'GET'])
def xu_ly_dang_xuat(request):
    """
    API /dang-xuat - xóa session và quay về trang đăng nhập.
    """
    try:
        # flush() xóa toàn bộ dữ liệu session => user bị "đá" ra.
        request.session.flush()
        # Nếu là GET (người dùng gõ URL) → chuyển hướng về trang đăng nhập.
        if request.method == 'GET':
            return redirect('/dang-nhap')
        # Nếu là POST (frontend gọi fetch) → trả JSON thành công.
        return JsonResponse({
            'trang_thai': 'thanh_cong',
            'thong_bao':  'Đã đăng xuất thành công.'
        })
    # Bất kỳ lỗi nào → trả JSON lỗi 500.
    except Exception as loi:
        return JsonResponse(
            {'trang_thai': 'loi', 'thong_bao': f'Lỗi khi đăng xuất: {str(loi)}'},
            status=500
        )


def thong_tin_nguoi_dung(request):
    """
    API GET /nguoi-dung - trả về thông tin người dùng đang đăng nhập.
    Frontend dùng để hiển thị tên + vai trò trên thanh đầu trang.
    """
    try:
        # Nếu chưa có 'ten_dang_nhap' trong session => chưa đăng nhập → trả 401.
        if 'ten_dang_nhap' not in request.session:
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': 'Chưa đăng nhập.'},
                status=401
            )
        # Trả JSON chứa thông tin người dùng lấy từ session.
        return JsonResponse({
            'trang_thai': 'thanh_cong',
            'nguoi_dung': {
                'ten_dang_nhap': request.session.get('ten_dang_nhap'),
                'ho_ten':        request.session.get('ho_ten', ''),
                'vai_tro':       request.session.get('vai_tro', 'nhan_vien'),
                'la_admin':      request.session.get('vai_tro', 'nhan_vien') == 'admin'
            }
        })
    # Lỗi bất ngờ → 500.
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


# ============================================================
# NHÓM 2: ĐỌC DANH SÁCH
# ============================================================

def lay_danh_sach(request):
    """
    API GET /danh-sach - trả về toàn bộ mặt hàng dưới dạng JSON.
    Frontend gọi khi load trang để fill vào bảng dữ liệu.
    """
    try:
        # Khởi tạo nếu chưa (defensive — phòng server mới khởi động).
        if Danh_sach_cua_hang is None:
            khoi_tao_danh_sach()
        # chuyen_thanh_danh_sach(): duyệt DSLK đôi, trả list các dict sản phẩm.
        danh_sach = Danh_sach_cua_hang.chuyen_thanh_danh_sach()
        # Trả JSON: trạng thái + số lượng + danh sách.
        return JsonResponse({
            'trang_thai': 'thanh_cong',
            'so_luong':   Danh_sach_cua_hang.so_luong,
            'danh_sach':  danh_sach
        })
    # Bất kỳ lỗi nào → trả 500 + thông báo chi tiết.
    except Exception as loi:
        return JsonResponse(
            {'trang_thai': 'loi', 'thong_bao': f'Lỗi khi tải danh sách: {str(loi)}'},
            status=500
        )


# ============================================================
# NHÓM 3: THÊM SẢN PHẨM
# ============================================================

# Tắt CSRF để frontend có thể POST JSON mà không cần token.
@csrf_exempt
# Chỉ chấp nhận method POST.
@require_http_methods(['POST'])
def them_san_pham(request):
    """
    API POST /them-san-pham - thêm một sản phẩm mới (hỗ trợ 5 loại).

    5 loại: Sách, Tạp chí, Báo giấy, Luận văn, Bản thảo.
    Mỗi loại có các trường dữ liệu riêng (tac_gia, so_phat_hanh, ...).
    """
    # Defensive: khởi tạo nếu chưa.
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()
    try:
        # Parse body JSON thành dict.
        du_lieu        = json.loads(request.body)
        # Lấy 'loai_hang' (Sách/Tạp chí/Báo giấy/Luận văn/Bản thảo).
        loai_hang      = du_lieu.get('loai_hang', '').strip()
        # Mã số sản phẩm (duy nhất, do user nhập — ví dụ: MH001).
        ma_so          = du_lieu.get('ma_so', '').strip()
        # Tên sản phẩm (ví dụ: "Sách Python cơ bản").
        ten_san_pham   = du_lieu.get('ten_san_pham', '').strip()
        # Giá cơ bản (float để hỗ trợ số thập phân).
        gia_co_ban     = float(du_lieu.get('gia_co_ban', 0))
        # Số lượng tồn kho (int — không thể có 0.5 cuốn sách).
        ton_kho        = int(du_lieu.get('ton_kho', 0))

        # --- VALIDATE DỮ LIỆU (kiểm tra hợp lệ) ---
        # Nếu thiếu mã, thiếu tên, hoặc thiếu loại → trả 400.
        if not ma_so or not ten_san_pham or not loai_hang:
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': 'Vui lòng điền đầy đủ thông tin.'},
                status=400
            )
        # Giá không được âm (không có sản phẩm nào giá âm).
        if gia_co_ban < 0:
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': 'Giá cơ bản không được âm.'},
                status=400
            )
        # Tồn kho không được âm.
        if ton_kho < 0:
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': 'Số lượng tồn kho không được âm.'},
                status=400
            )

        # --- KIỂM TRA TRÙNG MÃ ---
        # tim_theo_ma_so: tìm trong DSLK, trả về đối tượng nếu thấy, None nếu chưa có.
        if Danh_sach_cua_hang.tim_theo_ma_so(ma_so) is not None:
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': f'Mã số "{ma_so}" đã tồn tại.'},
                status=400
            )

        # --- TẠO ĐỐI TƯỢNG THEO LOẠI HÀNG (ĐA HÌNH OOP) ---
        # Import 5 lớp con kế thừa từ MatHang.
        from .loi_thuat_toan.lop_doi_tuong import Sach, TapChi, BaoGiay, LuanVan, BanThao

        # Nếu là Sách → cần thêm: tác giả + nhà xuất bản.
        if loai_hang == 'Sách':
            tac_gia       = du_lieu.get('tac_gia', '').strip()
            nha_xuat_ban  = du_lieu.get('nha_xuat_ban', '').strip()
            # Validate: cả 2 không được rỗng.
            if not tac_gia or not nha_xuat_ban:
                return JsonResponse(
                    {'trang_thai': 'loi', 'thong_bao': 'Vui lòng nhập tác giả và nhà xuất bản.'},
                    status=400
                )
            # Tạo đối tượng Sach (lớp con của MatHang).
            san_pham_moi = Sach(ma_so, ten_san_pham, gia_co_ban, ton_kho, tac_gia, nha_xuat_ban)

        # Nếu là Tạp chí → cần: số phát hành (ví dụ: "Tạp chí số 12").
        elif loai_hang == 'Tạp chí':
            so_phat_hanh = du_lieu.get('so_phat_hanh', '').strip()
            if not so_phat_hanh:
                return JsonResponse(
                    {'trang_thai': 'loi', 'thong_bao': 'Vui lòng nhập số phát hành.'},
                    status=400
                )
            san_pham_moi = TapChi(ma_so, ten_san_pham, gia_co_ban, ton_kho, so_phat_hanh)

        # Nếu là Báo giấy → cần: ngày xuất bản (ví dụ: "12/06/2025").
        elif loai_hang == 'Báo giấy':
            ngay_xuat_ban = du_lieu.get('ngay_xuat_ban', '').strip()
            if not ngay_xuat_ban:
                return JsonResponse(
                    {'trang_thai': 'loi', 'thong_bao': 'Vui lòng nhập ngày xuất bản.'},
                    status=400
                )
            san_pham_moi = BaoGiay(ma_so, ten_san_pham, gia_co_ban, ton_kho, ngay_xuat_ban)

        # Nếu là Luận văn → cần: tác giả + trường đại học.
        elif loai_hang == 'Luận văn':
            tac_gia        = du_lieu.get('tac_gia', '').strip()
            truong_dai_hoc = du_lieu.get('truong_dai_hoc', '').strip()
            if not tac_gia or not truong_dai_hoc:
                return JsonResponse(
                    {'trang_thai': 'loi', 'thong_bao': 'Vui lòng nhập tác giả và trường đại học.'},
                    status=400
                )
            # Tham số cuối là chuỗi rỗng '' (chưa dùng — để mở rộng sau).
            san_pham_moi = LuanVan(ma_so, ten_san_pham, gia_co_ban, ton_kho,
                                   tac_gia, truong_dai_hoc, '')
        # Nếu là Bản thảo → cần: tác giả + tình trạng (đã duyệt/chưa duyệt).
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
        # Nếu loai_hang không khớp bất kỳ loại nào ở trên → trả 400.
        else:
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': 'Loại hàng không hợp lệ.'},
                status=400
            )

        # --- LƯU VÀO DSLK + SQLITE ---
        # them_vao_cuoi: thêm sản phẩm vào cuối DSLK đôi (O(1) vì giữ con trỏ cuối).
        Danh_sach_cua_hang.them_vao_cuoi(san_pham_moi)
        # Lưu luôn vào SQLite để khi server restart không mất dữ liệu.
        from .loi_thuat_toan.ket_noi_sqlite import luu_mot_san_pham
        luu_mot_san_pham(san_pham_moi)

        # --- GHI VÀO STACK UNDO (để có thể hoàn tác) ---
        # Đẩy dict thao tác lên đỉnh stack Undo.
        Bo_undoredo['undo'].day_vao({
            'loai':        'them',                              # Loại thao tác.
            'du_lieu_cu':  None,                                # Trước khi thêm: chưa có gì.
            'du_lieu_moi': san_pham_moi.chuyen_thanh_dict()      # Sau khi thêm: sản phẩm mới.
        })
        # Khi có thao tác mới → xóa hết stack Redo (không thể redo thao tác cũ nữa).
        Bo_undoredo['redo'].xoa_tat_ca()

        # Trả JSON thành công.
        return JsonResponse({
            'trang_thai': 'thanh_cong',
            'thong_bao':  f'Đã thêm "{ten_san_pham}" vào cửa hàng.'
        })

    # Lỗi parse JSON → 400.
    except json.JSONDecodeError:
        return JsonResponse(
            {'trang_thai': 'loi', 'thong_bao': 'Dữ liệu gửi lên không hợp lệ.'},
            status=400
        )
    # ValueError: khi float() hoặc int() thất bại (user nhập "abc" cho giá) → 400.
    except ValueError:
        return JsonResponse(
            {'trang_thai': 'loi', 'thong_bao': 'Giá hoặc số lượng phải là số.'},
            status=400
        )
    # Lỗi bất kỳ khác → 500.
    except Exception as loi:
        return JsonResponse(
            {'trang_thai': 'loi', 'thong_bao': f'Lỗi máy chủ: {str(loi)}'},
            status=500
        )


# ============================================================
# NHÓM 4: SỬA SẢN PHẨM
# ============================================================

# Tắt CSRF + chỉ cho POST.
@csrf_exempt
@require_http_methods(['POST'])
def sua_san_pham(request):
    """
    API POST /sua-san-pham - cập nhật thông tin sản phẩm.

    Frontend gửi mã sản phẩm cần sửa + các trường mới → view cập nhật
    trong DSLK + SQLite, đồng thời ghi stack Undo để có thể hoàn tác.
    """
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()
    try:
        # Parse JSON body.
        du_lieu      = json.loads(request.body)
        # Mã số của sản phẩm cần sửa (dùng để tìm trong DSLK).
        ma_so        = du_lieu.get('ma_so', '').strip()
        # Tên mới (có thể giữ nguyên nếu user không đổi).
        ten_san_pham = du_lieu.get('ten_san_pham', '').strip()
        # Giá mới.
        gia_co_ban   = float(du_lieu.get('gia_co_ban', 0))
        # Tồn kho mới.
        ton_kho      = int(du_lieu.get('ton_kho', 0))

        # Validate: mã số không rỗng.
        if not ma_so:
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': 'Mã số không được để trống.'},
                status=400
            )

        # Tìm sản phẩm hiện tại trong DSLK để LƯU DỮ LIỆU CŨ (cho Undo).
        san_pham_cu = Danh_sach_cua_hang.tim_theo_ma_so(ma_so)
        # Nếu không tìm thấy → trả 404.
        if san_pham_cu is None:
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': f'Không tìm thấy sản phẩm mã {ma_so}.'},
                status=404
            )

        # Lưu snapshot dữ liệu cũ (trước khi sửa) để undo có thể khôi phục.
        du_lieu_cu = san_pham_cu.chuyen_thanh_dict()

        # Dict chứa các trường mới (chỉ trường chung — có ở mọi loại hàng).
        du_lieu_moi = {
            'ten_san_pham': ten_san_pham,
            'gia_co_ban':   gia_co_ban,
            'ton_kho':      ton_kho
        }

        # Lấy loại hàng từ sản phẩm cũ (không cho phép đổi loại khi sửa).
        loai_hang = san_pham_cu.loai_hang
        # Mỗi loại có các trường riêng khác nhau → cập nhật tương ứng.
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

        # Cập nhật node trong DSLK đôi với dữ liệu mới.
        Danh_sach_cua_hang.cap_nhat_node(ma_so, du_lieu_moi)
        # Đồng bộ xuống SQLite (persist).
        from .loi_thuat_toan.ket_noi_sqlite import cap_nhat_san_pham
        cap_nhat_san_pham(san_pham_cu)

        # GHI UNDO: lưu dict thao tác 'sua' với cả dữ liệu cũ + mới.
        Bo_undoredo['undo'].day_vao({
            'loai':        'sua',
            'du_lieu_cu':  du_lieu_cu,
            'du_lieu_moi': san_pham_cu.chuyen_thanh_dict()
        })
        # Có thao tác mới → xóa Redo.
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
    """
    API POST /xoa-san-pham - xóa sản phẩm. CHỈ ADMIN mới được xóa.

    Phân quyền: nhân viên gọi endpoint này sẽ bị từ chối với lỗi 403.
    """
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()

    # --- KIỂM TRA PHÂN QUYỀN ---
    # la_admin(request) trả True nếu vai_tro == 'admin'.
    if not la_admin(request):
        # Trả 403 Forbidden + thông báo rõ ràng cho user.
        return JsonResponse(
            {'trang_thai': 'loi', 'thong_bao': 'BẠN LÀ NHÂN VIÊN - KHÔNG ĐƯỢC PHÉP XÓA SẢN PHẨM.'},
            status=403
        )

    try:
        # Parse JSON body.
        du_lieu = json.loads(request.body)
        # Lấy mã số sản phẩm cần xóa.
        ma_so   = du_lieu.get('ma_so', '').strip()
        # Validate: mã không rỗng.
        if not ma_so:
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': 'Mã số không được để trống.'},
                status=400
            )

        # Lưu dữ liệu cũ TRƯỚC KHI XÓA (để có thể undo — khôi phục lại).
        san_pham_cu = Danh_sach_cua_hang.tim_theo_ma_so(ma_so)
        if san_pham_cu is None:
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': f'Không tìm thấy sản phẩm mã {ma_so}.'},
                status=404
            )
        du_lieu_cu = san_pham_cu.chuyen_thanh_dict()

        # Xóa node khỏi DSLK đôi (trả True nếu xóa thành công).
        ket_qua = Danh_sach_cua_hang.xoa_node(ma_so)
        if ket_qua:
            # Xóa luôn trong SQLite.
            from .loi_thuat_toan.ket_noi_sqlite import xoa_mot_san_pham
            xoa_mot_san_pham(ma_so)

            # GHI UNDO: thao tác 'xoa' — du_lieu_moi = None (vì sau khi xóa không còn gì).
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
            # Trường hợp xoa_node trả False (không tìm thấy) — trả 404.
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
    """
    API GET /tim-kiem - tìm kiếm nâng cao (tên / mã / loại).

    Query params:
        ?tu_khoa=python&tieu_chi=ten   (hoặc 'ma', 'loai')
    """
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()
    try:
        # Lấy từ khóa tìm kiếm từ query string (ví dụ: ?tu_khoa=python).
        tu_khoa   = request.GET.get('tu_khoa', '').strip()
        # Lấy tiêu chí tìm: 'ten' (mặc định), 'ma', hoặc 'loai'.
        tieu_chi  = request.GET.get('tieu_chi', 'ten').strip()

        # Phân nhánh theo tiêu chí:
        # Nếu tìm theo MÃ → tìm chính xác (tra theo ma_so).
        if tieu_chi == 'ma':
            ket_qua = []
            sp = Danh_sach_cua_hang.tim_theo_ma_so(tu_khoa)
            if sp:
                ket_qua.append(sp)
        # Nếu tìm theo LOẠI → lọc theo thể loại (Sách/Tạp chí/...).
        elif tieu_chi == 'loai':
            ket_qua = Danh_sach_cua_hang.tim_theo_the_loai(tu_khoa)
        # Mặc định: tìm theo TÊN (tìm gần đúng — substring).
        else:
            ket_qua = Danh_sach_cua_hang.tim_kiem(tu_khoa)

        # Chuyển từng đối tượng MatHang thành dict để JSON serialize được.
        danh_sach_ket_qua = []
        for mat_hang in ket_qua:
            # hasattr: kiểm tra đối tượng có hàm chuyen_thanh_dict không.
            if hasattr(mat_hang, 'chuyen_thanh_dict'):
                danh_sach_ket_qua.append(mat_hang.chuyen_thanh_dict())

        # Trả JSON: trạng thái + số kết quả + danh sách.
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
    """
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()
    try:
        # Lấy tiêu chí sắp xếp (mặc định: theo 'gia_ban').
        tieu_chi  = request.GET.get('tieu_chi', 'gia_ban').strip()
        # Gọi hàm sap_xep_tron (Merge Sort) — tự cài đặt trong DoublyLinkedList.
        Danh_sach_cua_hang.sap_xep_tron(tieu_chi)
        # Sau khi sắp xếp, chuyển DSLK thành list để trả về.
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
    """
    API GET /thong-ke - trả về thống kê tổng quan.

    Bao gồm: tổng số lượng, số mặt hàng sắp hết, tổng giá trị kho,
    mặt hàng đắt nhất, rẻ nhất, thống kê theo từng loại.
    """
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()
    try:
        # Gọi hàm thong_ke() của DSLK — trả dict số liệu.
        tk = Danh_sach_cua_hang.thong_ke()
        # Đổi tên key cho khớp với frontend JavaScript (camelCase vs snake_case).
        return JsonResponse({
            'trang_thai': 'thanh_cong',
            'thong_ke': {
                'tong_so_luong':         tk['tong_so'],            # Tổng số mặt hàng.
                'so_mat_hang_sap_het':   len(tk['sap_het_hang']),  # Số mặt hàng tồn kho < 5.
                'tong_gia_tri_ton_kho':  tk['tong_gia_tri_kho'],   # Tổng giá trị kho (đồng).
                'mat_hang_dat_nhat':     tk['dat_nhat'],           # Tên mặt hàng đắt nhất.
                'mat_hang_re_nhat':      tk['re_nhat'],            # Tên mặt hàng rẻ nhất.
                'thong_ke_theo_loai':    tk['theo_loai']           # Số lượng theo từng loại.
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
    """
    API POST /hoan-tac - hoàn tác thao tác gần nhất (Undo).

    Nguyên lý: Lấy thao tác gần nhất từ đỉnh stack Undo → đẩy sang Redo
    → thực hiện NGƯỢC thao tác đó (xóa nếu là 'them', thêm lại nếu là 'xoa'...).
    """
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()
    try:
        # Lấy thao tác trên đỉnh stack Undo (Pop).
        thao_tac = Bo_undoredo['undo'].lay_ra()
        # Nếu stack rỗng → không có gì để hoàn tác → trả 400.
        if thao_tac is None:
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': 'Không có thao tác nào để hoàn tác.'},
                status=400
            )

        # Đẩy thao tác vừa lấy sang stack Redo (để có thể redo lại sau).
        Bo_undoredo['redo'].day_vao(thao_tac)

        # Lấy loại thao tác để biết phải đảo ngược thế nào.
        loai = thao_tac['loai']
        # Trường hợp 1: Undo thao tác THÊM → phải XÓA sản phẩm đó đi.
        if loai == 'them':
            # Lấy mã sản phẩm từ dữ liệu mới (sản phẩm đã thêm).
            ma_so = thao_tac['du_lieu_moi']['ma_so']
            # Xóa khỏi DSLK.
            Danh_sach_cua_hang.xoa_node(ma_so)
            # Xóa khỏi SQLite.
            from .loi_thuat_toan.ket_noi_sqlite import xoa_mot_san_pham
            xoa_mot_san_pham(ma_so)
            # Thông báo cho user.
            thong_bao = f'Đã hoàn tác: xóa "{thao_tac["du_lieu_moi"]["ten_san_pham"]}".'

        # Trường hợp 2: Undo thao tác XÓA → phải THÊM LẠI sản phẩm cũ.
        elif loai == 'xoa':
            # Import 5 lớp con để tái tạo đối tượng.
            from .loi_thuat_toan.lop_doi_tuong import Sach, TapChi, BaoGiay, LuanVan, BanThao
            # Lấy dữ liệu cũ (đã lưu trước khi xóa).
            cu = thao_tac['du_lieu_cu']
            # Lấy loại hàng để biết cần tạo đối tượng lớp nào.
            loai_hang = cu['loai_hang']
            # Tái tạo đối tượng đúng loại (đa hình).
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
            # Nếu tái tạo thành công → thêm vào DSLK + SQLite.
            if sp:
                Danh_sach_cua_hang.them_vao_cuoi(sp)
                from .loi_thuat_toan.ket_noi_sqlite import luu_mot_san_pham
                luu_mot_san_pham(sp)
            thong_bao = f'Đã hoàn tác: thêm lại "{cu["ten_san_pham"]}".'

        # Trường hợp 3: Undo thao tác SỬA → đặt lại dữ liệu CŨ.
        elif loai == 'sua':
            cu = thao_tac['du_lieu_cu']
            ma_so = cu['ma_so']
            # Dict chứa các trường cũ cần khôi phục (trường chung).
            du_lieu_cu = {
                'ten_san_pham': cu['ten_san_pham'],
                'gia_co_ban':   cu['gia_co_ban'],
                'ton_kho':      cu['ton_kho']
            }
            # Khôi phục các trường riêng (nếu có) theo loại.
            if 'tac_gia' in cu:            du_lieu_cu['tac_gia'] = cu['tac_gia']
            if 'nha_xuat_ban' in cu:       du_lieu_cu['nha_xuat_ban'] = cu['nha_xuat_ban']
            if 'so_phat_hanh' in cu:       du_lieu_cu['so_phat_hanh'] = cu['so_phat_hanh']
            if 'ngay_xuat_ban' in cu:      du_lieu_cu['ngay_xuat_ban'] = cu['ngay_xuat_ban']
            if 'truong_dai_hoc' in cu:     du_lieu_cu['truong_dai_hoc'] = cu['truong_dai_hoc']
            if 'tinh_trang' in cu:         du_lieu_cu['tinh_trang'] = cu['tinh_trang']

            # Tìm sản phẩm trong DSLK.
            sp = Danh_sach_cua_hang.tim_theo_ma_so(ma_so)
            if sp:
                # Áp dụng dữ liệu cũ lên node.
                Danh_sach_cua_hang.cap_nhat_node(ma_so, du_lieu_cu)
                # Đồng bộ SQLite.
                from .loi_thuat_toan.ket_noi_sqlite import cap_nhat_san_pham
                cap_nhat_san_pham(sp)
            thong_bao = f'Đã hoàn tác: khôi phục thông tin "{cu["ten_san_pham"]}".'

        # Trường hợp 4: loại không hợp lệ (phòng khi dữ liệu bị hỏng).
        else:
            thong_bao = 'Thao tác không xác định.'

        # Trả JSON báo thành công + thông điệp mô tả.
        return JsonResponse({
            'trang_thai': 'thanh_cong',
            'thong_bao':  thong_bao
        })

    except Exception as loi:
        return JsonResponse(
            {'trang_thai': 'loi', 'thong_bao': f'Lỗi khi hoàn tác: {str(loi)}'},
            status=500
        )


# ============================================================
# REDO (LÀM LẠI) — Đảo ngược của Undo
# ============================================================

@csrf_exempt
@require_http_methods(['POST'])
def lam_lai(request):
    """
    API POST /lam-lai - làm lại thao tác đã hoàn tác (Redo).

    Nguyên lý: Lấy thao tác từ đỉnh stack Redo → đẩy ngược về Undo
    → thực hiện LẠI thao tác đó (them lại, xóa lại, sửa lại...).
    """
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()
    try:
        # Lấy thao tác trên đỉnh stack Redo (Pop).
        thao_tac = Bo_undoredo['redo'].lay_ra()
        # Nếu Redo rỗng → không có gì để làm lại → 400.
        if thao_tac is None:
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': 'Không có thao tác nào để làm lại.'},
                status=400
            )

        # Đẩy thao tác vừa lấy ngược về stack Undo (để undo tiếp được).
        Bo_undoredo['undo'].day_vao(thao_tac)

        # Lấy loại thao tác để biết phải thực hiện lại thế nào.
        loai = thao_tac['loai']
        # Trường hợp 1: Redo THÊM → thêm lại sản phẩm (đã bị undo xóa đi).
        if loai == 'them':
            from .loi_thuat_toan.lop_doi_tuong import Sach, TapChi, BaoGiay, LuanVan, BanThao
            # Lấy dữ liệu mới (sản phẩm đã thêm ban đầu).
            moi = thao_tac['du_lieu_moi']
            loai_hang = moi['loai_hang']
            # Tái tạo đối tượng đúng loại.
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
            # Nếu tạo được → thêm vào DSLK + SQLite.
            if sp:
                Danh_sach_cua_hang.them_vao_cuoi(sp)
                from .loi_thuat_toan.ket_noi_sqlite import luu_mot_san_pham
                luu_mot_san_pham(sp)
            thong_bao = f'Đã làm lại: thêm "{moi["ten_san_pham"]}".'

        # Trường hợp 2: Redo XÓA → xóa lại sản phẩm (đã bị undo thêm lại).
        elif loai == 'xoa':
            # Lấy mã sản phẩm từ dữ liệu cũ (đã bị xóa ban đầu).
            ma_so = thao_tac['du_lieu_cu']['ma_so']
            # Xóa khỏi DSLK.
            Danh_sach_cua_hang.xoa_node(ma_so)
            # Xóa khỏi SQLite.
            from .loi_thuat_toan.ket_noi_sqlite import xoa_mot_san_pham
            xoa_mot_san_pham(ma_so)
            thong_bao = f'Đã làm lại: xóa "{thao_tac["du_lieu_cu"]["ten_san_pham"]}".'

        # Trường hợp 3: Redo SỬA → áp dụng lại dữ liệu MỚI (đã bị undo về cũ).
        elif loai == 'sua':
            moi = thao_tac['du_lieu_moi']
            ma_so = moi['ma_so']
            # Dict chứa trường mới cần áp dụng lại.
            du_lieu_moi = {
                'ten_san_pham': moi['ten_san_pham'],
                'gia_co_ban':   moi['gia_co_ban'],
                'ton_kho':      moi['ton_kho']
            }
            # Áp dụng các trường riêng nếu có.
            if 'tac_gia' in moi:            du_lieu_moi['tac_gia'] = moi['tac_gia']
            if 'nha_xuat_ban' in moi:       du_lieu_moi['nha_xuat_ban'] = moi['nha_xuat_ban']
            if 'so_phat_hanh' in moi:       du_lieu_moi['so_phat_hanh'] = moi['so_phat_hanh']
            if 'ngay_xuat_ban' in moi:      du_lieu_moi['ngay_xuat_ban'] = moi['ngay_xuat_ban']
            if 'truong_dai_hoc' in moi:     du_lieu_moi['truong_dai_hoc'] = moi['truong_dai_hoc']
            if 'tinh_trang' in moi:         du_lieu_moi['tinh_trang'] = moi['tinh_trang']

            # Tìm sản phẩm trong DSLK.
            sp = Danh_sach_cua_hang.tim_theo_ma_so(ma_so)
            if sp:
                # Áp dụng dữ liệu mới lên node.
                Danh_sach_cua_hang.cap_nhat_node(ma_so, du_lieu_moi)
                # Đồng bộ SQLite.
                from .loi_thuat_toan.ket_noi_sqlite import cap_nhat_san_pham
                cap_nhat_san_pham(sp)
            thong_bao = f'Đã làm lại: cập nhật "{moi["ten_san_pham"]}".'

        # Trường hợp 4: loại không hợp lệ.
        else:
            thong_bao = 'Thao tác không xác định.'

        # Trả JSON thành công + thông điệp.
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
    """
    API POST /them-gio-hang - thêm sản phẩm vào giỏ (Enqueue).

    Frontend gửi mã sản phẩm → backend tìm sản phẩm trong DSLK →
    đóng gói thành dict → enqueue vào Queue (thêm vào cuối hàng).
    """
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()
    try:
        # Parse JSON body.
        du_lieu = json.loads(request.body)
        # Lấy mã sản phẩm cần thêm vào giỏ.
        ma_so   = du_lieu.get('ma_so', '').strip()
        # Validate: mã không rỗng.
        if not ma_so:
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': 'Mã số không được để trống.'},
                status=400
            )

        # Tìm sản phẩm trong DSLK để lấy thông tin.
        san_pham = Danh_sach_cua_hang.tim_theo_ma_so(ma_so)
        if san_pham is None:
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': f'Không tìm thấy sản phẩm mã {ma_so}.'},
                status=404
            )

        # Đóng gói thông tin sản phẩm thành dict để enqueue.
        mon_hang = {
            'ma_so':        san_pham.ma_so,                # Mã sản phẩm.
            'ten_san_pham': san_pham.ten_san_pham,         # Tên.
            'gia_ban':      san_pham.tinh_gia_ban(),       # Giá bán (đã tính thuế/sale theo loại).
            'loai_hang':    san_pham.loai_hang             # Loại (Sách/Tạp chí/...).
        }
        # them_vao(): Enqueue — thêm dict vào CUỐI hàng đợi (FIFO).
        Gio_hang_hien_tai.them_vao(mon_hang)

        # Trả JSON thành công + số món hiện có trong giỏ.
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
    """
    API GET /xem-gio-hang - xem toàn bộ giỏ hàng (peek all, không xóa).

    Frontend gọi để hiển thị bảng giỏ hàng cho user xem trước khi thanh toán.
    """
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()
    try:
        # xem_danh_sach(): duyệt Queue từ đầu → cuối, trả list dict.
        danh_sach = Gio_hang_hien_tai.xem_danh_sach()
        # Tính tổng tiền = tổng giá_ban của tất cả món.
        tong_tien = sum(mon.get('gia_ban', 0) for mon in danh_sach)
        # Trả JSON: số lượng + tổng tiền + danh sách.
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
    """
    API POST /xoa-gio-hang - xóa 1 mặt hàng khỏi giỏ (theo mã số).

    Lưu ý: Queue là FIFO, nhưng vẫn cho phép xóa 1 phần tử giữa hàng
    (vì user có thể đổi ý bỏ 1 món khỏi giỏ trước khi thanh toán).
    """
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()
    try:
        # Parse JSON body.
        du_lieu = json.loads(request.body)
        # Lấy mã sản phẩm cần xóa khỏi giỏ.
        ma_so   = du_lieu.get('ma_so', '').strip()
        # Validate.
        if not ma_so:
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': 'Mã số không được để trống.'},
                status=400
            )

        # xoa_theo_ma(): duyệt Queue tìm node có ma_so khớp → bỏ qua node đó.
        ket_qua = Gio_hang_hien_tai.xoa_theo_ma(ma_so)
        if ket_qua:
            return JsonResponse({
                'trang_thai': 'thanh_cong',
                'thong_bao':  f'Đã xóa "{ma_so}" khỏi giỏ hàng.'
            })
        else:
            # Không tìm thấy mã trong giỏ → 404.
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
    """
    API POST /thanh-toan - thanh toán toàn bộ giỏ hàng (Dequeue all).

    Nguyên lý FIFO: lần lượt lấy món từ ĐẦU Queue ra (theo thứ tự thêm vào),
    gom thành hóa đơn + tính tổng tiền, sau đó Queue rỗng.
    """
    if Danh_sach_cua_hang is None:
        khoi_tao_danh_sach()
    try:
        # Nếu giỏ rỗng → không có gì để thanh toán → 400.
        if Gio_hang_hien_tai.rong():
            return JsonResponse(
                {'trang_thai': 'loi', 'thong_bao': 'Giỏ hàng đang trống.'},
                status=400
            )

        # Danh sách chứa các món lấy ra để đưa vào hóa đơn.
        cac_mon = []
        # Biến cộng dồn tổng tiền.
        tong_tien = 0
        # Lặp cho đến khi Queue rỗng: mỗi vòng lấy 1 món từ đầu Queue.
        while not Gio_hang_hien_tai.rong():
            # lay_ra(): Dequeue — lấy + xóa phần tử đầu Queue.
            mon = Gio_hang_hien_tai.lay_ra()
            # Thêm món vào danh sách hóa đơn.
            cac_mon.append(mon)
            # Cộng giá_ban vào tổng tiền.
            tong_tien += mon.get('gia_ban', 0)

        # Trả JSON: thông báo + hóa đơn chi tiết.
        return JsonResponse({
            'trang_thai': 'thanh_cong',
            'thong_bao':  f'Đã thanh toán {len(cac_mon)} mặt hàng, tổng {tong_tien:,.0f}đ.',
            'hoa_don': {
                'cac_mon':  cac_mon,      # Danh sách các món đã mua.
                'tong_tien': tong_tien,   # Tổng tiền thanh toán.
                'so_mon':   len(cac_mon)  # Số món.
            }
        })
    except Exception as loi:
        return JsonResponse(
            {'trang_thai': 'loi', 'thong_bao': f'Lỗi khi thanh toán: {str(loi)}'},
            status=500
        )
