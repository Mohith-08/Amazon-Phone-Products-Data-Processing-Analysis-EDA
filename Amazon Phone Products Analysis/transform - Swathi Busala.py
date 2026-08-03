import pandas as pd
import numpy as np
import os

def clean_price(price):
    try:
        return float(str(price).replace(',','').strip())
    except Exception:
        return np.nan

def clean_rating(rating):
    try:
        return int(str(rating).replace(',','').split()[0])
    except Exception:
        return np.nan

def clean_reviews(reviews):
    try:
        return int(str(reviews).replace(',','').strip())
    except Exception:
        return np.nan
    
def transform_data():
    input_file = 'data/raw/amazon_phones_products.csv'
    output_dir = 'data/processed'
    output_file = os.path.join(output_dir,'amazon_processed_phone_products.csv')

    df = pd.read_csv(input_file)

    df['price'] = df['price'].apply(clean_price)
    df['rating'] = df['rating'].apply(clean_rating)
    df['reviews'] = df['reviews'].apply(clean_reviews)

    df['title'] = df['title'].astype(str)

    df = df.dropna(subset = ['title'])
    df = df.reset_index(drop = True)

    os.makedirs(output_dir,exist_ok=True)

    df.to_csv(output_file, index=False)

    print(f'Processed data is saved to location:{output_file}')


if __name__ =='__main__':
    transform_data()
