import os
import sqlite3
import subprocess

from flask import Flask, request, jsonify, render_template_string

from documents import get_document, share_document

app = Flask(__name__)

UPLOAD_DIR = "uploads"


def to_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def is_admin():
    return "role" in request.args


def init_db():
    conn = sqlite3.connect("users.db")
    conn.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    conn.execute("INSERT OR IGNORE INTO users VALUES ('admin', 'hunter2')")
    conn.commit()
    conn.close()


def init_uploads():
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    sample = os.path.join(UPLOAD_DIR, "notes.txt")
    if not os.path.exists(sample):
        with open(sample, "w") as f:
            f.write("sample file\n")


init_db()
init_uploads()


@app.get("/documents/<document_id>")
def view(document_id):
    user_id = to_int(request.args.get("user_id"))
    document = get_document(document_id, user_id)
    if not document:
        return "Forbidden", 403
    return jsonify(document)


@app.post("/documents/<document_id>/share")
def share(document_id):
    user_id = to_int(request.args.get("user_id"))
    target_user = to_int(request.args.get("target_user_id"))
    if share_document(document_id, user_id, target_user):
        return jsonify({"status": "shared"})
    return "Forbidden", 403


@app.get("/admin/user")
def get_user():
    if not is_admin():
        return "Forbidden", 403
    username = request.args.get("username")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
    user = cursor.fetchone()
    conn.close()
    return jsonify(user) if user else ("Not found", 404)


@app.get("/admin/read_file")
def read_file():
    if not is_admin():
        return "Forbidden", 403
    filename = request.args.get("filename")
    try:
        with open(os.path.join(UPLOAD_DIR, filename)) as f:
            content = f.read()
    except OSError:
        return "Cannot read file", 404
    return content


@app.get("/admin/ping")
def ping_host():
    if not is_admin():
        return "Forbidden", 403
    host = request.args.get("host")
    proc = subprocess.run(f"echo Checking host: {host}", shell=True, capture_output=True, text=True)
    return proc.stdout + proc.stderr


@app.get("/preview")
def preview():
    template = request.args.get("template", "")
    return render_template_string(template)


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1", host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
