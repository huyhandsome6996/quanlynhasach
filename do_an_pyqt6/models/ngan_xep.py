# ================================================================
# 👤 PHỤ TRÁCH: BÙI GIA NGỌ
# ----------------------------------------------------------------
# 📚 KIẾN THỨC CẦN HỌC ĐI THI:
#    1. NGĂN XẾP (STACK) - cấu trúc LIFO: Last In, First Out
#    2. Tưởng tượng như CHỒNG ĐĨA: đĩa để cuối cùng lấy ra trước
#    3. 3 thao tác chính: PUSH (day_vao), POP (lay_ra), PEEK (xem_dinh)
#    4. Ứng dụng: tính năng UNDO/REDO trong phần mềm
#    5. Cài đặt bằng Linked List (mỗi Node có 1 con trỏ duoi)
# ----------------------------------------------------------------
# 📝 NỘI DUNG FILE:
#    Cài đặt NganXep (Stack) bằng con trỏ. Dùng trong main_window.py
#    để tạo 2 Stack: ngan_xep_hoan_tac (Undo) + ngan_xep_lam_lai (Redo).
# ================================================================

# ====================================================================
# NGĂN XẾP (STACK) - Cấu trúc LIFO: Vào sau, ra trước
# --------------------------------------------------------------------
# Tưởng tượng như CHỒNG ĐĨA: đĩa để cuối cùng sẽ được lấy ra trước.
# Ứng dụng: dùng để làm tính năng UNDO/REDO trong phần mềm.
# ====================================================================


class NutNganXep:
    """Mỗi mắt xích trong ngăn xếp (giống như 1 chiếc đĩa)."""

    def __init__(self, du_lieu):
        self.du_lieu = du_lieu   # Dữ liệu chứa trong mắt xích
        self.duoi = None         # Trỏ tới mắt xích nằm ngay bên dưới


class NganXep:
    """
    Ngăn xếp (Stack) - LIFO: Last In, First Out.
    - Phần tử đẩy vào sau cùng sẽ được lấy ra đầu tiên.
    - Giống như chồng đĩa: đĩa để cuối cùng sẽ lấy ra trước.
    """

    def __init__(self):
        self.dinh = None      # Phần tử trên cùng (None = ngăn xếp rỗng)
        self.so_luong = 0     # Số phần tử đang có

    def day_vao(self, du_lieu):
        """
        Đẩy một phần tử lên đỉnh ngăn xếp (Push).
        - Tạo mắt xích mới.
        - Mắt xích mới trỏ xuống mắt xích đang ở đỉnh.
        - Đỉnh mới = mắt xích vừa tạo.
        """
        nut_moi = NutNganXep(du_lieu)
        nut_moi.duoi = self.dinh  # Mắt xích mới trỏ xuống mắt xích cũ
        self.dinh = nut_moi       # Đỉnh ngăn xếp giờ là mắt xích mới
        self.so_luong += 1

    def lay_ra(self):
        """
        Lấy phần tử trên cùng ra khỏi ngăn xếp (Pop).
        - Nếu rỗng: trả về None.
        - Nếu không rỗng: trả về dữ liệu, đỉnh mới = mắt xích bên dưới.
        """
        if self.dinh is None:
            return None
        nut_lay = self.dinh
        self.dinh = self.dinh.duoi  # Đỉnh mới = mắt xích ngay bên dưới
        self.so_luong -= 1
        return nut_lay.du_lieu

    def xem_dinh(self):
        """Xem phần tử trên cùng MÀ KHÔNG LẤY RA (Peek)."""
        if self.dinh is None:
            return None
        return self.dinh.du_lieu

    def rong(self):
        """Kiểm tra ngăn xếp có rỗng không."""
        return self.dinh is None

    def xoa_tat_ca(self):
        """Xóa sạch toàn bộ ngăn xếp."""
        self.dinh = None
        self.so_luong = 0
