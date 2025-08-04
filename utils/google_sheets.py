import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os

# Set up the Google Sheets API client
# Place your credentials file in the root directory and set this path
CREDENTIALS_FILE = os.environ.get('GOOGLE_SHEETS_CREDS', 'google-credentials.json')
SHEET_NAME = os.environ.get('GOOGLE_SHEETS_NAME', 'Spacecraft-streamlit')

scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
]

def get_gspread_client():
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
    client = gspread.authorize(creds)
    return client

def get_worksheet(sheet_name=SHEET_NAME, tab_name='Sheet1'):
    client = get_gspread_client()
    sheet = client.open(sheet_name)
    try:
        worksheet = sheet.worksheet(tab_name)
    except gspread.exceptions.WorksheetNotFound:
        worksheet = sheet.add_worksheet(title=tab_name, rows="1000", cols="20")
    return worksheet

def read_sheet(tab_name, sheet_name=SHEET_NAME):
    ws = get_worksheet(sheet_name, tab_name)
    data = ws.get_all_records()
    if not data:
        return pd.DataFrame()
    return pd.DataFrame(data)

def write_sheet(tab_name, df, sheet_name=SHEET_NAME):
    ws = get_worksheet(sheet_name, tab_name)
    ws.clear()
    if df.empty:
        return
    ws.update([df.columns.values.tolist()] + df.values.tolist())
