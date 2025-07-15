import pytest
from unittest.mock import patch, Mock
import pandas as pd
import requests  # <-- harus ditambahkan
from utils.extract import scrape_data, scrape_all_pages

# Mock response HTML dengan 1 produk valid
MOCK_HTML = '''
<div class="collection-card">
    <h3 class="product-title">Test Product</h3>
    <span class="price">$10.00</span>
    <div class="product-details">
        <p>4.5 / 5</p>
        <p>3 Colors</p>
        <p>Size: M</p>
        <p>Gender: Men</p>
    </div>
</div>
'''

def mock_requests_get_success(*args, **kwargs):
    mock_resp = Mock()
    mock_resp.status_code = 200
    mock_resp.text = MOCK_HTML
    mock_resp.raise_for_status = Mock()
    return mock_resp

def mock_requests_get_empty(*args, **kwargs):
    mock_resp = Mock()
    mock_resp.status_code = 200
    mock_resp.text = ''  # kosong, tidak ada produk
    mock_resp.raise_for_status = Mock()
    return mock_resp

def mock_requests_get_error(*args, **kwargs):
    raise requests.RequestException("Network error")

@patch('utils.extract.requests.get', side_effect=mock_requests_get_success)
def test_scrape_data_success(mock_get):
    df = scrape_data(1)
    assert not df.empty
    assert df.iloc[0]['Title'] == 'Test Product'
    assert df.iloc[0]['Price'] == '$10.00'
    assert df.iloc[0]['Rating'] == '4.5 / 5'
    assert df.iloc[0]['Colors'] == '3 Colors'
    assert df.iloc[0]['Size'] == 'Size: M'
    assert df.iloc[0]['Gender'] == 'Gender: Men'
    assert 'Timestamp' in df.columns

@patch('utils.extract.requests.get', side_effect=mock_requests_get_empty)
def test_scrape_data_no_products(mock_get):
    df = scrape_data(1)
    assert df.empty

@patch('utils.extract.requests.get', side_effect=mock_requests_get_error)
def test_scrape_data_request_exception(mock_get):
    df = scrape_data(1)
    assert df.empty

@patch('utils.extract.requests.get', side_effect=[mock_requests_get_success(), mock_requests_get_empty()])
def test_scrape_all_pages(mock_get):
    df_all = scrape_all_pages(1, 2)
    assert not df_all.empty
    assert 'Title' in df_all.columns
    assert any(df_all['Title'] == 'Test Product')

@patch('utils.extract.requests.get', side_effect=mock_requests_get_empty)
def test_scrape_all_pages_all_empty(mock_get):
    # Semua halaman kosong, harus mengembalikan df kosong
    df_all = scrape_all_pages(1, 2)
    assert df_all.empty
