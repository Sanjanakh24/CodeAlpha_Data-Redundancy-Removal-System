from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("data.db")

@app.route("/")
def home():
    return "Data Redundancy Removal System is running in the cloud!"

@app.route("/add", methods=["POST"])
def add_user():
    data = request.json
    name = data["name"]
    email = data["email"]
    phone = data["phone"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        phone TEXT
    )
    """)

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
