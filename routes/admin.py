from flask import Blueprint, render_template, session, redirect, request, send_file
from models.user_model import get_all_users, delete_user, update_user
from models.registration_model import (get_all_registrations, update_registration, get_registration_by_id, get_dashboard_stats, delete_register)
from werkzeug.security import generate_password_hash
from datetime import datetime
import pandas as pd
from io import BytesIO

admin_bp = Blueprint("admin", __name__, template_folder="templates")

def admin_login_required():
    return "admin_id" in session


@admin_bp.route("/")
def admin_root():
    if not admin_login_required():
        return redirect("/login")
    return redirect("/admin/dashboard")

# --------untuk masuk ke dashboard--------
@admin_bp.route("/dashboard")
def dashboard():
    if not admin_login_required():
        return redirect("/login")

    stats = get_dashboard_stats()

    return render_template(
        "admin/index.html",   # 🔥 HARUS index.html
        page="dashboard",
        stats=stats
    )


# -------- masuk halaman user--------
@admin_bp.route("/users")
def users_list():
    if not admin_login_required():
        return redirect("/login")
    return render_template("admin/index.html", page="users", users=get_all_users())

# --------untuk menghapus user--------
@admin_bp.route("/user/delete", methods=["POST"])
def delete_user_admin():
    if not admin_login_required():
        return redirect("/login")
    delete_user(request.form.get("id"))
    return redirect("/admin/users")

# --------untuk mengedit user--------
@admin_bp.route("/user/edit")
def edit_user():
    if not admin_login_required():
        return redirect("/login")

    user_id = request.args.get("id")
    users = get_all_users()
    user = next((u for u in users if str(u["id"]) == str(user_id)), None)

    return render_template("admin/index.html", page="edit_user", user=user)

# --------untuk mengupdate user--------
@admin_bp.route("/user/update", methods=["POST"])
def update_user_admin():
    if not admin_login_required():
        return redirect("/login")

    user_id = request.form.get("id")
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    if password:
        password = generate_password_hash(password)

    update_user(user_id, name, email, password)

    return redirect("/admin/users")

# -------- masuk halaman register--------
@admin_bp.route("/register")
def register():
    if not admin_login_required():
        return redirect("/login")

    registrations = get_all_registrations()
    return render_template("admin/index.html", page="register", registrations=registrations)

# --------untuk mengedit register--------
@admin_bp.route("/register/edit")
def edit_register():
    if not admin_login_required():
        return redirect("/login")

    reg_id = request.args.get("id")
    register = get_registration_by_id(reg_id)

    return render_template(
    "admin/index.html",
    page="edit_register",
    register=register,
    now=datetime.now()
)

# --------untuk mengupdate register--------
@admin_bp.route("/register/update", methods=["POST"])
def update_register():
    if not admin_login_required():
        return redirect("/login")

    update_registration(
        request.form
    )

    return redirect("/admin/register")

# --------untuk logout--------
@admin_bp.route("/logout")
def logout():
    session.clear()   # hapus semua session
    return redirect("/login")

#--------untuk menghapus user--------
@admin_bp.route("/register/delete", methods=["POST"])
def delete_register_admin():
    if not admin_login_required():
        return redirect("/login")
    delete_register(request.form.get("id"))
    return redirect("/admin/register")


# --------untuk download excel--------
@admin_bp.route("/register/export")
def export_register_excel():
    if not admin_login_required():
        return redirect("/login")

    data = get_all_registrations()

    df = pd.DataFrame(data)

    # sort terbaru (kalau belum pernah diupdate, pakai created_at)
    df = df.sort_values(
        by=["updated_at", "created_at"],
        ascending=False,
        na_position="last"
    )

    df = df.rename(columns={
        "nama_lengkap": "Nama Lengkap",
        "tempat_lahir": "Tempat Lahir",
        "tanggal_lahir": "Tanggal Lahir",
        "gender": "Gender",
        "email": "Email",
        "nomor_hp": "Nomor HP",
        "provinsi": "Provinsi",
        "kota": "Kota",
        "kecamatan": "Kecamatan",
        "kelurahan": "Kelurahan",
        "kode_pos": "Kode Pos",
        "status_pernikahan": "Status Pernikahan",
        "alamat_lengkap": "Alamat Lengkap",
        "created_at": "Created At",
        "updated_at": "Updated At",
    })

    filename = f"laporan_registrasi_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"

    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Registrations")

    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name=filename,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )