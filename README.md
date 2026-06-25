# Hệ thống Quản lý Cửa hàng Sách

Đồ án kiểm tra cuối kì môn **Lập trình Nâng cao**.

Phiên bản giao diện **Web (HTML + CSS + JavaScript) + Django (Python)**.

> Sau khi nghe phản hồi từ các thành viên về việc PyQt6 có quá nhiều hàm mới phải học,
> nhóm đã quyết định quay lại phiên bản Web + Django vì gần gũi với các kiến thức
> đã học (HTML/CSS/JS cơ bản + Python thuần). Tất cả tính năng và yêu cầu theo
> barem chấm điểm đều được GIỮ NGUYÊN.

Xem tài liệu chi tiết tại: [`du_an_cua_hang_sach/README.md`](du_an_cua_hang_sach/README.md)

## Chạy nhanh

```bash
pip install django
cd du_an_cua_hang_sach
python manage.py runserver
```

Mở trình duyệt tại: <http://127.0.0.1:8000/>

Tài khoản mẫu:

| Tài khoản | Mật khẩu | Quyền |
|-----------|----------|-------|
| `admin` | `123` | Toàn quyền (xem + thêm + sửa + xóa + giỏ hàng) |
| `nhanvien` | `123` | Hạn chế (không được xóa) |

## Đầy đủ tính năng theo barem

1. **OOP đa hình** - 5 loại mặt hàng: Sách, Tạp chí, Báo giấy, Luận văn, Bản thảo
2. **Danh sách liên kết đôi** + **thuật toán Merge Sort** trên con trỏ
3. **SQLite CRUD** - Lưu trữ bền vững, parameterized query chống SQL Injection
4. **Tìm kiếm nâng cao** - Theo tên / mã số / loại hàng
5. **Undo/Redo** - Cấu trúc Stack LIFO tự cài đặt
6. **Giỏ hàng** - Cấu trúc Queue FIFO tự cài đặt
7. **Đăng nhập phân quyền** - Admin (toàn quyền) / Nhân viên (không được xóa)
8. **Thống kê + tổng giá trị kho**
9. **Try/except** cho 7 thao tác chính (Thêm / Sửa / Xóa / Undo / Redo / Giỏ hàng / Thanh toán)

## Chạy kiểm thử

```bash
cd du_an_cua_hang_sach
python -m ung_dung_giao_tiep.loi_thuat_toan.kiem_thu
```

## Cấu trúc thư mục

```
quanlynhasach/
├── README.md                       ← File này
├── do_an_pyqt6/                    ← Phiên bản PyQt6 (đã bỏ - giữ để tham khảo)
├── du_an_cua_hang_sach/            ← Phiên bản Django (đang dùng)
│   ├── manage.py
│   ├── cau_hinh_he_thong/          ← Cấu hình Django
│   ├── ung_dung_giao_tiep/         ← Ứng dụng chính
│   │   ├── xu_ly_yeu_cau.py        ← 17 API endpoints
│   │   ├── duong_dan.py            ← Điều hướng URL
│   │   └── loi_thuat_toan/
│   │       ├── lop_doi_tuong.py    ← 5 lớp OOP (MatHang + 5 con)
│   │       ├── danh_sach_lien_ket.py ← DSLK đôi + Merge Sort
│   │       ├── cau_truc_du_lieu.py ← Stack + Queue tự cài
│   │       ├── ket_noi_sqlite.py   ← SQLite CRUD + User
│   │       ├── nguoi_dung.py       ← Lớp NguoiDung + phân quyền
│   │       └── kiem_thu.py         ← Test DSLK + Merge Sort
│   ├── giao_dien/                  ← Template HTML
│   │   ├── trang_chu.html
│   │   ├── dang_nhap.html          ← Trang đăng nhập
│   │   └── thanh_phan/             ← Header/Toolbar/Table/Form/Cart
│   └── tep_tinh/                   ← Static files
│       ├── hinh_thuc/trang_tri.css ← CSS (~1240 dòng)
│       └── ma_lenh/                ← JavaScript
│           ├── goi_du_lieu.js      ← Fetch API
│           └── tuong_tac.js        ← Xử lý UI + phân quyền
├── tai_lieu_hoc_thi/               ← Tài liệu ôn thi HTML/CSS/JS
└── phan_chia_cong_viec.docx        ← Bảng phân chia công việc
```
