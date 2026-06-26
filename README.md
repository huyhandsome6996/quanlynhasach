# Hệ thống Quản lý Cửa hàng Sách

Đồ án kiểm tra cuối kì môn **Lập trình Nâng cao**.

Phiên bản giao diện **Tkinter (Python thuần)** — bản chính để ôn thi vì dễ làm và dễ hiểu nhất.

> Nhóm quyết định dùng Tkinter thay cho PyQt6 và Django vì Tkinter có sẵn trong Python
> tiêu chuẩn, cú pháp đơn giản, dễ ôn thi. Tất cả tính năng và yêu cầu theo barem chấm
> điểm đều được GIỮ NGUYÊN.

Xem tài liệu chi tiết tại: [`do_an_tkinter/`](do_an_tkinter/)

## Chạy nhanh

```bash
# Tkinter đi kèm Python, không cần cài thêm thư viện.
cd do_an_tkinter
python main.py
```

Tài khoản mẫu:

| Tài khoản | Mật khẩu | Quyền |
|-----------|----------|-------|
| `admin` | `123` | Toàn quyền (xem + thêm + sửa + xóa + giỏ hàng) |
| `nhanvien` | `123` | Hạn chế (không được xóa) |

## Đầy đủ tính năng theo barem

1. **Đăng nhập + phân quyền** — Admin (toàn quyền) / Nhân viên (không được xóa)
2. **Đọc danh sách** — Hiển thị toàn bộ mặt hàng từ SQLite ra bảng
3. **Thêm sản phẩm** — Thêm 1 trong 5 loại (Sách / Tạp chí / Báo giấy / Luận văn / Bản thảo)
4. **Sửa sản phẩm** — Cập nhật thông tin mặt hàng đã có
5. **Xóa sản phẩm** — Có xác nhận và kiểm tra phân quyền
6. **Tìm kiếm + sắp xếp** — Theo tên / mã / loại + Merge Sort trên DSLK đôi
7. **Thống kê** — Tổng số, giá cao/thấp nhất, tổng giá trị kho, phân bố theo loại
8. **Undo / Redo** — Cấu trúc Stack LIFO tự cài đặt
9. **Giỏ hàng + thanh toán** — Cấu trúc Queue FIFO tự cài đặt

## Yêu cầu kỹ thuật theo barem

- **OOP kế thừa + đa hình**: lớp `MatHang` + 5 lớp con (Sách, Tạp chí, Báo giấy, Luận văn, Bản thảo)
- **Danh sách liên kết đôi**: tự cài đặt, không dùng `list` встроенный
- **Merge Sort**: sắp xếp trên con trỏ DSLK đôi
- **Stack LIFO**: tự cài cho Undo/Redo
- **Queue FIFO**: tự cài cho Giỏ hàng
- **SQLite CRUD**: lưu trữ bền vững, parameterized query chống SQL Injection
- **Try/except**: bọc 7 thao tác chính (Thêm / Sửa / Xóa / Undo / Redo / Giỏ / Thanh toán)

## Chạy kiểm thử

```bash
cd do_an_tkinter
python test_app.py
```

Kết quả mong đợi: `47/47 PASS`.

## Cấu trúc thư mục

```
quanlynhasach/
├── README.md                       ← File này
├── do_an_tkinter/                  ← BẢN CHÍNH — Tkinter
│   ├── main.py                     ← Điểm vào ứng dụng
│   ├── test_app.py                 ← 47 test tự động
│   ├── quan_ly_trung_tam.py        ← State container (DB + DSLK + Stack + Queue)
│   ├── loi_thuat_toan/             ← 7 module thuật toán dùng chung
│   │   ├── lop_doi_tuong.py        ← MatHang + 5 con (OOP đa hình)
│   │   ├── danh_sach_lien_ket.py   ← DSLK đôi + Merge Sort
│   │   ├── cau_truc_du_lieu.py     ← Stack LIFO + Queue FIFO
│   │   ├── ket_noi_sqlite.py       ← SQLite CRUD + User
│   │   ├── nguoi_dung.py           ← NguoiDung + phân quyền
│   │   └── kiem_thu.py             ← Test DSLK + Merge Sort
│   ├── khung_chinh/                ← Cửa sổ chính (UI + Điều khiển + Thuật toán)
│   │   ├── khung_chinh_tt.py       ← Thuật toán khung chính (_tt)
│   │   ├── cua_so_chinh_ui.py      ← Giao diện (_ui)
│   │   └── cua_so_chinh_dk.py      ← Điều khiển (_dk)
│   └── chuc_nang/                  ← 9 chức năng theo barem
│       ├── _shared/                ← UI dùng chung (form thêm/sửa)
│       ├── cn01_dang_nhap_phan_quyen/
│       │   ├── dang_nhap_tt.py     ← Thuật toán (_tt)
│       │   ├── dang_nhap_ui.py     ← Giao diện (_ui)
│       │   └── dang_nhap_dk.py     ← Điều khiển (_dk)
│       ├── cn02_doc_danh_sach/     ← doc_danh_sach_{tt,ui,dk}.py
│       ├── cn03_them_san_pham/     ← them_san_pham_{tt,ui,dk}.py
│       ├── cn04_sua_san_pham/      ← sua_san_pham_{tt,ui,dk}.py
│       ├── cn05_xoa_san_pham/      ← xoa_san_pham_{tt,ui,dk}.py
│       ├── cn06_tim_kiem_sap_xep/  ← tim_kiem_sap_xep_{tt,ui,dk}.py
│       ├── cn07_thong_ke/          ← thong_ke_{tt,ui,dk}.py
│       ├── cn08_hoan_tac_lam_lai/  ← hoan_tac_lam_lai_{tt,ui,dk}.py
│       └── cn09_gio_hang/          ← gio_hang_{tt,ui,dk}.py
├── tai_lieu_hoc_thi/               ← Tài liệu ôn thi HTML/CSS/JS cho 3 thành viên
└── phan_chia_cong_viec.docx        ← Bảng phân chia công việc
```

## Quy ước đặt tên file

Trong mỗi folder chức năng:

| Hậu tố | Vai trò | Ví dụ |
|--------|---------|-------|
| `_tt` | **Thuật toán** — chứa các hàm xử lý logic thuần | `dang_nhap_tt.py` |
| `_ui` | **Giao diện** — chỉ vẽ widget Tkinter, không chứa logic | `dang_nhap_ui.py` |
| `_dk` | **Điều khiển** — kết nối `_ui` với `_tt`, gắn sự kiện | `dang_nhap_dk.py` |
