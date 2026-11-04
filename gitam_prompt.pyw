import os
import sys
import subprocess
from pathlib import Path
import tkinter as tk

CLI_DIR = Path(__file__).parent.resolve()
VENV_PYTHON = CLI_DIR / ".venv" / "Scripts" / "python.exe"
GITAM_APP = CLI_DIR / "gitam_app.py"


def execute_and_show_cli(cmd_text):
    cmd_text = cmd_text.strip()
    if not cmd_text:
        return
    # Spawns a visible CMD terminal window that executes the command and stays open
    run_cmd = f'"{VENV_PYTHON}" "{GITAM_APP}" {cmd_text}'
    full_cmd = f'start "GITAM Assistant" cmd /k "{run_cmd}"'
    subprocess.Popen(full_cmd, shell=True)


def main():
    root = tk.Tk()
    root.title("GITAM Quick Command")
    root.configure(bg="#181825")
    root.attributes("-topmost", True)

    # Size and position in center of screen
    w, h = 480, 100
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = int((sw - w) / 2)
    y = int((sh - h) / 3)  # Slightly above middle
    root.geometry(f"{w}x{h}+{x}+{y}")
    root.resizable(False, False)

    # Header label
    lbl = tk.Label(
        root,
        text="🎓 GITAM Command  (e.g. attendance, download <course>, open, quiz)",
        font=("Segoe UI", 9),
        bg="#181825",
        fg="#a6adc8"
    )
    lbl.pack(anchor="w", padx=16, pady=(10, 4))

    # Entry frame
    entry_frame = tk.Frame(root, bg="#313244", padx=2, pady=2)
    entry_frame.pack(fill="x", padx=16, pady=(0, 10))

    entry = tk.Entry(
        entry_frame,
        font=("Segoe UI", 12),
        bg="#1e1e2e",
        fg="#cdd6f4",
        insertbackground="#89b4fa",
        relief="flat"
    )
    entry.pack(fill="x", ipady=5, padx=6)
    entry.focus_set()

    def on_submit(event=None):
        val = entry.get().strip()
        root.destroy()
        if val:
            execute_and_show_cli(val)

    def on_cancel(event=None):
        root.destroy()

    entry.bind("<Return>", on_submit)
    entry.bind("<Escape>", on_cancel)
    root.bind("<Escape>", on_cancel)

    root.mainloop()


if __name__ == "__main__":
    main()
