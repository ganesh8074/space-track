import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os

SHEET_NAME = os.environ.get('GOOGLE_SHEETS_NAME', 'Spacecraft-streamlit')

def get_gspread_client():
    import json
    try:
        import streamlit as st
        if "GOOGLE_SERVICE_ACCOUNT_JSON" in st.secrets:
            creds_dict = json.loads(st.secrets["GOOGLE_SERVICE_ACCOUNT_JSON"])
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive',
            ]
            creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
            client = gspread.authorize(creds)
            return client
    except ImportError:
        pass
    # Fallback for local dev
    CREDENTIALS_FILE = os.environ.get('GOOGLE_SHEETS_CREDS', 'google-credentials.json')
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive',
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
    client = gspread.authorize(creds)
    return client

def get_worksheet(sheet_name=SHEET_NAME, tab_name='Sheet1'):
    client = get_gspread_client()
    try:
        sheet = client.open(sheet_name)
    except Exception:
        return None
    try:
        worksheet = sheet.worksheet(tab_name)
    except Exception:
        worksheet = sheet.add_worksheet(title=tab_name, rows="1000", cols="20")
    return worksheet

import streamlit as st

@st.cache_data(ttl=60)
def read_sheet(tab_name, sheet_name=SHEET_NAME):
    ws = get_worksheet(sheet_name, tab_name)
    if ws is None:
        return pd.DataFrame()
    data = ws.get_all_records()
    if not data:
        return pd.DataFrame()
    return pd.DataFrame(data)

def write_sheet(tab_name, df, sheet_name=SHEET_NAME):
    ws = get_worksheet(sheet_name, tab_name)
    if ws is None:
        return
    ws.clear()
    if df.empty:
        return
    ws.update([df.columns.values.tolist()] + df.values.tolist())
    try:
        read_sheet.clear()
    except Exception:
        pass
