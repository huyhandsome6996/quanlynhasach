/**
 * Tệp goi_du_lieu.js - Đoạn mã JavaScript giao tiếp máy chủ.
 * Chứa các hàm dùng Fetch API để gọi các endpoint trên máy chủ Django.
 *
 * Các hàm chính:
 *   - lay_danh_sach(): Gọi API GET /danh-sach để lấy toàn bộ mặt hàng.
 *   - tim_kiem(tu_khoa): Gọi API GET /tim-kiem để tìm kiếm sản phẩm.
 *   - sap_xep(tieu_chi): Gọi API GET /sap-xep để sắp xếp danh sách.
 *   - them_san_pham(du_lieu): Gọi API POST /them-san-pham để thêm sản phẩm.
 *   - xoa_san_pham(ma_so): Gọi API POST /xoa-san-pham để xóa sản phẩm.
 */


/**
 * Gọi API GET /danh-sach để lấy toàn bộ danh sách mặt hàng.
 *
 * Trả về:
 *   Promise chứa dữ liệu JSON từ máy chủ.
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
 * Gọi API GET /tim-kiem để tìm kiếm sản phẩm theo từ khóa.
 *
 * Tham số:
 *   tu_khoa (string): Từ khóa tìm kiếm.
 *
 * Trả về:
 *   Promise chứa dữ liệu JSON từ máy chủ.
 */
async function tim_kiem(tu_khoa) {
    try {
        const phan_hoi = await fetch(`/tim-kiem?tu_khoa=${encodeURIComponent(tu_khoa)}`);
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
 *
 * Trả về:
 *   Promise chứa dữ liệu JSON từ máy chủ.
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
 * Gọi API POST /them-san-pham để thêm một sản phẩm mới vào hệ thống.
 *
 * Tham số:
 *   du_lieu (object): Đối tượng chứa thông tin sản phẩm cần thêm.
 *
 * Trả về:
 *   Promise chứa dữ liệu JSON phản hồi từ máy chủ.
 */
async function them_san_pham(du_lieu) {
    try {
        const phan_hoi = await fetch('/them-san-pham', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
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
 * Gọi API POST /xoa-san-pham để xóa một sản phẩm khỏi hệ thống.
 *
 * Tham số:
 *   ma_so (string): Mã số định danh của sản phẩm cần xóa.
 *
 * Trả về:
 *   Promise chứa dữ liệu JSON phản hồi từ máy chủ.
 */
async function xoa_san_pham(ma_so) {
    try {
        const phan_hoi = await fetch('/xoa-san-pham', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
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
