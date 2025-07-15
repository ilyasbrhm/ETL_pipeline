import pytest
import pandas as pd
import os
from utils.load import save_to_csv, save_to_google_sheets
from unittest.mock import patch, MagicMock

def test_save_to_csv(tmp_path):
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    file_path = tmp_path / "output" / "test.csv"

    save_to_csv(df, str(file_path))
    assert file_path.exists()

@patch('utils.load.gspread.authorize')
@patch('utils.load.Credentials.from_service_account_file')
def test_save_to_google_sheets_empty_df(mock_creds, mock_auth):
    df_empty = pd.DataFrame()
    save_to_google_sheets(df_empty, "dummy_id", "dummy_credentials.json")  # harusnya skip dan print warning

@patch('utils.load.gspread.authorize')
@patch('utils.load.Credentials.from_service_account_file')
def test_save_to_google_sheets_success(mock_creds, mock_auth):
    mock_sheet = MagicMock()
    mock_client = MagicMock()
    mock_client.open_by_key.return_value.sheet1 = mock_sheet
    mock_auth.return_value = mock_client

    df = pd.DataFrame({"A": [1, 2], "Timestamp": [pd.Timestamp.now(), pd.Timestamp.now()]})

    save_to_google_sheets(df, "spreadsheet_id", "credentials.json")

    mock_sheet.clear.assert_called_once()
    mock_sheet.update.assert_called_once()
