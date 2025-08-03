# utils/layout.py
import streamlit as st

def set_custom_theme():
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(120deg, #f8fafc 0%, #e0e7ef 100%); }
        .st-emotion-cache-1v0mbdj, .st-emotion-cache-1kyxreq, .st-emotion-cache-1d391kg {
            border-radius: 16px !important;
            box-shadow: 0 2px 8px #d1d5db33;
        }
        .stButton>button {
            background: #2d6cdf;
            color: white;
            border-radius: 8px;
            font-weight: 600;
        }
        .stSidebar {
            background: #2d6cdf11;
        }
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: #2d6cdf;
        }
        </style>
    """, unsafe_allow_html=True)
