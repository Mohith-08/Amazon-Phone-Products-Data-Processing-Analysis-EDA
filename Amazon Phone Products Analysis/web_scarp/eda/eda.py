
import pandas as pd
import matplotlib.pyplot as plt
import os

def perform_eda():
    input_file = 'data/processed/amazon_processed_phone_products.csv'
    df = pd.read_csv(input_file)

    print("\nDataInformation")
    print(df.info())

    print("\nDescription of the processed data")
    print(df.describe())

    print("\n null values present in the data")
    print(df.isnull().sum())

    print("\n Top 10 products in the data")
    print(df[['title','price','rating']].head(10))


    os.makedirs('reports/charts', exist_ok=True)

    plt.figure(figsize = (10,6))
    df['price'].dropna().hist(bins =20)
    plt.xlabel("price")
    plt.ylabel('Frequency')
    plt.title("Products price Distribution")
    plt.savefig('reports/charts/price_distribution.png')
    plt.close()

    plt.figure(figsize = (10,6))
    df['rating'].dropna().hist(bins =20)
    plt.xlabel("rating")
    plt.ylabel('Frequency')
    plt.title("Products rating Distribution")
    plt.savefig('reports/charts/rating_distribution.png')
    plt.close()

    top_products = df.sort_values('price', ascending = False)
    plt.figure(figsize = (12,6))
    plt.bar(top_products['title'],top_products['price'])
    plt.xticks(rotation = 45, ha = 'right')
    plt.xlabel("Product name")
    plt.ylabel('Price')
    plt.title("Top 10 expensive phones")
    plt.tight_layout()
    plt.savefig('reports/charts/top_10_phones.png')
    plt.close()

    if 'price' in df.columns and 'rating' in df.columns:
        plt.figure(figsize = (10,5))
        avg_by_rating = df['rating'].dropna().round(0)
        if not avg_by_rating.empty:
            avg_by_rating = df.groupby(avg_by_rating)['price'].mean()
            if not avg_by_rating.empty:
                avg_by_rating.plot(kind='bar')
       
        
        plt.xlabel("Rating")
        plt.ylabel("Average Price")
        plt.title("Average price vs rating")
        plt.savefig("reports/charts/price_cat_avg.png")
        plt.tight_layout()
        plt.close


if __name__ == '__main__':
    perform_eda()
