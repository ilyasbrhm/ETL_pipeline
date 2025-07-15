import pytest
import pandas as pd
import numpy as np  # import numpy

from utils.transform import transform_data

def test_transform_data_basic():
    raw_data = pd.DataFrame({
        "Title": ["Product A", "Unknown Product", "Product A"],
        "Price": ["$10.5", "$20", "$10.5"],
        "Rating": ["4.5 / 5", "3.0 / 5", "4.5 / 5"],
        "Colors": ["3 Colors", "1 Colors", "3 Colors"],
        "Size": ["Size: M", "Size: L", "Size: M"],
        "Gender": ["Gender: Men", "Gender: Women", "Gender: Men"],
        "Timestamp": [pd.Timestamp.now()] * 3
    })

    df_clean = transform_data(raw_data)

    assert "Unknown Product" not in df_clean['Title'].values
    assert len(df_clean) == 1

    expected_price = 10.5 * 16000
    assert df_clean.iloc[0]['Price'] == expected_price

    assert isinstance(df_clean.iloc[0]['Rating'], float)
    assert isinstance(df_clean.iloc[0]['Colors'], (int, np.integer))

    assert not df_clean.iloc[0]['Size'].startswith("Size:")
    assert not df_clean.iloc[0]['Gender'].startswith("Gender:")
