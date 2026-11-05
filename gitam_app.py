import os
import re
import sys
import time
import argparse
import shlex
import difflib
import subprocess
from pathlib import Path

# Force UTF-8 encoding on Windows console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Load credentials safely from local .env
env_file = Path(__file__).parent / ".env"
if env_file.exists():
    try:
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())
    except Exception:
        pass

STUDENT_ID = os.getenv("GITAM_STUDENT_ID", "")
PASSWORD = os.getenv("GITAM_PASSWORD", "")

PORTAL_HOME = "https://gstudent.gitam.edu/Home"
LOGIN_URL = "https://login.gitam.edu/Login.aspx"

# Paths
BRAVE_EXE = os.path.expandvars(r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\Application\brave.exe")
CAPTCHA_EXT = r"C:\Users\madha\Downloads\captcha-paster-4.1\captcha-paster"
GITAM_EXT = r"C:\Users\madha\gitam-extension"
CUSTOM_CSS_PATH = r"C:\Users\madha\gitam-extension\custom_styles.css"
PROFILE_DIR = str(Path(__file__).parent / "brave_profile")
MATERIALS_BASE_DIR = r"C:\Users\madha\GITAM_Materials"

# ==============================================================================
# GSTUDENT APPLICATION ARCHITECTURE & ROUTE MAP (In-and-Out Knowledge)
# ==============================================================================
PORTAL_ROUTES = {
    "home": "https://gstudent.gitam.edu/Home",
    "dashboard": "https://gstudent.gitam.edu/Home",
    "attendance": "https://gstudent.gitam.edu/Student/Attendance",
    "timetable": "https://gstudent.gitam.edu/Student/TimeTable",
    "schedule": "https://gstudent.gitam.edu/Student/TimeTable",
    "courses": "https://gstudent.gitam.edu/Courses",
    "course": "https://gstudent.gitam.edu/Courses",
    "lms": "https://gstudent.gitam.edu/Courses",
    "assignments": "https://gstudent.gitam.edu/CourseWork/Assignments",
    "assignment": "https://gstudent.gitam.edu/CourseWork/Assignments",
    "results": "https://gstudent.gitam.edu/Results",
    "grades": "https://gstudent.gitam.edu/Results",
    "marks": "https://gstudent.gitam.edu/Results",
    "gpa": "https://gstudent.gitam.edu/Results",
    "fee": "https://gstudent.gitam.edu/Fee",
    "fees": "https://gstudent.gitam.edu/Fee",
    "dues": "https://gstudent.gitam.edu/Fee",
    "registration": "https://gstudent.gitam.edu/CourseRegistration",
    "reg": "https://gstudent.gitam.edu/CourseRegistration",
    "hallticket": "https://gstudent.gitam.edu/HallTicket",
    "admitcard": "https://gstudent.gitam.edu/HallTicket",
    "profile": "https://gstudent.gitam.edu/Student/Profile",
    "feedback": "https://gstudent.gitam.edu/Feedback",
    "logout": "https://gstudent.gitam.edu/Home/Logout"
}

COMMAND_ALIASES = {
    "open": ["open", "opn", "oepn", "goto", "go", "launch", "view", "start"],
    "logout": ["logout", "signout", "logoff", "signoff", "exit_session"],
    "attendance": ["attendance", "attendence", "atendance", "attndance", "att", "attend", "atndnc"],
    "timetable": ["timetable", "timetabl", "schedule", "routine"],
    "courses": ["courses", "course", "corse", "cours", "crs", "subject", "subjects", "lms"],
    "quiz": ["quiz", "quz", "qiuz", "quizz", "test", "assessment", "exam", "exm"],
    "download": ["download", "dowload", "downlod", "dwonload", "dwnload", "dl", "get", "materials", "material"],
    "submit": ["submit", "submt", "submitt", "upload", "upld", "assignment", "assigment"],
    "reg": ["reg", "register", "regester", "faculty", "fac", "registration"],
    "grades": ["grades", "grade", "results", "result", "marks", "gpa"],
    "fee": ["fee", "fees", "dues", "payment"],
    "style": ["style", "stlye", "sytle", "css", "customize", "look"],
    "theme": ["theme", "teme", "thme", "dark", "light", "mode"],
    "map": ["map", "routes", "info", "help", "structure"],
    "exit": ["exit", "quit", "q", "close", "bye"]
}


def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name).strip()


def resolve_command(user_cmd):
    clean = user_cmd.lower().strip()
    for canonical, aliases in COMMAND_ALIASES.items():
        if clean in aliases:
            return canonical
    all_cmds = list(COMMAND_ALIASES.keys())
    matches = difflib.get_close_matches(clean, all_cmds, n=1, cutoff=0.55)
    return matches[0] if matches else clean


def clean_orphan_locks():
    try:
        cmd = 'Get-CimInstance Win32_Process -Filter "name = \'brave.exe\'" | Where-Object { $_.CommandLine -like "*brave_profile*" } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }'
        subprocess.run(["powershell", "-Command", cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=4)
    except Exception:
        pass


def launch_brave_natively(url):
    clean_orphan_locks()
    target_url = url if url else PORTAL_HOME
    print(f"[GITAM] Opening in Brave (Profile 1) -> {target_url}")
    try:
        subprocess.Popen([
            BRAVE_EXE,
            "--profile-directory=Profile 1",
            target_url
        ])
        print("[SUCCESS] Launched successfully in Brave!")
        return True
    except Exception as e:
        print(f"[ERROR] Could not launch Brave: {e}")
        return False


def show_application_map():
    print("\n" + "=" * 70)
    print("GITAM GSTUDENT APPLICATION ARCHITECTURE & ROUTE MAP")
    print("=" * 70)
    print(f"{'SECTION / MODULE':<22} | {'COMMAND':<18} | DIRECT URL")
    print("-" * 70)
    print(f"{'Student Dashboard':<22} | {'open home':<18} | {PORTAL_ROUTES['home']}")
    print(f"{'Attendance System':<22} | {'attendance':<18} | {PORTAL_ROUTES['attendance']}")
    print(f"{'Class Timetable':<22} | {'timetable':<18} | {PORTAL_ROUTES['timetable']}")
    print(f"{'Courses & LMS':<22} | {'courses':<18} | {PORTAL_ROUTES['courses']}")
    print(f"{'Assignments':<22} | {'open assignments':<18} | {PORTAL_ROUTES['assignments']}")
    print(f"{'Semester Results':<22} | {'grades':<18} | {PORTAL_ROUTES['results']}")
    print(f"{'Fee Payments':<22} | {'fee':<18} | {PORTAL_ROUTES['fee']}")
    print(f"{'Course Registration':<22} | {'reg <faculty>':<18} | {PORTAL_ROUTES['registration']}")
    print(f"{'Exam Hall Ticket':<22} | {'open hallticket':<18} | {PORTAL_ROUTES['hallticket']}")
    print(f"{'Student Profile':<22} | {'open profile':<18} | {PORTAL_ROUTES['profile']}")
    print(f"{'Faculty Feedback':<22} | {'open feedback':<18} | {PORTAL_ROUTES['feedback']}")
    print("=" * 70)
    print("Tip: Type any command above to open that section directly in Brave!\n")


def edit_styles():
    print(f"\nOpening custom stylesheet in Notepad...")
    subprocess.Popen(["notepad.exe", CUSTOM_CSS_PATH])
    print("Edit your CSS rules, press Ctrl+S to save, and reload portal to see changes!")


def interactive_cli():
    print("=" * 68)
    print("[GITAM] GStudent Master Controller (Native & Zero-Friction)")
    print(f"Student ID: {STUDENT_ID} | Profile: Brave (Profile 1)")
    print("=" * 68)
    print("Command Shortcuts:")
    print("  open [tab/page]                 - Open dashboard or jump to any section")
    print("  attendance                      - Open live attendance directly in Brave")
    print("  timetable                       - Open class schedule / timetable")
    print("  courses                         - Open courses and LMS")
    print("  grades / results                - View grade card & exam results")
    print("  fee                             - View fee details & payment receipts")
    print("  map                             - Display complete portal routes & structure")
    print("  style                           - Open custom CSS in Notepad to change portal look")
    print("  exit                            - Quit CLI")
    print("=" * 68)

    while True:
        try:
            raw = input("\ngitam> ").strip()
            if not raw:
                continue

            parts = raw.split()
            first_word = parts[0].lower()
            cmd = resolve_command(first_word)

            if cmd != first_word:
                print(f"[AUTO-CORRECT] '{first_word}' -> '{cmd}'")

            if cmd == "exit":
                print("Exiting GStudent Controller.")
                break

            elif cmd == "map":
                show_application_map()

            elif cmd == "logout":
                print("[LOGOUT] Terminating active GStudent session...")
                launch_brave_natively("https://gstudent.gitam.edu/Home/Logout")

            elif cmd == "style":
                edit_styles()

            elif cmd == "open":
                if len(parts) > 1:
                    target = raw[len(parts[0]):].strip().lower()
                    matched_route = PORTAL_ROUTES.get(target)
                    if not matched_route:
                        close = difflib.get_close_matches(target, list(PORTAL_ROUTES.keys()), n=1, cutoff=0.5)
                        if close:
                            matched_route = PORTAL_ROUTES[close[0]]
                    launch_brave_natively(matched_route or PORTAL_HOME)
                else:
                    launch_brave_natively(PORTAL_HOME)

            elif cmd in PORTAL_ROUTES:
                launch_brave_natively(PORTAL_ROUTES[cmd])

            elif cmd == "quiz":
                launch_brave_natively(PORTAL_ROUTES["courses"])

            elif cmd in ["download", "dl"]:
                print(f"[ACTION] Opening Courses page to download materials...")
                launch_brave_natively(PORTAL_ROUTES["courses"])

            elif cmd == "submit":
                print(f"[ACTION] Opening Assignments page...")
                launch_brave_natively(PORTAL_ROUTES["assignments"])

            elif cmd == "reg":
                launch_brave_natively(PORTAL_ROUTES["registration"])

            elif cmd == "help":
                show_application_map()

            else:
                close = difflib.get_close_matches(raw.lower(), list(PORTAL_ROUTES.keys()), n=1, cutoff=0.5)
                if close:
                    launch_brave_natively(PORTAL_ROUTES[close[0]])
                else:
                    launch_brave_natively(PORTAL_HOME)

        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break
        except Exception as err:
            print(f"[ERROR] {err}")


def main():
    parser = argparse.ArgumentParser(description="GStudent Master Controller")
    parser.add_argument("command", nargs="?", default="cli", help="Command to run")
    parser.add_argument("--target", help="Specific target to open")

    args = parser.parse_args()

    if args.command == "open":
        route = PORTAL_ROUTES.get(args.target.lower()) if args.target else PORTAL_HOME
        launch_brave_natively(route)
    elif args.command in PORTAL_ROUTES:
        launch_brave_natively(PORTAL_ROUTES[args.command])
    elif args.command == "map":
        show_application_map()
    elif args.command == "style":
        edit_styles()
    else:
        interactive_cli()


if __name__ == "__main__":
    main()
