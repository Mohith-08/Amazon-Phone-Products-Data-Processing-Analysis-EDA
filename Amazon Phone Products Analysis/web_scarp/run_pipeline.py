import subprocess
import sys
import os

print("\n Scrapping amazon data for phones in 1st 10 pages......")
subprocess.run([sys.executable, "scraper/scraper_all.py"],check=True)

print("\n Transforming the scraped data")
subprocess.run([sys.executable, "transform/transform.py"],check=True)

print("\n Performing EDA on the processed data")
subprocess.run([sys.executable, "eda/eda.py"],check=True)