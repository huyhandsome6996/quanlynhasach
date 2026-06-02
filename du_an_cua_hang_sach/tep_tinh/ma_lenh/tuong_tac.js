/**
 * Tệp tuong_tac.js - Đoạn mã JavaScript xử lý tương tác người dùng.
 * Chứa các hàm bắt sự kiện nhấn nút, vẽ bảng, hiển thị thông báo, validate form.
 */


// ========== Khởi tạo khi trang web tải xong ==========
document.addEventListener('DOMContentLoaded', function () {
    // Tải danh sách sản phẩm khi mở trang
    tai_va_hien_thi_danh_sach();

    // Gắn sự kiện cho các nút
    document.getElementById('nut_tim_kiem').addEventListener('click', xu_ly_tim_kiem);
    document.getElementById('nut_sap_xep').addEventListener('click', xu_ly_sap_xep);
    document.getElementById('nut_lam_moi').addEventListener('click', tai_va_hien_thi_danh_sach);
    document.getElementById('nut_mo_form').addEventListener('click', mo_form_them);
    document.getElementById('nut_dong_form').addEventListener('click', dong_form_them);
    document.getElementById('nut_huy').addEventListener('click', dong_form_them);
    document.getElementById('bieu_mau_them').addEventListener('submit', xu_ly_them_san_pham);

    // Gắn sự kiện Enter cho ô tìm kiếm
    document.getElementById('o_tim_kiem').addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            xu_ly_tim_kiem();
        }
    });

    // Gắn sự kiện thay đổi loại hàng để hiện/ẩn các trường riêng
    document.getElementById('chon_loai_hang').addEventListener('change', xu_ly_doi_loai_hang);
});


// ========== Hiển thị thông báo ==========
/**
 * Hiển thị thông báo trên đầu trang.
 *
 * Tham số:
 *   noi_dung (string): Nội dung thông báo.
 *   loai (string): Loại thông báo ('thanh_cong', 'loi', 'thong_tin').
 */
function hien_thong_bao(noi_dung, loai) {
    const thong_bao = document.getElementById('thong_bao');
    thong_bao.textContent = noi_dung;
    thong_bao.className = 'thong_bao ' + loai;

    // Tự động ẩn sau 4 giây
    setTimeout(function () {
        thong_bao.classList.add('an_di');
    }, 4000);
}


// ========== Vẽ bảng dữ liệu ==========
/**
 * Vẽ (render) các hàng <tr> vào bảng dữ liệu từ danh sách sản phẩm.
 *
 * Tham số:
 *   danh_sach (array): Mảng các đối tượng sản phẩm (dict).
 */
function ve_bang(danh_sach) {
    const than_bang = document.getElementById('than_bang');
    than_bang.innerHTML = '';

    if (!danh_sach || danh_sach.length === 0) {
        than_bang.innerHTML = '<tr><td colspan="8" class="dang_tai">Không có dữ liệu</td></tr>';
        return;
    }

    danh_sach.forEach(function (san_pham) {
        const hang = document.createElement('tr');

        // Mã số
        const o_ma = document.createElement('td');
        o_ma.textContent = san_pham.ma_so;
        o_ma.style.fontWeight = '600';
        hang.appendChild(o_ma);

        // Loại hàng (có nhãn màu)
        const o_loai = document.createElement('td');
        const nhan = document.createElement('span');
        nhan.textContent = san_pham.loai_hang;
        nhan.className = 'nhan_loai';
        if (san_pham.loai_hang === 'Sách') nhan.classList.add('nhan_sach');
        else if (san_pham.loai_hang === 'Tạp chí') nhan.classList.add('nhan_tap_chi');
        else if (san_pham.loai_hang === 'Báo giấy') nhan.classList.add('nhan_bao_giay');
        o_loai.appendChild(nhan);
        hang.appendChild(o_loai);

        // Tên sản phẩm
        const o_ten = document.createElement('td');
        o_ten.textContent = san_pham.ten_san_pham;
        hang.appendChild(o_ten);

        // Giá cơ bản
        const o_gia_co_ban = document.createElement('td');
        o_gia_co_ban.textContent = dinh_dang_tien(san_pham.gia_co_ban);
        hang.appendChild(o_gia_co_ban);

        // Giá bán
        const o_gia_ban = document.createElement('td');
        o_gia_ban.textContent = dinh_dang_tien(san_pham.gia_ban);
        o_gia_ban.style.fontWeight = '700';
        o_gia_ban.style.color = '#1a237e';
        hang.appendChild(o_gia_ban);

        // Tồn kho
        const o_ton_kho = document.createElement('td');
        o_ton_kho.textContent = san_pham.ton_kho;
        if (san_pham.ton_kho <= 10) {
            o_ton_kho.style.color = '#e53935';
            o_ton_kho.style.fontWeight = '700';
        }
        hang.appendChild(o_ton_kho);

        // Chi tiết (thuộc tính riêng theo loại hàng)
        const o_chi_tiet = document.createElement('td');
        o_chi_tiet.style.fontSize = '12px';
        o_chi_tiet.style.color = '#666';
        if (san_pham.loai_hang === 'Sách') {
            o_chi_tiet.textContent = 'TG: ' + (san_pham.tac_gia || '') + ' | NXB: ' + (san_pham.nha_xuat_ban || '');
        } else if (san_pham.loai_hang === 'Tạp chí') {
            o_chi_tiet.textContent = 'Số PH: ' + (san_pham.so_phat_hanh || '');
        } else if (san_pham.loai_hang === 'Báo giấy') {
            o_chi_tiet.textContent = 'Ngày XB: ' + (san_pham.ngay_xuat_ban || '');
        }
        hang.appendChild(o_chi_tiet);

        // Nút xóa
        const o_thao_tac = document.createElement('td');
        const nut_xoa = document.createElement('button');
        nut_xoa.textContent = 'Xóa';
        nut_xoa.className = 'nut nut_xoa';
        nut_xoa.addEventListener('click', function () {
            xu_ly_xoa(san_pham.ma_so, san_pham.ten_san_pham);
        });
        o_thao_tac.appendChild(nut_xoa);
        hang.appendChild(o_thao_tac);

        than_bang.appendChild(hang);
    });
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
    return so.toLocaleString('vi-VN') + 'đ';
}


// ========== Tải và hiển thị danh sách ==========
/**
 * Tải danh sách sản phẩm từ máy chủ và hiển thị lên bảng.
 */
async function tai_va_hien_thi_danh_sach() {
    const du_lieu = await lay_danh_sach();
    if (du_lieu && du_lieu.trang_thai === 'thanh_cong') {
        ve_bang(du_lieu.danh_sach);
        hien_thong_bao('Đã tải ' + du_lieu.so_luong + ' mặt hàng.', 'thong_tin');
    }
}


// ========== Xử lý tìm kiếm ==========
/**
 * Xử lý sự kiện nhấn nút Tìm kiếm.
 */
async function xu_ly_tim_kiem() {
    const tu_khoa = document.getElementById('o_tim_kiem').value.trim();
    if (!tu_khoa) {
        tai_va_hien_thi_danh_sach();
        return;
    }

    const du_lieu = await tim_kiem(tu_khoa);
    if (du_lieu && du_lieu.trang_thai === 'thanh_cong') {
        ve_bang(du_lieu.danh_sach);
        hien_thong_bao('Tìm thấy ' + du_lieu.so_luong + ' kết quả cho "' + tu_khoa + '".', 'thong_tin');
    }
}


// ========== Xử lý sắp xếp ==========
/**
 * Xử lý sự kiện nhấn nút Sắp xếp.
 */
async function xu_ly_sap_xep() {
    const tieu_chi = document.getElementById('chon_sap_xep').value;
    const du_lieu = await sap_xep(tieu_chi);
    if (du_lieu && du_lieu.trang_thai === 'thanh_cong') {
        ve_bang(du_lieu.danh_sach);
        hien_thong_bao('Đã sắp xếp theo ' + tieu_chi + '.', 'thanh_cong');
    }
}


// ========== Xử lý xóa sản phẩm ==========
/**
 * Xử lý sự kiện nhấn nút Xóa sản phẩm.
 *
 * Tham số:
 *   ma_so (string): Mã số sản phẩm cần xóa.
 *   ten (string): Tên sản phẩm (để xác nhận).
 */
async function xu_ly_xoa(ma_so, ten) {
    if (!confirm('Bạn có chắc muốn xóa "' + ten + '" (Mã: ' + ma_so + ')?')) {
        return;
    }

    const ket_qua = await xoa_san_pham(ma_so);
    if (ket_qua) {
        if (ket_qua.du_lieu.trang_thai === 'thanh_cong') {
            hien_thong_bao(ket_qua.du_lieu.thong_bao, 'thanh_cong');
            tai_va_hien_thi_danh_sach();
        } else {
            hien_thong_bao(ket_qua.du_lieu.thong_bao, 'loi');
        }
    }
}


// ========== Quản lý Form thêm sản phẩm ==========
/**
 * Mở hộp thoại thêm sản phẩm.
 */
function mo_form_them() {
    document.getElementById('form_them').classList.remove('an_di');
}

/**
 * Đóng hộp thoại thêm sản phẩm và xóa dữ liệu form.
 */
function dong_form_them() {
    document.getElementById('form_them').classList.add('an_di');
    document.getElementById('bieu_mau_them').reset();
    // Ẩn tất cả các nhóm trường riêng
    document.getElementById('nhom_sach').classList.add('an_di');
    document.getElementById('nhom_tap_chi').classList.add('an_di');
    document.getElementById('nhom_bao_giay').classList.add('an_di');
}

/**
 * Xử lý sự kiện thay đổi loại hàng - Hiện/ẩn các trường nhập liệu riêng.
 */
function xu_ly_doi_loai_hang() {
    const loai_hang = document.getElementById('chon_loai_hang').value;

    // Ẩn tất cả nhóm trường riêng
    document.getElementById('nhom_sach').classList.add('an_di');
    document.getElementById('nhom_tap_chi').classList.add('an_di');
    document.getElementById('nhom_bao_giay').classList.add('an_di');

    // Hiện nhóm trường riêng tương ứng
    if (loai_hang === 'Sách') {
        document.getElementById('nhom_sach').classList.remove('an_di');
    } else if (loai_hang === 'Tạp chí') {
        document.getElementById('nhom_tap_chi').classList.remove('an_di');
    } else if (loai_hang === 'Báo giấy') {
        document.getElementById('nhom_bao_giay').classList.remove('an_di');
    }
}


// ========== Xử lý submit form thêm sản phẩm ==========
/**
 * Xử lý sự kiện submit biểu mẫu thêm sản phẩm mới.
 * Bao gồm kiểm tra dữ liệu (validate) trước khi gửi lên máy chủ.
 */
async function xu_ly_them_san_pham(event) {
    event.preventDefault();

    // Lấy giá trị từ form
    const loai_hang = document.getElementById('chon_loai_hang').value;
    const ma_so = document.getElementById('nhap_ma_so').value.trim();
    const ten_san_pham = document.getElementById('nhap_ten').value.trim();
    const gia_co_ban = parseFloat(document.getElementById('nhap_gia').value);
    const ton_kho = parseInt(document.getElementById('nhap_ton_kho').value);

    // Kiểm tra dữ liệu hợp lệ (Validate)
    if (!loai_hang) {
        hien_thong_bao('Vui lòng chọn loại hàng.', 'loi');
        return;
    }
    if (!ma_so) {
        hien_thong_bao('Mã số không được để trống.', 'loi');
        return;
    }
    if (!ten_san_pham) {
        hien_thong_bao('Tên sản phẩm không được để trống.', 'loi');
        return;
    }
    if (isNaN(gia_co_ban) || gia_co_ban < 0) {
        hien_thong_bao('Giá cơ bản phải là số không âm.', 'loi');
        return;
    }
    if (isNaN(ton_kho) || ton_kho < 0) {
        hien_thong_bao('Số lượng tồn kho phải là số không âm.', 'loi');
        return;
    }

    // Tạo đối tượng dữ liệu gửi lên máy chủ
    const du_lieu_gui = {
        loai_hang: loai_hang,
        ma_so: ma_so,
        ten_san_pham: ten_san_pham,
        gia_co_ban: gia_co_ban,
        ton_kho: ton_kho
    };

    // Thêm các thuộc tính riêng theo loại hàng
    if (loai_hang === 'Sách') {
        const tac_gia = document.getElementById('nhap_tac_gia').value.trim();
        const nha_xuat_ban = document.getElementById('nhap_nha_xuat_ban').value.trim();
        if (!tac_gia) {
            hien_thong_bao('Tác giả không được để trống.', 'loi');
            return;
        }
        if (!nha_xuat_ban) {
            hien_thong_bao('Nhà xuất bản không được để trống.', 'loi');
            return;
        }
        du_lieu_gui.tac_gia = tac_gia;
        du_lieu_gui.nha_xuat_ban = nha_xuat_ban;
    } else if (loai_hang === 'Tạp chí') {
        const so_phat_hanh = document.getElementById('nhap_so_phat_hanh').value.trim();
        if (!so_phat_hanh) {
            hien_thong_bao('Số phát hành không được để trống.', 'loi');
            return;
        }
        du_lieu_gui.so_phat_hanh = so_phat_hanh;
    } else if (loai_hang === 'Báo giấy') {
        const ngay_xuat_ban = document.getElementById('nhap_ngay_xuat_ban').value.trim();
        if (!ngay_xuat_ban) {
            hien_thong_bao('Ngày xuất bản không được để trống.', 'loi');
            return;
        }
        du_lieu_gui.ngay_xuat_ban = ngay_xuat_ban;
    }

    // Gọi API thêm sản phẩm
    const ket_qua = await them_san_pham(du_lieu_gui);
    if (ket_qua) {
        if (ket_qua.du_lieu.trang_thai === 'thanh_cong') {
            hien_thong_bao(ket_qua.du_lieu.thong_bao, 'thanh_cong');
            dong_form_them();
            tai_va_hien_thi_danh_sach();
        } else {
            hien_thong_bao(ket_qua.du_lieu.thong_bao, 'loi');
        }
    }
}
