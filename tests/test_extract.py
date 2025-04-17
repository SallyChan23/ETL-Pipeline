import unittest
from utils.extract_selenium import scrape_with_selenium
import pandas as pd

class TestExtract(unittest.TestCase):
    def test_scrape_returns_dataframe(self):
        df = scrape_with_selenium()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty, "Scraped dataframe is empty!")

if __name__ == '__main__':
    unittest.main()