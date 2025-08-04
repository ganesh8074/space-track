import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os
import time

import streamlit as st

SHEET_NAME = os.environ.get('GOOGLE_SHEETS_NAME', 'Spacecraft-streamlit')

def get_gspread_client():
    import json
    try:
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

def get_worksheet(sheet_name=SHEET_NAME, tab_name="Sheet1"):
    client = get_gspread_client()
    try:
        sheet = client.open(sheet_name)
    except gspread.exceptions.APIError as e:
        st.error(f"Google Sheets API error: {e}. Please check sheet name, sharing, and API limits.")
        return None

    try:
        worksheet = sheet.worksheet(tab_name)
    except gspread.exceptions.WorksheetNotFound:
        worksheet = sheet.add_worksheet(title=tab_name, rows="1000", cols="20")
    return worksheet

@st.cache_data(show_spinner=False, ttl=60)
def _read_sheet(tab_name, sheet_name=SHEET_NAME):
    ws = get_worksheet(sheet_name, tab_name)
    if ws is None:
        return pd.DataFrame()
    data = ws.get_all_records()
    if not data:
        return pd.DataFrame()
    return pd.DataFrame(data)

def read_sheet(tab_name, sheet_name=SHEET_NAME):
    """Read a sheet with a visible spinner and timing info."""
    with st.spinner(f"Loading data from {tab_name} ..."):
        start = time.time()
        df = _read_sheet(tab_name, sheet_name)
        elapsed = time.time() - start

        if elapsed > 2:  # Customize the threshold as needed
            st.info(f"Loaded {len(df)} rows from '{tab_name}' in {elapsed:.1f}s")
        elif df.empty:
            st.warning(f"No data found in sheet '{tab_name}'.")
        return df

def write_sheet(tab_name, df, sheet_name=SHEET_NAME):
    ws = get_worksheet(sheet_name, tab_name)
    if ws is None:
        st.error("Unable to write to Google Sheet (worksheet not found).")
        return
    ws.clear()
    if df.empty:
        return
    ws.update([df.columns.values.tolist()] + df.values.tolist())
    # Clear the cache for _read_sheet so UI updates immediately
    try:
        _read_sheet.clear()
    except Exception:
        pass
