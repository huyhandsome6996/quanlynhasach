# Cấu trúc Hệ thống Quản lý Nhà Sách - Giải thích Chi tiết

Tài liệu này giải thích chi tiết cấu trúc thư mục, các tệp tin, ý nghĩa của từng Class (Lớp) và Function (Hàm) trong hệ thống quản lý nhà sách của bạn. Tài liệu này được thiết kế đặc biệt để giúp bạn nắm vững kiến thức cho môn **Lập trình nâng cao** (chú trọng vào Thuật toán và Lập trình Hướng Đối Tượng - OOP).

---

## 🌳 Cây cấu trúc thư mục (Project Tree)

```text
du_an_cua_hang_sach/
├── cau_hinh_he_thong/       # Cấu hình gốc của Django (settings, wsgi, asgi)
├── giao_dien/               # Chứa các tệp HTML giao diện (Template)
│   └── thanh_phan/          # Các tệp HTML được tách nhỏ (header, footer, table...)
├── tep_tinh/                # Chứa CSS (hinh_thuc) và Javascript (ma_lenh)
└── ung_dung_giao_tiep/      # THƯ MỤC BACKEND CHÍNH XỬ LÝ LOGIC
    ├── duong_dan.py         # Định tuyến URL (URL Routing)
    ├── xu_ly_yeu_cau.py     # Nơi tiếp nhận và xử lý yêu cầu từ Web (Views)
    └── loi_thuat_toan/      # LÕI THUẬT TOÁN (Algorithms & OOP)
        ├── lop_doi_tuong.py         # Định nghĩa các Class sản phẩm (Kế thừa, Đa hình)
        ├── danh_sach_lien_ket.py    # Thuật toán Danh sách liên kết đôi (Doubly Linked List)
        ├── ket_noi_sqlite.py        # Logic truy xuất Cơ sở dữ liệu
                └── kiem_thu.py              # Tệp chạy thử nghiệm thuật toán ngoài môi trường Web
```

---

## 📂 Chi tiết thư mục: `ung_dung_giao_tiep/loi_thuat_toan/`
Đây là phần cốt lõi nhất của dự án, chứa toàn bộ kiến thức về cấu trúc dữ liệu và thuật toán.

### 1. Tệp `lop_doi_tuong.py` (Tính Kế Thừa và Đa Hình)
Tệp này định nghĩa các thực thể sản phẩm của cửa hàng sách dựa trên các nguyên lý OOP.

*   **`class MatHang`**: Lớp cha (Base Class)
    *   **Ý nghĩa:** Chứa các thuộc tính chung mà mọi sản phẩm đều có (Mã số, Tên, Giá cơ bản, Tồn kho).
    *   **`def __init__(...)`**: Hàm khởi tạo (Constructor) để gán giá trị ban đầu cho đối tượng.
    *   **`def tinh_gia_ban(self)`**: Hàm ảo (có thể bị ghi đè). Ở lớp cha, giá bán mặc định bằng giá cơ bản.
    *   **`def to_dict(self)`**: Hàm chuyển đổi đối tượng thành dạng Dictionary (chuẩn bị dữ liệu để gửi về giao diện web dưới dạng JSON).

*   **`class Sach(MatHang)`**: Lớp con kế thừa từ Lớp `MatHang`
    *   **Ý nghĩa:** Kế thừa mọi thứ từ `MatHang` nhưng có thêm thuộc tính riêng: `tac_gia` (Tác giả) và `nha_xuat_ban`.
    *   **`def __init__(...)`**: Sử dụng `super().__init__(...)` để gọi hàm khởi tạo của lớp cha, sau đó khởi tạo các thuộc tính riêng của lớp con.
    *   **`def tinh_gia_ban(self)`**: Ghi đè (Override - tính Đa hình). Sách sẽ được tính giá bán = giá cơ bản + 10% thuế.

*   **`class TapChi(MatHang)`** và **`class BaoGiay(MatHang)`**: Các lớp con khác
    *   Tương tự như lớp Sách, nhưng chứa các thuộc tính riêng (như `so_phat_hanh`, `ngay_xuat_ban`). Giá bán của Tạp chí có thể được thiết lập khác (ví dụ: +5% thuế).

### 2. Tệp `danh_sach_lien_ket.py` (Cấu trúc dữ liệu & Thuật toán)
Tệp này tự xây dựng lại cấu trúc dữ liệu Danh sách liên kết đôi (Doubly Linked List) trên RAM mà không dùng List có sẵn của Python.

*   **`class Node`**: Lớp Mắt Xích
    *   **Ý nghĩa:** Đại diện cho 1 phần tử trong danh sách.
    *   **`data`**: Chứa dữ liệu thực tế (chính là 1 đối tượng `MatHang` đã tạo ở trên).
    *   **`truoc` (prev)**: Con trỏ trỏ về Node đứng trước nó.
    *   **`next`**: Con trỏ trỏ đến Node đứng sau nó.

*   **`class DoublyLinkedList`**: Lớp quản lý cấu trúc dữ liệu
    *   **`def __init__(self)`**: Khởi tạo danh sách rỗng, gồm `head` (đầu), `tail` (đuôi) và `so_luong` (số lượng phần tử).
    *   **`def them_vao_cuoi(self, data)`**:
        *   Tạo ra một `Node` mới chứa dữ liệu.
        *   Nếu danh sách trống (`head == None`), Node mới chính là head và tail.
        *   Nếu không trống, móc nối `next` của tail hiện tại vào Node mới, và `truoc` của Node mới trỏ ngược lại tail. Cuối cùng cập nhật lại tail.
    *   **`def xoa_theo_ma(self, ma_so)`**:
        *   Thuật toán duyệt (Traverse): Bắt đầu từ `head`, dùng vòng lặp `while` duyệt qua từng Node.
        *   Nếu tìm thấy `Node.data.ma_so == ma_so`, tiến hành móc nối lại con trỏ `truoc` và `next` của 2 Node xung quanh để cô lập Node cần xóa, rồi giảm `so_luong`.
    *   **`def lay_tat_ca(self)`**: Duyệt từ đầu đến cuối danh sách, gọi hàm `to_dict()` của mỗi sản phẩm và gộp vào một mảng để trả về cho Frontend.
    *   **`def kiem_tra_ton_tai(self, ma_so)`**: Duyệt tuần tự để tìm kiếm (Linear Search) xem mã sản phẩm đã tồn tại hay chưa.

### 3. Tệp `ket_noi_sqlite.py`
Xử lý lưu trữ dữ liệu vĩnh viễn (Persistence) để dữ liệu không bị mất khi tắt server.

*   **`def lay_ket_noi()`**: Thiết lập kết nối an toàn với cơ sở dữ liệu `db.sqlite3`.
*   **`def tai_du_lieu(danh_sach_lien_ket)`**:
    *   Mở kết nối DB, thực hiện câu lệnh `SELECT * FROM mat_hang`.
    *   Khởi tạo các đối tượng OOP tương ứng (`Sach`, `TapChi`...) dựa vào cột `loai_hang`.
    *   Dùng hàm `them_vao_cuoi()` để đẩy các đối tượng này vào danh sách liên kết trên RAM.
*   **`def them_mat_hang(mat_hang)`** / **`def xoa_mat_hang_db(ma_so)`**: Thực thi các lệnh `INSERT` và `DELETE` trong CSDL.

## 📂 Chi tiết thư mục: `ung_dung_giao_tiep/` (Controller)

### 1. Tệp `xu_ly_yeu_cau.py`
Nơi tiếp nhận các yêu cầu (Request) từ trình duyệt và trả về kết quả (Response).
*   **`Danh_sach_cua_hang = DoublyLinkedList()`**: Khởi tạo biến toàn cục (Global variable) lưu trữ danh sách liên kết duy nhất cho toàn ứng dụng.
*   **`def khoi_tao_danh_sach()`**: Nạp dữ liệu từ DB lên RAM khi server vừa bật.
*   **`def trang_chu(request)`**: Render giao diện `trang_chu.html`.
*   **`def danh_sach(request)`**: Trả về toàn bộ dữ liệu dưới dạng JSON (gọi `lay_tat_ca()`).
*   **`def them_api(request)`**: Tiếp nhận dữ liệu POST, kiểm tra xem mã đã tồn tại chưa (`kiem_tra_ton_tai`). Nếu chưa thì tạo Đối tượng, lưu vào DB và đẩy vào danh sách liên kết.
*   **`def xoa_api(request)`**: Nhận yêu cầu xóa, thực hiện xóa trong RAM (`xoa_theo_ma`) và xóa trong DB (`xoa_mat_hang_db`).

### 2. Tệp `duong_dan.py`
*   Khớp nối đường dẫn trên thanh địa chỉ trình duyệt với hàm tương ứng. 
    *   Ví dụ: người dùng vào `127.0.0.1:8000/api/danh-sach`, hệ thống sẽ gọi hàm `danh_sach(request)` trong `xu_ly_yeu_cau.py`.
