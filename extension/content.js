(function () {
    'use strict';

    // Completely ignore the login portal to avoid triggering bot detection
    if (window.location.hostname.includes('login.gitam.edu')) {
        return;
    }

    // ========================================================
    // 1. AUTO-KILL POPUPS ON HOME PORTAL
    // ========================================================
    function killAnnoyingPopups() {
        const popupSelectors = [
            '.modal.show',
            '.modal-backdrop',
            '#announcementModal',
            '#notificationModal',
            '.swal2-container',
            '.fancybox-overlay'
        ];

        const closeSelectors = [
            '.modal.show .close',
            '.modal.show [data-dismiss="modal"]',
            '.modal.show [data-bs-dismiss="modal"]',
            '.swal2-close',
            '.swal2-confirm',
            '#announcementModal button.close',
            'button.btn-close',
            '.modal-header button'
        ];

        closeSelectors.forEach(selector => {
            document.querySelectorAll(selector).forEach(btn => {
                if (btn && btn.offsetParent !== null) {
                    btn.click();
                }
            });
        });

        popupSelectors.forEach(sel => {
            document.querySelectorAll(sel).forEach(el => {
                el.style.display = 'none';
            });
        });
    }
    setInterval(killAnnoyingPopups, 1200);

    // ========================================================
    // 2. CREATE IN-PAGE TERMINAL OVERLAY
    // ========================================================
    if (document.getElementById('gitam-cli-window')) return;

    const term = document.createElement('div');
    term.id = 'gitam-cli-window';
    term.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #30363d; padding-bottom:8px; margin-bottom:8px;">
            <span style="color:#58a6ff; font-weight:bold; font-size:13px;">⚡ GStudent CLI</span>
            <span id="gitam-cli-close" style="color:#8b949e; cursor:pointer; font-size:16px; font-weight:bold; padding:0 4px;">✕</span>
        </div>
        <div id="gitam-cli-logs">
            <div style="color:#8b949e;">Type <b style="color:#58a6ff;">help</b> for commands. Press <b>Esc</b> or <b>Ctrl+\`</b> to close.</div>
        </div>
        <input id="gitam-cli-input" type="text" placeholder="Type a command..." autocomplete="off" />
    `;
    document.body.appendChild(term);

    const input = document.getElementById('gitam-cli-input');
    const logs = document.getElementById('gitam-cli-logs');
    const closeBtn = document.getElementById('gitam-cli-close');

    function log(msg, color = '#c9d1d9') {
        const line = document.createElement('div');
        line.style.color = color;
        line.innerHTML = `> ${msg}`;
        logs.appendChild(line);
        logs.scrollTop = logs.scrollHeight;
    }

    closeBtn.onclick = () => {
        term.style.display = 'none';
    };

    // ========================================================
    // 3. IN-PAGE CLI COMMANDS (Password-Free)
    // ========================================================
    const commands = {
        help: () => {
            log("<b>In-Page Commands:</b>", "#79c0ff");
            log("<b>dark / light</b> : Toggle dark mode instantly", "#c9d1d9");
            log("<b>edit</b> : Click & edit any text live on screen", "#c9d1d9");
            log("<b>hide &lt;selector&gt;</b> : Hide any element (e.g. 'hide .banner')", "#c9d1d9");
            log("<b>reg &lt;name&gt;</b> : Select faculty in dropdowns/radios", "#c9d1d9");
            log("<b>submit &lt;name&gt;</b> : Find assignment & open file upload", "#c9d1d9");
            log("<b>kill-popup</b> : Dismiss any stubborn popups", "#c9d1d9");
            log("<b>clear</b> : Clear terminal logs", "#c9d1d9");
        },

        dark: () => {
            document.documentElement.style.filter = 'invert(0.92) hue-rotate(180deg)';
            localStorage.setItem('gitam_custom_theme', 'dark');
            log("Dark mode enabled & saved.", "#56d364");
        },

        light: () => {
            document.documentElement.style.filter = 'none';
            localStorage.setItem('gitam_custom_theme', 'light');
            log("Default theme restored & saved.", "#56d364");
        },

        edit: () => {
            document.designMode = document.designMode === 'on' ? 'off' : 'on';
            log(`Live on-screen text edit is now: <b>${document.designMode}</b>`, "#79c0ff");
        },

        hide: (selector) => {
            if (!selector) return log("Usage: hide &lt;css_selector&gt;", "#ff7b72");
            const target = document.querySelector(selector);
            if (target) {
                target.style.display = 'none';
                log(`Hidden: ${selector}`, "#56d364");
            } else {
                log(`Element '${selector}' not found.`, "#e3b341");
            }
        },

        reg: (name) => {
            if (!name) return log("Usage: reg &lt;Faculty Name&gt;", "#ff7b72");
            const target = name.toLowerCase();
            let count = 0;

            document.querySelectorAll('select option').forEach(opt => {
                if (opt.text.toLowerCase().includes(target)) {
                    opt.parentElement.value = opt.value;
                    opt.parentElement.dispatchEvent(new Event('change', { bubbles: true }));
                    log(`Selected in dropdown: <b>${opt.text}</b>`, "#56d364");
                    count++;
                }
            });

            document.querySelectorAll('tr, .faculty-item, label').forEach(row => {
                if (row.textContent.toLowerCase().includes(target)) {
                    const r = row.querySelector('input[type="radio"], input[type="checkbox"]');
                    if (r) {
                        r.checked = true;
                        r.dispatchEvent(new Event('change', { bubbles: true }));
                        row.style.background = 'rgba(46, 160, 67, 0.25)';
                        log(`Selected faculty row: <b>${name}</b>`, "#56d364");
                        count++;
                    }
                }
            });

            if (count === 0) log(`Faculty '${name}' not found on this screen.`, "#e3b341");
        },

        submit: (keyword) => {
            if (!keyword) return log("Usage: submit &lt;Assignment Keyword&gt;", "#ff7b72");
            const target = keyword.toLowerCase();
            let found = false;

            document.querySelectorAll('tr, .assignment-item, .card').forEach(row => {
                if (row.textContent.toLowerCase().includes(target)) {
                    const btn = Array.from(row.querySelectorAll('button, a, input[type="button"]'))
                        .find(b => /submit|upload|view/i.test(b.textContent || b.value));
                    if (btn) {
                        found = true;
                        log(`Opening assignment: "${keyword}"...`, "#56d364");
                        btn.click();
                        setTimeout(() => {
                            const fileInput = document.querySelector('input[type="file"]');
                            if (fileInput) fileInput.click();
                        }, 800);
                    }
                }
            });

            if (!found) {
                const fileInput = document.querySelector('input[type="file"]');
                if (fileInput) {
                    fileInput.click();
                    log("Opened file upload dialog on current page.", "#56d364");
                } else {
                    log(`Assignment "${keyword}" not found on current page.`, "#ff7b72");
                }
            }
        },

        "kill-popup": () => {
            killAnnoyingPopups();
            log("Popup purge executed.", "#56d364");
        },

        clear: () => {
            logs.innerHTML = '';
        }
    };

    // Input listener
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            const raw = input.value.trim();
            input.value = '';
            if (!raw) return;

            log(raw, '#ffffff');
            const spaceIdx = raw.indexOf(' ');
            const cmd = (spaceIdx === -1 ? raw : raw.slice(0, spaceIdx)).toLowerCase();
            const args = spaceIdx === -1 ? '' : raw.slice(spaceIdx + 1).trim();

            if (commands[cmd]) {
                commands[cmd](args);
            } else {
                log(`Unknown command: '${cmd}'. Type 'help' for options.`, '#ff7b72');
            }
        }
    });

    // ========================================================
    // 4. HOTKEY: Ctrl + ` (Backtick) or Esc
    // ========================================================
    window.addEventListener('keydown', (e) => {
        // Toggle on Ctrl + ` (backtick, the key above Tab)
        if (e.ctrlKey && (e.key === '`' || e.code === 'Backquote')) {
            e.preventDefault();
            const isHidden = term.style.display === 'none' || !term.style.display;
            term.style.display = isHidden ? 'block' : 'none';
            if (isHidden) input.focus();
        } else if (e.key === 'Escape' && term.style.display === 'block') {
            term.style.display = 'none';
        }
    });

    // Apply saved theme on load
    const activeTheme = localStorage.getItem('gitam_custom_theme');
    if (activeTheme === 'dark') {
        document.documentElement.style.filter = 'invert(0.92) hue-rotate(180deg)';
    }
})();
