import streamlit as st
from views import book_page
from views import member_page
from views import borrow_page
from views import admin_page
from views import login_page
from views import report_page


# =========================
# Init session state (login/logout)
# =========================
if "is_logged_in" not in st.session_state:
    st.session_state["is_logged_in"] = False

if "user" not in st.session_state:
    st.session_state["user"] = None

if "page" not in st.session_state:
    st.session_state["page"] = "books"

# =========================
# Hide Streamlit auto multipage nav
# =========================
st.markdown(
    """
    <style>
    section[data-testid="stSidebarNav"] {display: none !important;}
    div[data-testid="stSidebarNav"] {display: none !important;}
    nav[data-testid="stSidebarNav"] {display: none !important;}
    div[data-testid="stSidebarNavItems"] {display: none !important;}
    div[data-testid="stSidebarNavSeparator"] {display: none !important;}
    aside ul:has(a[href*="?page="]) {display: none !important;}
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# Page config
# =========================
st.set_page_config(
    page_title="ระบบยืม-คืนหนังสือ",
    page_icon="📚",
    layout="wide"
)

# =========================
# Login Gate
# =========================
if not st.session_state["is_logged_in"]:
    login_page.render_login()
    st.stop()

# =========================
# Header (after login)
# =========================
st.title("📚 ระบบยืม-คืนหนังสือ (Streamlit + SQLite)")
st.write("ตัวอย่าง Web App เชื่อมฐานข้อมูล (โครงสร้างแนว MVC)")

# =========================
# Sidebar: user info + logout
# =========================
user = st.session_state.get("user") or {}

st.sidebar.markdown(f"👤 ผู้ใช้: **{user.get('username', '-')}**")
st.sidebar.markdown(f"🔑 บทบาท: **{user.get('role', '-')}**")

if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.session_state["is_logged_in"] = False
    st.session_state["user"] = None
    st.session_state["page"] = "books"
    st.rerun()

# =========================
# Sidebar menu title
# =========================
st.sidebar.markdown(
    """
    <style>
    .menu-title {
        text-align: center;
        font-size: 22px;
        font-weight: 700;
        margin-top: 10px;
        margin-bottom: 20px;
    }
    </style>
    <div class="menu-title">เมนู</div>
    """,
    unsafe_allow_html=True
)

# =========================
# Navigation helper
# =========================
def nav_button(label, key, icon=""):
    active = st.session_state.page == key
    btn = st.sidebar.button(
        f"{icon} {label}",
        key=f"btn_{key}",
        use_container_width=True
    )
    if btn:
        st.session_state.page = key
        st.rerun()

# =========================
# Role-based menu
# =========================
role = user.get("role")

nav_button("หนังสือ", "books", "📚")
nav_button("สมาชิก", "members", "👤")
nav_button("ยืม-คืน", "borrows", "🔄")

# (เผื่ออนาคต)
if role == "admin":
    nav_button("จัดการผู้ใช้", "admin", "🛠️")
    nav_button("รายงาน", "reports", "📊")


# ---------- Routing ----------
# ป้องกัน staff เข้าหน้า admin ด้วยการบังคับ routing
# เอาการบังคับ staff ไปหน้า borrows ออก (staff ทำได้ทุกอย่างแล้ว)

if st.session_state.page == "books":
    book_page.render_book()

elif st.session_state.page == "members":
    member_page.render_member()

elif st.session_state.page == "borrows":
    borrow_page.render_borrow()

elif st.session_state.page == "reports":
    if role != "admin":
        st.warning("⚠ หน้านี้อนุญาตเฉพาะผู้ดูแลระบบ (admin) เท่านั้น")
    else:
        report_page.render_report()

elif st.session_state.page == "admin":
    # guard กัน staff เข้าหน้า admin แม้พยายามเปลี่ยน state เอง
    if role != "admin":
        st.warning("⚠ หน้านี้อนุญาตเฉพาะผู้ดูแลระบบ (admin) เท่านั้น")
    else:
        admin_page.render_admin()

else:
    # fallback
    book_page.render_book()

