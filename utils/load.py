import pandas as pd
import os
import gspread
from google.oauth2.service_account import Credentials
import traceback

def save_to_csv(df, filename):
    dirname = os.path.dirname(filename)
    if dirname:  # hanya buat folder kalau dirname tidak kosong
        os.makedirs(dirname, exist_ok=True)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")


def save_to_google_sheets(df, spreadsheet_id, credentials_json):
    if df.empty:
        print("Warning: Empty DataFrame, nothing to save on Google Sheets.")
        return

    try:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = Credentials.from_service_account_file(credentials_json, scopes=scopes)
        client = gspread.authorize(creds)

        df = df.copy()
        for col in df.select_dtypes(include=['datetime64[ns]', 'datetime64[ns, UTC]']).columns:
            df[col] = df[col].dt.strftime('%Y-%m-%d %H:%M:%S')

        sheet = client.open_by_key(spreadsheet_id).sheet1
        sheet.clear()
        sheet.update([df.columns.values.tolist()] + df.values.tolist())
        print(f"✅ Data saved to Google Sheets with ID: {spreadsheet_id}")

    except Exception:
        print("❌ Failed to save data to Google Sheets:")
        traceback.print_exc()