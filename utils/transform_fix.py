import pandas as pd 
import logging

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    try:
        df = df.dropna(subset=["Title", "Price", "Rating"])
        df = df.drop_duplicates()

        df["Price"] = df["Price"].astype(str)
        df["Title"] = df["Title"].astype(str)

        df = df[~df["Price"].str.contains("unavailable|-", case=False, na=False)]
        df = df[~df["Title"].str.lower().str.contains("unknown", na=False)]

        df["Price"] = (
            df["Price"]
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
            .astype(float)
            .mul(16000)
        )
        rating_clean = df["Rating"].astype(str).str.extract(r"([0-5](?:\.\d)?)")  
        df["Rating"] = pd.to_numeric(rating_clean[0], errors="coerce")
        df = df.dropna(subset=["Rating"])
        

        for col in ["Colors", "Size", "Gender"]:
            df[col] = df[col].astype(str).str.strip().str.lower()

        df["Title"] = df["Title"].str.title()

        df["is_discounted"] = df["Price"] < 100000

        def get_category(title):
            if not isinstance(title, str):
                return "other"
            title = title.lower()
            if "shirt" in title or "t-shirt" in title:
                return "top"
            elif "pants" in title or "jeans" in title:
                return "bottom"
            elif "jacket" in title:
                return "outer"
            else:
                return "other"

        df["category"] = df["Title"].apply(get_category)

        return df

    except Exception as e:
        logging.error(f"Error during data transformation: {e}")
        raise