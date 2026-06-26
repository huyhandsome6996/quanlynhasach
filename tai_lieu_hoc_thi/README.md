# 📚 Tài liệu học thi — Đồ án Quản lý Cửa hàng Sách

Tài liệu ôn thi trực quan (HTML + CSS + JavaScript) cho 3 thành viên nhóm.

Đồ án dùng **Django + HTML/CSS/JS** (không còn PyQt6). Mỗi file học liệu có nhãn màu
cho biết ai phụ trách phần nào:

- 🟢 <span style="background:#047857;color:white;padding:2px 8px;border-radius:8px;font-weight:bold;">HUY</span> — Hồ Quang Huy (trưởng nhóm, phần khó)
- 🔵 <span style="background:#1D4ED8;color:white;padding:2px 8px;border-radius:8px;font-weight:bold;">NGỌ</span> — Bùi Gia Ngọ (OOP + SQLite + phân quyền)
- 🟠 <span style="background:#C2410C;color:white;padding:2px 8px;border-radius:8px;font-weight:bold;">TÚ</span> — Phan Anh Tú (Stack/Queue + HTML/JS)

## 📂 Cấu trúc

```
tai_lieu_hoc_thi/
├── README.md                          ← File này
├── highlight.js                       ← (chung) Syntax highlighter Python (VSCode Dark+)
├── 01_ho_quang_huy/                   ← Của Hồ Quang Huy
│   ├── index.html                       Mở file này bằng trình duyệt
│   ├── style.css                        CSS đẹp + bảng màu VSCode Dark+
│   ├── highlight.js                     Tô màu code Python (offline)
│   └── app.js                           JavaScript tương tác
├── 02_bui_gia_ngo/                    ← Của Bùi Gia Ngọ
│   ├── index.html
│   ├── style.css
│   ├── highlight.js
│   └── app.js
└── 03_phan_anh_tu/                    ← Của Phan Anh Tú
    ├── index.html
    ├── style.css
    ├── highlight.js
    └── app.js
```

## ▶️ Cách mở tài liệu

1. Tải repo về máy (hoặc `git pull` nếu đã clone)
2. Mở thư mục `tai_lieu_hoc_thi/<tên bạn>/`
3. **Click đúp vào file `index.html`** — sẽ mở bằng trình duyệt (Chrome/Edge/Firefox)
4. Đọc lý thuyết, xem mô phỏng động, làm quiz kiểm tra

## 🎯 Nội dung mỗi folder

| Folder | Người | Chủ đề ôn thi | File code phụ trách |
|--------|-------|---------------|---------------------|
| `01_ho_quang_huy/` | Huy 🟢 | DSLK đôi + Merge Sort + Django Views + URL routes + Trang chủ HTML + Undo/Redo | `danh_sach_lien_ket.py`, `xu_ly_yeu_cau.py`, `duong_dan.py`, `trang_chu.html` |
| `02_bui_gia_ngo/`  | Ngọ 🔵 | Stack + SQLite CRUD + Đa hình OOP + Phân quyền + Test case | `lop_doi_tuong.py`, `ket_noi_sqlite.py`, `nguoi_dung.py`, `dang_nhap.html` |
| `03_phan_anh_tu/`  | Tú 🟠  | OOP Class + Đa hình + Queue FIFO + HTML partials + JavaScript frontend | `cau_truc_du_lieu.py`, `undo_redo_gio_hang.py`, `thanh_phan/*.html`, `ma_lenh/*.js` |

## 📊 Bảng phân chia công việc chi tiết

| Thành viên | File phụ trách | Vai trò |
|------------|----------------|---------|
| 🟢 Huy | `danh_sach_lien_ket.py` | DSLK đôi + Merge Sort (phần khó nhất) |
| 🟢 Huy | `xu_ly_yeu_cau.py` | Django Views + 17 API endpoints (930 dòng) |
| 🟢 Huy | `duong_dan.py` | Điều hướng URL |
| 🟢 Huy | `trang_chu.html` | Trang chủ HTML chính |
| 🔵 Ngọ | `lop_doi_tuong.py` | 5 lớp OOP (kế thừa + đa hình) |
| 🔵 Ngọ | `ket_noi_sqlite.py` | SQLite CRUD + try/except/finally |
| 🔵 Ngọ | `nguoi_dung.py` | Lớp NguoiDung + phân quyền Admin/NV |
| 🔵 Ngọ | `dang_nhap.html` | Trang đăng nhập HTML |
| 🟠 Tú | `cau_truc_du_lieu.py` | Stack (LIFO) + Queue (FIFO) |
| 🟠 Tú | `undo_redo_gio_hang.py` | Undo/Redo + Giỏ hàng |
| 🟠 Tú | `thanh_phan/*.html` | 5 HTML partials (header, toolbar, table, form, footer) |
| 🟠 Tú | `ma_lenh/*.js` | 2 file JavaScript (gọi API + tương tác) |

## 💡 Nguyên tắc học

1. **Đọc lý thuyết** trước (có hình ảnh + ví dụ đời thường)
2. **Mô phỏng tương tác** để hiểu cách hoạt động (bấm nút, xem animation)
3. **Đọc code thực tế** trong đồ án + xem giải thích từng dòng
4. **Làm quiz** ở cuối mỗi chương để kiểm tra
5. **Mở file Python/HTML/JS tương ứng** trong `du_an_cua_hang_sach/` để đối chiếu

## 🔄 Đổi mới so với bản cũ

Bản cũ dạy PyQt6 — đã **xoá toàn bộ** phần PyQt6 và thay bằng nội dung Django + HTML/CSS/JS:

| Bài cũ (PyQt6) | Bài mới (Django) |
|----------------|------------------|
| Bài 3: PyQt6 cơ bản (QLabel, QLineEdit, QPushButton...) | Bài 3: Django Views (`xu_ly_yeu_cau.py`) |
| Bài 4: `main_window.py` (QMainWindow, layouts) | Bài 4: URL routes + `trang_chu.html` |
| Bài 4 (Tú): PyQt6 Dialogs (QDialog) | Bài 4 (Tú): HTML partials + JavaScript |

## 📌 Lưu ý

- Vì code 100% tiếng Việt nên tài liệu cũng tiếng Việt
- Mô phỏng dùng vanilla JS (không framework) để dễ đọc
- File HTML chạy offline, không cần internet
- **Code Python được tô màu giống y hệt VSCode Dark+** (xanh dương cho `def`/`class`/`if`, cam cho string, xanh lá cho comment, vàng cho tên hàm, v.v.) bằng script `highlight.js` tự viết
- Mỗi khối code có **nút "📋 Sao chép"** ở góc trên-phải để copy nhanh
- Badge tên file màu xanh ở góc trên-trái cho biết code nằm trong file nào của đồ án
- Mỗi bài học có **nhãn màu** (🟢 HUY / 🔵 NGỌ / 🟠 TÚ) cho biết ai phụ trách

Chúc 3 bạn thi tốt! 🎓
