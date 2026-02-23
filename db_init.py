import sqlite3
import hashlib # 👈 ต้องมี

def hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()

conn = sqlite3.connect("library.db")
c = conn.cursor()

# ตาราง books
c.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT,
    status TEXT DEFAULT 'available'
)
""")

# ตาราง members
c.execute("""
CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    gender TEXT,
    email TEXT UNIQUE,
    phone TEXT,
    is_active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

# -------------------------
# users (NEW)
# -------------------------

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('admin','staff')),
    is_active INTEGER NOT NULL DEFAULT 1
)
""")

# -------------------------
# seed admin (ถ้ายังไม่มี user เลย)
# -------------------------

c.execute("SELECT COUNT(*) FROM users")
(count,) = c.fetchone()

if count == 0:
    c.execute(
        """
        INSERT INTO users (username, password_hash, role, is_active)
        VALUES (?, ?, ?, ?)
        """,
        ("admin", hash_password("1234"), "admin", 1)
    )

# -------------------------
# commit & close
# -------------------------
conn.commit()
conn.close()


print("✅ สร้างฐานข้อมูลและตารางเรียบร้อยแล้ว")
