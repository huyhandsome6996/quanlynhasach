/* ================================================================
 * highlight.js — Syntax highlighter Python (VSCode Dark+ theme)
 * Hoạt động offline, không cần CDN.
 *
 * Cách dùng:
 *   1. Bọc code trong <pre class="code-block"><code class="language-python">...</code></pre>
 *   2. Thêm <script src="highlight.js"></script> trước </body>
 *   3. Script tự chạy khi DOM ready
 * ================================================================ */

(function () {
    'use strict';

    // ---- Bảng màu giống VSCode Dark+ theme (default dark) ----
    // class CSS                → màu hex     (mục đích)
    // .tok-keyword             → #569CD6      (def, class, if, return, import, from, ...)
    // .tok-control             → #C586C0      (if, else, while, for, return, try, except — control flow)
    // .tok-builtin             → #4EC9B0      (True, False, None, self)
    // .tok-string              → #CE9178      ("...", '...', """...""")
    // .tok-comment             → #6A9955      (# ...)
    // .tok-number              → #B5CEA8      (123, 4.5)
    // .tok-function            → #DCDCAA      (tên hàm sau `def`)
    // .tok-class               → #4EC9B0      (tên lớp sau `class`)
    // .tok-decorator           → #DCDCAA      (@decorator)
    // .tok-self                → #569CD6      (self)
    // .tok-operator            → #D4D4D4      (+ - * / = == != ...)
    // .tok-bracket             → #FFD700      (() [] {})
    // (text thường)            → #D4D4D4      (mặc định)

    const KEYWORDS_CONTROL = new Set([
        'if', 'elif', 'else', 'for', 'while', 'return', 'break',
        'continue', 'try', 'except', 'finally', 'raise', 'with',
        'yield', 'await', 'async', 'match', 'case'
    ]);

    const KEYWORDS_DEF = new Set([
        'def', 'class', 'import', 'from', 'as', 'global', 'nonlocal',
        'lambda', 'pass', 'del', 'assert', 'in', 'is', 'not', 'and', 'or'
    ]);

    const BUILTINS = new Set([
        'True', 'False', 'None', 'self', 'cls',
        'print', 'len', 'range', 'int', 'str', 'float', 'bool', 'list',
        'dict', 'set', 'tuple', 'type', 'isinstance', 'getattr', 'setattr',
        'hasattr', 'super', 'staticmethod', 'classmethod', 'property',
        'input', 'open', 'enumerate', 'zip', 'map', 'filter', 'sorted',
        'sum', 'min', 'max', 'abs', 'round', 'format', 'repr', 'ord', 'chr',
        'Exception', 'ValueError', 'TypeError', 'KeyError', 'IndexError',
        'AttributeError', 'RuntimeError', 'StopIteration'
    ]);

    function escapeHtml(s) {
        return s
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');
    }

    /**
     * Tokenize một dòng code Python và trả về HTML đã tô màu.
     * Quy tắc ưu tiên (match theo thứ tự):
     *   1. Comment      : # ... (cho đến cuối dòng)
     *   2. String triple: """...""" hoặc '''...'''
     *   3. String       : "..." hoặc '...'
     *   4. Decorator    : @name
     *   5. Number       : 123, 4.5, 0x1F, 1e10
     *   6. Identifier   : tên biến / hàm / class / keyword
     *   7. Operator     : + - * / = == != < > <= >= ...
     *   8. Bracket      : ( ) [ ] { }
     *   9. Whitespace   : khoảng trắng
     *  10. Other        : dấu phẩy, chấm, hai chấm, ...
     */
    function highlightLine(line) {
        let result = '';
        let i = 0;
        const n = line.length;

        while (i < n) {
            const ch = line[i];
            const next = line[i + 1] || '';

            // 1. Comment: # đến cuối dòng
            if (ch === '#') {
                result += '<span class="tok-comment">' + escapeHtml(line.slice(i)) + '</span>';
                break;
            }

            // 2 & 3. String — triple first
            if ((ch === '"' && next === '"' && line[i + 2] === '"') ||
                (ch === "'" && next === "'" && line[i + 2] === "'")) {
                const quote = ch + ch + ch;
                const end = line.indexOf(quote, i + 3);
                let endIdx = end === -1 ? n : end + 3;
                result += '<span class="tok-string">' + escapeHtml(line.slice(i, endIdx)) + '</span>';
                i = endIdx;
                continue;
            }

            // 3. String — single line
            if (ch === '"' || ch === "'") {
                // Tìm dấu quote đóng (không phải escape)
                let j = i + 1;
                while (j < n) {
                    if (line[j] === '\\') { j += 2; continue; }
                    if (line[j] === ch) { j++; break; }
                    j++;
                }
                result += '<span class="tok-string">' + escapeHtml(line.slice(i, j)) + '</span>';
                i = j;
                continue;
            }

            // 4. Decorator
            if (ch === '@' && /[A-Za-z_]/.test(next)) {
                let j = i + 1;
                while (j < n && /[A-Za-z0-9_.]/.test(line[j])) j++;
                result += '<span class="tok-decorator">' + escapeHtml(line.slice(i, j)) + '</span>';
                i = j;
                continue;
            }

            // 5. Number
            if (/[0-9]/.test(ch) || (ch === '.' && /[0-9]/.test(next))) {
                let j = i;
                // Hỗ trợ: 123, 4.5, 0x1F, 0b101, 0o17, 1e10, 1_000
                if (ch === '0' && (next === 'x' || next === 'X' || next === 'b' || next === 'B' || next === 'o' || next === 'O')) {
                    j = i + 2;
                    while (j < n && /[0-9a-fA-F_]/.test(line[j])) j++;
                } else {
                    while (j < n && /[0-9._eE+\-]/.test(line[j])) j++;
                }
                result += '<span class="tok-number">' + escapeHtml(line.slice(i, j)) + '</span>';
                i = j;
                continue;
            }

            // 6. Identifier / keyword
            if (/[A-Za-z_]/.test(ch)) {
                let j = i;
                while (j < n && /[A-Za-z0-9_]/.test(line[j])) j++;
                const word = line.slice(i, j);

                // Nhìn lùi về trước (bỏ qua space) để xem có phải `def`/`class` không
                let k = i - 1;
                while (k >= 0 && (line[k] === ' ' || line[k] === '\t')) k--;
                const prevWord = (k >= 0 && line[k] === ':') ? false : (function () {
                    // Tìm token identifier trước đó
                    let m = k;
                    while (m >= 0 && /[A-Za-z0-9_]/.test(line[m])) m--;
                    return line.slice(m + 1, k + 1);
                })();

                let cls = null;
                if (prevWord === 'def') {
                    cls = 'tok-function';
                } else if (prevWord === 'class') {
                    cls = 'tok-class';
                } else if (word === 'self' || word === 'cls') {
                    cls = 'tok-self';
                } else if (KEYWORDS_CONTROL.has(word)) {
                    cls = 'tok-control';
                } else if (KEYWORDS_DEF.has(word)) {
                    cls = 'tok-keyword';
                } else if (BUILTINS.has(word)) {
                    cls = 'tok-builtin';
                } else {
                    // Nhìn tới sau (bỏ qua space) xem có phải gọi hàm (có `(` ngay sau) không
                    let m = j;
                    while (m < n && (line[m] === ' ' || line[m] === '\t')) m++;
                    if (line[m] === '(') {
                        cls = 'tok-function';
                    }
                }

                if (cls) {
                    result += '<span class="' + cls + '">' + escapeHtml(word) + '</span>';
                } else {
                    result += escapeHtml(word);
                }
                i = j;
                continue;
            }

            // 7. Operator
            if (/[+\-*/%=<>!&|^~]/.test(ch)) {
                let j = i;
                while (j < n && /[+\-*/%=<>!&|^~]/.test(line[j])) j++;
                result += '<span class="tok-operator">' + escapeHtml(line.slice(i, j)) + '</span>';
                i = j;
                continue;
            }

            // 8. Bracket
            if (/[(){}\[\]]/.test(ch)) {
                result += '<span class="tok-bracket">' + escapeHtml(ch) + '</span>';
                i++;
                continue;
            }

            // 9. Whitespace & 10. Other
            result += escapeHtml(ch);
            i++;
        }

        return result;
    }

    /**
     * Xử lý một block code:
     *  - Tách code thành từng dòng
     *  - Tô màu từng dòng (nhận diện string triple kéo dài nhiều dòng)
     *  - Trả về HTML cho cả block
     */
    function highlightBlock(code) {
        const lines = code.split('\n');
        let html = '';
        let inTripleString = false;
        let tripleQuote = null;

        for (let idx = 0; idx < lines.length; idx++) {
            let line = lines[idx];

            if (inTripleString) {
                // Đang ở giữa triple-string → tìm dấu đóng
                const endPos = line.indexOf(tripleQuote);
                if (endPos === -1) {
                    html += '<span class="tok-string">' + escapeHtml(line) + '</span>\n';
                    continue;
                } else {
                    // Phần đầu là string, phần còn lại highlight bình thường
                    const endIdx = endPos + 3;
                    html += '<span class="tok-string">' + escapeHtml(line.slice(0, endIdx)) + '</span>';
                    inTripleString = false;
                    tripleQuote = null;
                    line = line.slice(endIdx);
                    if (line.length === 0) {
                        html += '\n';
                        continue;
                    }
                }
            }

            // Kiểm tra xem dòng này có mở triple-string không đóng không
            const tripleMatch = line.match(/("""|''')/);
            if (tripleMatch) {
                const quote = tripleMatch[1];
                const firstPos = line.indexOf(quote);
                const secondPos = line.indexOf(quote, firstPos + 3);
                if (secondPos === -1) {
                    // Triple-string mở nhưng không đóng trong dòng này
                    // → highlight phần trước + phần string mở
                    const before = line.slice(0, firstPos);
                    const strPart = line.slice(firstPos);
                    html += highlightLine(before);
                    html += '<span class="tok-string">' + escapeHtml(strPart) + '</span>\n';
                    inTripleString = true;
                    tripleQuote = quote;
                    continue;
                }
            }

            html += highlightLine(line);
            if (idx < lines.length - 1) {
                html += '\n';
            }
        }

        return html;
    }

    /**
     * Tìm tất cả <code class="language-python"> trong document và tô màu.
     */
    function run() {
        const blocks = document.querySelectorAll('code.language-python');
        blocks.forEach(function (code) {
            // Lấy text thuần (đã escape sẵn trong DOM)
            const raw = code.textContent;
            code.innerHTML = highlightBlock(raw);
        });

        // Thêm nút "Sao chép" cho mỗi <pre class="code-block">
        const pres = document.querySelectorAll('pre.code-block');
        pres.forEach(function (pre) {
            if (pre.querySelector('.copy-btn')) return;
            const btn = document.createElement('button');
            btn.className = 'copy-btn';
            btn.textContent = '📋 Sao chép';
            btn.addEventListener('click', function () {
                const code = pre.querySelector('code');
                if (!code) return;
                const text = code.textContent;
                if (navigator.clipboard) {
                    navigator.clipboard.writeText(text).then(function () {
                        btn.textContent = '✅ Đã chép!';
                        setTimeout(function () { btn.textContent = '📋 Sao chép'; }, 1500);
                    });
                } else {
                    // Fallback cho trình duyệt cũ
                    const ta = document.createElement('textarea');
                    ta.value = text;
                    document.body.appendChild(ta);
                    ta.select();
                    try { document.execCommand('copy'); } catch (e) {}
                    document.body.removeChild(ta);
                    btn.textContent = '✅ Đã chép!';
                    setTimeout(function () { btn.textContent = '📋 Sao chép'; }, 1500);
                }
            });
            pre.appendChild(btn);
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', run);
    } else {
        run();
    }
})();
