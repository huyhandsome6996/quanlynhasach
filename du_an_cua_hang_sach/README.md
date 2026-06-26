# HỆ THỐNG QUẢN LÝ CỬA HÀNG SÁCH

## Giới thiệu đồ án

Đây là đồ án kiểm tra cuối kì môn **Lập trình Nâng cao**. Hệ thống quản lý cửa hàng sách được xây dựng theo mô hình Web Application, sử dụng **Django (Python)** làm backend và **JavaScript + HTML/CSS** làm frontend.

### Mục tiêu đồ án

- Vận dụng **OOP** (Hướng đối tượng): Thiết kế hệ thống lớp có tính kế thừa, đa hình, đóng gói.
- Cài đặt **Cấu trúc dữ liệu tự định nghĩa**: Danh sách liên kết đôi (Doubly Linked List), Ngăn xếp (Stack), Hàng đợi (Queue).
- Xây dựng **giao diện Web** chuyên nghiệp bằng HTML/CSS/JavaScript.
- **Xử lý tệp và Ngoại lệ**: Lưu trữ dữ liệu bền vững (SQLite) và kiểm soát lỗi người dùng.

---

## Công nghệ sử dụng

| Công nghệ | Vai trò | Phiên bản |
|-----------|---------|-----------|
| Python | Ngôn ngữ lập trình backend | 3.x |
| Django | Web framework backend | 6.0 |
| SQLite | Cơ sở dữ liệu | 3.x |
| JavaScript | Ngôn ngữ lập trình frontend | ES6+ |
| HTML/CSS | Giao diện người dùng | 5/3 |
| Fetch API | Giao tiếp giữa frontend và backend | - |

---

## Cấu trúc thư mục dự án

```
du_an_cua_hang_sach/
│
├── manage.py                          # Điểm chạy chương trình Django
├── db.sqlite3                         # Cơ sở dữ liệu SQLite
│
├── cau_hinh_he_thong/                 # Cấu hình hệ thống Django
│   ├── __init__.py
│   ├── settings.py                    # Cài đặt dự án (DB, Static, Apps)
│   ├── duong_dan.py                   # Điều hướng URL chính
│   ├── wsgi.py                        # Cấu hình WSGI
│   └── asgi.py                        # Cấu hình ASGI
│
├── ung_dung_giao_tiep/                # Ứng dụng chính
│   ├── __init__.py
│   ├── apps.py                        # Cấu hình ứng dụng
│   ├── duong_dan.py                   # Điều hướng URL ứng dụng (17 endpoint)
│   ├── xu_ly_yeu_cau.py               # Xử lý yêu cầu HTTP + 9 nhóm API
│   │
│   └── loi_thuat_toan/               # Lõi thuật toán & cấu trúc dữ liệu
│       ├── __init__.py
│       ├── lop_doi_tuong.py           # 5 lớp OOP (MatHang + Sach/TapChi/BaoGiay/LuanVan/BanThao)
│       ├── danh_sach_lien_ket.py      # Danh sách liên kết đôi + Merge Sort
│       ├── cau_truc_du_lieu.py        # Stack (Undo/Redo) + Queue (Giỏ hàng)
│       ├── ket_noi_sqlite.py          # SQLite CRUD + bảng người dùng
│       ├── nguoi_dung.py              # Lớp NguoiDung + phân quyền Admin/NV
│       └── kiem_thu.py                # Kiểm thử các cấu trúc dữ liệu
│
├── giao_dien/                         # Giao diện HTML (Templates)
│   ├── trang_chu.html                 # Trang chủ (sau đăng nhập)
│   ├── dang_nhap.html                 # Trang đăng nhập
│   └── thanh_phan/                    # Các thành phần giao diện
│       ├── dau_trang.html             # Thanh tiêu đề + khung người dùng + nút Đăng xuất
│       ├── thanh_cong_cu.html         # Thanh công cụ (Tìm kiếm, Sắp xếp...)
│       ├── bang_du_lieu.html          # Bảng dữ liệu + Thống kê
│       ├── bieu_mau_them.html         # Biểu mẫu Thêm/Sửa sản phẩm
│       └── cuoi_trang.html            # Giỏ hàng + Chân trang
│
└── tep_tinh/                          # Tệp tĩnh (Static files)
    ├── ma_lenh/                       # JavaScript
    │   ├── goi_du_lieu.js             # Gọi API từ backend
    │   └── tuong_tac.js               # Xử lý tương tác người dùng
    └── hinh_thuc/                     # CSS
        └── trang_tri.css              # Trang trí giao diện
```

---

## Cấu trúc dữ liệu (Data Structures)

### 1. Danh sách liên kết đôi (DoublyLinkedList)

Đây là cấu trúc dữ liệu **chính** quản lý toàn bộ mặt hàng trên RAM.

#### Lớp Node (Mắt xích)

```python
class Node:
    data   # Dữ liệu (đối tượng Sách, Tạp chí...)
    truoc  # Con trỏ trỏ về Node phía trước
    next   # Con trỏ trỏ đến Node phía sau
```

**Minh họa:**
```
None <-- [Node A] <--> [Node B] <--> [Node C] --> None
           head                         cuoi
```

#### Lớp DoublyLinkedList

```python
class DoublyLinkedList:
    head     # Trỏ đến Node đầu tiên
    cuoi     # Trỏ đến Node cuối cùng
    so_luong # Số lượng phần tử
```

**Các phương thức:**

| Phương thức | Mô tả | Độ phức tạp |
|-------------|-------|-------------|
| `them_vao_cuoi(data)` | Thêm phần tử vào cuối danh sách | O(1) |
| `xoa_node(ma_so)` | Xóa Node theo mã số | O(n) |
| `tim_theo_ma(ma_so)` | Tìm kiếm theo mã số chính xác | O(n) |
| `tim_kiem(tu_khoa, tieu_chi)` | Tìm kiếm nâng cao (tên/mã/loại) | O(n) |
| `sap_xep_tron(tieu_chi)` | Sắp xếp Merge Sort | O(n log n) |
| `chuyen_thanh_danh_sach()` | Chuyển DSLK thành list Python (để gửi JSON) | O(n) |

---

### 2. Ngăn xếp - Stack (Undo/Redo)

Cấu trúc **LIFO** (Last In, First Out) - Vào sau, ra trước.

```python
class NganXep:
    dinh      # Trỏ đến Node trên cùng
    so_luong  # Số lượng phần tử
```

**Các phương thức:**

| Phương thức | Mô tả |
|-------------|-------|
| `day_vao(data)` | Đẩy phần tử vào đỉnh ngăn xếp (Push) |
| `lay_ra()` | Lấy phần tử khỏi đỉnh ngăn xếp (Pop) |
| `xem_dinh()` | Xem phần tử đỉnh mà không lấy ra (Peek) |
| `rong()` | Kiểm tra ngăn xếp rỗng |
| `xoa_tat_ca()` | Xóa toàn bộ ngăn xếp |

**Ứng dụng - Undo/Redo:**
- Mỗi thao tác (Thêm/Sửa/Xóa) được đẩy vào **Stack Undo**.
- Nhấn **Undo**: Lấy thao tác từ Stack Undo → Hoàn tác → Đẩy vào Stack Redo.
- Nhấn **Redo**: Lấy thao tác từ Stack Redo → Làm lại → Đẩy vào Stack Undo.
- Thao tác mới sẽ xóa Stack Redo (chuỗi thao tác bị đứt).

---

### 3. Hàng đợi - Queue (Giỏ hàng)

Cấu trúc **FIFO** (First In, First Out) - Vào trước, ra trước.

```python
class HangDoi:
    dau       # Trỏ đến Node đầu hàng đợi (lấy ra ở đây)
    cuoi_hang # Trỏ đến Node cuối hàng đợi (thêm vào ở đây)
    so_luong  # Số lượng phần tử
```

**Các phương thức:**

| Phương thức | Mô tả |
|-------------|-------|
| `them_vao(data)` | Thêm phần tử vào cuối hàng đợi (Enqueue) |
| `lay_ra()` | Lấy phần tử khỏi đầu hàng đợi (Dequeue) |
| `xem_danh_sach()` | Xem toàn bộ hàng đợi |
| `xoa_theo_ma(ma_so)` | Xóa một phần tử theo mã số |
| `rong()` | Kiểm tra hàng đợi rỗng |

**Ứng dụng - Giỏ hàng:**
- Thêm mặt hàng vào giỏ → `them_vao()`
- Thanh toán → Lấy từng mặt hàng ra theo thứ tự FIFO (`lay_ra()`) và giảm tồn kho.

---

## Thiết kế OOP (Hướng đối tượng)

### Sơ đồ kế thừa

```
MatHang (Lớp cha trừu tượng - ABC)
  ├── Sach (Sách)           → tinh_gia_ban() = gia_co_ban × 1.10
  ├── TapChi (Tạp chí)      → tinh_gia_ban() = gia_co_ban × 1.05
  ├── BaoGiay (Báo giấy)    → tinh_gia_ban() = gia_co_ban × 1.00
  ├── LuanVan (Luận văn)    → tinh_gia_ban() = gia_co_ban × 1.15
  └── BanThao (Bản thảo)    → tinh_gia_ban() = gia_co_ban × 1.08
```

### Thuộc tính chung (lớp cha MatHang)

| Thuộc tính | Kiểu | Mô tả |
|------------|------|-------|
| `ma_so` | str | Mã định danh duy nhất |
| `loai_hang` | str | Loại mặt hàng |
| `ten_san_pham` | str | Tên sản phẩm |
| `gia_co_ban` | float | Giá cơ bản (>= 0) |
| `ton_kho` | int | Số lượng tồn kho (>= 0) |

### Thuộc tính riêng (lớp con)

| Lớp con | Thuộc tính riêng |
|---------|-----------------|
| Sach | `tac_gia`, `nha_xuat_ban` |
| TapChi | `so_phat_hanh` |
| BaoGiay | `ngay_xuat_ban` |
| LuanVan | `tac_gia`, `truong_dai_hoc` |
| BanThao | `tac_gia`, `trang_thai` |

### Tính đa hình (Polymorphism)

Mỗi lớp con **ghi đè** phương thức `tinh_gia_ban()` với công thức thuế khác nhau:

- **Sách**: +10% thuế → `gia_co_ban × 1.10`
- **Tạp chí**: +5% thuế → `gia_co_ban × 1.05`
- **Báo giấy**: Không thuế → `gia_co_ban × 1.00`
- **Luận văn**: +15% thuế → `gia_co_ban × 1.15`
- **Bản thảo**: +8% thuế → `gia_co_ban × 1.08`

---

## Thuật toán Sắp xếp - Merge Sort

### Nguyên lý

Thuật toán **Sắp xếp trộn (Merge Sort)** trên danh sách liên kết đôi:

1. **Chia đôi**: Dùng kỹ thuật **con trỏ nhanh/chậm** để tìm điểm giữa.
   - Con trỏ chậm đi 1 bước mỗi lần.
   - Con trỏ nhanh đi 2 bước mỗi lần.
   - Khi con trỏ nhanh đến cuối → Con trỏ chậm ở giữa.

2. **Sắp xếp đệ quy**: Gọi đệ quy Merge Sort trên từng nửa.

3. **Trộn**: So sánh Node đầu của hai nửa, Node có giá trị nhỏ hơn được nối vào kết quả.

### Độ phức tạp

- **Thời gian**: O(n log n) - Tối ưu cho danh sách liên kết.
- **Không gian**: O(1) - Chỉ thao tác trên con trỏ, không cần mảng phụ.
- **Ổn định**: Có - Các phần tử có giá trị bằng nhau giữ nguyên thứ tự.

### Tiêu chí sắp xếp

| Giá trị `tieu_chi` | Sắp xếp theo |
|---------------------|--------------|
| `gia_ban` | Giá bán (mặc định) |
| `ten_san_pham` | Tên sản phẩm (thứ tự alphabet) |
| `ton_kho` | Số lượng tồn kho |

---

## Cơ sở dữ liệu (SQLite)

### Bảng `bang_mat_hang`

| Cột | Kiểu | Mô tả |
|-----|------|-------|
| `ma_so` | TEXT PRIMARY KEY | Mã định danh duy nhất |
| `loai_hang` | TEXT NOT NULL | Loại mặt hàng |
| `ten_san_pham` | TEXT NOT NULL | Tên sản phẩm |
| `gia_co_ban` | REAL NOT NULL | Giá cơ bản |
| `ton_kho` | INTEGER NOT NULL | Số lượng tồn kho |
| `tac_gia` | TEXT | Tên tác giả (Sách, Luận văn, Bản thảo) |
| `nha_xuat_ban` | TEXT | Nhà xuất bản (Sách) |
| `so_phat_hanh` | TEXT | Số phát hành (Tạp chí) |
| `ngay_xuat_ban` | TEXT | Ngày xuất bản (Báo giấy) |
| `truong_dai_hoc` | TEXT | Trường đại học (Luận văn) |
| `trang_thai` | TEXT | Trạng thái (Bản thảo) |

---

## API Endpoints

### Quản lý sản phẩm (CRUD)

| Phương thức | Endpoint | Mô tả |
|-------------|----------|-------|
| GET | `/danh-sach` | Lấy toàn bộ danh sách mặt hàng |
| POST | `/them-san-pham` | Thêm sản phẩm mới |
| POST | `/sua-san-pham` | Sửa thông tin sản phẩm |
| POST | `/xoa-san-pham` | Xóa sản phẩm theo mã số |

### Tìm kiếm và Sắp xếp

| Phương thức | Endpoint | Tham số | Mô tả |
|-------------|----------|---------|-------|
| GET | `/tim-kiem` | `tu_khoa`, `tieu_chi` (ten/ma/loai) | Tìm kiếm nâng cao |
| GET | `/sap-xep` | `tieu_chi` (gia_ban/ten_san_pham/ton_kho) | Sắp xếp Merge Sort |

### Thống kê

| Phương thức | Endpoint | Mô tả |
|-------------|----------|-------|
| GET | `/thong-ke` | Thống kê tổng quan (đắt nhất, rẻ nhất, sắp hết hàng...) |

### Giỏ hàng (Queue)

| Phương thức | Endpoint | Mô tả |
|-------------|----------|-------|
| POST | `/them-gio-hang` | Thêm mặt hàng vào giỏ hàng |
| GET | `/xem-gio-hang` | Xem danh sách giỏ hàng |
| POST | `/xoa-gio-hang` | Xóa mặt hàng khỏi giỏ hàng |
| POST | `/thanh-toan` | Thanh toán toàn bộ giỏ hàng |

### Undo/Redo (Stack)

| Phương thức | Endpoint | Mô tả |
|-------------|----------|-------|
| POST | `/hoan-tac` | Hoàn tác thao tác gần nhất (Undo) |
| POST | `/lam-lai` | Làm lại thao tác vừa hoàn tác (Redo) |

---

## Luồng hoạt động tổng thể

### 1. Khởi động hệ thống

```
Người dùng mở trang web
       ↓
Django nhận yêu cầu GET /
       ↓
khoi_tao_danh_sach() được gọi lần đầu
       ↓
Tạo DoublyLinkedList rỗng
       ↓
tai_du_lieu() đọc từ SQLite
       ↓
Tạo đối tượng OOP (Sach, TapChi, BaoGiay, LuanVan, BanThao)
       ↓
them_vao_cuoi() nối vào DSLK đôi trên RAM
       ↓
Khởi tạo Stack Undo/Redo và Queue Giỏ hàng
       ↓
Trả về trang HTML cho trình duyệt
```

### 2. Thêm sản phẩm

```
Người dùng điền form → Nhấn "Thêm"
       ↓
JavaScript validate dữ liệu
       ↓
Fetch API POST /them-san-pham
       ↓
Django kiểm tra hợp lệ + trùng mã
       ↓
Tạo đối tượng OOP tương ứng
       ↓
them_vao_cuoi() → Thêm vào DSLK trên RAM
       ↓
INSERT INTO SQLite → Lưu vĩnh viễn
       ↓
day_vao() → Lưu thao tác vào Stack Undo
       ↓
Trả về JSON → JavaScript cập nhật bảng
```

### 3. Tìm kiếm

```
Người dùng nhập từ khóa + chọn tiêu chí
       ↓
Fetch API GET /tim-kiem?tu_khoa=...&tieu_chi=...
       ↓
Django gọi tim_kiem() trên DSLK đôi
       ↓
Duyệt qua từng Node bằng con trỏ next
       ↓
So sánh theo tiêu chí (tên/mã/loại)
       ↓
Trả về danh sách kết quả JSON
       ↓
JavaScript vẽ lại bảng với kết quả
```

### 4. Sắp xếp (Merge Sort)

```
Người dùng chọn tiêu chí → Nhấn "Sắp xếp"
       ↓
Fetch API GET /sap-xep?tieu_chi=...
       ↓
Django gọi sap_xep_tron() trên DSLK đôi
       ↓
Bước 1: _chia_doi() - Con trỏ nhanh/chậm
       ↓
Bước 2: Gọi đệ quy sắp xếp từng nửa
       ↓
Bước 3: _tron() - Trộn hai nửa đã sắp xếp
       ↓
Trả về danh sách đã sắp xếp JSON
       ↓
JavaScript vẽ lại bảng với kết quả
```

### 5. Giỏ hàng (Queue - FIFO)

```
Nhấn 🛒 → them_vao() thêm vào Hàng đợi
       ↓
Xem giỏ hàng → xem_danh_sach() hiển thị
       ↓
Nhấn "Thanh toán"
       ↓
lay_ra() lấy từng mặt hàng (FIFO)
       ↓
Giảm ton_kho của sản phẩm đi 1
       ↓
Cập nhật SQLite
       ↓
Xóa giỏ hàng → Hoàn tất
```

### 6. Undo/Redo (Stack - LIFO)

```
Mỗi thao tác (Thêm/Sửa/Xóa) → day_vao() Stack Undo
       ↓
Nhấn Undo → lay_ra() từ Stack Undo
       ↓
Hoàn tác thao tác (Xóa phần đã thêm / Khôi phục phần đã xóa/sửa)
       ↓
day_vao() vào Stack Redo
       ↓
Nhấn Redo → lay_ra() từ Stack Redo
       ↓
Làm lại thao tác
       ↓
day_vao() vào Stack Undo
```

---

## Cách chạy dự án

### Yêu cầu

- Python 3.x
- Django (cài bằng `pip install django`)

### Các bước chạy

```bash
# 1. Di chuyển vào thư mục dự án
cd du_an_cua_hang_sach

# 2. Chạy migration (chỉ lần đầu)
python manage.py migrate

# 3. Khởi động máy chủ
python manage.py runserver

# 4. Mở trình duyệt và truy cập
# http://127.0.0.1:8000/
```

### Chạy kiểm thử

```bash
cd du_an_cua_hang_sach
python -m ung_dung_giao_tiep.loi_thuat_toan.kiem_thu
```

---

## Tiêu chí đánh giá và mức độ đáp ứng

| Tiêu chí | Trọng số | Đáp ứng | Chi tiết |
|----------|----------|---------|----------|
| Cấu trúc dữ liệu | 30% | ✅ 100% | DoublyLinkedList + Stack + Queue tự cài đặt hoàn toàn |
| Tư duy OOP | 20% | ✅ 100% | 5 lớp con kế thừa + đa hình tinh_gia_ban() |
| Giao diện | 20% | ✅ 100% | Web responsive, validate form, thông báo lỗi |
| Thuật toán | 15% | ✅ 100% | Merge Sort + tìm kiếm tuyến tính trên Linked List |
| Xử lý File/Ngoại lệ | 15% | ✅ 100% | SQLite CRUD + bắt lỗi nhập liệu đầy đủ |

### Tính năng mở rộng (điểm cộng)

| Tính năng | Cấu trúc dữ liệu | Mô tả |
|-----------|-----------------|-------|
| Đăng nhập phân quyền | Session + SQLite | Admin (toàn quyền) / Nhân viên (không được xóa) |
| Undo/Redo | Stack (LIFO) | Hoàn tác/làm lại thao tác Thêm/Sửa/Xóa |
| Giỏ hàng | Queue (FIFO) | Thêm/xóa/thanh toán giỏ hàng |
| Thống kê | Duyệt DSLK | Đắt nhất, rẻ nhất, sắp hết hàng, tổng giá trị kho |
| Tìm kiếm nâng cao | Duyệt DSLK | Theo tên, mã số, loại hàng |
| 5 loại mặt hàng | Kế thừa OOP | Sách, Tạp chí, Báo giấy, Luận văn, Bản thảo |

### Danh sách 17 API Endpoint

| # | Nhóm | Phương thức | Đường dẫn | Mô tả |
|---|------|------------|-----------|-------|
| 1 | Đăng nhập | GET | `/` | Trang chủ (yêu cầu đăng nhập) |
| 2 | Đăng nhập | GET | `/dang-nhap` | Trang đăng nhập |
| 3 | Đăng nhập | POST | `/api/dang-nhap` | Xác thực tài khoản |
| 4 | Đăng nhập | POST/GET | `/api/dang-xuat` hoặc `/dang-xuat` | Đăng xuất |
| 5 | Đăng nhập | GET | `/api/nguoi-dung` | Lấy thông tin người dùng |
| 6 | Đọc | GET | `/danh-sach` | Lấy toàn bộ mặt hàng |
| 7 | Thêm | POST | `/them-san-pham` | Thêm sản phẩm (5 loại) |
| 8 | Sửa | POST | `/sua-san-pham` | Cập nhật sản phẩm |
| 9 | Xóa | POST | `/xoa-san-pham` | Xóa sản phẩm (chỉ Admin) |
| 10 | Tìm | GET | `/tim-kiem` | Tìm kiếm theo tên/mã/loại |
| 11 | Sắp xếp | GET | `/sap-xep` | Merge Sort trên DSLK |
| 12 | Thống kê | GET | `/thong-ke` | Tổng quan + theo loại |
| 13 | Undo | POST | `/hoan-tac` | Hoàn tác (Stack LIFO) |
| 14 | Redo | POST | `/lam-lai` | Làm lại (Stack LIFO) |
| 15 | Giỏ | POST | `/them-gio-hang` | Thêm vào giỏ (Queue FIFO) |
| 16 | Giỏ | GET | `/xem-gio-hang` | Xem giỏ hàng |
| 17 | Giỏ | POST | `/xoa-gio-hang` | Xóa khỏi giỏ |
| 18 | Giỏ | POST | `/thanh-toan` | Thanh toán toàn bộ |

### Try/except cho 7 thao tác chính (theo barem)

| # | Thao tác | Vị trí | Loại ngoại lệ bắt |
|---|---------|--------|------------------|
| 1 | Thêm | `them_san_pham` | JSONDecodeError, ValueError, Exception |
| 2 | Sửa | `sua_san_pham` | JSONDecodeError, ValueError, Exception |
| 3 | Xóa | `xoa_san_pham` | JSONDecodeError, Exception |
| 4 | Undo | `hoan_tac` | Exception |
| 5 | Redo | `lam_lai` | Exception |
| 6 | Thêm giỏ | `them_vao_gio_hang` | JSONDecodeError, Exception |
| 7 | Thanh toán | `thanh_toan` | Exception |

Ngoài ra, các hàm SQLite trong `ket_noi_sqlite.py` đều dùng try/except/finally để đảm bảo đóng kết nối.
