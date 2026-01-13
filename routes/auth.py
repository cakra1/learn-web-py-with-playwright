from flask import Blueprint, render_template, request, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db
import uuid
import smtplib

auth_bp = Blueprint("auth", __name__)

# ================= LOGIN =================
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "SELECT id, password_hash FROM users WHERE email=%s",
            (email,)
        )
        user = cursor.fetchone()
        cursor.close()
        db.close()

        if not user or not check_password_hash(user["password_hash"], password):
             flash("Email atau password salah", "danger")
             return redirect("/login")

        # ✅ PENTING
        session["admin_id"] = user["id"]

        flash("Login berhasil", "login")
        return redirect("/admin/dashboard")

    return render_template("auth/index.html", page="login")


# ================= REGISTER =================
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        confirm = request.form.get("confirm_password", "").strip()  # ✅ FIX DI SINI

        if not name or not email or not password:
            flash("Semua field wajib diisi", "danger")
            return redirect("/register")

        if password != confirm:
            flash("Password tidak sama", "danger")
            return redirect("/register")

        password_hash = generate_password_hash(password)

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
        if cursor.fetchone():
            cursor.close()
            db.close()
            flash("Email sudah terdaftar", "danger")
            return redirect("/register")

        cursor.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (%s,%s,%s)",
            (name, email, password_hash)
        )
        db.commit()
        cursor.close()
        db.close()

        flash("Akun berhasil dibuat, silakan login", "success")
        return redirect("/login")

    return render_template("auth/index.html", page="register")


# ================= FORGOT PASSWORD =================
@auth_bp.route("/forgot", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"]
        token = str(uuid.uuid4())

        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "UPDATE users SET reset_token=%s WHERE email=%s",
            (token, email)
        )
        db.commit()

        cursor.close()
        db.close()

        # BYPASS EMAIL → LANGSUNG KE RESET PAGE
        return redirect(f"/reset/{token}")

    return render_template("auth/index.html", page="forgot")

# ================= RESET PASSWORD =================
@auth_bp.route("/reset/<token>", methods=["GET", "POST"])
def reset_password(token):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT id FROM users WHERE reset_token=%s", (token,))
    user = cursor.fetchone()

    if not user:
        flash("Token tidak valid", "danger")
        cursor.close()
        db.close()
        return redirect("/")

    if request.method == "POST":
        password = request.form["password"]
        confirm = request.form["confirm_password"]

        if password != confirm:
            flash("Password tidak sama", "danger")
            return redirect(request.url)

        password_hash = generate_password_hash(password)

        cursor.execute(
            "UPDATE users SET password_hash=%s, reset_token=NULL WHERE id=%s",
            (password_hash, user["id"])
        )
        db.commit()

        session["user_id"] = user["id"]  # ✅ AUTO LOGIN
        flash("Password berhasil direset & login otomatis", "success")

        cursor.close()
        db.close()
        return redirect("/")

    cursor.close()
    db.close()
    return render_template("auth/index.html", page="reset_password")

# ================= fungsi kirim email =================
def send_reset_email(to_email, reset_link):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Reset Password"
    msg["From"] = EMAIL_SENDER
    msg["To"] = to_email

    html = f"""
    <html>
      <body>
        <p>Halo,</p>
        <p>Klik link berikut untuk reset password:</p>
        <p><a href="{reset_link}">Reset Password</a></p>
        <p>Jika kamu tidak meminta reset, abaikan email ini.</p>
      </body>
    </html>
    """

    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, to_email, msg.as_string())