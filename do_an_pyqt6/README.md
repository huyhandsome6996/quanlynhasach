# ĐỒ ÁN PYQT6 - HỆ THỐNG QUẢN LÝ CỬA HÀNG SÁCH

Đồ án môn **Lập trình Nâng cao** - phiên bản Giao diện Desktop (PyQt6).

> **Nguyên tắc:** Code dùng **100% tiếng Việt**, cực kỳ đơn giản, nhiều comment
> giải thích chi tiết, ai cũng đọc được.

---

## 1. Cách chạy chương trình

### Cài đặt thư viện

```bash
pip install PyQt6
```

### Chạy ứng dụng

```bash
cd do_an_pyqt6
python main.py
```

### Chạy kiểm thử (test các cấu trúc dữ liệu)

```bash
cd do_an_pyqt6
python test_app.py
```

---

## 2. Cấu trúc thư mục

```
do_an_pyqt6/
│
├── main.py                       # Điểm bắt đầu chương trình (đăng nhập → vào app)
├── test_app.py                   # File kiểm thử các cấu trúc dữ liệu
│
├── models/                       # Lớp đối tượng + cấu trúc dữ liệu
│   ├── item.py                   # Lớp cha MatHang (có đa hình tinh_gia_ban)
│   ├── subclasses.py             # 5 lớp con: Sach, TapChi, Bao, LuanVan, BanThao
│   ├── linked_list.py            # Danh sách liên kết ĐÔI + Merge Sort
│   ├── ngan_xep.py               # Ngăn xếp (Stack LIFO) - dùng cho Undo/Redo
│   ├── hang_doi.py               # Hàng đợi (Queue FIFO) - dùng cho Giỏ hàng
│   └── nguoi_dung.py             # Phân quyền Admin / Nhân viên
│
├── ui/                           # Giao diện PyQt6
│   ├── main_window.py            # Cửa sổ chính (bảng + nút bấm)
│   ├── dialogs.py                # Hộp thoại Thêm/Sửa sản phẩm
│   ├── hop_thoai_gio_hang.py     # Hộp thoại Giỏ hàng
│   └── hop_thoai_dang_nhap.py    # Màn hình đăng nhập phân quyền
│
└── data/
    └── sqlite_db.py              # Kết nối CSDL SQLite
```

---

## 3. Cấu trúc dữ liệu đã cài đặt

| # | Tên file | Cấu trúc | Đặc điểm | Ứng dụng |
|---|----------|----------|----------|----------|
| 1 | `linked_list.py` | Danh sách liên kết ĐÔI | Mỗi nút trỏ tới nút sau + nút trước | Chứa toàn bộ mặt hàng |
| 2 | `linked_list.py` | Merge Sort | O(n log n) | Sắp xếp theo giá/tên/số lượng |
| 3 | `ngan_xep.py` | Ngăn xếp (Stack LIFO) | Vào sau, ra trước | Undo/Redo |
| 4 | `hang_doi.py` | Hàng đợi (Queue FIFO) | Vào trước, ra trước | Giỏ hàng |
| 5 | `subclasses.py` | Kế thừa OOP | 5 lớp con kế thừa MatHang | Đa hình tinh_gia_ban() |
| 6 | `nguoi_dung.py` | Phân quyền | 2 vai trò: Admin / Nhân viên | Đăng nhập phân quyền |

---

## 4. CÁC TÍNH NĂNG MỞ RỘNG (ĐIỂM CỘNG)

### 4.0. Đăng nhập phân quyền (Admin / Nhân viên)

Khi mở ứng dụng, màn hình **Đăng Nhập** sẽ xuất hiện trước. Có 2 loại tài khoản:

| Tài khoản | Mật khẩu | Quyền |
|-----------|----------|-------|
| `admin` | `123` | Toàn quyền: xem + thêm + sửa + **XÓA** + giỏ hàng |
| `nhanvien` | `123` | Hạn chế: xem + thêm + sửa + giỏ hàng (KHÔNG được XÓA) |

**Chi tiết:**

- Khi đăng nhập bằng **Nhân viên**: nút **🗑️ Xóa Mặt Hàng** bị ẩn.
- Khi đăng nhập bằng **Admin**: thấy được tất cả các nút.
- Bấm nút **🚪 Đăng Xuất** để quay về màn hình đăng nhập đổi tài khoản.
- Tiêu đề cửa sổ luôn hiển thị: `Đăng nhập: <tên> (Admin/Nhân viên)`.

### 4.1. 5 loại mặt hàng (Kế thừa OOP + Đa hình)

Mỗi loại có cách tính giá bán khác nhau (ghi đè `tinh_gia_ban()`):

| Lớp con | Công thức giá bán |
|---------|------------------|
| `Sach` (Sách) | `gia_co_ban × 1.20` (+20%) |
| `TapChi` (Tạp chí) | `gia_co_ban × 0.90` (-10%) |
| `Bao` (Báo) | `gia_co_ban × 1.00` (giữ nguyên) |
| `LuanVan` (Luận văn) | `gia_co_ban × 1.30` (+30%) |
| `BanThao` (Bản thảo) | `gia_co_ban × 1.50` nếu mới / `× 1.20` nếu cũ |

### 4.2. Tìm kiếm nâng cao (Duyệt DSLK)

Tại ô tìm kiếm, có thể chọn tiêu chí:

- **Tất cả**: tìm trong cả mã + tên + loại
- **Theo Tên**: chỉ tìm trong tên
- **Theo Mã**: chỉ tìm trong mã số
- **Theo Loại**: chỉ tìm trong loại mặt hàng (sách/tạp chí/báo/luận văn/bản thảo)

### 4.3. Sắp xếp (Merge Sort trên Linked List)

Có 5 cách sắp xếp:

- Giá bán tăng dần
- Giá bán giảm dần
- Tên A-Z
- Tên Z-A
- Số lượng tồn kho tăng dần

### 4.4. Thống kê (Duyệt DSLK)

Bấm nút **"📊 Xem Thống Kê"** sẽ hiển thị:

- Tổng số mặt hàng khác nhau
- Sản phẩm đắt tiền nhất (dùng `tinh_gia_ban()` - đa hình)
- Sản phẩm rẻ tiền nhất
- **TỔNG GIÁ TRỊ KHO** = Tổng (giá bán × số lượng) của mọi sản phẩm
- Cảnh báo các sản phẩm sắp hết hàng (tồn kho < 5)

### 4.5. Undo/Redo (Stack LIFO)

| Nút | Tác dụng |
|-----|----------|
| **↩️ Hoàn Tác (Undo)** | Hoàn tác thao tác Thêm/Sửa/Xóa gần nhất |
| **↪️ Làm Lại (Redo)** | Làm lại thao tác vừa bị hoàn tác |

**Cách hoạt động:**

- Mỗi lần Thêm/Sửa/Xóa → lưu thao tác đó vào **Stack Undo**.
- Khi bấm **Undo**: lấy 1 thao tác từ Stack Undo → đảo ngược tác dụng → đẩy sang **Stack Redo**.
- Khi bấm **Redo**: lấy 1 thao tác từ Stack Redo → làm lại → đẩy về Stack Undo.
- Khi có thao tác mới → **xóa sạch Stack Redo** (chuỗi redo bị đứt).

### 4.6. Giỏ hàng (Queue FIFO)

| Nút | Tác dụng |
|-----|----------|
| **🛒 Thêm Vào Giỏ** | Thêm sản phẩm đang chọn vào cuối hàng đợi |
| **🛍️ Xem Giỏ Hàng** | Mở hộp thoại giỏ hàng |

**Trong hộp thoại Giỏ Hàng:**

- Bảng hiển thị các món theo thứ tự **FIFO** (vào trước, ra trước).
- Nút **"🗑️ Bỏ Khỏi Giỏ"**: xóa 1 món đang chọn.
- Nút **"💳 Thanh Toán (FIFO)"**:
  - Lấy từng món ra theo thứ tự FIFO.
  - Mỗi món: giảm tồn kho của sản phẩm tương ứng đi 1.
  - Lưu xuống SQLite.
  - Hiển thị tổng tiền.

---

## 5. Luồng dữ liệu tổng thể

```
Người dùng thao tác trên giao diện PyQt6
            ↓
CửaSoChinh (ui/main_window.py) xử lý sự kiện
            ↓
Tác động tới DanhSachLienKetDoi (models/linked_list.py)
            ↓
Lưu thao tác vào NganXep Undo (models/ngan_xep.py)
            ↓
Đồng bộ xuống SQLite (data/sqlite_db.py)
            ↓
Cập nhật lại bảng hiển thị
```

---

## 6. Tiêu chí đánh giá

| Tiêu chí | Đáp ứng |
|----------|---------|
| Cấu trúc dữ liệu (30%) | ✅ Danh sách liên kết đôi + Stack + Queue (tự cài đặt 100%) |
| Tư duy OOP (20%) | ✅ 5 lớp con kế thừa + đa hình `tinh_gia_ban()` |
| Giao diện (20%) | ✅ PyQt6 desktop, có form, bắt lỗi nhập liệu |
| Thuật toán (15%) | ✅ Merge Sort + tìm kiếm tuyến tính trên Linked List |
| Xử lý File/Ngoại lệ (15%) | ✅ SQLite CRUD + try/except đầy đủ |
| **Tính năng mở rộng** | ✅ Đủ 6/6 (Đăng nhập phân quyền, Undo/Redo, Giỏ hàng, Thống kê, Tìm kiếm, 5 loại) |
