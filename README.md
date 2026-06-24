# Hệ thống Quản lý Cửa hàng Sách

Đồ án kiểm tra cuối kì môn **Lập trình Nâng cao**.

Phiên bản giao diện Desktop dùng **PyQt6 + Python** (đã thay thế phiên bản Django).

Xem tài liệu chi tiết tại: [`do_an_pyqt6/README.md`](do_an_pyqt6/README.md)

## Chạy nhanh

```bash
pip install PyQt6
cd do_an_pyqt6
python main.py
```

Tài khoản mẫu:

| Tài khoản | Mật khẩu | Quyền |
|-----------|----------|-------|
| `admin` | `123` | Toàn quyền (xem + thêm + sửa + xóa + giỏ hàng) |
| `nhanvien` | `123` | Hạn chế (không được xóa) |

## Chạy kiểm thử

```bash
cd do_an_pyqt6
python test_app.py
```
