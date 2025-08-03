import streamlit as st
import hashlib

# Demo user database (replace with real DB in production)
USERS = {
    "admin": {"password": "admin123", "role": "Admin"},
    "customer": {"password": "cust123", "role": "Customer"},
    "engineer": {"password": "eng123", "role": "Engineer"},
}

ROLES = ["Admin", "Customer", "Engineer"]

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_form():
    st.session_state['login_error'] = ''
    st.markdown("""
        <style>
        body {
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%) !important;
        .centered-login {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            min-height: 30vh;
        }
        .login-card-vibrant {
            background: rgba(255,255,255,0.97);
            border-radius: 32px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.25);
            padding: 0.5em 1.2em 0.5em 1.2em;
            max-width: 440px;
            width: 100%;
            margin: 0 auto;
            text-align: center;
            position: relative;
        }
        .login-heading-main {
            font-size: 2em;
            font-weight: 900;
            color: #ff512f;
            margin: 0 !important;
            padding: 0 !important;
            letter-spacing: 1.5px;
            font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
        }
        .login-logo {
            width: 56px;
            height: 56px;
            margin: 0 !important;
            border-radius: 16px;
            box-shadow: 0 2px 8px #a5b4fc;
            object-fit: cover;
            display: block;
        }
            font-size: 1.1em;
            color: #6366f1;
            margin: 0 !important;
            padding: 0 !important;
            font-weight: 500;
        }
        .stTextInput > div > input, .stTextInput > div > div > input {
            background: #fff !important;
            border-radius: 16px !important;
            font-size: 1.15em !important;
            color: #22223b !important;
            border: 2.5px solid #38bdf8 !important;
            padding: 0.9em 1.2em !important;
            margin-bottom: 1.2em !important;
            box-shadow: 0 2px 8px #e0e7ef;
        }
        .stButton > button {
            background: linear-gradient(90deg, #ff512f 0%, #dd2476 100%) !important;
            color: white !important;
            border-radius: 16px !important;
            font-weight: 800 !important;
            font-size: 1.2em !important;
            box-shadow: 0 4px 16px #a5b4fc;
            border: none !important;
            transition: background 0.2s;
            margin-top: 1.5em;
            padding: 0.7em 0;
            min-width: 160px !important;
        }
        .stButton > button:hover {
            background: linear-gradient(90deg, #36d1c4 0%, #5b86e5 100%) !important;
        }
        .login-logo {
            width: 64px;
            height: 64px;
            margin-bottom: 1.2em;
            border-radius: 16px;
            box-shadow: 0 2px 8px #a5b4fc;
            object-fit: cover;
        }
        </style>
        <div class='vibrant-bg'></div>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class='centered-login'>
            <div class='login-card-vibrant'>
                <div class='login-heading-main' style='font-size:1.3em;font-weight:900;margin:0;padding:0;white-space:normal;'>Welcome to <span style='color:#ff512f;'>Spacecraft Interiors</span></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submitted = st.button("Login")
    if submitted:
        user = USERS.get(username)
        if user and user['password'] == password:
            st.session_state['user'] = username
            st.session_state['role'] = user['role']
            return True
        else:
            st.session_state['login_error'] = 'Invalid username or password.'
    return False

def require_login():
    if 'user' not in st.session_state:
        # Hide sidebar while on login page
        st.markdown("""
            <style>
            [data-testid="stSidebar"] { display: none; }
            </style>
        """, unsafe_allow_html=True)
        #t.warning("Please log in to continue.")
        login_success = login_form()
        # Prevent rerun recursion by using a session flag
        if login_success and not st.session_state.get('_rerunning', False):
            st.session_state['_rerunning'] = True
            st.rerun()
        # Only reset _rerunning if login was not successful
        if not login_success:
            st.session_state['_rerunning'] = False
        if st.session_state.get('login_error'):
            st.error(st.session_state['login_error'])
        st.stop()

def logout_button():
    if st.button("Logout", key="logout_btn"):
        for k in ['user', 'role']:
            if k in st.session_state:
                del st.session_state[k]
        st.rerun()

# Add missing get_current_role function
def get_current_role():
    return st.session_state.get('role', None)
