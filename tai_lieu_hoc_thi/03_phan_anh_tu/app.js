/* ====================================================================
   APP JS - TÀI LIỆU HỌC THI - PHAN ANH TÚ
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


// ===== PHẦN 1: OOP — TẠO ĐỐI TƯỢNG =====
function oopTaoSach() {
    const sp = {
        loai: "Sach",
        ma_so: "S01",
        ten: "Lập trình C++",
        gia_co_ban: 100000,
        so_luong: 10,
        tac_gia: "Bjarne Stroustrup",
        nha_xuat_ban: "NXB Trẻ"
    };
    hienThiDoiTuong(sp);
}

function oopTaoTapChi() {
    const sp = {
        loai: "TapChi",
        ma_so: "T01",
        ten: "Công nghệ PC",
        gia_co_ban: 50000,
        so_luong: 20,
        so_phat_hanh: "Số 15"
    };
    hienThiDoiTuong(sp);
}

function oopTaoBao() {
    const sp = {
        loai: "Bao",
        ma_so: "B01",
        ten: "Báo Tuổi Trẻ",
        gia_co_ban: 5000,
        so_luong: 100,
        ngay_phat_hanh: "25/06/2025"
    };
    hienThiDoiTuong(sp);
}

function hienThiDoiTuong(sp) {
    const div = document.getElementById("oop-result");
    let html = `<div style="color:#047857;font-weight:bold;">✅ Đã tạo đối tượng ${sp.loai}</div>`;
    html += '<table style="margin-top:10px;"><tbody>';
    for (const [k, v] of Object.entries(sp)) {
        html += `<tr><td style="font-weight:bold;width:40%;">${k}</td><td>${v}</td></tr>`;
    }
    html += '</tbody></table>';
    div.innerHTML = html;
}

function oopReset() {
    document.getElementById("oop-result").innerHTML = '<em style="color:#9CA3AF">Chưa tạo đối tượng nào.</em>';
}


// ===== PHẦN 2: ĐA HÌNH =====

// Ví dụ đời thường: Động vật kêu — cùng lệnh keu() nhưng mỗi con trả về âm thanh khác nhau
function animalKeu(cardEl, ten, amThanh) {
    // Reset tất cả card
    document.querySelectorAll('.poly-card').forEach(c => c.classList.remove('called'));
    // Highlight card được bấm
    cardEl.classList.add('called');
    // Hiển thị kết quả
    const result = document.getElementById('animal-result');
    result.innerHTML = `
        <div style="font-size:14px;color:#6B7280;margin-bottom:6px;">
            <code>con_vat.keu()</code> — cùng 1 lệnh gọi, nhưng...
        </div>
        <div style="font-size:24px;font-weight:bold;color:#047857;">
            ${ten} kêu: "${amThanh}"
        </div>
    `;
    setTimeout(() => cardEl.classList.remove('called'), 800);
}

function daHinhTinh() {
    const gia = parseFloat(document.getElementById("dh-gia").value);
    if (isNaN(gia) || gia < 0) {
        alert("Vui lòng nhập giá hợp lệ!");
        return;
    }

    const ds = [
        { loai: "Sach",         icon: "📚", cong_thuc: "× 1.20", gia: gia * 1.20, mo_ta: "+20%" },
        { loai: "TapChi",       icon: "📰", cong_thuc: "× 0.90", gia: gia * 0.90, mo_ta: "-10%" },
        { loai: "Bao",          icon: "📄", cong_thuc: "× 1.00", gia: gia * 1.00, mo_ta: "nguyên giá" },
        { loai: "LuanVan",      icon: "🎓", cong_thuc: "× 1.30", gia: gia * 1.30, mo_ta: "+30%" },
        { loai: "BanThao mới",  icon: "📝", cong_thuc: "× 1.50", gia: gia * 1.50, mo_ta: "+50% (mới)" },
        { loai: "BanThao cũ",   icon: "📝", cong_thuc: "× 1.20", gia: gia * 1.20, mo_ta: "+20% (cũ)" }
    ];

    let html = `<div style="margin-bottom:14px;color:#047857;font-weight:bold;font-size:15px;">📊 Giá cơ bản = ${gia.toLocaleString()} đ — cùng gọi <code>tinh_gia_ban()</code>:</div>`;
    html += '<div class="poly-demo">';
    ds.forEach((sp, idx) => {
        html += `<div class="poly-card" style="animation: cellPop 0.4s ease ${idx * 0.08}s both;">
            <div class="icon">${sp.icon}</div>
            <div class="title">${sp.loai}</div>
            <div style="font-size:11px;color:#6B7280;margin:2px 0;">${sp.cong_thuc} (${sp.mo_ta})</div>
            <div class="price">${sp.gia.toLocaleString()} đ</div>
        </div>`;
    });
    html += '</div>';
    html += '<div class="tip" style="margin-top:14px;"><strong>💡 Đây chính là ĐA HÌNH!</strong> Cùng <code>tinh_gia_ban()</code> nhưng mỗi loại trả về giá khác nhau. Python tự biết gọi đúng phương thức của lớp con tương ứng.</div>';

    document.getElementById("dh-result").innerHTML = html;
}

function daHinhReset() {
    document.getElementById("dh-result").innerHTML = "";
}


// ===== PHẦN 3: QUEUE =====
let qData = [];
let qCounter = 0;

function qRender() {
    const visual = document.getElementById("queue-visual");
    if (qData.length === 0) {
        visual.innerHTML = '<em style="color:#9CA3AF">(giỏ hàng rỗng)</em>';
        return;
    }
    let html = "";
    qData.forEach((v, i) => {
        const label = i === 0 ? " ← RA" : (i === qData.length - 1 ? " ← VÀO" : "");
        html += `<div class="queue-item">${v}${label}</div>`;
    });
    visual.innerHTML = html;
}

function qEnqueue() {
    qCounter++;
    const v = "Món " + qCounter;
    qData.push(v);  // them_vao cuối
    qRender();
    themLog("queue-log", `➕ ENQUEUE("${v}") — thêm vào CUỐI hàng. Hiện có ${qData.length} món.`, "success");
}

function qDequeue() {
    if (qData.length === 0) {
        themLog("queue-log", "❌ Hàng đợi rỗng!", "error");
        return;
    }
    const v = qData.shift();  // lay_ra đầu
    qRender();
    themLog("queue-log", `💳 DEQUEUE() → lấy "${v}" từ ĐẦU hàng → thanh toán. Còn ${qData.length} món.`, "success");
}

function qReset() {
    qData = [];
    qCounter = 0;
    qRender();
    xoaLog("queue-log");
}


// ===== PHẦN 4: DIALOG FORM =====
function dlgDoiLoai() {
    const loai = document.getElementById("dlg-loai").value;
    const r1Label = document.getElementById("dlg-rieng1-label");
    const r2Label = document.getElementById("dlg-rieng2-label");
    const r2 = document.getElementById("dlg-rieng2");
    const r1 = document.getElementById("dlg-rieng1");

    if (loai === "Sách") {
        r1Label.textContent = "Tác giả:";
        r2Label.textContent = "Nhà xuất bản:";
        r1.placeholder = "Tác giả";
        r2.placeholder = "NXB";
        r2.style.display = "";
        r2Label.style.display = "";
    } else if (loai === "Tạp Chí") {
        r1Label.textContent = "Số phát hành:";
        r1.placeholder = "Số 15";
        r2.style.display = "none";
        r2Label.style.display = "none";
    } else if (loai === "Báo") {
        r1Label.textContent = "Ngày phát hành:";
        r1.placeholder = "dd/mm/yyyy";
        r2.style.display = "none";
        r2Label.style.display = "none";
    } else if (loai === "Luận Văn") {
        r1Label.textContent = "Trường Đại học:";
        r1.placeholder = "ĐH Bách Khoa";
        r2.style.display = "none";
        r2Label.style.display = "none";
    } else { // Bản Thảo
        r1Label.textContent = "Tình trạng (mới/cũ):";
        r1.placeholder = "mới hoặc cũ";
        r2.style.display = "none";
        r2Label.style.display = "none";
    }
    themLog("dlg-log", `🔄 Đổi loại → "${loai}". Form tự ẩn/hiện ô nhập riêng.`);
}

function dlgLuu() {
    const ma = document.getElementById("dlg-ma").value.trim();
    const ten = document.getElementById("dlg-ten").value.trim();
    const loai = document.getElementById("dlg-loai").value;

    if (!ma || !ten) {
        themLog("dlg-log", "❌ QMessageBox.warning: Vui lòng nhập đầy đủ Mã và Tên!", "error");
        return;
    }

    // Tạo đối tượng theo loại (mô phỏng đa hình)
    themLog("dlg-log", `✅ Đã tạo đối tượng ${loai} [${ma}] — ${ten}`, "success");
    themLog("dlg-log", `✅ self.accept() → đóng dialog với kết quả Accepted`);
    themLog("dlg-log", `   → main_window sẽ thêm sp vào DSLK + lưu SQLite`);
}

function dlgHuy() {
    themLog("dlg-log", `❌ self.reject() → đóng dialog với kết quả Rejected (Hủy)`);
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
    qRender();
});
