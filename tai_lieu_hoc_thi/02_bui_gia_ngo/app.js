/* ====================================================================
   APP JS - TÀI LIỆU HỌC THI - BÙI GIA NGỌ
   ==================================================================== */

function themLog(id, text, type = "info") {
    const log = document.getElementById(id);
    if (!log) return;
    const line = document.createElement("div");
    line.className = "log-line " + (type === "success" ? "success" : type === "error" ? "error" : "");
    line.textContent = "> " + text;
    log.appendChild(line);
    log.scrollTop = log.scrollHeight;
}

function xoaLog(id) {
    const log = document.getElementById(id);
    if (log) log.innerHTML = '<div class="log-line">Sẵn sàng.</div>';
}


// ===== PHẦN 1: MÔ PHỎNG STACK =====
let stackData = [];
let stackCounter = 0;

function stackRender() {
    const visual = document.getElementById("stack-visual");
    if (!visual) return;

    if (stackData.length === 0) {
        visual.innerHTML = '<div style="color:#9CA3AF;font-size:12px;">(rỗng)</div>';
        return;
    }

    visual.innerHTML = "";
    // Đỉnh ở trên cùng → duyệt từ cuối mảng đến đầu
    for (let i = stackData.length - 1; i >= 0; i--) {
        const div = document.createElement("div");
        div.className = "stack-item";
        div.textContent = stackData[i];
        if (i === stackData.length - 1) {
            div.style.backgroundColor = "#F59E0B";  // Đỉnh highlight
            div.textContent = "📍 " + stackData[i] + " (đỉnh)";
        }
        visual.appendChild(div);
    }
}

function stackPush() {
    stackCounter++;
    const val = "P" + stackCounter;
    stackData.push(val);
    stackRender();
    themLog("stack-log", `⬆ PUSH("${val}") — Stack hiện có ${stackData.length} phần tử`, "success");
}

function stackPop() {
    if (stackData.length === 0) {
        themLog("stack-log", "❌ POP thất bại: Stack rỗng!", "error");
        return;
    }
    const val = stackData.pop();
    stackRender();
    themLog("stack-log", `⬇ POP() → trả về "${val}" — còn ${stackData.length} phần tử`, "success");
}

function stackPeek() {
    if (stackData.length === 0) {
        themLog("stack-log", "❌ PEEK thất bại: Stack rỗng!", "error");
        return;
    }
    const val = stackData[stackData.length - 1];
    themLog("stack-log", `👁 PEEK() → trả về "${val}" (KHÔNG xóa)`);
}

function stackReset() {
    stackData = [];
    stackCounter = 0;
    stackRender();
    xoaLog("stack-log");
}


// ===== PHẦN 2: MÔ PHỎNG SQLITE CRUD =====
let sqlData = [];

function sqlRender() {
    const div = document.getElementById("sql-table");
    if (!div) return;
    if (sqlData.length === 0) {
        div.innerHTML = '<em style="color:#9CA3AF">Bảng SanPham đang rỗng.</em>';
        return;
    }
    let html = '<table class="sql-table-view"><thead><tr><th>ma_so</th><th>ten</th><th>gia_co_ban</th><th>loai</th></tr></thead><tbody>';
    sqlData.forEach(r => {
        const cls = r._new ? 'inserted' : '';
        html += `<tr class="${cls}"><td>${r.ma}</td><td>${r.ten}</td><td>${r.gia.toLocaleString()} đ</td><td>${r.loai||'Sach'}</td></tr>`;
        r._new = false;
    });
    html += '</tbody></table>';
    div.innerHTML = html;
}

function sqlInsert() {
    const ma = document.getElementById("sql-ma").value.trim();
    const ten = document.getElementById("sql-ten").value.trim();
    const gia = parseFloat(document.getElementById("sql-gia").value);

    if (!ma || !ten || isNaN(gia)) {
        themLog("sql-log", "❌ Vui lòng nhập đủ mã, tên, giá!", "error");
        return;
    }

    if (sqlData.find(r => r.ma === ma)) {
        themLog("sql-log", `❌ Mã "${ma}" đã tồn tại (PRIMARY KEY trùng)!`, "error");
        return;
    }

    sqlData.push({ ma, ten, gia, loai: 'Sach', _new: true });
    sqlRender();
    themLog("sql-log", `➕ INSERT INTO SanPham VALUES ('${ma}', '${ten}', ${gia}) — commit()`, "success");

    // Clear inputs
    document.getElementById("sql-ma").value = "";
    document.getElementById("sql-ten").value = "";
    document.getElementById("sql-gia").value = "";
}

function sqlSelect() {
    if (sqlData.length === 0) {
        themLog("sql-log", "📥 SELECT * FROM SanPham → 0 dòng", "error");
        return;
    }
    themLog("sql-log", `📥 SELECT * FROM SanPham → trả về ${sqlData.length} dòng`, "success");
    sqlData.forEach((r, i) => {
        themLog("sql-log", `   [${i+1}] ${r.ma} | ${r.ten} | ${r.gia.toLocaleString()}đ`);
    });
}

function sqlDelete() {
    if (sqlData.length === 0) {
        themLog("sql-log", "❌ Bảng đã rỗng!", "error");
        return;
    }
    const count = sqlData.length;
    sqlData = [];
    sqlRender();
    themLog("sql-log", `🗑 DELETE FROM SanPham → xóa ${count} dòng — commit()`, "success");
}


// ===== PHẦN 3: MÔ PHỎNG ĐĂNG NHẬP PHÂN QUYỀN =====
const DSTK = [
    { ten: "admin",    mk: "123", quyen: "admin" },
    { ten: "nhanvien", mk: "123", quyen: "nhan_vien" }
];
let dnNguoiDung = null;

function dnRender() {
    const result = document.getElementById("dn-result");
    const buttons = document.getElementById("dn-buttons");

    if (dnNguoiDung === null) {
        result.innerHTML = '<em style="color:#9CA3AF">Chưa đăng nhập.</em>';
        buttons.innerHTML = "";
        return;
    }

    const laAdmin = dnNguoiDung.quyen === "admin";
    const badge = laAdmin
        ? '<span class="role-badge admin">👑 ADMIN</span>'
        : '<span class="role-badge nv">🧹 NHÂN VIÊN</span>';
    result.innerHTML = `
        <div style="margin-bottom:8px;">${badge}</div>
        <div style="color:#047857;"><strong>✅ Đăng nhập thành công!</strong></div>
        <div>Tên: <code>${dnNguoiDung.ten}</code></div>
    `;

    // Hiện các nút chức năng theo quyền
    buttons.innerHTML = "";
    const dsNut = [
        { ten: "📋 Xem SP", admin: false, icon: "📋" },
        { ten: "➕ Thêm SP", admin: false, icon: "➕" },
        { ten: "✏️ Sửa SP", admin: false, icon: "✏️" },
        { ten: "❌ Xóa SP", admin: true, icon: "❌" },
        { ten: "🛒 Giỏ hàng", admin: false, icon: "🛒" },
        { ten: "📊 Thống kê", admin: false, icon: "📊" }
    ];
    dsNut.forEach(n => {
        const b = document.createElement("button");
        b.textContent = n.ten;
        if (n.admin && !laAdmin) {
            b.className = "secondary";
            b.disabled = true;
            b.style.opacity = "0.4";
            b.style.cursor = "not-allowed";
            b.style.textDecoration = "line-through";
            b.title = "Nhân viên không được phép!";
        } else {
            b.onclick = () => themLog("dn-log", `▶ Thực hiện: ${n.ten}`, "success");
        }
        buttons.appendChild(b);
    });
}

function dnDangNhap() {
    const ten = document.getElementById("dn-ten").value.trim();
    const mk = document.getElementById("dn-mk").value.trim();

    if (!ten || !mk) {
        themLog("dn-log", "❌ Vui lòng nhập tên + mật khẩu!", "error");
        return;
    }

    const nguoi = DSTK.find(n => n.ten === ten && n.mk === mk);
    if (!nguoi) {
        themLog("dn-log", `❌ Đăng nhập thất bại: sai tên hoặc mật khẩu!`, "error");
        dnNguoiDung = null;
        dnRender();
        return;
    }

    dnNguoiDung = nguoi;
    dnRender();
    themLog("dn-log", `✅ Đăng nhập OK: ${nguoi.ten} (${nguoi.quyen === "admin" ? "Admin" : "Nhân viên"})`, "success");
}

function dnAdmin() {
    document.getElementById("dn-ten").value = "admin";
    document.getElementById("dn-mk").value = "123";
    dnDangNhap();
}

function dnNV() {
    document.getElementById("dn-ten").value = "nhanvien";
    document.getElementById("dn-mk").value = "123";
    dnDangNhap();
}

function dnDangXuat() {
    if (dnNguoiDung) {
        themLog("dn-log", `🚪 Đăng xuất: ${dnNguoiDung.ten}`);
    }
    dnNguoiDung = null;
    dnRender();
    document.getElementById("dn-ten").value = "";
    document.getElementById("dn-mk").value = "";
}


// ===== PHẦN 4: MÔ PHỎNG CHẠY TEST =====
let testRunning = false;

function testChay() {
    if (testRunning) return;
    testRunning = true;
    xoaLog("test-log");

    // Reset progress bar
    const cells = document.querySelectorAll('#test-bar .test-cell');
    cells.forEach(c => c.className = 'test-cell');
    const summary = document.getElementById('test-summary');
    if (summary) {
        summary.textContent = 'Đang chạy test...';
        summary.style.color = '#FDE68A';
    }

    const steps = [
        { msg: "BẮT ĐẦU KIỂM THỬ ĐỒ ÁN PYQT6", type: "info", cell: null },
        { msg: "────────────────────────────────", type: "info", cell: null },
        { msg: "1. KIỂM TRA TÍNH ĐA HÌNH (tinh_gia_ban):", type: "info", cell: 0 },
        { msg: "   - Sách 'Lập trình C++': 100000 × 1.20 = 120000 ✓", type: "success", cell: 0 },
        { msg: "   - Tạp chí 'Công Nghệ PC': 50000 × 0.90 = 45000 ✓", type: "success", cell: 0 },
        { msg: "   - Báo 'Tuổi Trẻ': 5000 × 1.00 = 5000 ✓", type: "success", cell: 0 },
        { msg: "   - Luận văn: 200000 × 1.30 = 260000 ✓", type: "success", cell: 0 },
        { msg: "   - Bản thảo mới: 100000 × 1.50 = 150000 ✓", type: "success", cell: 0 },
        { msg: "2. DSLK ĐÔI — thêm 5 sp → so_luong = 5 ✓", type: "success", cell: 1 },
        { msg: "3. DSLK — duyệt danh sách ✓", type: "success", cell: 2 },
        { msg: "4. MERGE SORT — sắp xếp theo gia_co_ban tăng dần ✓", type: "success", cell: 3 },
        { msg: "5. TÌM KIẾM — tim_kiem_theo_ma('T01') → trả về TapChi ✓", type: "success", cell: 4 },
        { msg: "6. XÓA — xóa 'B01' → so_luong = 4 ✓", type: "success", cell: 5 },
        { msg: "7. STACK LIFO — đẩy 3, lấy ra theo LIFO (3→2→1) ✓", type: "success", cell: 6 },
        { msg: "8. QUEUE FIFO — giỏ hàng: thêm 3, thanh toán theo FIFO ✓", type: "success", cell: 7 },
        { msg: "9. SQLITE — lưu 4 sp, đọc lại, đa hình còn ✓", type: "success", cell: 8 },
        { msg: "10. PHÂN QUYỀN — sai mk = None ✓, admin = True ✓, NV = True ✓", type: "success", cell: 9 },
        { msg: "────────────────────────────────", type: "info", cell: null },
        { msg: "MỌI THỨ HOẠT ĐỘNG HOÀN HẢO! Test pass 100%.", type: "success", cell: null }
    ];

    let i = 0;
    const interval = setInterval(() => {
        if (i >= steps.length) {
            clearInterval(interval);
            testRunning = false;
            if (summary) {
                summary.innerHTML = '✅ <strong>10/10 test PASS</strong> — Mọi thứ hoạt động hoàn hảo!';
                summary.style.color = '#6EE7B7';
            }
            return;
        }
        themLog("test-log", steps[i].msg, steps[i].type);
        if (steps[i].cell !== null && steps[i].cell !== undefined) {
            const cell = cells[steps[i].cell];
            if (cell) cell.className = 'test-cell pass';
            if (summary) summary.innerHTML = `Đang chạy test <strong>${steps[i].cell + 1}/10</strong>...`;
        }
        i++;
    }, 250);
}

function testReset() {
    xoaLog("test-log");
    const cells = document.querySelectorAll('#test-bar .test-cell');
    cells.forEach(c => c.className = 'test-cell');
    const summary = document.getElementById('test-summary');
    if (summary) {
        summary.textContent = 'Sẵn sàng. Bấm "Chạy test" để bắt đầu.';
        summary.style.color = '#6EE7B7';
    }
    testRunning = false;
}

// ===== VÍ DỤ ĐỜI THƯỜNG: CHỒNG ĐĨA =====
let plateCount = 3;

function plateRender() {
    const stack = document.getElementById('plate-demo');
    if (!stack) return;
    stack.innerHTML = '';
    for (let i = 1; i <= plateCount; i++) {
        const plate = document.createElement('div');
        plate.className = 'plate' + (i === plateCount ? ' new' : '');
        plate.textContent = '🍽 Đĩa ' + i;
        stack.appendChild(plate);
    }
}

function platePush() {
    plateCount++;
    plateRender();
}

function platePop() {
    if (plateCount === 0) return;
    const stack = document.getElementById('plate-demo');
    if (stack && stack.lastChild) {
        stack.lastChild.style.animation = 'fadeOut 0.4s ease forwards';
        setTimeout(() => {
            plateCount--;
            plateRender();
        }, 350);
    } else {
        plateCount--;
        plateRender();
    }
}


// ===== QUIZ =====
function kiemTra(quizId, dapAnDung) {
    const quiz = document.getElementById(quizId);
    if (!quiz) return;
    const nameQ = quizId.replace('quiz', 'q');
    const selected = quiz.querySelector(`input[name="${nameQ}"]:checked`);
    const feedback = quiz.querySelector(".feedback");
    quiz.querySelectorAll("label").forEach(l => l.classList.remove("correct", "wrong"));

    if (!selected) {
        feedback.className = "feedback show wrong";
        feedback.textContent = "❌ Vui lòng chọn 1 đáp án!";
        return;
    }

    if (selected.value === dapAnDung) {
        feedback.className = "feedback show correct";
        feedback.textContent = "✅ Chính xác!";
        selected.parentElement.classList.add("correct");
    } else {
        feedback.className = "feedback show wrong";
        feedback.textContent = `❌ Sai. Đáp án đúng là: ${dapAnDung}`;
        selected.parentElement.classList.add("wrong");
        const dung = quiz.querySelector(`input[value="${dapAnDung}"]`);
        if (dung) dung.parentElement.classList.add("correct");
    }
}


// KHỞI TẠO
window.addEventListener("DOMContentLoaded", () => {
    stackRender();
    sqlRender();
    dnRender();
    plateRender();
});
