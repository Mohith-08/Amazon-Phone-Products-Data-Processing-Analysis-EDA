import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

os.makedirs('reports/chart', exist_ok=True)

stocks = ['AAPL', 'TSLA','MSFT','GOOGL']

for stock in stocks:
    input_file = f'data/processed/{stock}_processed.csv'
    df = pd.read_csv(input_file)
    print(f'Running EDA for {stock}')
    print(df.describe())
    df['Date'] = pd.to_datetime(df['Date'])
    print(df.info())
    print(df.isnull().sum())
    
    #closing proce trend

    plt.figure(figsize=(12,6))
    plt.plot(df['Close'])
    plt.title(f'{stock} closing price trend')
    plt.xlabel("Days")
    plt.ylabel("Closing price")

    plt.savefig(f'reports/chart/{stock}_closing_price.jpg')

    plt.close()

    plt.figure(figsize=(12,6))
    plt.plot(df['Volume'])
    plt.title(f'{stock} closing price trend')
    plt.xlabel("Days")
    plt.ylabel("volume")

    plt.savefig(f'reports/chart/{stock}_volume.jpg')

    plt.figure(figsize=(12,6))
    plt.plot(df['Close'], label = 'Close')
    plt.plot(df['MA_10'], label = 'MA 10')
    plt.plot(df['MA_30'], label = 'MA 30')

    plt.legend()
    plt.title(f"{stock} Moving averages")
    plt.savefig(f'reports/chart/{stock}_moving_averages.jpg')
    plt.close()


    plt.figure(figsize=(15,8))
    corr = df[['Close','High','Low','Open','Volume',
               'daily_return','MA_10','MA_30','volatility','price_change']].corr()
    sns.heatmap(corr,
                annot=True,
                cmap='coolwarm',
                fmt='.2f',
                vmin=-1,
                vmax=1,
                linewidths=0.5)
    plt.title(f"Correlation map for {stock}")
    plt.savefig(f'reports/chart/{stock}_heatmap.jpg')
    plt.close()
print("eda charts are saved to location")


