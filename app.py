import os
import csv
import qrcode
import random
import string
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file

app = Flask(__name__)
app.secret_key = "super_secret"  # For flash messages

# Folders & files
QR_FOLDER = "static/qrcodes"
STUDENT_FILE = "students.csv"
ATTENDANCE_FILE = "attendance.csv"
PASSWORD = "admin123"

os.makedirs(QR_FOLDER, exist_ok=True)

# Ensure CSV files exist
if not os.path.exists(STUDENT_FILE):
    with open(STUDENT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Roll No", "Name", "Dept", "Year", "Section"])

if not os.path.exists(ATTENDANCE_FILE):
    with open(ATTENDANCE_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Roll No", "Name", "Dept", "Year", "Section", "Timestamp"])

# ------------------ Helper ------------------
def generate_unique_qr(roll_no):
    random_id = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
    return f"{roll_no}_{random_id}"

# ------------------ Routes ------------------
@app.route("/")
def home():
    return render_template("index.html")

# Add student / generate QR
@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        password = request.form["password"]
        if password != PASSWORD:
            flash("❌ Incorrect password!")
            return redirect(url_for("add_user"))

        name = request.form["name"]
        roll = request.form["roll"]
        dept = request.form["dept"]
        year = request.form["year"]
        section = request.form["section"]

        # Check duplicate
        with open(STUDENT_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Roll No"].startswith(roll):
                    qr_files = os.listdir(QR_FOLDER)
                    for file in qr_files:
                        if file.startswith(row["Roll No"]):
                            flash("⚠ Duplicate! Showing existing QR.")
                            return render_template("add_user.html", qr_image=file)

        # Generate QR
        unique_id = generate_unique_qr(roll)
        qr_filename = f"{unique_id}.png"
        qr_img = qrcode.make(unique_id)
        qr_img.save(os.path.join(QR_FOLDER, qr_filename))

        # Save student
        with open(STUDENT_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([unique_id, name, dept, year, section])

        flash("✅ Student added & QR generated!")
        return render_template("add_user.html", qr_image=qr_filename)

    return render_template("add_user.html", qr_image=None)

# Delete all data
@app.route("/delete_all", methods=["GET", "POST"])
def delete_all():
    if request.method == "POST":
        password = request.form["password"]
        confirm_text = request.form["confirm_text"]

        if password != PASSWORD:
            flash("❌ Incorrect password!")
            return redirect(url_for("delete_all"))

        if confirm_text != "DELETE":
            flash("⚠ You must type DELETE to confirm!")
            return redirect(url_for("delete_all"))

        # Delete QR codes
        for file in os.listdir(QR_FOLDER):
            os.remove(os.path.join(QR_FOLDER, file))

        # Reset CSVs
        for file in [STUDENT_FILE, ATTENDANCE_FILE]:
            with open(file, "w", newline="") as f:
                writer = csv.writer(f)
                if file == STUDENT_FILE:
                    writer.writerow(["Roll No", "Name", "Dept", "Year", "Section"])
                else:
                    writer.writerow(["Roll No", "Name", "Dept", "Year", "Section", "Timestamp"])

        flash("✅ All QR codes and data deleted successfully!")
        return redirect(url_for("home"))

    return render_template("delete_all.html")

# Download attendance CSV
@app.route("/download_csv")
def download_csv():
    return send_file(ATTENDANCE_FILE, as_attachment=True)

# QR scanner page
@app.route("/scan")
def scan():
    return render_template("scan.html")

# AJAX endpoint for attendance
@app.route('/mark_attendance', methods=["POST"])
def mark_attendance():
    data = request.get_json()
    qr_data = data.get("qr_data")
    if not qr_data:
        return jsonify({"status": "error", "message": "No QR data received"})

    qr_data = qr_data.strip()  # remove extra whitespace

    # Look up student details
    student = None
    with open(STUDENT_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Roll No"] == qr_data:
                student = row
                break

    if not student:
        return jsonify({"status": "error", "message": f"Student not found for QR {qr_data}"})

    # Check duplicate
    already_marked = False
    if os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, "r") as f:
            reader = csv.DictReader(f)
            for r in reader:
                if r["Roll No"] == qr_data:
                    already_marked = True
                    break

    if already_marked:
        return jsonify({"status": "exists", "message": f"{student['Name']} already marked!"})

    # Append full student details + timestamp
    fieldnames = ["Roll No", "Name", "Dept", "Year", "Section", "Timestamp"]
    with open(ATTENDANCE_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        # Write header if empty
        if os.stat(ATTENDANCE_FILE).st_size == 0:
            writer.writeheader()
        writer.writerow({
            "Roll No": student["Roll No"],
            "Name": student["Name"],
            "Dept": student["Dept"],
            "Year": student["Year"],
            "Section": student["Section"],
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    return jsonify({"status": "success", "message": f"Attendance marked for {student['Name']}"})

# ------------------ Run ------------------
if __name__ == "__main__":
    app.run(debug=True)
