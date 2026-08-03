
import time
import random
import os
from datetime import datetime

import pandas as pd
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# ==============================
# CONFIGURATION
# ==============================

SEARCH_QUERY = "phones"
MAX_PAGES = 10

# ==============================
# SCRAPER
# ==============================

def scrape_amazon():

    print("Launching Browser...")

    options = webdriver.ChromeOptions()

    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")

    options.add_argument(
        "user-agent=Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    all_products_data = []

    try:

        for page in range(1, MAX_PAGES + 1):

            url = f"https://www.amazon.in/s?k={SEARCH_QUERY}&page={page}"

            print(f"\nScraping Page {page}")
            print(url)

            driver.get(url)

            time.sleep(random.randint(4, 7))

            # CAPTCHA check
            if "captcha" in driver.page_source.lower():
                print("CAPTCHA detected. Stopping scraper.")
                break

            soup = BeautifulSoup(
                driver.page_source,
                "html.parser"
            )

            products = soup.find_all(
                "div",
                {"data-component-type": "s-search-result"}
            )

            print(f"Products Found: {len(products)}")

            for item in products:

                # TITLE
                try:
                    title = item.find("h2").get_text(strip=True)
                except:
                    title = None

                # PRICE
                try:
                    price = item.find(
                        "span",
                        class_="a-price-whole"
                    ).get_text(strip=True)
                except:
                    price = None

                # RATING
                try:
                    rating = item.find(
                        "span",
                        class_="a-icon-alt"
                    ).get_text(strip=True)
                except:
                    rating = None

                # REVIEW COUNT
                try:
                    reviews = item.select_one(
                        "span.a-size-base.s-underline-text"
                    ).get_text(strip=True)
                except:
                    reviews = None

                # PRODUCT URL
                try:
                    link = item.select_one(
                        "a.a-link-normal.s-no-outline"
                    )

                    product_url = (
                        "https://www.amazon.in"
                        + link.get("href")
                    )
                except:
                    product_url = None

                all_products_data.append({
                    "title": title,
                    "price": price,
                    "rating": rating,
                    "reviews": reviews,
                    "product_url": product_url,
                    "page_number": page,
                    "scraped_at": datetime.now()
                })

            time.sleep(random.randint(2, 5))

    finally:
        driver.quit()

    # ==============================
    # DATAFRAME
    # ==============================

    df = pd.DataFrame(all_products_data)

    # Remove duplicates
    df.drop_duplicates(
        subset=["product_url"],
        inplace=True
    )

    print("\nTotal Products Collected:")
    print(len(df))

    print("\nSample Data:")
    print(df.head())

    # ==============================
    # SAVE
    # ==============================

    os.makedirs(
        "data/raw",
        exist_ok=True
    )

    output_file = (
        f"data/raw/amazon_"
        f"{SEARCH_QUERY}_products.csv"
    )

    df.to_csv(
        output_file,
        index=False,
        encoding="utf-8-sig"
    )

    print(
        f"\nData saved successfully:\n{output_file}"
    )

    return df


# ==============================
# MAIN
# ==============================

if __name__ == "__main__":

    scrape_amazon()