import unittest
import pandas as pd
import os
from utils.load import save_to_csv
from unittest.mock import patch, MagicMock

class TestLoad(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            "Title": ["Test Product"],
            "Price": [100000.0],
            "Rating": [4.5],
            "Colors": ["3 colors"],
            "Size": ["M"],
            "Gender": ["men"],
            "Timestamp": ["2025-01-01"],
            "is_discounted": [False],
            "category": ["top"]
        })

    def test_save_to_csv_creates_file(self):
        filename = "test_output.csv"
        save_to_csv(self.df, filename)
        self.assertTrue(os.path.exists(filename))
        os.remove(filename)
        
    @patch("pandas.DataFrame.to_csv")
    def test_save_to_csv_mock(self, mock_to_csv):
        save_to_csv(self.df, "file.csv")
        mock_to_csv.assert_called_once_with("file.csv", index=False)
    
    @patch("utils.load.gspread.service_account")
    def test_save_to_google_sheets_mock(self, mock_service_account):
        from utils.load import save_to_google_sheets
        mock_client = MagicMock()
        mock_sheet = MagicMock()
        mock_service_account.return_value = mock_client
        mock_client.open.return_value.sheet1 = mock_sheet

        save_to_google_sheets(self.df, "Mock Sheet")

        mock_sheet.update.assert_called_once()
    @patch("utils.load.create_engine")
    @patch("pandas.DataFrame.to_sql")
    def test_save_to_postgresql_mock(self, mock_to_sql, mock_engine):
        from utils.load import save_to_postgresql
        save_to_postgresql(self.df)
        mock_to_sql.assert_called_once()

if __name__ == '__main__':
    unittest.main()