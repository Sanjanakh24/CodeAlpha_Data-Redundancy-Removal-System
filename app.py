import os
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

DB_NAME = "data.db"

# -------------------------
# Database helpers
# -------------------------
def get_db():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Initialize DB at startup (IMPORTANT for Render Free)
init_db()

# -------------------------
# Browser UI (GET + POST)
# -------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    message = ""

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")

        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (name, email, phone) VALUES (?, ?, ?)",
                (name, email, phone)
            )
            conn.commit()
            message = "✅ Unique data stored successfully"
        except sqlite3.IntegrityError:
            message = "❌ Duplicate data detected (email already exists)"
        finally:
            conn.close()

    return f"""
    <h2>Data Redundancy Removal System</h2>

    <form method="post">
        <label>Name:</label><br>
        <input type="text" name="name" required><br><br>

        <label>Email:</label><br>
        <input type="email" name="email" required><br><br>

        <label>Phone:</label><br>
        <input type="text" name="phone" required><br><br>

        <input type="submit" value="Add User">
    </form>

    <p><b>{message}</b></p>
    """

# -------------------------
# API Endpoint (POST JSON)
# -------------------------
@app.route("/add", methods=["POST"])
def add_user():
    data = request.get_json()

    if not data:
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400

    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")

    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (name, email, phone) VALUES (?, ?, ?)",
            (name, email, phone)
        )
        conn.commit()
        return jsonify({"status": "success", "message": "Unique data stored"})
    except sqlite3.IntegrityError:
        return jsonify({"status": "error", "message": "Duplicate data detected"})
    finally:
        conn.close()

# -------------------------
# App runner
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
