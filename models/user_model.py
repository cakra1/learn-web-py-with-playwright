from db import get_db

# ---------- memanpilkan database ke web ----------
def get_all_users():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, email, created_at
        FROM users
        ORDER BY created_at DESC
    """)

    users = cursor.fetchall()

    cursor.close()
    conn.close()
    return users

# ---------- menghapus data di database ----------
def delete_user(user_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM users WHERE id = %s",
        (user_id,)
    )

    conn.commit()
    cursor.close()
    conn.close()


# ---------- update data di database ----------
def update_user(user_id, name, email, password=None):
    conn = get_db()
    cursor = conn.cursor()

    if password:
        cursor.execute("""
            UPDATE users
            SET name=%s, email=%s, password_hash=%s
            WHERE id=%s
        """, (name, email, password, user_id))
    else:
        cursor.execute("""
            UPDATE users
            SET name=%s, email=%s
            WHERE id=%s
        """, (name, email, user_id))

    conn.commit()
