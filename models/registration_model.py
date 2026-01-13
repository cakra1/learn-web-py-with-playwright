from db import get_db
import pymysql

# ------------- tampilkan semua data -------------
def get_all_registrations():
    conn = get_db()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute("""
        SELECT 
            id,
            nama_lengkap,
            tempat_lahir,
            tanggal_lahir,
            gender,
            email,
            nomor_hp,
            status_pernikahan,
            CONCAT(
                alamat_lengkap, ' ',
                kelurahan, ' ',
                kecamatan, ' ',
                kota, ' ',
                provinsi, ' ',
                kode_pos
            ) AS alamat_lengkap,
            created_at,
            updated_at
        FROM registrations
        ORDER BY created_at DESC
    """)

    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


# ------------- ambil 1 data -------------
def get_registration_by_id(reg_id):
    conn = get_db()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute("SELECT * FROM registrations WHERE id=%s", (reg_id,))
    data = cursor.fetchone()

    cursor.close()
    conn.close()
    return data


# ------------- update data -------------
def update_registration(form):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE registrations SET
            nama_lengkap=%s,
            tempat_lahir=%s,
            tanggal_lahir=%s,
            gender=%s,
            email=%s,
            nomor_hp=%s,
            provinsi=%s,
            kota=%s,
            kecamatan=%s,
            kelurahan=%s,
            kode_pos=%s,
            status_pernikahan=%s,
            alamat_lengkap=%s,
            updated_at = NOW()
        WHERE id=%s
    """, (
        form["nama_lengkap"],
        form["tempat_lahir"],
        form["tanggal_lahir"],
        form["gender"],
        form["email"],
        form["nomor_hp"],
        form["provinsi"],
        form["kota"],
        form["kecamatan"],
        form["kelurahan"],
        form["kode_pos"],
        form["status_pernikahan"],
        form["alamat_lengkap"],
        form["id"]
    ))

    conn.commit()
    cursor.close()
    conn.close()

 #---------- menghapus data di database ----------
def delete_register(register_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM registrations WHERE id = %s",
        (register_id,)
    )

    conn.commit()
    cursor.close()
    conn.close()


# ------------- DASHBOARD FIX -------------
def get_dashboard_stats():
    conn = get_db()
    cursor = conn.cursor(pymysql.cursors.DictCursor)  # ← WAJIB

    cursor.execute("SELECT COUNT(*) AS total FROM registrations")
    total = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS male FROM registrations WHERE gender='Male'")
    male = cursor.fetchone()["male"]

    cursor.execute("SELECT COUNT(*) AS female FROM registrations WHERE gender='Female'")
    female = cursor.fetchone()["female"]

    cursor.close()
    conn.close()

    return {
        "total": total,
        "male": male,
        "female": female
    }
