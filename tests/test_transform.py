import unittest
import pandas as pd
from utils.transform_fix import clean_data

class TestTransform(unittest.TestCase):
    def test_clean_data_output(self):
        raw_data = {
            "Title": ["T-Shirt", None, "Unknown Product"],
            "Price": ["$10.00", "$20.00", "Unavailable"],
            "Rating": ["⭐ 4.5 / 5", "⭐ Invalid Rating / 5", None],
            "Colors": ["3 colors", "2 colors", "5 colors"],
            "Size": ["M", "L", "XL"],
            "Gender": ["men", "women", "unisex"],
            "Timestamp": ["2025-01-01", "2025-01-01", "2025-01-01"]
        }
        df_raw = pd.DataFrame(raw_data)
        df_cleaned = clean_data(df_raw)

        self.assertFalse(df_cleaned.isnull().any().any(), "Masih ada nilai kosong")
        self.assertTrue(df_cleaned["Price"].dtype == float, "Kolom Price belum float")
        self.assertFalse(df_cleaned["Title"].str.lower().str.contains("unknown").any())

if __name__ == '__main__':
    unittest.main()