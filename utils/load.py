import os
import logging
import gspread
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

def save_to_csv(df, filename="products_clean.csv"):
    df.to_csv(filename, index=False)
    logging.info(f"Saved to {filename}")

def save_to_parquet(df, filename="products_clean.parquet"):
    df.to_parquet(filename, index=False)
    logging.info(f"Saved to {filename}")

def save_to_google_sheets(df, spreadsheet_name="ETL Products Clean"):
    try:
        client = gspread.service_account(filename="feisty-flow-457106-u5-21c11261af09.json")

        try:
            sheet = client.open(spreadsheet_name).sheet1
        except gspread.SpreadsheetNotFound:
            spreadsheet = client.create(spreadsheet_name)
            sheet = spreadsheet.sheet1
            spreadsheet.share('codingcamp@feisty-flow-457106-u5.iam.gserviceaccount.com', perm_type='user', role='writer')

        sheet.clear()
        sheet.update([df.columns.values.tolist()] + df.values.tolist())
        logging.info("Saved to Google Sheets successfully.")
    except Exception as e:
        logging.error(f"Failed to save to Google Sheets: {e}")

def save_to_postgresql(df):
    try:
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")
        db_name = os.getenv("DB_NAME")

        conn_str = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        engine = create_engine(conn_str)

        df.to_sql("products_clean", engine, if_exists="replace", index=False)
        logging.info("Saved to PostgreSQL successfully.")
    except Exception as e:
        logging.error(f"Failed to save to PostgreSQL: {e}")

def save_all(df):
    save_to_csv(df)
    save_to_parquet(df)
    save_to_google_sheets(df)
    save_to_postgresql(df)