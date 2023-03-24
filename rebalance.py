import yfinance as yf
import pandas as pd

def get_prices_amount(prices, amounts):
    # Convert the DataFrame to a list of lists
    prices = prices.iloc[0].values.tolist()
    # Convert the DataFrame to a list of lists
    prices = [float(item) for item in prices]
    # Calculate total portfolio value
    prices_amount = [p * a for p, a in zip(prices, amounts)]
    total_value = sum(prices_amount)

    return prices_amount, total_value


# 미국 주식 특별
tickers_1 = ['O', 'TLT', 'LQD']
amounts_1 = [37, 35, 8]
prices_1 = yf.download(tickers_1, '2023-03-01')['Adj Close'].tail(1)[tickers_1]
prices_amount_1, sum_1 = get_prices_amount(prices_1, amounts_1)

# 미국 주식
tickers_2 = ['CVX', 'JPM', 'JNJ', 'VZ', 'MMM', 'PEP', 'SBUX']
amounts_2 = [5, 6, 5, 19, 7, 4, 7]
prices_2 = yf.download(tickers_2, '2023-03-01')['Adj Close'].tail(1)[tickers_2]
prices_amount_2, sum_2 = get_prices_amount(prices_2, amounts_2)


# Load the exchange rate data
ticker_symbol = 'USDKRW=X'
exchange_rate = yf.download(ticker_symbol, '2023-03-01')['Adj Close'].tail(1)[0]


# S&P500, KOSPI
korean_tickers_1 = ['360200.KS', '361580.KS']
korean_amounts_1 = [225, 87]
korean_prices_1 = yf.download(korean_tickers_1, '2023-03-01')['Adj Close'].tail(1)[korean_tickers_1]
korean_prices_1 = korean_prices_1 / exchange_rate   # USD로 보정
korean_prices_amount_1, korean_sum_1 = get_prices_amount(korean_prices_1, korean_amounts_1)

# 삼성전자우, 현대차우
korean_tickers_2 = ['005930.KS', '005387.KS']
korean_amounts_2 = [18, 10]
korean_prices_2 = yf.download(korean_tickers_2, '2023-03-01')['Adj Close'].tail(1)[korean_tickers_2]
korean_prices_2 = korean_prices_2 / exchange_rate   # USD로 보정
korean_prices_amount_2, korean_sum_2 = get_prices_amount(korean_prices_2, korean_amounts_2)

total_balance_ISA = 10769422 / exchange_rate
korean_bonds = total_balance_ISA - korean_sum_1 - korean_sum_2      # 한국 채권 직접 투자

gold = 3051325 / exchange_rate      # 금

stock = [sum_2 + korean_sum_2]      # 주식 다 합쳐서

KRW = 0 / exchange_rate      # 현금 얼마 추가?
USD = 0     # 현금 얼마 추가?

big_portfolio = korean_prices_amount_1 + stock + prices_amount_1 + [korean_bonds] + [gold] + [KRW, USD]
total_value = sum_1 + sum_2 + korean_sum_1 + korean_sum_2 + korean_bonds + gold + KRW + USD

# Calculate portions
portions = [x / total_value for x in big_portfolio]



# Define desired portfolio portions (as decimal fractions)
desired_asset = ['S&P500', 'KOSPI', 'Stock', 'O', 'TLT', 'LQD', 'Korean Bonds', 'Gold', 'KRW', 'USD']
desired_portions = [0.1, 0.05, 0.3, 0.1, 0.16, 0.04, 0.15, 0.1, 0, 0]


# Calculate desired value for each stock based on desired portions
desired_value = [total_value * p for p in desired_portions]

# Calculate necessary buy or sell orders to achieve desired balance
orders = [d - p for d, p in zip(desired_value, big_portfolio)]

# Print results
print(f'Total Portfolio Value: {total_value : .2f}\t({total_value * exchange_rate : .2f})')
for ticker, portion, order_amount in zip(desired_asset, portions, orders):
    print('--------------------------------------------------------------')
    print(f'{ticker} Current Portion: {portion:.2%}')
    print(f'{ticker} Desired Portion: {desired_portions[desired_asset.index(ticker)]:.2%}')
    print(f'{ticker} Necessary Order Amount: {order_amount:.2f}\t({order_amount * exchange_rate : .2f})')



import matplotlib.pyplot as plt

# Except Cash (KRW, USD)
portions = portions[:-2]
desired_asset = desired_asset[:-2]

# plot the graph
plt.pie(portions, labels = desired_asset, autopct='%1.2f%%')

# show the graph
plt.show()