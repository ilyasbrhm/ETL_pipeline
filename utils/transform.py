import pandas as pd

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Bersihkan dan transform data yang sudah di-scrape.
    - Buang baris dengan Title "Unknown Product"
    - Buang data duplikat
    - Buang data yang null
    - Konversi Price dari dolar ke rupiah (Rp16.000)
    - Bersihkan kolom Rating, Colors, Size, Gender sesuai kriteria
    - Konversi tipe data sesuai ekspektasi
    """
    if df.empty:
        print("Empty DataFrame received in transform_data.")
        return df

    # Hapus produk 'Unknown Product'
    df = df[~df['Title'].str.contains("Unknown Product", na=False)]

    # Buang duplikat dan null
    df = df.drop_duplicates()
    df = df.dropna()

    # Transform kolom Price, hapus $ dan ubah ke float
    df['Price'] = df['Price'].str.replace(r'[^0-9.]', '', regex=True).astype(float)
    # Konversi ke Rupiah
    df['Price'] = df['Price'] * 16000

    # Bersihkan Rating (ambil angka float sebelum " / 5")
    df['Rating'] = df['Rating'].str.extract(r'(\d+\.?\d*)').astype(float)

    # Bersihkan Colors (ambil angka sebelum " Colors")
    df['Colors'] = df['Colors'].str.extract(r'(\d+)').astype(int)

    # Bersihkan Size (hapus teks "Size: ")
    df['Size'] = df['Size'].str.replace('Size: ', '').astype(str)

    # Bersihkan Gender (hapus teks "Gender: ")
    df['Gender'] = df['Gender'].str.replace('Gender: ', '').astype(str)

    return df.reset_index(drop=True)
