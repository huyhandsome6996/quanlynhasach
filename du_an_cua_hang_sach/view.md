# TỔNG HỢP 20 HÀM TRONG `xu_ly_yeu_cau.py`

File `xu_ly_yeu_cau.py` đóng vai trò là "Bộ điều khiển" (Controller / View) của toàn bộ hệ thống cửa hàng sách. Dưới đây là phân tích chi tiết từng hàm, tác dụng, và cách mà JavaScript (Frontend) sử dụng chúng để tạo ra sự tương tác mượt mà.

---

### 1. `khoi_tao_danh_sach()`
- **Tác dụng:** Nạp dữ liệu ban đầu từ cơ sở dữ liệu lên RAM.
- **Cơ chế:** Khởi tạo Danh sách liên kết đôi, Hàng đợi (Giỏ hàng) và Ngăn xếp (Undo/Redo). Truy vấn SQLite lấy sách nạp vào danh sách liên kết.
- **Tác động:** Đưa dữ liệu sẵn sàng cho hệ thống hoạt động.
- **Đầu ra:** Không có.
- **Tương tác JS:** Chạy ngầm phía Server, JS không gọi trực tiếp.

### 2. `trang_chu(request)`
- **Tác dụng:** Hiển thị màn hình chính của ứng dụng.
- **Cơ chế:** Kiểm tra `session`, nếu người dùng chưa đăng nhập thì tự động đá văng sang trang đăng nhập.
- **Tác động:** Cung cấp giao diện `trang_chu.html` cho người dùng.
- **Đầu ra:** File HTML.
- **Tương tác JS:** Cung cấp khung sườn HTML để JS có thể chèn bảng, nút bấm vào.

### 3. `trang_dang_nhap(request)`
- **Tác dụng:** Hiển thị màn hình đăng nhập.
- **Cơ chế:** Render tệp `dang_nhap.html`. 
- **Đầu ra:** File HTML.
- **Tương tác JS:** Cung cấp ô nhập liệu và nút bấm để JS gắn sự kiện Submit.

### 4. `xu_ly_dang_nhap(request)`
- **Tác dụng:** Xác thực tài khoản của người dùng.
- **Cơ chế:** Lấy `ten_dang_nhap` và `mat_khau` từ yêu cầu. So sánh với cơ sở dữ liệu. Nếu khớp, lưu `session`.
- **Tác động:** Cấp quyền sử dụng ứng dụng.
- **Đầu ra:** Chuỗi JSON báo thành công hoặc thất bại (`400`, `401`).
- **Tương tác JS:** JS dùng hàm `fetch()` (phương thức POST) để gửi tài khoản mật khẩu lên hàm này mà không cần tải lại trang.

### 5. `xu_ly_dang_xuat(request)`
- **Tác dụng:** Đăng xuất người dùng.
- **Cơ chế:** Xóa sạch `session` (phiên đăng nhập).
- **Tác động:** Tước quyền sử dụng ứng dụng.
- **Đầu ra:** Chuyển hướng (Redirect) về trang đăng nhập.
- **Tương tác JS:** JS gọi hàm này khi người dùng bấm nút Đăng xuất.

### 6. `thong_tin_nguoi_dung(request)`
- **Tác dụng:** Lấy thông tin cá nhân của người dùng hiện tại.
- **Cơ chế:** Đọc dữ liệu từ `request.session`.
- **Đầu ra:** Chuỗi JSON chứa tên, vai trò (Admin hay Nhân viên).
- **Tương tác JS:** JS (AJAX) sẽ gọi hàm này lúc vừa tải trang xong để in dòng chữ "Xin chào, [Tên]" lên góc phải màn hình.

### 7. `la_admin(request)`
- **Tác dụng:** Bảo vệ hệ thống khỏi truy cập trái phép.
- **Cơ chế:** Hàm tiện ích kiểm tra xem `vai_tro == 'admin'` hay không.
- **Đầu ra:** `True` hoặc `False`.
- **Tương tác JS:** Dùng nội bộ ở Server để chặn JS của nhân viên gửi lệnh xóa sản phẩm.

### 8. `lay_danh_sach(request)`
- **Tác dụng:** Lấy toàn bộ hàng hóa trong cửa hàng.
- **Cơ chế:** Quét từ đầu đến cuối Danh sách liên kết đôi, chuyển đổi thành danh sách từ điển (Dict).
- **Tác động:** Trả dữ liệu thực tế về cho Frontend.
- **Đầu ra:** JSON danh sách mảng chứa các món đồ.
- **Tương tác JS:** JS dùng hàm `fetch(GET)` lấy cái JSON này về rồi vòng lặp `for` để vẽ ra từng dòng <tr> trong bảng `bang_du_lieu.html`.

### 9. `them_san_pham(request)`
- **Tác dụng:** Thêm mặt hàng mới vào cửa hàng.
- **Cơ chế:** Phân loại món hàng (Sách, Tạp chí...), tạo Đối tượng tương ứng, thêm vào cuối Danh sách liên kết, thêm vào SQLite, và đánh dấu vào ngăn xếp Undo.
- **Đầu ra:** JSON thông báo thành công.
- **Tương tác JS:** JS thu thập dữ liệu từ Form thêm mới, đóng gói thành JSON và dùng `POST` đẩy vào hàm này.

### 10. `sua_san_pham(request)`
- **Tác dụng:** Cập nhật thông tin hàng hóa.
- **Cơ chế:** Tìm món hàng theo Mã Số, dùng hàm `setattr` để thay giá trị cũ bằng giá trị mới.
- **Tác động:** Đổi thông tin trên RAM và lưu vào SQLite. Cất bản cũ vào Undo.
- **Đầu ra:** JSON thông báo.
- **Tương tác JS:** Bấm nút "Sửa" trên màn hình, JS hiện popup, người dùng gõ giá mới, JS lấy giá mới đó gửi `POST` vào đây.

### 11. `xoa_san_pham(request)`
- **Tác dụng:** Xóa hẳn một món hàng. (Chỉ Admin).
- **Cơ chế:** Cắt đứt liên kết Node (`truoc`, `next`) để văng món đó ra khỏi Danh sách liên kết. Xóa trong CSDL.
- **Đầu ra:** JSON trạng thái xóa.
- **Tương tác JS:** JS gắn nút Xóa màu đỏ ở mỗi dòng. Bấm vào là JS gửi Mã số qua đây để triệt tiêu.

### 12. `tim_kiem_san_pham(request)`
- **Tác dụng:** Tìm món hàng theo tên, mã hoặc loại.
- **Cơ chế:** Duyệt vòng lặp danh sách liên kết, dùng toán tử `in` để dò chuỗi khớp với từ khóa người dùng gõ.
- **Đầu ra:** JSON danh sách các món tìm được.
- **Tương tác JS:** Mỗi khi bạn gõ một chữ vào ô Tìm kiếm, JS sẽ gửi chữ đó lên hàm này để lấy kết quả mới nhất về hiển thị.

### 13. `sap_xep_danh_sach(request)`
- **Tác dụng:** Sắp xếp danh sách (ví dụ: giá từ thấp đến cao).
- **Cơ chế:** Dùng thuật toán đệ quy Trộn (Merge Sort). Chặt danh sách làm đôi liên tục rồi ghép lại theo đúng thứ tự.
- **Đầu ra:** JSON danh sách đã được sắp xếp thẳng tắp.
- **Tương tác JS:** Khi bạn bấm vào tiêu đề cột (ví dụ bấm cột 'Giá bán'), JS sẽ gửi yêu cầu `GET /sap-xep?tieu_chi=gia_ban` cho hàm này.

### 14. `lay_thong_ke(request)`
- **Tác dụng:** Tính toán tổng số lượng, món đắt nhất, mặt hàng sắp hết.
- **Cơ chế:** Vòng lặp duyệt toàn bộ danh sách, cộng dồn tổng giá trị kho.
- **Đầu ra:** JSON cục thống kê.
- **Tương tác JS:** JS lấy cục JSON này để vẽ ra các ô Thống kê hoặc biểu đồ trên màn hình.

### 15. `hoan_tac(request)`
- **Tác dụng:** Nút Undo (Ctrl + Z).
- **Cơ chế:** Lấy lệnh gần nhất trong ngăn xếp Undo Stack. Nếu lệnh đó là "Thêm", thì nó tiến hành "Xóa" lại. Đẩy lệnh đó qua Redo Stack.
- **Đầu ra:** JSON báo cáo đã lùi lại 1 bước.
- **Tương tác JS:** JS gọi hàm này khi người dùng bấm nút ↩️ Hoàn tác.

### 16. `lam_lai(request)`
- **Tác dụng:** Nút Redo (Ctrl + Y).
- **Cơ chế:** Lấy lệnh trên đỉnh Redo Stack, làm lại i chang thao tác đó, rồi đẩy ngược về Undo Stack.
- **Tương tác JS:** JS gọi khi bấm nút ↪️ Làm lại.

### 17. `them_vao_gio_hang(request)`
- **Tác dụng:** Cho món hàng vào Hàng đợi (Queue) Giỏ hàng.
- **Cơ chế:** Đóng gói thông tin món hàng thành Dict. Cho vào CUỐI hàng (Enqueue).
- **Tác động:** Tăng số lượng món trong giỏ.
- **Đầu ra:** JSON thông báo thành công.
- **Tương tác JS:** Bấm nút "Mua", JS sẽ kêu hàm này đem hàng vô giỏ.

### 18. `xem_gio_hang(request)`
- **Tác dụng:** Hiển thị bên trong Giỏ hàng đang có gì.
- **Cơ chế:** Chạy hàm Peek All của hàng đợi, chuyển thành dạng mảng (Array).
- **Đầu ra:** JSON danh sách giỏ hàng.
- **Tương tác JS:** JS dùng cái này để liên tục làm mới giao diện cái bảng Giỏ hàng bên góc phải màn hình.

### 19. `xoa_khoi_gio_hang(request)`
- **Tác dụng:** Khách đổi ý, vứt một món ra khỏi giỏ.
- **Cơ chế:** Duyệt hàng đợi, rút cái node đó ra, nối đuôi lại với nhau.
- **Tương tác JS:** Bấm icon thùng rác bên trong giỏ hàng, JS gửi mã qua đây xử lý.

### 20. `thanh_toan(request)`
- **Tác dụng:** Thu tiền, xuất hóa đơn.
- **Cơ chế:** Dùng nguyên tắc FIFO của hàng đợi (Queue). Lấy từng món từ ĐẦU hàng ra (Dequeue), cộng tiền. Làm đến khi giỏ hàng trống trơn.
- **Tác động:** Xuất Bill (Hóa đơn), làm sạch hàng đợi.
- **Đầu ra:** JSON in ra số lượng món và tổng tiền cần trả.
- **Tương tác JS:** Khách chốt đơn bấm Thanh toán. JS đợi kết quả JSON và bật lên cái bảng thông báo: "Đã thanh toán thành công 3 mặt hàng, tổng 500.000đ".
