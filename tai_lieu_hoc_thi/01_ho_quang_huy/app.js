/* ====================================================================
   APP JS - TÀI LIỆU HỌC THI - HỒ QUANG HUY
   - Mô phỏng DSLK đôi (thêm / xóa đầu / xóa cuối)
   - Mô phỏng Merge Sort (animation từng bước)
   - Mô phỏng Undo/Redo (2 stack)
   - Quiz kiểm tra
   ==================================================================== */

// ===== TIỆN ÍCH CHUNG =====
function themLog(elementId, text, type = "info") {
    const log = document.getElementById(elementId);
    if (!log) return;
    const line = document.createElement("div");
    line.className = "log-line " + (type === "success" ? "success" : type === "error" ? "error" : "");
    line.textContent = "> " + text;
    log.appendChild(line);
    log.scrollTop = log.scrollHeight;
}

function xoaLog(elementId) {
    const log = document.getElementById(elementId);
    if (log) log.innerHTML = '<div class="log-line">Sẵn sàng.</div>';
}


// ====================================================================
// PHẦN 1: MÔ PHỎNG DSLK ĐÔI
// ====================================================================
let dslkData = []; // Mỗi phần tử: { ma: "S01", ten: "Sách A" }
let dslkCounter = 0;

function dslkRender() {
    const visual = document.getElementById("dslk-visual");
    if (!visual) return;

    if (dslkData.length === 0) {
        visual.innerHTML = '<em style="color:#9CA3AF">(Danh sách rỗng)</em>';
        return;
    }

    let html = "";
    dslkData.forEach((sp, i) => {
        if (i > 0) html += '<span class="arrow">⇄</span>';
        const label = i === 0 ? " (đầu)" : (i === dslkData.length - 1 ? " (cuối)" : "");
        html += `<div class="node-box">${sp.ma}<br><small>${label}</small></div>`;
    });
    visual.innerHTML = html;
}

function dslkThem() {
    dslkCounter++;
    const ma = "S" + String(dslkCounter).padStart(2, "0");
    const sp = { ma: ma, ten: "Sản phẩm " + dslkCounter };
    dslkData.push(sp); // them_vao_cuoi
    dslkRender();
    themLog("dslk-log", `➕ them_vao_cuoi("${ma}") — DSLK hiện có ${dslkData.length} nút`, "success");
}

function dslkXoaDau() {
    if (dslkData.length === 0) {
        themLog("dslk-log", "❌ Không thể xóa: DSLK rỗng!", "error");
        return;
    }
    const ma = dslkData[0].ma;
    dslkData.shift();
    dslkRender();
    themLog("dslk-log", `❌ Xóa nút đầu (${ma}) — còn ${dslkData.length} nút`, "success");
}

function dslkXoaCuoi() {
    if (dslkData.length === 0) {
        themLog("dslk-log", "❌ Không thể xóa: DSLK rỗng!", "error");
        return;
    }
    const ma = dslkData[dslkData.length - 1].ma;
    dslkData.pop();
    dslkRender();
    themLog("dslk-log", `❌ Xóa nút cuối (${ma}) — còn ${dslkData.length} nút`, "success");
}

function dslkReset() {
    dslkData = [];
    dslkCounter = 0;
    dslkRender();
    xoaLog("dslk-log");
}


// ====================================================================
// PHẦN 2: MÔ PHỎNG MERGE SORT
// ====================================================================
function mergeSort(arr) {
    if (arr.length <= 1) return arr;

    const giua = Math.floor(arr.length / 2);
    const trai = mergeSort(arr.slice(0, giua));
    const phai = mergeSort(arr.slice(giua));

    return merge(trai, phai);
}

function merge(trai, phai) {
    const ket_qua = [];
    let i = 0, j = 0;
    while (i < trai.length && j < phai.length) {
        if (trai[i] <= phai[j]) {
            ket_qua.push(trai[i]);
            i++;
        } else {
            ket_qua.push(phai[j]);
            j++;
        }
    }
    while (i < trai.length) ket_qua.push(trai[i++]);
    while (j < phai.length) ket_qua.push(phai[j++]);
    return ket_qua;
}

function mergeSortDemo() {
    const input = document.getElementById("ms-input").value;
    const arr = input.split(",").map(s => parseFloat(s.trim())).filter(n => !isNaN(n));

    if (arr.length === 0) {
        themLog("ms-log", "❌ Nhập mảng số hợp lệ (vd: 5, 3, 8, 1)", "error");
        return;
    }

    const visual = document.getElementById("ms-visual");
    themLog("ms-log", `📥 Mảng ban đầu: [${arr.join(", ")}]`);

    // Hiển thị mảng ban đầu
    visual.innerHTML = `
        <div style="font-weight:bold;color:#047857;">MẢNG BAN ĐẦU:</div>
        <div style="display:flex;gap:6px;flex-wrap:wrap;justify-content:center;">
            ${arr.map(v => `<div class="node-box">${v}</div>`).join("")}
        </div>
    `;

    setTimeout(() => {
        const sorted = mergeSort([...arr]);
        themLog("ms-log", `⚡ Đang sắp xếp bằng Merge Sort (đệ quy)...`);
        themLog("ms-log", `   - Chia đôi → sắp xếp từng nửa → trộn lại`);

        setTimeout(() => {
            visual.innerHTML += `
                <div style="font-weight:bold;color:#047857;margin-top:14px;">SAU KHI SẮP XẾP:</div>
                <div style="display:flex;gap:6px;flex-wrap:wrap;justify-content:center;">
                    ${sorted.map(v => `<div class="node-box highlight">${v}</div>`).join("")}
                </div>
            `;
            themLog("ms-log", `✅ Kết quả: [${sorted.join(", ")}]`, "success");
        }, 600);
    }, 400);
}

function mergeSortReset() {
    document.getElementById("ms-visual").innerHTML = '<em style="color:#9CA3AF">Bấm Sắp xếp để xem</em>';
    xoaLog("ms-log");
}


// ====================================================================
// PHẦN 3: MÔ PHỎNG UNDO/REDO
// ====================================================================
let urList = [];        // Danh sách hiện tại
let urUndoStack = [];   // Stack Undo (LIFO)
let urRedoStack = [];   // Stack Redo (LIFO)
let urCounter = 0;

function urRender() {
    // Hiện danh sách
    document.getElementById("ur-list").textContent = "[" + urList.map(x => x.ten).join(", ") + "]";

    // Hiện Stack Undo (LIFO → đỉnh ở trên)
    const undoDiv = document.getElementById("ur-undo-stack");
    undoDiv.innerHTML = "";
    if (urUndoStack.length === 0) {
        undoDiv.innerHTML = '<div style="color:#9CA3AF;font-size:12px;">(rỗng)</div>';
    } else {
        // Đỉnh stack ở trên cùng
        for (let i = urUndoStack.length - 1; i >= 0; i--) {
            const t = urUndoStack[i];
            const div = document.createElement("div");
            div.className = "stack-item";
            div.textContent = `${t.thao_tac} ${t.sp.ten}`;
            undoDiv.appendChild(div);
        }
    }

    // Hiện Stack Redo
    const redoDiv = document.getElementById("ur-redo-stack");
    redoDiv.innerHTML = "";
    if (urRedoStack.length === 0) {
        redoDiv.innerHTML = '<div style="color:#9CA3AF;font-size:12px;">(rỗng)</div>';
    } else {
        for (let i = urRedoStack.length - 1; i >= 0; i--) {
            const t = urRedoStack[i];
            const div = document.createElement("div");
            div.className = "stack-item";
            div.style.backgroundColor = "#1D4E89";
            div.textContent = `${t.thao_tac} ${t.sp.ten}`;
            redoDiv.appendChild(div);
        }
    }
}

function urThem() {
    urCounter++;
    const sp = { ten: "P" + urCounter };
    urList.push(sp);

    // Đẩy thao tác THÊM vào Stack Undo
    urUndoStack.push({ thao_tac: "them", sp: sp });

    // QUY TẮC VÀNG: có thao tác mới → xóa Stack Redo
    urRedoStack = [];

    urRender();
    themLog("ur-log", `➕ THÊM "${sp.ten}" → DSLK + đẩy vào Stack Undo. Redo bị xóa.`, "success");
}

function urUndo() {
    if (urUndoStack.length === 0) {
        themLog("ur-log", "⚠ Stack Undo rỗng — không còn gì để hoàn tác!", "error");
        return;
    }
    const thao_tac = urUndoStack.pop(); // Lấy từ đỉnh

    if (thao_tac.thao_tac === "them") {
        // Đã THÊM → Undo = XÓA
        urList = urList.filter(x => x.ten !== thao_tac.sp.ten);
    }

    // Đẩy sang Stack Redo
    urRedoStack.push(thao_tac);

    urRender();
    themLog("ur-log", `↩ UNDO: lấy "${thao_tac.thao_tac} ${thao_tac.sp.ten}" từ Stack Undo → đẩy sang Redo`);
}

function urRedo() {
    if (urRedoStack.length === 0) {
        themLog("ur-log", "⚠ Stack Redo rỗng — không còn gì để làm lại!", "error");
        return;
    }
    const thao_tac = urRedoStack.pop();

    if (thao_tac.thao_tac === "them") {
        urList.push(thao_tac.sp);
    }

    urUndoStack.push(thao_tac);

    urRender();
    themLog("ur-log", `↪ REDO: làm lại "${thao_tac.thao_tac} ${thao_tac.sp.ten}" → đẩy về Undo`, "success");
}

function urReset() {
    urList = [];
    urUndoStack = [];
    urRedoStack = [];
    urCounter = 0;
    urRender();
    xoaLog("ur-log");
}


// ====================================================================
// PHẦN 4: QUIZ
// ====================================================================
function kiemTra(quizId, dapAnDung) {
    const quiz = document.getElementById(quizId);
    if (!quiz) return;

    const selected = quiz.querySelector(`input[name="${quizId.replace('quiz','q')}"]:checked`);
    const feedback = quiz.querySelector(".feedback");

    // Reset style
    quiz.querySelectorAll("label").forEach(l => l.classList.remove("correct", "wrong"));

    if (!selected) {
        feedback.className = "feedback show wrong";
        feedback.textContent = "❌ Vui lòng chọn 1 đáp án!";
        return;
    }

    if (selected.value === dapAnDung) {
        feedback.className = "feedback show correct";
        feedback.textContent = "✅ Chính xác! Bạn đã hiểu.";
        selected.parentElement.classList.add("correct");
    } else {
        feedback.className = "feedback show wrong";
        feedback.textContent = `❌ Sai rồi. Đáp án đúng là: ${dapAnDung}`;
        selected.parentElement.classList.add("wrong");
        // Highlight đáp án đúng
        const dung = quiz.querySelector(`input[value="${dapAnDung}"]`);
        if (dung) dung.parentElement.classList.add("correct");
    }
}


// ====================================================================
// KHỞI TẠO BAN ĐẦU
// ====================================================================
window.addEventListener("DOMContentLoaded", () => {
    dslkRender();
    urRender();
});
