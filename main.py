from utils.extract import scrape_all_pages  
from utils.transform import transform_data
from utils.load import save_to_csv, save_to_google_sheets
import os

def main():
    # Scrape data dari website
    print("Start scraping...")
    df_raw = scrape_all_pages ()
    print(f"Data scraped: {df_raw.shape}")

    # Transform data (bersihkan & format)
    df_cleaned = transform_data(df_raw)
    print(f"Data after cleaning: {df_cleaned.shape}")

    # Simpan ke CSV
    csv_path = "products.csv"
    save_to_csv(df_cleaned, csv_path)

    # Simpan ke Google Sheets
    spreadsheet_id = "1osszvMa34gcIK38q3dFp2Q8bqAh7bwFdicmD5m1pyF8"  # ganti dengan nama sheetmu yang sudah dibuat
    credentials_path = "google-sheets-api.json"  # path ke service account json
    if os.path.exists(credentials_path):
        save_to_google_sheets(df_cleaned, spreadsheet_id, credentials_path)
    else:
        print(f"Google Sheets credentials not found at {credentials_path}, skipping Google Sheets upload.")

if __name__ == "__main__":
    main()
