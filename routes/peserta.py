from flask import Blueprint, render_template, request, redirect, flash, get_flashed_messages
from flask import get_flashed_messages
from datetime import datetime
from db import get_db

peserta_bp = Blueprint("peserta", __name__)

@peserta_bp.route("/index-peserta", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nama_lengkap = request.form.get("nama_lengkap")
        tempat_lahir = request.form.get("tempat_lahir")
        tanggal_raw = request.form.get("tanggal_lahir")
        gender = request.form.get("gender")
        email = request.form.get("email")
        nomor_hp = request.form.get("nomor_hp")
        provinsi = request.form.get("provinsi")
        kota = request.form.get("kota")
        kecamatan = request.form.get("kecamatan")
        kelurahan = request.form.get("kelurahan")
        kode_pos = request.form.get("kode_pos")
        status_pernikahan = request.form.get("status_pernikahan")
        alamat_lengkap = request.form.get("alamat_lengkap")

        if not nama_lengkap or not email:
            flash("Nama & Email wajib diisi", "danger")
            return redirect("/index-peserta")

        tanggal_lahir = None
        if tanggal_raw:
            tanggal_lahir = datetime.strptime(
                tanggal_raw, "%d/%m/%Y"
            ).strftime("%Y-%m-%d")

        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO registrations
            (nama_lengkap, tempat_lahir, tanggal_lahir, gender, email,
             nomor_hp, provinsi, kota, kecamatan, kelurahan, kode_pos,
             status_pernikahan, alamat_lengkap)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            nama_lengkap, tempat_lahir, tanggal_lahir, gender, email,
            nomor_hp, provinsi, kota, kecamatan, kelurahan, kode_pos,
            status_pernikahan, alamat_lengkap
        ))
        db.commit()
        cursor.close()
        db.close()

        flash("Data peserta berhasil disimpan", "success")
        return redirect("/index-peserta")


    return render_template("peserta/index-peserta.html", page="peserta")