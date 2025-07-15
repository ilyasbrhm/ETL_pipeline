import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

def scrape_data(page: int) -> pd.DataFrame:
    # Perbaiki URL sesuai keterangan sebelumnya
    if page == 1:
        url = "https://fashion-studio.dicoding.dev/"
    else:
        url = f"https://fashion-studio.dicoding.dev/page{page}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching page {page}: {e}")
        return pd.DataFrame()

    soup = BeautifulSoup(response.text, 'html.parser')
    products = soup.select('div.collection-card')

    data = []
    for product in products:
        title = product.select_one('h3.product-title').text.strip() if product.select_one('h3.product-title') else None
        price = product.select_one('span.price').text.strip() if product.select_one('span.price') else None

        details = product.select('div.product-details > p')
        rating_text = details[0].text.strip() if len(details) > 0 else None
        colors_text = details[1].text.strip() if len(details) > 1 else None
        size_text = details[2].text.strip() if len(details) > 2 else None
        gender_text = details[3].text.strip() if len(details) > 3 else None

        data.append({
            "Title": title,
            "Price": price,
            "Rating": rating_text,
            "Colors": colors_text,
            "Size": size_text,
            "Gender": gender_text,
            "Timestamp": datetime.now()
        })

    return pd.DataFrame(data)


def scrape_all_pages(start_page=1, end_page=50) -> pd.DataFrame:
    """
    Scrape semua halaman dari start_page sampai end_page,
    lalu gabungkan semua DataFrame.
    """
    all_data = []
    for page in range(start_page, end_page + 1):
        print(f"Scraping page {page}...")
        df_page = scrape_data(page)    # <<< panggil scrape_data, bukan scrape_all_pages
        if df_page.empty:
            print(f"⚠️ No data found on page {page}")
            continue
        all_data.append(df_page)
        time.sleep(1)  # delay 1 detik untuk menghindari rate limit

    if all_data:
        df_all = pd.concat(all_data, ignore_index=True)
        print(f"Data scraped: {df_all.shape}")
        return df_all
    else:
        print("No data scraped from any pages.")
        return pd.DataFrame()
