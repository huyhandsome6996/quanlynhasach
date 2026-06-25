/**
 * Tệp tuong_tac.js - Đoạn mã JavaScript xử lý tương tác người dùng.
 * Chứa các hàm bắt sự kiện nhấn nút, vẽ bảng, hiển thị thông báo, validate form.
 *
 * Chức năng:
 *   - Hiển thị danh sách sản phẩm (bảng)
 *   - Tìm kiếm nâng cao (theo tên, mã số, loại hàng)
 *   - Sắp xếp (Merge Sort trên DoublyLinkedList)
 *   - Thêm / Sửa / Xóa sản phẩm (CRUD)
 *   - Thống kê tổng quan
 *   - Giỏ hàng (Queue - FIFO)
 *   - Undo/Redo (Stack - LIFO)
 */


// ========== Biến toàn cục - lưu thông tin người dùng hiện tại ==========
var nguoi_dung_hien_tai = null;


// ========== Khởi tạo khi trang web tải xong ==========
document.addEventListener('DOMContentLoaded', async function () {
    // Tải thông tin người dùng trước (để biết quyền → ẩn/hiện nút Xóa)
    await tai_thong_tin_nguoi_dung();

    // Tải danh sách sản phẩm khi mở trang
    tai_va_hien_thi_danh_sach();

    // Gắn sự kiện cho các nút
    document.getElementById('nut_tim_kiem').addEventListener('click', xu_ly_tim_kiem);
    document.getElementById('nut_sap_xep').addEventListener('click', xu_ly_sap_xep);
    document.getElementById('nut_lam_moi').addEventListener('click', tai_va_hien_thi_danh_sach);
    document.getElementById('nut_mo_form').addEventListener('click', mo_form_them);
    document.getElementById('nut_dong_form').addEventListener('click', dong_form);
    document.getElementById('nut_huy').addEventListener('click', dong_form);
    document.getElementById('bieu_mau_them').addEventListener('submit', xu_ly_submit_form);
    document.getElementById('nut_thong_ke').addEventListener('click', xu_ly_thong_ke);
    document.getElementById('nut_gio_hang').addEventListener('click', xu_ly_gio_hang);
    document.getElementById('nut_hoan_tac').addEventListener('click', xu_ly_hoan_tac);
    document.getElementById('nut_lam_lai').addEventListener('click', xu_ly_lam_lai);

    // Gắn sự kiện Enter cho ô tìm kiếm
    document.getElementById('o_tim_kiem').addEventListener('keypress', function (e) {
        if (e.key === 'Enter') xu_ly_tim_kiem();
    });

    // Gắn sự kiện thay đổi loại hàng để hiện/ẩn các trường riêng
    document.getElementById('chon_loai_hang').addEventListener('change', xu_ly_doi_loai_hang);
});


// ========== Tải thông tin người dùng hiện tại ==========
async function tai_thong_tin_nguoi_dung() {
    try {
        var phan_hoi = await fetch('/api/nguoi-dung');
        var du_lieu = await phan_hoi.json();

        if (du_lieu.trang_thai === 'thanh_cong' && du_lieu.nguoi_dung) {
            nguoi_dung_hien_tai = du_lieu.nguoi_dung;
            // Cập nhật hiển thị
            document.getElementById('ten_nguoi_dung').textContent =
                '👤 ' + (nguoi_dung_hien_tai.ho_ten || nguoi_dung_hien_tai.ten_dang_nhap);

            var nhan = document.getElementById('nhan_vai_tro');
            if (nguoi_dung_hien_tai.la_admin) {
                nhan.textContent = '👑 Admin';
                nhan.className = 'nhan_vai_tro admin';
            } else {
                nhan.textContent = '👤 Nhân viên';
                nhan.className = 'nhan_vai_tro nhan_vien';
            }

            // Nếu là nhân viên → ẩn nút "Thêm sản phẩm" để chặn thao tác (tùy chọn)
            // Theo yêu cầu barem: NHÂN VIÊN KHÔNG ĐƯỢC XÓA → nút Xóa trong bảng sẽ bị ẩn (xem ve_bang)
        } else {
            // Chưa đăng nhập → chuyển về trang đăng nhập
            window.location.href = '/dang-nhap';
        }
    } catch (loi) {
        console.error('Lỗi khi tải thông tin người dùng:', loi);
        window.location.href = '/dang-nhap';
    }
}


// ========== Hiển thị thông báo ==========
/**
 * Hiển thị thông báo trên đầu trang.
 *
 * Tham số:
 *   noi_dung (string): Nội dung thông báo.
 *   loai (string):     Loại thông báo ('thanh_cong', 'loi', 'thong_tin').
 */
function hien_thong_bao(noi_dung, loai) {
    var thong_bao = document.getElementById('thong_bao');
    thong_bao.textContent = noi_dung;
    thong_bao.className = 'thong_bao ' + loai;
    setTimeout(function () {
        thong_bao.classList.add('an_di');
    }, 4000);
}


// ========== Định dạng tiền tệ ==========
/**
 * Định dạng số thành chuỗi tiền tệ Việt Nam.
 *
 * Tham số:
 *   so (number): Số cần định dạng.
 *
 * Trả về:
 *   string: Chuỗi đã định dạng (Ví dụ: 100.000đ).
 */
function dinh_dang_tien(so) {
    return Number(so).toLocaleString('vi-VN') + 'đ';
}


// ========== Vẽ bảng dữ liệu ==========
/**
 * Vẽ (render) các hàng <tr> vào bảng dữ liệu từ danh sách sản phẩm.
 *
 * Tham số:
 *   danh_sach (array): Mảng các đối tượng sản phẩm (dict).
 */
function ve_bang(danh_sach) {
    var than_bang = document.getElementById('than_bang');
    than_bang.innerHTML = '';

    if (!danh_sach || danh_sach.length === 0) {
        than_bang.innerHTML = '<tr><td colspan="8" class="dang_tai">Không có dữ liệu</td></tr>';
        return;
    }

    danh_sach.forEach(function (san_pham) {
        var hang = document.createElement('tr');

        // Mã số
        var o_ma = document.createElement('td');
        o_ma.textContent = san_pham.ma_so;
        o_ma.style.fontWeight = '600';
        hang.appendChild(o_ma);

        // Loại hàng (có nhãn màu)
        var o_loai = document.createElement('td');
        var nhan = document.createElement('span');
        nhan.textContent = san_pham.loai_hang;
        nhan.className = 'nhan_loai';
        if (san_pham.loai_hang === 'Sách') nhan.classList.add('nhan_sach');
        else if (san_pham.loai_hang === 'Tạp chí') nhan.classList.add('nhan_tap_chi');
        else if (san_pham.loai_hang === 'Báo giấy') nhan.classList.add('nhan_bao_giay');
        else if (san_pham.loai_hang === 'Luận văn') nhan.classList.add('nhan_luan_van');
        else if (san_pham.loai_hang === 'Bản thảo') nhan.classList.add('nhan_ban_thao');
        o_loai.appendChild(nhan);
        hang.appendChild(o_loai);

        // Tên sản phẩm
        var o_ten = document.createElement('td');
        o_ten.textContent = san_pham.ten_san_pham;
        hang.appendChild(o_ten);

        // Giá cơ bản
        var o_gia_co_ban = document.createElement('td');
        o_gia_co_ban.textContent = dinh_dang_tien(san_pham.gia_co_ban);
        hang.appendChild(o_gia_co_ban);

        // Giá bán
        var o_gia_ban = document.createElement('td');
        o_gia_ban.textContent = dinh_dang_tien(san_pham.gia_ban);
        o_gia_ban.style.fontWeight = '700';
        o_gia_ban.style.color = '#1a237e';
        hang.appendChild(o_gia_ban);

        // Tồn kho
        var o_ton_kho = document.createElement('td');
        o_ton_kho.textContent = san_pham.ton_kho;
        if (san_pham.ton_kho <= 10) {
            o_ton_kho.style.color = '#e53935';
            o_ton_kho.style.fontWeight = '700';
        }
        hang.appendChild(o_ton_kho);

        // Chi tiết (thuộc tính riêng theo loại hàng)
        var o_chi_tiet = document.createElement('td');
        o_chi_tiet.style.fontSize = '12px';
        o_chi_tiet.style.color = '#666';
        if (san_pham.loai_hang === 'Sách') {
            o_chi_tiet.textContent = 'TG: ' + (san_pham.tac_gia || '') + ' | NXB: ' + (san_pham.nha_xuat_ban || '');
        } else if (san_pham.loai_hang === 'Tạp chí') {
            o_chi_tiet.textContent = 'Số PH: ' + (san_pham.so_phat_hanh || '');
        } else if (san_pham.loai_hang === 'Báo giấy') {
            o_chi_tiet.textContent = 'Ngày XB: ' + (san_pham.ngay_xuat_ban || '');
        } else if (san_pham.loai_hang === 'Luận văn') {
            o_chi_tiet.textContent = 'TG: ' + (san_pham.tac_gia || '') + ' | Trường: ' + (san_pham.truong_dai_hoc || '');
        } else if (san_pham.loai_hang === 'Bản thảo') {
            o_chi_tiet.textContent = 'TG: ' + (san_pham.tac_gia || '') + ' | TT: ' + (san_pham.trang_thai || '');
        }
        hang.appendChild(o_chi_tiet);

        // Nút thao tác
        var o_thao_tac = document.createElement('td');
        o_thao_tac.className = 'nhom_thao_tac';

        // Nút thêm vào giỏ hàng
        var nut_gio = document.createElement('button');
        nut_gio.textContent = '🛒';
        nut_gio.className = 'nut nut_gio_nho';
        nut_gio.title = 'Thêm vào giỏ hàng';
        nut_gio.addEventListener('click', function () {
            xu_ly_them_gio_hang(san_pham.ma_so);
        });
        o_thao_tac.appendChild(nut_gio);

        // Nút sửa (cả admin và nhân viên đều được sửa)
        var nut_sua = document.createElement('button');
        nut_sua.textContent = 'Sửa';
        nut_sua.className = 'nut nut_sua';
        nut_sua.addEventListener('click', function () {
            mo_form_sua(san_pham);
        });
        o_thao_tac.appendChild(nut_sua);

        // Nút xóa - CHỈ ADMIN mới được xóa, nhân viên thì ẩn nút
        if (nguoi_dung_hien_tai && nguoi_dung_hien_tai.la_admin) {
            var nut_xoa = document.createElement('button');
            nut_xoa.textContent = 'Xóa';
            nut_xoa.className = 'nut nut_xoa';
            nut_xoa.addEventListener('click', function () {
                xu_ly_xoa(san_pham.ma_so, san_pham.ten_san_pham);
            });
            o_thao_tac.appendChild(nut_xoa);
        } else {
            // Nhân viên: hiện nhãn "Không thể xóa" thay vì nút Xóa
            var nhan_chan = document.createElement('span');
            nhan_chan.textContent = '🔒';
            nhan_chan.className = 'nhan_bi_khoa';
            nhan_chan.title = 'Nhân viên không được phép xóa sản phẩm';
            o_thao_tac.appendChild(nhan_chan);
        }

        hang.appendChild(o_thao_tac);
        than_bang.appendChild(hang);
    });
}


// ========== Tải và hiển thị danh sách ==========
async function tai_va_hien_thi_danh_sach() {
    var du_lieu = await lay_danh_sach();
    if (du_lieu && du_lieu.trang_thai === 'thanh_cong') {
        ve_bang(du_lieu.danh_sach);
        hien_thong_bao('Đã tải ' + du_lieu.so_luong + ' mặt hàng.', 'thong_tin');
    }
}


// ========== Xử lý tìm kiếm nâng cao ==========
async function xu_ly_tim_kiem() {
    var tu_khoa = document.getElementById('o_tim_kiem').value.trim();
    var tieu_chi = document.getElementById('chon_tieu_chi_tim').value;

    if (!tu_khoa) {
        tai_va_hien_thi_danh_sach();
        return;
    }

    var du_lieu = await tim_kiem(tu_khoa, tieu_chi);
    if (du_lieu && du_lieu.trang_thai === 'thanh_cong') {
        ve_bang(du_lieu.danh_sach);
        var ten_tieu_chi = { 'ten': 'tên', 'ma': 'mã số', 'loai': 'loại hàng' };
        hien_thong_bao('Tìm thấy ' + du_lieu.so_luong + ' kết quả theo ' + (ten_tieu_chi[tieu_chi] || tieu_chi) + '.', 'thong_tin');
    }
}


// ========== Xử lý sắp xếp ==========
async function xu_ly_sap_xep() {
    var tieu_chi = document.getElementById('chon_sap_xep').value;
    var du_lieu = await sap_xep(tieu_chi);
    if (du_lieu && du_lieu.trang_thai === 'thanh_cong') {
        ve_bang(du_lieu.danh_sach);
        hien_thong_bao('Đã sắp xếp theo ' + tieu_chi + '.', 'thanh_cong');
    }
}


// ========== Xử lý xóa sản phẩm ==========
async function xu_ly_xoa(ma_so, ten) {
    if (!confirm('Bạn có chắc muốn xóa "' + ten + '" (Mã: ' + ma_so + ')?')) return;

    var ket_qua = await xoa_san_pham(ma_so);
    if (ket_qua) {
        if (ket_qua.du_lieu.trang_thai === 'thanh_cong') {
            hien_thong_bao(ket_qua.du_lieu.thong_bao, 'thanh_cong');
            tai_va_hien_thi_danh_sach();
        } else {
            hien_thong_bao(ket_qua.du_lieu.thong_bao, 'loi');
        }
    }
}


// ========== Quản lý Form thêm/sửa sản phẩm ==========
function mo_form_them() {
    // Reset form về chế độ thêm
    document.getElementById('che_do_form').value = 'them';
    document.getElementById('ma_so_dang_sua').value = '';
    document.getElementById('tieu_de_form').textContent = 'Thêm sản phẩm mới';
    document.getElementById('nut_xac_nhan_form').textContent = 'Thêm sản phẩm';
    document.getElementById('nhom_ma_so').style.display = 'block';
    document.getElementById('chon_loai_hang').disabled = false;
    document.getElementById('bieu_mau_them').reset();
    an_tat_ca_nhom_rieng();
    document.getElementById('form_them').classList.remove('an_di');
}


function mo_form_sua(san_pham) {
    // Chuyển form sang chế độ sửa
    document.getElementById('che_do_form').value = 'sua';
    document.getElementById('ma_so_dang_sua').value = san_pham.ma_so;
    document.getElementById('tieu_de_form').textContent = 'Sửa thông tin sản phẩm';
    document.getElementById('nut_xac_nhan_form').textContent = 'Cập nhật';

    // Ẩn trường mã số và khóa loại hàng (không cho đổi loại khi sửa)
    document.getElementById('nhom_ma_so').style.display = 'none';
    document.getElementById('chon_loai_hang').value = san_pham.loai_hang;
    document.getElementById('chon_loai_hang').disabled = true;

    // Điền dữ liệu hiện tại vào form
    document.getElementById('nhap_ten').value = san_pham.ten_san_pham;
    document.getElementById('nhap_gia').value = san_pham.gia_co_ban;
    document.getElementById('nhap_ton_kho').value = san_pham.ton_kho;

    // Hiện nhóm trường riêng và điền dữ liệu
    an_tat_ca_nhom_rieng();
    xu_ly_doi_loai_hang();

    if (san_pham.loai_hang === 'Sách') {
        document.getElementById('nhap_tac_gia').value = san_pham.tac_gia || '';
        document.getElementById('nhap_nha_xuat_ban').value = san_pham.nha_xuat_ban || '';
    } else if (san_pham.loai_hang === 'Tạp chí') {
        document.getElementById('nhap_so_phat_hanh').value = san_pham.so_phat_hanh || '';
    } else if (san_pham.loai_hang === 'Báo giấy') {
        document.getElementById('nhap_ngay_xuat_ban').value = san_pham.ngay_xuat_ban || '';
    } else if (san_pham.loai_hang === 'Luận văn') {
        document.getElementById('nhap_tac_gia_lv').value = san_pham.tac_gia || '';
        document.getElementById('nhap_truong_dai_hoc').value = san_pham.truong_dai_hoc || '';
    } else if (san_pham.loai_hang === 'Bản thảo') {
        document.getElementById('nhap_tac_gia_bt').value = san_pham.tac_gia || '';
        document.getElementById('nhap_trang_thai').value = san_pham.trang_thai || 'Chưa duyệt';
    }

    document.getElementById('form_them').classList.remove('an_di');
}


function dong_form() {
    document.getElementById('form_them').classList.add('an_di');
    document.getElementById('bieu_mau_them').reset();
    document.getElementById('nhom_ma_so').style.display = 'block';
    document.getElementById('chon_loai_hang').disabled = false;
    an_tat_ca_nhom_rieng();
}


function an_tat_ca_nhom_rieng() {
    document.getElementById('nhom_sach').classList.add('an_di');
    document.getElementById('nhom_tap_chi').classList.add('an_di');
    document.getElementById('nhom_bao_giay').classList.add('an_di');
    document.getElementById('nhom_luan_van').classList.add('an_di');
    document.getElementById('nhom_ban_thao').classList.add('an_di');
}


function xu_ly_doi_loai_hang() {
    var loai_hang = document.getElementById('chon_loai_hang').value;
    an_tat_ca_nhom_rieng();

    if (loai_hang === 'Sách') {
        document.getElementById('nhom_sach').classList.remove('an_di');
    } else if (loai_hang === 'Tạp chí') {
        document.getElementById('nhom_tap_chi').classList.remove('an_di');
    } else if (loai_hang === 'Báo giấy') {
        document.getElementById('nhom_bao_giay').classList.remove('an_di');
    } else if (loai_hang === 'Luận văn') {
        document.getElementById('nhom_luan_van').classList.remove('an_di');
    } else if (loai_hang === 'Bản thảo') {
        document.getElementById('nhom_ban_thao').classList.remove('an_di');
    }
}


// ========== Xử lý submit form (Thêm hoặc Sửa) ==========
async function xu_ly_submit_form(event) {
    event.preventDefault();

    var che_do = document.getElementById('che_do_form').value;
    var loai_hang = document.getElementById('chon_loai_hang').value;
    var ten_san_pham = document.getElementById('nhap_ten').value.trim();
    var gia_co_ban = parseFloat(document.getElementById('nhap_gia').value);
    var ton_kho = parseInt(document.getElementById('nhap_ton_kho').value);

    // ---- Kiểm tra dữ liệu hợp lệ (Validate) ----
    if (!loai_hang) { hien_thong_bao('Vui lòng chọn loại hàng.', 'loi'); return; }
    if (!ten_san_pham) { hien_thong_bao('Tên sản phẩm không được để trống.', 'loi'); return; }
    if (isNaN(gia_co_ban) || gia_co_ban < 0) { hien_thong_bao('Giá cơ bản phải là số không âm.', 'loi'); return; }
    if (isNaN(ton_kho) || ton_kho < 0) { hien_thong_bao('Tồn kho phải là số không âm.', 'loi'); return; }

    // Tạo đối tượng dữ liệu gửi lên máy chủ
    var du_lieu_gui = {
        loai_hang: loai_hang,
        ten_san_pham: ten_san_pham,
        gia_co_ban: gia_co_ban,
        ton_kho: ton_kho
    };

    // Thêm các thuộc tính riêng theo loại hàng
    if (loai_hang === 'Sách') {
        var tac_gia = document.getElementById('nhap_tac_gia').value.trim();
        var nha_xuat_ban = document.getElementById('nhap_nha_xuat_ban').value.trim();
        if (!tac_gia || !nha_xuat_ban) { hien_thong_bao('Vui lòng nhập đầy đủ tác giả và nhà xuất bản.', 'loi'); return; }
        du_lieu_gui.tac_gia = tac_gia;
        du_lieu_gui.nha_xuat_ban = nha_xuat_ban;
    } else if (loai_hang === 'Tạp chí') {
        var so_phat_hanh = document.getElementById('nhap_so_phat_hanh').value.trim();
        if (!so_phat_hanh) { hien_thong_bao('Vui lòng nhập số phát hành.', 'loi'); return; }
        du_lieu_gui.so_phat_hanh = so_phat_hanh;
    } else if (loai_hang === 'Báo giấy') {
        var ngay_xuat_ban = document.getElementById('nhap_ngay_xuat_ban').value.trim();
        if (!ngay_xuat_ban) { hien_thong_bao('Vui lòng chọn ngày xuất bản.', 'loi'); return; }
        du_lieu_gui.ngay_xuat_ban = ngay_xuat_ban;
    } else if (loai_hang === 'Luận văn') {
        var tac_gia_lv = document.getElementById('nhap_tac_gia_lv').value.trim();
        var truong_dai_hoc = document.getElementById('nhap_truong_dai_hoc').value.trim();
        if (!tac_gia_lv || !truong_dai_hoc) { hien_thong_bao('Vui lòng nhập đầy đủ tác giả và trường đại học.', 'loi'); return; }
        du_lieu_gui.tac_gia = tac_gia_lv;
        du_lieu_gui.truong_dai_hoc = truong_dai_hoc;
    } else if (loai_hang === 'Bản thảo') {
        var tac_gia_bt = document.getElementById('nhap_tac_gia_bt').value.trim();
        var trang_thai = document.getElementById('nhap_trang_thai').value;
        if (!tac_gia_bt) { hien_thong_bao('Vui lòng nhập tác giả.', 'loi'); return; }
        du_lieu_gui.tac_gia = tac_gia_bt;
        du_lieu_gui.trang_thai = trang_thai;
    }

    var ket_qua;

    if (che_do === 'them') {
        // ---- Chế độ THÊM ----
        var ma_so = document.getElementById('nhap_ma_so').value.trim();
        if (!ma_so) { hien_thong_bao('Mã số không được để trống.', 'loi'); return; }
        du_lieu_gui.ma_so = ma_so;
        ket_qua = await them_san_pham(du_lieu_gui);
    } else {
        // ---- Chế độ SỬA ----
        var ma_so_sua = document.getElementById('ma_so_dang_sua').value;
        du_lieu_gui.ma_so = ma_so_sua;
        ket_qua = await sua_san_pham(du_lieu_gui);
    }

    if (ket_qua) {
        if (ket_qua.du_lieu.trang_thai === 'thanh_cong') {
            hien_thong_bao(ket_qua.du_lieu.thong_bao, 'thanh_cong');
            dong_form();
            tai_va_hien_thi_danh_sach();
        } else {
            hien_thong_bao(ket_qua.du_lieu.thong_bao, 'loi');
        }
    }
}


// ========== Xử lý thống kê ==========
async function xu_ly_thong_ke() {
    var du_lieu = await lay_thong_ke();
    if (!du_lieu || du_lieu.trang_thai !== 'thanh_cong') return;

    var tk = du_lieu.thong_ke;
    var html = '';

    // Tổng quan
    html += '<div class="the_thong_ke">';
    html += '<div class="so_lieu"><span class="so">' + tk.tong_so_luong + '</span><span class="nhan_so">Tổng mặt hàng</span></div>';
    html += '<div class="so_lieu"><span class="so">' + (tk.so_mat_hang_sap_het) + '</span><span class="nhan_so" style="color:#e53935">Sắp hết hàng</span></div>';
    html += '<div class="so_lieu"><span class="so">' + dinh_dang_tien(tk.tong_gia_tri_ton_kho) + '</span><span class="nhan_so">Tổng giá trị kho</span></div>';
    html += '</div>';

    // Mặt hàng đắt nhất và rẻ nhất
    if (tk.mat_hang_dat_nhat) {
        html += '<div class="the_chi_tiet">';
        html += '<h4>Đắt nhất: ' + tk.mat_hang_dat_nhat.ten_san_pham + '</h4>';
        html += '<p>Giá bán: ' + dinh_dang_tien(tk.mat_hang_dat_nhat.gia_ban) + '</p>';
        html += '</div>';
    }
    if (tk.mat_hang_re_nhat) {
        html += '<div class="the_chi_tiet">';
        html += '<h4>Rẻ nhất: ' + tk.mat_hang_re_nhat.ten_san_pham + '</h4>';
        html += '<p>Giá bán: ' + dinh_dang_tien(tk.mat_hang_re_nhat.gia_ban) + '</p>';
        html += '</div>';
    }

    // Thống kê theo loại hàng
    if (tk.thong_ke_theo_loai) {
        html += '<div class="the_chi_tiet"><h4>Thống kê theo loại hàng:</h4>';
        for (var loai in tk.thong_ke_theo_loai) {
            var sl = tk.thong_ke_theo_loai[loai];
            html += '<p>' + loai + ': ' + sl.so_luong + ' mặt hàng, tổng tồn kho: ' + sl.tong_ton_kho + '</p>';
        }
        html += '</div>';
    }

    document.getElementById('bang_thong_ke').innerHTML = html;
    document.getElementById('khu_vuc_thong_ke').classList.remove('an_di');
}


// ========== Xử lý giỏ hàng (Queue - FIFO) ==========
async function xu_ly_gio_hang() {
    var du_lieu = await xem_gio_hang();
    if (!du_lieu || du_lieu.trang_thai !== 'thanh_cong') return;

    var html = '';
    if (du_lieu.so_luong === 0) {
        html = '<p style="text-align:center;padding:20px;color:#999;">Giỏ hàng đang trống</p>';
    } else {
        html += '<table class="bang_gio_hang"><thead><tr><th>Mã</th><th>Tên</th><th>Giá bán</th><th>Xóa</th></tr></thead><tbody>';
        du_lieu.gio_hang.forEach(function (sp) {
            html += '<tr>';
            html += '<td>' + sp.ma_so + '</td>';
            html += '<td>' + sp.ten_san_pham + '</td>';
            html += '<td>' + dinh_dang_tien(sp.gia_ban) + '</td>';
            html += '<td><button class="nut nut_xoa" onclick="xu_ly_xoa_gio_hang(\'' + sp.ma_so + '\')">Xóa</button></td>';
            html += '</tr>';
        });
        html += '</tbody></table>';
        html += '<div class="tong_tien_gio">Tổng tiền: <strong>' + dinh_dang_tien(du_lieu.tong_tien) + '</strong></div>';
        html += '<button class="nut nut_chinh" style="width:100%;margin-top:10px" onclick="xu_ly_thanh_toan()">Thanh toán toàn bộ</button>';
    }

    document.getElementById('noi_dung_gio_hang').innerHTML = html;
    document.getElementById('hop_gio_hang').classList.remove('an_di');
    cap_nhat_dem_gio(du_lieu.so_luong);
}


async function xu_ly_them_gio_hang(ma_so) {
    var ket_qua = await them_vao_gio_hang(ma_so);
    if (ket_qua) {
        if (ket_qua.du_lieu.trang_thai === 'thanh_cong') {
            hien_thong_bao(ket_qua.du_lieu.thong_bao, 'thanh_cong');
            // Cập nhật số lượng giỏ hàng
            var du_lieu_gio = await xem_gio_hang();
            if (du_lieu_gio) cap_nhat_dem_gio(du_lieu_gio.so_luong);
        } else {
            hien_thong_bao(ket_qua.du_lieu.thong_bao, 'loi');
        }
    }
}


async function xu_ly_xoa_gio_hang(ma_so) {
    await xoa_khoi_gio_hang(ma_so);
    xu_ly_gio_hang(); // Tải lại giỏ hàng
}


async function xu_ly_thanh_toan() {
    if (!confirm('Bạn có chắc muốn thanh toán toàn bộ giỏ hàng?')) return;

    var ket_qua = await thanh_toan_gio_hang();
    if (ket_qua && ket_qua.du_lieu.trang_thai === 'thanh_cong') {
        hien_thong_bao(ket_qua.du_lieu.thong_bao, 'thanh_cong');
        document.getElementById('hop_gio_hang').classList.add('an_di');
        cap_nhat_dem_gio(0);
        tai_va_hien_thi_danh_sach();
    } else if (ket_qua) {
        hien_thong_bao(ket_qua.du_lieu.thong_bao, 'loi');
    }
}


function cap_nhat_dem_gio(so_luong) {
    document.getElementById('so_gio_hang').textContent = so_luong;
}


// ========== Xử lý Undo/Redo (Stack - LIFO) ==========
async function xu_ly_hoan_tac() {
    var ket_qua = await hoan_tac();
    if (ket_qua) {
        if (ket_qua.du_lieu.trang_thai === 'thanh_cong') {
            hien_thong_bao(ket_qua.du_lieu.thong_bao, 'thanh_cong');
            tai_va_hien_thi_danh_sach();
        } else {
            hien_thong_bao(ket_qua.du_lieu.thong_bao, 'loi');
        }
    }
}


async function xu_ly_lam_lai() {
    var ket_qua = await lam_lai();
    if (ket_qua) {
        if (ket_qua.du_lieu.trang_thai === 'thanh_cong') {
            hien_thong_bao(ket_qua.du_lieu.thong_bao, 'thanh_cong');
            tai_va_hien_thi_danh_sach();
        } else {
            hien_thong_bao(ket_qua.du_lieu.thong_bao, 'loi');
        }
    }
}
