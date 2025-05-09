from utils.transform_fix import clean_data
from utils.load import save_all
import logging
import os
import pandas as pd
from utils.extract_selenium import scrape_with_selenium
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

if __name__ == "__main__":
    try:
        if os.path.exists("products.csv"):
            logging.info("products.csv found, loading from file...")
            df = pd.read_csv("products.csv")
            logging.info(df.head(3).to_string())
            logging.info(f"Jumlah data awal: {len(df)}")
        else:
            logging.info("products.csv not found, starting scrape...")
            df = scrape_with_selenium()
            df.to_csv("products.csv", index=False)
            logging.info("Scraping done! Saved to products.csv")
        
        df_clean = clean_data(df)
        logging.info(df_clean.head(3).to_string())
        logging.info(f"Jumlah data setelah transform: {len(df_clean)}")
        logging.info("Cleaning done!")
        
        save_all(df_clean)

    except Exception as e:
        logging.error(f"ETL pipeline failed: {e}")