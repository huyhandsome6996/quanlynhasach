import re

CSS_COMMENTS = {
    "display: flex": "Bật chế độ Flexbox (hộp linh hoạt) để sắp xếp các phần tử con",
    "display: grid": "Bật chế độ Grid (lưới) để sắp xếp theo hàng và cột",
    "display: block": "Hiển thị dưới dạng khối (chiếm trọn chiều ngang)",
    "display: none": "Ẩn phần tử này đi hoàn toàn",
    "display: inline-flex": "Flexbox nhưng gọn gàng theo chiều ngang như một dòng chữ",
    "flex-direction: column": "Sắp xếp các phần tử con theo chiều dọc (từ trên xuống)",
    "flex-direction: row": "Sắp xếp các phần tử con theo chiều ngang (trái qua phải)",
    "align-items: center": "Căn giữa các phần tử con theo trục chéo (vd: dọc)",
    "align-items: flex-start": "Căn phần tử con dồn lên trên cùng",
    "align-items: baseline": "Căn ngang bám theo đường chân chữ",
    "justify-content: center": "Căn giữa các phần tử con theo trục chính (vd: ngang)",
    "justify-content: space-between": "Dàn đều: đẩy bám sát 2 bên lề, ở giữa rỗng",
    "justify-content: flex-end": "Dồn tất cả các phần tử con sang bên phải/cuối",
    "gap": "Tạo khoảng trống giữa các phần tử con",
    "margin-top": "Đẩy phần tử khác ra xa ở phía trên",
    "margin-bottom": "Đẩy phần tử khác ra xa ở phía dưới",
    "margin-left": "Đẩy phần tử khác ra xa ở phía trái",
    "margin-right": "Đẩy phần tử khác ra xa ở phía phải",
    "margin": "Căn lề bên ngoài (đẩy các phần tử khác ra xa mình)",
    "padding-top": "Tạo vùng đệm bên trong ở phía trên",
    "padding-bottom": "Tạo vùng đệm bên trong ở phía dưới",
    "padding-left": "Tạo vùng đệm bên trong ở phía trái",
    "padding-right": "Tạo vùng đệm bên trong ở phía phải",
    "padding": "Căn lề bên trong (từ viền vào đến nội dung)",
    "background-color": "Đổ màu nền",
    "background": "Đổ màu nền hoặc hình nền",
    "color": "Đổi màu chữ",
    "font-size": "Kích thước chữ",
    "font-weight": "Độ đậm của chữ (400 mỏng, 500 vừa, 700 đậm)",
    "font-family": "Chọn kiểu dáng font chữ",
    "line-height": "Khoảng cách giữa các dòng chữ (chiều cao dòng)",
    "text-align: center": "Căn giữa chữ",
    "text-align: right": "Căn chữ sang phải",
    "text-align: left": "Căn chữ sang trái",
    "text-transform: uppercase": "Ép tất cả các chữ biến thành in hoa",
    "text-decoration: none": "Xóa gạch chân của đường link",
    "border-radius": "Bo cong các góc của viền",
    "border-bottom": "Kẻ đường viền ở cạnh dưới",
    "border-top": "Kẻ đường viền ở cạnh trên",
    "border-left": "Kẻ đường viền ở cạnh trái",
    "border-right": "Kẻ đường viền ở cạnh phải",
    "border": "Kẻ đường viền xung quanh phần tử",
    "box-shadow": "Đổ bóng cho phần tử (tạo hiệu ứng nổi)",
    "position: relative": "Vị trí tương đối (làm mốc cho phần tử con bám theo)",
    "position: absolute": "Vị trí tuyệt đối (bay lơ lửng, định vị theo phần tử cha)",
    "position: fixed": "Đóng đinh trên màn hình (cuộn chuột vẫn đứng im)",
    "position: sticky": "Bám dính vào cạnh màn hình khi cuộn chuột qua",
    "top": "Định vị khoảng cách từ mép trên cùng",
    "bottom": "Định vị khoảng cách từ mép dưới cùng",
    "left": "Định vị khoảng cách từ mép trái",
    "right": "Định vị khoảng cách từ mép phải",
    "min-width": "Chiều rộng tối thiểu (không thể bóp nhỏ hơn)",
    "max-width": "Chiều rộng tối đa (không thể kéo giãn to hơn)",
    "width": "Chiều rộng của phần tử",
    "min-height": "Chiều cao tối thiểu",
    "max-height": "Chiều cao tối đa",
    "height": "Chiều cao của phần tử",
    "overflow-y: auto": "Tự động hiện thanh cuộn dọc nếu nội dung quá dài",
    "overflow-x: auto": "Tự động hiện thanh cuộn ngang nếu nội dung quá dài",
    "overflow: hidden": "Giấu/Cắt bỏ phần nội dung bị tràn ra ngoài khung",
    "overflow": "Xử lý nội dung bị tràn (ẩn hoặc hiện cuộn)",
    "z-index": "Thứ tự xếp lớp (số to hơn sẽ đè lên thằng số nhỏ)",
    "cursor: pointer": "Đổi biểu tượng chuột thành BÀN TAY khi lướt qua",
    "cursor: not-allowed": "Đổi biểu tượng chuột thành dấu CẤM",
    "transition": "Tạo hiệu ứng chuyển động mượt mà (không bị giật cục)",
    "opacity": "Độ trong suốt (1 là rõ, 0.5 là mờ, 0 là tàng hình)",
    "white-space: nowrap": "Ép chữ không được rớt dòng, phải nằm trên 1 hàng",
    "box-sizing: border-box": "Ép viền và padding gộp vào trong width (chống phình to)",
    "flex-wrap: wrap": "Nếu thiếu chỗ xếp ngang, cho phép rớt xuống hàng dưới",
    "flex: 1": "Tự động giãn ra chiếm hết không gian trống còn lại",
    "outline: none": "Tắt viền sáng mặc định của trình duyệt khi click vào",
    "vertical-align": "Căn chỉnh phần tử theo chiều dọc so với chữ xung quanh",
    "letter-spacing": "Khoảng cách giữa các chữ cái",
    "transform": "Biến đổi hình dạng (phóng to, thu nhỏ, xoay, dịch chuyển)",
}

def add_comments(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        stripped = line.strip()
        # Bỏ qua các dòng trống hoặc dòng đóng mở ngoặc hoặc dòng đã có comment
        if not stripped or stripped.startswith("/*") or stripped.endswith("*/") or stripped in ("}", "{"):
            new_lines.append(line)
            continue
            
        # Tìm xem có thuộc tính nào khớp không
        matched = False
        # Ưu tiên các quy tắc chính xác (chứa cả cặp key-value)
        for key in ["display: flex", "display: grid", "display: block", "display: none", 
                    "display: inline-flex", "flex-direction: column", "flex-direction: row",
                    "align-items: center", "align-items: flex-start", "align-items: baseline",
                    "justify-content: center", "justify-content: space-between", "justify-content: flex-end",
                    "flex-wrap: wrap", "flex: 1", "outline: none", "text-align: center", 
                    "text-align: right", "text-align: left", "position: relative", 
                    "position: absolute", "position: fixed", "position: sticky",
                    "cursor: pointer", "cursor: not-allowed", "white-space: nowrap",
                    "box-sizing: border-box", "overflow-y: auto", "overflow-x: auto", "overflow: hidden",
                    "text-transform: uppercase", "text-decoration: none"]:
            if key in stripped:
                comment = CSS_COMMENTS[key]
                if "/*" not in line:
                    line = line.rstrip() + f" /* {comment} */\n"
                matched = True
                break
        
        if not matched:
            # Nếu không tìm thấy quy tắc chính xác, dò theo tiền tố (như margin, padding)
            prop_name = stripped.split(":")[0].strip()
            if prop_name in CSS_COMMENTS:
                comment = CSS_COMMENTS[prop_name]
                if "/*" not in line:
                    line = line.rstrip() + f" /* {comment} */\n"
        
        new_lines.append(line)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    add_comments("c:/Users/PC/quanlynhasach/du_an_cua_hang_sach/tep_tinh/hinh_thuc/trang_tri.css")
    print("Done")
