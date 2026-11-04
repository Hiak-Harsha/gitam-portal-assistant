# ⚡ GITAM GStudent Portal Master Assistant & CLI

A terminal controller, auto-popup blocker, and customization suite for the **GITAM University Student Portal** (`gstudent.gitam.edu`).

Designed for high efficiency, sub-second latency, and zero friction from the Windows command line.

---

## 🚀 Features

- **⚡ Instant Native Portal Launcher:** Launch directly into the authenticated GStudent portal in Brave without automation lags.
- **🛡️ Auto-Popup Blocker:** Silently dismisses university announcement modals and backdrops.
- **⌨️ Universal Command-Line Navigation:** Jump directly to any section:
  - `attendance` ➔ Live attendance table
  - `timetable` ➔ Class schedules
  - `courses` ➔ Courses and LMS modules
  - `grades` ➔ Semester grade cards & SGPA/CGPA
  - `fee` ➔ Fee dues & payment history
  - `map` ➔ Complete interactive architectural route map
- **📥 Modular Course Materials Downloader:** Automatically downloads course documents and organizes them by unit into `GITAM_Materials/<Course>/<Unit>/`.
- **🎨 Custom Appearance & Theming:** Custom CSS stylesheet (`custom_styles.css`) for permanent dark mode, custom typography, and cleaner layout.
- **💡 Smart Typo Tolerance:** Automatically corrects mistyped commands (e.g. `attndnc` ➔ `attendance`, `dowload` ➔ `download`).
- **🔒 Privacy First:** Credentials are stored locally in `.env` and never tracked in version control.

---

## 📁 Repository Structure

```text
gitam-portal-assistant/
├── gitam_app.py          # Main CLI automation engine & route controller
├── gitam.cmd             # Windows Command Prompt launcher
├── gitam_prompt.pyw      # Quick Desktop HUD command bar (GUI)
├── requirements.txt      # Python dependencies
├── .env.example          # Template for student credentials
├── .gitignore            # Git exclusion rules (protects credentials & caches)
└── extension/            # Browser Extension for Brave / Chrome
    ├── manifest.json     # Manifest V3 configuration
    ├── content.js        # In-page helper & popup blocker
    ├── style.css         # Styling for optional in-page CLI
    └── custom_styles.css # User-customizable CSS stylesheet
```

---

## 🛠️ Quick Setup

### 1. Prerequisites
- **Python 3.10+**
- **Brave Browser** (or Google Chrome)

### 2. Configure Credentials
Copy `.env.example` to `.env`:
```cmd
copy .env.example .env
```
Open `.env` and add your details:
```env
GITAM_STUDENT_ID=your_registration_number
GITAM_PASSWORD=your_portal_password
```

### 3. Load the Extension into Brave / Chrome
1. Open Brave and go to `brave://extensions`.
2. Toggle **Developer mode** to **ON** (top right).
3. Click **Load unpacked** (top left).
4. Select the `extension/` folder in this repository.

---

## 💻 CLI Command Reference

Run the master controller:
```cmd
gitam
```

| Command | Action |
| :--- | :--- |
| `open [target]` | Opens GStudent or jumps directly to a specific section |
| `attendance` | Jumps straight to the live attendance records |
| `timetable` | Opens the class timetable schedule |
| `courses` | Opens active registered courses & LMS |
| `grades` | Opens semester exam results and grade sheets |
| `fee` | Opens fee details & payment receipts |
| `quiz <course>` | Opens the specified course and locates active quizzes |
| `download <course>` | Downloads course resources and sorts them into Unit folders |
| `style` | Opens `custom_styles.css` in Notepad to customize portal look |
| `map` | Displays the complete architectural route map |
| `exit` | Closes the CLI session |

---

## 🎨 Customizing Portal Look

Run `style` or open `extension/custom_styles.css` in any editor:
- **Dark Mode:** Uncomment the modern dark mode block.
- **Hide Elements:** Add any unwanted selectors to `display: none !important;`.
- **Custom Fonts:** Apply your preferred fonts (Inter, Roboto, Segoe UI).

---

## 📜 License
MIT License. Built for personal educational productivity.
