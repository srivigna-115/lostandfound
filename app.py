from flask import Flask, render_template, request, redirect, url_for, flash
import os, sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "devops-demo-secret")
DB_PATH = os.environ.get("DB_PATH", "/app/data/items.db")

def connect_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with connect_db() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT, item_name TEXT NOT NULL,
            status TEXT NOT NULL, location TEXT NOT NULL, description TEXT NOT NULL,
            contact TEXT NOT NULL, created_at TEXT NOT NULL)''')
        conn.commit()

@app.route("/")
def home():
    status = request.args.get("status", "All")
    with connect_db() as conn:
        if status in ("Lost", "Found"):
            items = conn.execute("SELECT * FROM items WHERE status=? ORDER BY id DESC", (status,)).fetchall()
        else:
            items = conn.execute("SELECT * FROM items ORDER BY id DESC").fetchall()
    return render_template("index.html", items=items, selected_status=status)

@app.route("/report", methods=["POST"])
def report():
    fields = [request.form.get(k, "").strip() for k in ("item_name", "status", "location", "description", "contact")]
    item_name, status, location, description, contact = fields
    if not all(fields) or status not in ("Lost", "Found"):
        flash("Please complete every field.")
        return redirect(url_for("home"))
    with connect_db() as conn:
        conn.execute("INSERT INTO items (item_name,status,location,description,contact,created_at) VALUES (?,?,?,?,?,?)",
                     (item_name, status, location, description, contact, datetime.now().strftime("%d %b %Y, %I:%M %p")))
        conn.commit()
    flash("Your item report was added successfully.")
    return redirect(url_for("home"))

@app.route("/health")
def health():
    return {"status": "healthy", "application": "Campus Lost and Found Portal"}, 200

init_db()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
