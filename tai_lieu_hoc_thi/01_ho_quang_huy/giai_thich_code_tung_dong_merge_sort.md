# GIẢI THÍCH TỪNG DÒNG CODE MERGE SORT
*(Dùng để học thuộc và trả lời Giảng Viên khi bảo vệ)*

---

## 1. Hàm `_chia_doi(self)`
Mục đích: Tìm điểm chính giữa của danh sách liên kết để cắt nó ra làm 2 nửa. (Dùng kỹ thuật 2 con trỏ: Nhanh và Chậm).

```python
def _chia_doi(self):
```
- Khai báo hàm `_chia_doi`. Chỉ nhận tham số `self` vì nó tự xử lý chính danh sách hiện tại.

```python
    con_tro_cham = self.head
    con_tro_nhanh = self.head
```
- Khởi tạo 2 con trỏ cùng xuất phát từ Node đầu tiên (`self.head`) của danh sách. `con_tro_cham` (rùa) sẽ đi 1 bước, `con_tro_nhanh` (thỏ) sẽ đi 2 bước.

```python
    while con_tro_nhanh.next is not None and con_tro_nhanh.next.next is not None:
```
- Vòng lặp `while` chạy liên tục CHỈ KHI: 
  - `con_tro_nhanh.next` tồn tại (chưa tới phần tử cuối).
  - `con_tro_nhanh.next.next` tồn tại (bảo đảm nó có thể nhảy 2 bước mà không bị lỗi Null Pointer).

```python
        con_tro_cham = con_tro_cham.next
```
- Trong vòng lặp: Con trỏ chậm lết đi 1 Node (giống như Rùa đi 1 bước).

```python
        con_tro_nhanh = con_tro_nhanh.next.next
```
- Trong vòng lặp: Con trỏ nhanh nhảy cóc qua 2 Node (giống như Thỏ nhảy 2 bước).
- *Kết quả khi vòng lặp kết thúc: Con trỏ nhanh chạm đích (cuối danh sách), thì con trỏ chậm chắc chắn đang nằm đúng ở CHÍNH GIỮA.*

```python
    nua_dau = self.head
```
- Bắt đầu thực hiện thao tác CẮT đứt danh sách. Đặt biến `nua_dau` trỏ vào điểm đầu tiên của danh sách.

```python
    nua_sau = con_tro_cham.next
```
- Đặt biến `nua_sau` trỏ vào Node ngay phía sau `con_tro_cham` (Node đầu tiên của nửa thứ hai).

```python
    con_tro_cham.next = None
```
- **Cắt đứt liên kết tiến:** Cho `next` của con trỏ chậm trỏ vào `None`. (Chính thức tách nửa đầu ra khỏi nửa sau).

```python
    if nua_sau is not None:
        nua_sau.truoc = None
```
- **Cắt đứt liên kết lùi:** Nếu nửa sau có tồn tại, thì cho con trỏ lùi (`truoc`) của nó trỏ vào `None` (vì giờ nó đã thành Head của 1 danh sách mới, không còn dính líu gì tới nửa đầu nữa).

```python
    return (nua_dau, nua_sau)
```
- Trả về 2 mảnh (nửa đầu, nửa sau) cho hàm khác sử dụng.


---

## 2. Hàm `_tron(self, ds_a, ds_b, tieu_chi)`
Mục đích: Gộp 2 danh sách `ds_a` và `ds_b` (đã được sắp xếp sẵn) thành 1 danh sách kết quả hoàn chỉnh mà vẫn giữ thứ tự tăng dần.

```python
def _tron(self, ds_a, ds_b, tieu_chi):
```
- Nhận vào danh sách trái (`ds_a`), danh sách phải (`ds_b`), và tiêu chí (ví dụ: 'gia_ban').

```python
    node_tam = Node(None)
    hien_tai = node_tam
```
- Tạo một `node_tam` (Dummy Node / Node giả) không có giá trị. Nó có tác dụng làm "chiếc mỏ neo" ban đầu để dễ dàng nối các Node kết quả phía sau mà không cần quan tâm trường hợp Head bị rỗng.
- `hien_tai` là con trỏ để xây dựng dần danh sách kết quả.

```python
    node_a = ds_a.head
    node_b = ds_b.head
```
- Đặt 2 con trỏ `node_a` và `node_b` đứng ở đầu 2 danh sách A và B để chuẩn bị đọ sức (so sánh).

```python
    while node_a is not None and node_b is not None:
```
- Lặp liên tục cho đến khi 1 trong 2 danh sách bị hết phần tử. (Giống việc so sánh lấy học sinh nhỏ con nhất ra xếp hàng, vòng lặp dừng khi 1 trong 2 hàng đã trống trơn).

```python
        gia_tri_a = self._lay_gia_tri(node_a.data, tieu_chi)
        gia_tri_b = self._lay_gia_tri(node_b.data, tieu_chi)
```
- Trích xuất giá trị thực sự của quyển sách dựa trên `tieu_chi` (ví dụ lấy `gia_ban` ra) để chuẩn bị so sánh.

```python
        if gia_tri_a <= gia_tri_b:
            hien_tai.next = node_a
            node_a.truoc = hien_tai
            node_a = node_a.next
```
- Nếu sách bên A rẻ hơn hoặc bằng bên B:
  - Cho mỏ neo `hien_tai.next` móc vào `node_a`.
  - Nối liên kết ngược `node_a.truoc` về lại `hien_tai` (bởi vì đây là danh sách liên kết kép).
  - Tịnh tiến `node_a` lên 1 bước để xét cuốn sách tiếp theo trong hàng A.

```python
        else:
            hien_tai.next = node_b
            node_b.truoc = hien_tai
            node_b = node_b.next
```
- Tương tự như trên nhưng áp dụng nếu sách bên B rẻ hơn. Ta nối `node_b` vào kết quả và tịnh tiến `node_b` lên.

```python
        hien_tai = hien_tai.next
```
- Tịnh tiến con trỏ kết quả (`hien_tai`) lên 1 bước để đón Node tiếp theo ở vòng lặp sau.

```python
    if node_a is not None:
        hien_tai.next = node_a
        node_a.truoc = hien_tai
        self.cuoi = ds_a.cuoi
```
- Thoát khỏi vòng lặp, lúc này chắc chắn 1 hàng đã cạn, 1 hàng còn sót lại. Dòng này hỏi "Hàng A còn dư không?".
- Nếu còn: Nối TOÀN BỘ phần dư của hàng A vào đuôi kết quả. Cập nhật `self.cuoi` bằng với cái đuôi của danh sách A.

```python
    if node_b is not None:
        hien_tai.next = node_b
        node_b.truoc = hien_tai
        self.cuoi = ds_b.cuoi
```
- Hỏi "Hàng B còn dư không?". Nếu còn thì nối TOÀN BỘ phần dư của hàng B vào cuối kết quả. Cập nhật `self.cuoi` bằng đuôi của B.

```python
    self.head = node_tam.next
    if self.head is not None:
        self.head.truoc = None
```
- Cuối cùng, vứt bỏ chiếc `node_tam` (mỏ neo giả) đi. Lấy Node thật ngay sau mỏ neo (`node_tam.next`) làm `self.head` chính thức của danh sách. 
- Ngắt kết nối `truoc` của `self.head` về `None` (vì nó đã là Node đầu đàn).


---

## 3. Hàm `sap_xep_tron(self, tieu_chi='gia_ban')`
Mục đích: Hàm chính để gọi Đệ Quy, thực hiện việc chia nhỏ danh sách ra liên tục rồi ráp lại bằng hàm `_tron`.

```python
def sap_xep_tron(self, tieu_chi='gia_ban'):
```
- Khai báo hàm, tiêu chí mặc định nếu không truyền vào sẽ là sắp xếp theo Giá Bán.

```python
    if self.head is None or self.head.next is None:
        return
```
- ĐIỀU KIỆN DỪNG CỦA ĐỆ QUY: Nếu danh sách rỗng (0 phần tử) hoặc chỉ có 1 Node duy nhất, thì hiển nhiên là nó đã được sắp xếp sẵn. Không cần làm gì cả, `return` thoát hàm ngay lập tức.

```python
    nua_dau, nua_sau = self._chia_doi()
```
- Gọi hàm Cắt Đôi (ở mục 1), lấy ra điểm đầu của 2 nửa danh sách.

```python
    ds_nua_dau = DoublyLinkedList()
    ds_nua_dau.head = nua_dau
    node_cuoi_dau = nua_dau
    while node_cuoi_dau.next is not None:
        node_cuoi_dau = node_cuoi_dau.next
    ds_nua_dau.cuoi = node_cuoi_dau
    ds_nua_dau.so_luong = self._dem_node(nua_dau)
```
- Biến `nua_dau` lúc nãy chỉ là 1 Node. Muốn dùng được các hàm của danh sách, ta phải bọc nó vào thành một đối tượng `DoublyLinkedList` hoàn chỉnh tên là `ds_nua_dau`.
- Vòng lặp `while` có tác dụng chạy từ đầu tới cuối để tìm xem Node cuối cùng là thằng nào, rồi gán cho thuộc tính `ds_nua_dau.cuoi`. Tính luôn `so_luong`.

```python
    ds_nua_sau = DoublyLinkedList()
    # (Đoạn này giống hệt đoạn trên, bọc nua_sau vào đối tượng ds_nua_sau)
```
- Khởi tạo tương tự để có danh sách thứ 2 là `ds_nua_sau`.

```python
    ds_nua_dau.sap_xep_tron(tieu_chi)
    ds_nua_sau.sap_xep_tron(tieu_chi)
```
- TỰ GỌI LẠI CHÍNH MÌNH (ĐỆ QUY): Ép nửa đầu và nửa sau tự phân thân tiếp tục chia nhỏ bản thân chúng ra, chia đến khi nào về còn 1 phần tử (đụng điều kiện dừng ở trên) thì thôi.

```python
    self._tron(ds_nua_dau, ds_nua_sau, tieu_chi)
```
- Sau khi đã chia nát bét ra, và đệ quy bắt đầu thu hồi lại, ta gọi hàm `_tron` (ở mục 2) để Gộp các nửa đó lại vào biến `self` (tức là biến danh sách tổng ban đầu) với thứ tự hoàn chỉnh. Tới đây là sắp xếp thành công!
