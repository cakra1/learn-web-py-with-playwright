    
from flask import Flask, redirect
from routes.peserta import peserta_bp
from routes.admin import admin_bp
from routes.auth import auth_bp

app = Flask(__name__)
app.secret_key = "secret-key"

app.register_blueprint(peserta_bp)
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(auth_bp)

@app.route("/")
def home():
    return redirect("/login")

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)
