"""
Tệp doc_danh_sach_ui.py — GIAO DIỆN cho chức năng Đọc danh sách sản phẩm
========================================================================

Chứa lớp BangSanPhamUI — tạo bảng Treeview hiển thị danh sách sản phẩm.
Không chứa logic nghiệp vụ — chỉ vẽ widget + cung cấp hàm cập nhật dữ liệu.
"""

import tkinter as tk
from tkinter import ttk


class BangSanPhamUI:
    """
    Bảng dữ liệu sản phẩm dùng Treeview — hiển thị các cột:
    Mã số, Tên, Loại, Giá cơ bản, Tồn kho, Giá bán, Thông tin riêng.
    """

    # Định nghĩa cột của bảng — dùng tuple để gọn.
    COT = ('ma', 'ten', 'loai', 'gia_cb', 'ton', 'gia_ban', 'rieng')

    def __init__(self, parent):
        """
        Tạo bảng Treeview trong parent.

        Tham số:
            parent : widget cha (thường là LabelFrame hoặc Frame).
        """
        # Tạo Treeview với 7 cột, show='headings' để ẩn cột #0 (cây).
        self.tree = ttk.Treeview(parent, columns=self.COT, show='headings', height=15)

        # Định nghĩa header (tiêu đề cột) + căn lề + độ rộng.
        self.tree.heading('ma', text='Mã số')
        self.tree.heading('ten', text='Tên sản phẩm')
        self.tree.heading('loai', text='Loại')
        self.tree.heading('gia_cb', text='Giá cơ bản')
        self.tree.heading('ton', text='Tồn kho')
        self.tree.heading('gia_ban', text='Giá bán (đã tính)')
        self.tree.heading('rieng', text='Thông tin riêng')
        self.tree.column('ma', width=70, anchor='center')
        self.tree.column('ten', width=200)
        self.tree.column('loai', width=80, anchor='center')
        self.tree.column('gia_cb', width=100, anchor='e')
        self.tree.column('ton', width=70, anchor='center')
        self.tree.column('gia_ban', width=110, anchor='e')
        self.tree.column('rieng', width=250)

        # Tạo scrollbar dọc để cuộn danh sách dài.
        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Đặt widget vào parent: tree bên trái, scrollbar bên phải.
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    # ----------------------------------------------------------------
    # CÁC HÀM TIỆN ÍCH CHO ĐIỀU KHIỂN GỌI
    # ----------------------------------------------------------------
    def xoa_tat_ca_dong(self):
        """Xóa toàn bộ dòng trong bảng — dùng trước khi vẽ lại."""
        for item in self.tree.get_children(): # self.tree: là bảng hiển thị dsach
                                              #sản phẩm do (dc tạo bằng công cụ 
                                              #Treeview của tkinter)
                                              #- hàm get_children(): lấy hết con của tree
            self.tree.delete(item) # hàm delete(item): xoá hết item trong tree

    def them_dong(self, sp_dict):
        """
        Thêm 1 dòng vào bảng từ dict sản phẩm.
        -mông má lại dư liệu thô thành dạng đẹp đẽ 

        Tham số:
            sp_dict : dict chứa các key ma_so, ten_san_pham, loai_hang, gia_co_ban, ton_kho, gia_ban, ...
        """
        # Tạo chuỗi "thông tin riêng" theo loại hàng.
        rieng = self._str_truong_rieng(sp_dict)
        # Format giá tiền có dấu phẩy hàng nghìn.
        gia_cb  = f"{sp_dict.get('gia_co_ban', 0):,.0f}"
        gia_ban = f"{sp_dict.get('gia_ban', 0):,.0f}"
        # Insert 1 dòng mới vào cuối bảng.
        self.tree.insert('', 'end', values=(
            sp_dict.get('ma_so', ''),
            sp_dict.get('ten_san_pham', ''),
            sp_dict.get('loai_hang', ''),
            gia_cb,
            sp_dict.get('ton_kho', 0),
            gia_ban,
            rieng
        ))

    def lay_ma_dang_chon(self):
        """
        Trả về mã số của dòng đang được chọn trong bảng.
        Trả về None nếu chưa chọn dòng nào.
        -chỉ lựa chọn các dòng hiện tại trong tree
        """
        selected = self.tree.selection()
        if not selected:
            return None
        # Lấy tuple values của dòng đầu tiên được chọn.
        values = self.tree.item(selected[0], 'values')
        # values[0] là cột "Mã số".
        return values[0]

    # ----------------------------------------------------------------
    # HÀM NỘI BỘ
    # ----------------------------------------------------------------
    def _str_truong_rieng(self, sp):
        """Bổ trợ cho hàm them_dong() dựa trên đặc thù cùa từng loại mặt hàng"""

        """Tạo chuỗi hiển thị thông tin riêng theo loại hàng."""
        loai = sp.get('loai_hang', '')
        # Mỗi loại có các trường riêng khác nhau.
        if loai == 'Sách':
            return f"Tác giả: {sp.get('tac_gia', '')} | NXB: {sp.get('nha_xuat_ban', '')}"
        elif loai == 'Tạp chí':
            return f"Số phát hành: {sp.get('so_phat_hanh', '')}"
        elif loai == 'Báo giấy':
            return f"Ngày XB: {sp.get('ngay_xuat_ban', '')}"
        elif loai == 'Luận văn':
            return f"Tác giả: {sp.get('tac_gia', '')} | Trường: {sp.get('truong_dai_hoc', '')}"
        elif loai == 'Bản thảo':
            return f"Tác giả: {sp.get('tac_gia', '')} | TT: {sp.get('tinh_trang', '')}"
        return ''
