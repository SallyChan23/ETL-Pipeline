from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import time
import re

def scrape_with_selenium():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    all_products = []

    for page in range(1, 51):
        url = "https://fashion-studio.dicoding.dev/" if page == 1 else f"https://fashion-studio.dicoding.dev/page{page}"
        print(f"Scraping {url}...")

        driver.get(url)
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        products = soup.find_all("div", class_="collection-card")  

        for p in products:
            try:
                title = p.find("h3", class_="product-title")
                info = p.find_all("p")
                
                price_span = p.find("span", class_="price")
                price = price_span.text.strip().replace("$", "") if price_span else None
                
                rating, colors, size, gender = None, None, None, None

                for line in info:
                    text = line.text.strip().lower()
                    if "rating" in text:
                        match = re.search(r"(\d+(\.\d+)?)", line.text)
                        rating = match.group(1) if match else None
                    elif "color" in text:
                        colors = line.text.strip()
                    elif "size" in text:
                        size = line.text.strip().replace("Size: ", "")
                    elif "gender" in text:
                        gender = line.text.strip().replace("Gender: ", "")

                if title and price:
                    all_products.append({
                        "Title": title.text.strip(),
                        "Price": price,
                        "Rating": rating,
                        "Colors": colors,
                        "Size": size,
                        "Gender": gender,
                        "Timestamp": datetime.now().isoformat()
                    })
                else:
                    print("Skipped due to missing title or price.")
            except Exception as e:
                print("Error parsing:", e)
                print("→ Element content:")
                print(p.prettify())

    driver.quit()
    return pd.DataFrame(all_products)