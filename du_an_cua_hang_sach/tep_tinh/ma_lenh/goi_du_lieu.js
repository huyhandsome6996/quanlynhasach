/**
 * Tệp goi_du_lieu.js - Đoạn mã JavaScript giao tiếp máy chủ.
 * Chứa các hàm dùng Fetch API để gọi các endpoint trên máy chủ Django.
 *
 * Các hàm chính:
 *   - lay_danh_sach():          Gọi API GET /danh-sach
 *   - tim_kiem(tu_khoa, tieu_chi): Gọi API GET /tim-kiem
 *   - sap_xep(tieu_chi):        Gọi API GET /sap-xep
 *   - them_san_pham(du_lieu):    Gọi API POST /them-san-pham
 *   - sua_san_pham(du_lieu):     Gọi API POST /sua-san-pham
 *   - xoa_san_pham(ma_so):      Gọi API POST /xoa-san-pham
 *   - lay_thong_ke():           Gọi API GET /thong-ke
 *   - them_vao_gio_hang(ma_so): Gọi API POST /them-gio-hang
 *   - xem_gio_hang():           Gọi API GET /xem-gio-hang
 *   - xoa_khoi_gio_hang(ma_so):Gọi API POST /xoa-gio-hang
 *   - thanh_toan_gio_hang():    Gọi API POST /thanh-toan
 *   - hoan_tac():               Gọi API POST /hoan-tac
 *   - lam_lai():                Gọi API POST /lam-lai
 */


/**
 * Gọi API GET /danh-sach để lấy toàn bộ danh sách mặt hàng.
 */
async function lay_danh_sach() {
    try {
        const phan_hoi = await fetch('/danh-sach');
        const du_lieu = await phan_hoi.json();
        return du_lieu;
    } catch (loi) {
        console.error('Lỗi khi lấy danh sách:', loi);
        hien_thong_bao('Không thể kết nối đến máy chủ.', 'loi');
        return null;
    }
}


/**
 * Gọi API GET /tim-kiem để tìm kiếm sản phẩm theo từ khóa và tiêu chí.
 *
 * Tham số:
 *   tu_khoa (string):   Từ khóa tìm kiếm.
 *   tieu_chi (string):  Tiêu chí tìm kiếm ('ten', 'ma', 'loai').
 */
async function tim_kiem(tu_khoa, tieu_chi) {
    try {
        const phan_hoi = await fetch(`/tim-kiem?tu_khoa=${encodeURIComponent(tu_khoa)}&tieu_chi=${encodeURIComponent(tieu_chi)}`);
        const du_lieu = await phan_hoi.json();
        return du_lieu;
    } catch (loi) {
        console.error('Lỗi khi tìm kiếm:', loi);
        hien_thong_bao('Không thể tìm kiếm. Vui lòng thử lại.', 'loi');
        return null;
    }
}


/**
 * Gọi API GET /sap-xep để sắp xếp danh sách theo tiêu chí.
 *
 * Tham số:
 *   tieu_chi (string): Tiêu chí sắp xếp ('gia_ban', 'ten_san_pham', 'ton_kho').
 */
async function sap_xep(tieu_chi) {
    try {
        const phan_hoi = await fetch(`/sap-xep?tieu_chi=${encodeURIComponent(tieu_chi)}`);
        const du_lieu = await phan_hoi.json();
        return du_lieu;
    } catch (loi) {
        console.error('Lỗi khi sắp xếp:', loi);
        hien_thong_bao('Không thể sắp xếp. Vui lòng thử lại.', 'loi');
        return null;
    }
}


/**
 * Gọi API POST /them-san-pham để thêm một sản phẩm mới.
 *
 * Tham số:
 *   du_lieu (object): Đối tượng chứa thông tin sản phẩm cần thêm.
 */
async function them_san_pham(du_lieu) {
    try {
        const phan_hoi = await fetch('/them-san-pham', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(du_lieu)
        });
        const ket_qua = await phan_hoi.json();
        return { trang_thai: phan_hoi.status, du_lieu: ket_qua };
    } catch (loi) {
        console.error('Lỗi khi thêm sản phẩm:', loi);
        hien_thong_bao('Không thể thêm sản phẩm. Vui lòng thử lại.', 'loi');
        return null;
    }
}


/**
 * Gọi API POST /sua-san-pham để sửa thông tin một sản phẩm.
 *
 * Tham số:
 *   du_lieu (object): Đối tượng chứa thông tin sản phẩm cần sửa.
 */
async function sua_san_pham(du_lieu) {
    try {
        const phan_hoi = await fetch('/sua-san-pham', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(du_lieu)
        });
        const ket_qua = await phan_hoi.json();
        return { trang_thai: phan_hoi.status, du_lieu: ket_qua };
    } catch (loi) {
        console.error('Lỗi khi sửa sản phẩm:', loi);
        hien_thong_bao('Không thể sửa sản phẩm. Vui lòng thử lại.', 'loi');
        return null;
    }
}


/**
 * Gọi API POST /xoa-san-pham để xóa một sản phẩm.
 *
 * Tham số:
 *   ma_so (string): Mã số sản phẩm cần xóa.
 */
async function xoa_san_pham(ma_so) {
    try {
        const phan_hoi = await fetch('/xoa-san-pham', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ma_so: ma_so })
        });
        const ket_qua = await phan_hoi.json();
        return { trang_thai: phan_hoi.status, du_lieu: ket_qua };
    } catch (loi) {
        console.error('Lỗi khi xóa sản phẩm:', loi);
        hien_thong_bao('Không thể xóa sản phẩm. Vui lòng thử lại.', 'loi');
        return null;
    }
}


/**
 * Gọi API GET /thong-ke để lấy thống kê tổng quan.
 */
async function lay_thong_ke() {
    try {
        const phan_hoi = await fetch('/thong-ke');
        const du_lieu = await phan_hoi.json();
        return du_lieu;
    } catch (loi) {
        console.error('Lỗi khi lấy thống kê:', loi);
        hien_thong_bao('Không thể tải thống kê.', 'loi');
        return null;
    }
}


/**
 * Gọi API POST /them-gio-hang để thêm sản phẩm vào giỏ hàng.
 */
async function them_vao_gio_hang(ma_so) {
    try {
        const phan_hoi = await fetch('/them-gio-hang', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ma_so: ma_so })
        });
        const ket_qua = await phan_hoi.json();
        return { trang_thai: phan_hoi.status, du_lieu: ket_qua };
    } catch (loi) {
        console.error('Lỗi khi thêm vào giỏ hàng:', loi);
        hien_thong_bao('Không thể thêm vào giỏ hàng.', 'loi');
        return null;
    }
}


/**
 * Gọi API GET /xem-gio-hang để xem giỏ hàng.
 */
async function xem_gio_hang() {
    try {
        const phan_hoi = await fetch('/xem-gio-hang');
        const du_lieu = await phan_hoi.json();
        return du_lieu;
    } catch (loi) {
        console.error('Lỗi khi xem giỏ hàng:', loi);
        return null;
    }
}


/**
 * Gọi API POST /xoa-gio-hang để xóa sản phẩm khỏi giỏ hàng.
 */
async function xoa_khoi_gio_hang(ma_so) {
    try {
        const phan_hoi = await fetch('/xoa-gio-hang', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ma_so: ma_so })
        });
        const ket_qua = await phan_hoi.json();
        return { trang_thai: phan_hoi.status, du_lieu: ket_qua };
    } catch (loi) {
        console.error('Lỗi khi xóa khỏi giỏ hàng:', loi);
        return null;
    }
}


/**
 * Gọi API POST /thanh-toan để thanh toán giỏ hàng.
 */
async function thanh_toan_gio_hang() {
    try {
        const phan_hoi = await fetch('/thanh-toan', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        const ket_qua = await phan_hoi.json();
        return { trang_thai: phan_hoi.status, du_lieu: ket_qua };
    } catch (loi) {
        console.error('Lỗi khi thanh toán:', loi);
        hien_thong_bao('Không thể thanh toán. Vui lòng thử lại.', 'loi');
        return null;
    }
}


/**
 * Gọi API POST /hoan-tac để hoàn tác (Undo).
 */
async function hoan_tac() {
    try {
        const phan_hoi = await fetch('/hoan-tac', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        const ket_qua = await phan_hoi.json();
        return { trang_thai: phan_hoi.status, du_lieu: ket_qua };
    } catch (loi) {
        console.error('Lỗi khi hoàn tác:', loi);
        hien_thong_bao('Không thể hoàn tác.', 'loi');
        return null;
    }
}


/**
 * Gọi API POST /lam-lai để làm lại (Redo).
 */
async function lam_lai() {
    try {
        const phan_hoi = await fetch('/lam-lai', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        const ket_qua = await phan_hoi.json();
        return { trang_thai: phan_hoi.status, du_lieu: ket_qua };
    } catch (loi) {
        console.error('Lỗi khi làm lại:', loi);
        hien_thong_bao('Không thể làm lại.', 'loi');
        return null;
    }
}
