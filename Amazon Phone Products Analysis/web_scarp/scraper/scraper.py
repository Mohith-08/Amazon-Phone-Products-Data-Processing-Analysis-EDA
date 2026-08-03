import os
import time
import random
from datetime import datetime

import pandas as pd
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

SEARCH_QUERY = "laptops"
URL = f"https://www.amazon.com/s?k={SEARCH_QUERY}"


def scrape_amazon():

    print("Launching Chrome...")

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
        "Chrome/138.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    print("Opening Amazon...")
    driver.get(URL)

    time.sleep(random.randint(5, 8))

    # Save HTML for debugging
    with open("amazon_page.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    soup = BeautifulSoup(driver.page_source, "lxml")

    products = soup.select("div[data-component-type='s-search-result']")

    print(f"\nProducts Found : {len(products)}")

    all_data = []

    for product in products:

        # ---------------- Title ----------------
        title = "Not Available"
        title_tag = product.select_one("h2 a span")
        if title_tag:
            title = title_tag.get_text(strip=True)

        # ---------------- Price ----------------
        price = "Not Available"

        price_tag = product.select_one("span.a-price span.a-offscreen")

        if price_tag:
            price = price_tag.get_text(strip=True)

        # ---------------- Rating ----------------
        rating = "Not Available"

        rating_tag = product.select_one("span.a-icon-alt")

        if rating_tag:
            rating = rating_tag.get_text(strip=True)

        # ---------------- Reviews ----------------
        reviews = "Not Available"

        review_tag = product.select_one("span.a-size-base.s-underline-text")

        if review_tag:
            reviews = review_tag.get_text(strip=True)

        all_data.append({
            "Title": title,
            "Price": price,
            "Rating": rating,
            "Reviews": reviews,
            "Scraped At": datetime.now()
        })

    driver.quit()

    df = pd.DataFrame(all_data)

    print("\nFirst 5 Products\n")
    print(df.head())

    os.makedirs("data/raw", exist_ok=True)

    output_file = "data/raw/amazon_raw_products.csv"

    df.to_csv(output_file, index=False)

    print(f"\nSaved to {output_file}")


if __name__ == "__main__":
    scrape_amazon()