
import time
import random
import os
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


SEARCH_QUERY = "phones"

URL = f"https://www.amazon.in/s?k={SEARCH_QUERY}"

def scrape_amazon():
    print("Launching Browser........")
    options = webdriver.ChromeOptions()


    #Browser settings
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")


    options.add_argument(
        "user-agent=Mozilla/5.0 "
        "(Windows NT 10.0;Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )

    #Launch Chrome
    driver = webdriver.Chrome(
        service = Service(ChromeDriverManager().install()),
        options = options
    )

    print("Opening Amazon.....")

    driver.get(URL)


    time.sleep(random.randint(5,8))

    print("Fetching page source....")

    soup = BeautifulSoup(driver.page_source,"html.parser")

    all_products = soup.find_all(
        "div",
        {"data-component-type": "s-search-result"}
    )

    print("Products Found:", len(all_products))

    products = []
    #Product price details
    for item in all_products:
        try:
            price = item.find(
                "span",
                class_ = "a-price-whole"
            ).text.strip()
        except:
            price = None

        #product rating
        try:
            rating = item.find(
                "span",
                class_ = "a-icon-alt"
            ).text.strip()
        except:
            rating = None

        #count of reviews
        try:
            reviews = item.find(
                "span",
                class_ = "a-size-base s-underline-text"
            ).text.strip()
        except:
            reviews = None
        #product title
        try:
            title = item.h2.text.strip()
        except:
            title = None
        products.append({
            "title": title,
            "price": price,
            "rating": rating,
            "reviews": reviews,
            "scraped_at":datetime.now()
        })
    
    df = pd.DataFrame(products)

    print("\nFirst 5 products of the query:\n")
    print(df.head())

    os.makedirs("data/raw", exist_ok=True)

    output_file = "data/raw/amazon_raw_products.csv"

    df.to_csv(output_file,index= False)

    print(f"\nRaw data is saved to location: {output_file}")


    driver.quit()

    print("\n scraping is completed for the given product")

if __name__ == "__main__":
    scrape_amazon()
    