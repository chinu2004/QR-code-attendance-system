
 # 📷 QR Code Attendance System

A web-based attendance management system that uses **QR codes** to mark student attendance in real time — built with Flask and deployable anywhere.

🔗 Live Demo: https://qr-code-attendance-system-project.onrender.com

---

## ✨ Features

- 🎓 **Register students** with name, roll number, department, year, and section
- 🔳 **Auto-generate unique QR codes** per student on registration
- 📷 **Scan QR codes** via webcam to mark attendance instantly
- 🚫 **Duplicate prevention** — same student can't be marked twice
- 📥 **Download attendance** as a CSV file anytime
- 🗑️ **Admin panel** to delete all data securely (password + confirmation)
- 🕐 **IST timestamps** recorded for every attendance entry

---

## Tech Stack

| Layer | Tool |
|---|---|
| Backend | [Flask](https://flask.palletsprojects.com/) |
| QR Generation | [qrcode](https://pypi.org/project/qrcode/) |
| QR Scanning | Browser-based webcam (JS) |
| Data Storage | CSV files |
| Timezone | `pytz` (Asia/Kolkata) |
| Deployment | [Render](https://render.com) |

---

## 📁 Project Structure

```
QR-code-attendance-system/
│
├── app.py                  # Main Flask application
├── students.csv            # Registered student data
├── attendance.csv          # Attendance log with timestamps
├── requirements.txt        # Python dependencies
│
├── static/
│   └── qrcodes/            # Generated QR code images
│
└── templates/
    ├── index.html          # Home page
    ├── add_user.html       # Student registration page
    ├── scan.html           # QR scanner page
    └── delete_all.html     # Data deletion page
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/chinu2004/QR-code-attendance-system.git
cd QR-code-attendance-system
```

### 2. Create and activate a virtual environment

```bash
python -m venv myvenv

# Windows
myvenv\Scripts\activate

# macOS / Linux
source myvenv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

---

## 🔐 Admin Password

The default admin password is `admin123`. Change it in `app.py` before deploying:

```python
PASSWORD = "your_secure_password"
```

---

## 🚀 Routes

| Route | Description |
|---|---|
| `/` | Home page |
| `/add_user` | Register a new student & generate QR |
| `/scan` | Open QR scanner to mark attendance |
| `/mark_attendance` | AJAX endpoint — called by the scanner |
| `/download_csv` | Download attendance log as CSV |
| `/delete_all` | Delete all students, QR codes & attendance |

---

## 📋 How It Works

1. **Admin registers a student** → a unique QR code is generated and saved.
2. **Student shows their QR code** on the scan page.
3. **Webcam scans the QR** → attendance is marked via an AJAX call.
4. **Duplicate check** ensures a student can only be marked once per session.
5. **Download the CSV** at any time for records.

---

## 📦 Requirements

flask
qrcode[pil]
pytz
 

 

 

