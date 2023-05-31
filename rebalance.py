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


date = '2023-05-04'  # start date

# 미국 주식 특별
tickers_1 = ['O', 'TLT', 'LQD']
amounts_1 = [43, 40, 9]
prices_1 = yf.download(tickers_1, date)['Adj Close'].tail(1)[tickers_1]
prices_amount_1, sum_1 = get_prices_amount(prices_1, amounts_1)

# 미국 주식
tickers_2 = ['CVX', 'JPM', 'JNJ', 'VZ', 'MMM', 'PEP', 'SBUX']
amounts_2 = [6, 6, 6, 23, 9, 5, 8]
prices_2 = yf.download(tickers_2, date)['Adj Close'].tail(1)[tickers_2]
prices_amount_2, sum_2 = get_prices_amount(prices_2, amounts_2)


# Load the exchange rate data
ticker_symbol = 'USDKRW=X'
exchange_rate = yf.download(ticker_symbol, date)['Adj Close'].tail(1)[0]


# S&P500, KOSPI
korean_tickers_1 = ['360200.KS', '361580.KS']
korean_amounts_1 = [240, 93]
korean_prices_1 = yf.download(korean_tickers_1, date)['Adj Close'].tail(1)[korean_tickers_1]
korean_prices_1 = korean_prices_1 / exchange_rate   # USD로 보정
korean_prices_amount_1, korean_sum_1 = get_prices_amount(korean_prices_1, korean_amounts_1)

# 삼성전자우, 현대차우
korean_tickers_2 = ['005935.KS', '005387.KS']
korean_amounts_2 = [18, 10]
korean_prices_2 = yf.download(korean_tickers_2, date)['Adj Close'].tail(1)[korean_tickers_2]
korean_prices_2 = korean_prices_2 / exchange_rate   # USD로 보정
korean_prices_amount_2, korean_sum_2 = get_prices_amount(korean_prices_2, korean_amounts_2)

gold = 3338000      # 금
gold_in_USD = gold / exchange_rate

stock = [sum_2 + korean_sum_2]      # 주식 다 합쳐서

# gold + ISA + 추가할
KRW = (7 + 0) + 0      # 현금 얼마 추가? or 출금? (마이너스도 가능)
KRW_in_USD = KRW / exchange_rate      # 현금 얼마 추가?
USD = 73.22     # 현금 얼마 추가?

total_balance_ISA = 12210990 / exchange_rate
korean_bonds = total_balance_ISA - korean_sum_1 - korean_sum_2 - 0 / exchange_rate      # 한국 채권 직접 투자

big_portfolio = korean_prices_amount_1 + stock + prices_amount_1 + [korean_bonds] + [gold_in_USD] + [KRW_in_USD, USD]
total_value = sum_1 + sum_2 + korean_sum_1 + korean_sum_2 + korean_bonds + gold_in_USD + KRW_in_USD + USD

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
portions = portions
desired_asset = desired_asset

# plot the graph
plt.pie(portions, labels = desired_asset, autopct='%1.2f%%')

# Add text outside of the pie chart
plt.text(-1.5, 1.5, 'Asset Allocation')


# show the graph
plt.show()





# For stock balance
stock_tickers = tickers_2 + korean_tickers_2
stock_values = prices_amount_2 + korean_prices_amount_2
stocks_pair = {t : v for t, v in zip(stock_tickers, stock_values)}

stocks_pair = dict(sorted(stocks_pair.items(), key=lambda x: x[1]))

# 삼성전자우, 현대차우
# '005935.KS', '005387.KS'
print(stocks_pair)




from datetime import datetime

history = True

transfer = 1900000

if history == True : 
    # Get today's date
    today = datetime.today()
    today_str = today.strftime('%Y-%m-%d')


    total_value_USD = total_value
    total_value_KRW = total_value * exchange_rate

    print(exchange_rate)
    print(total_value_USD)
    print(total_value_KRW)


    # make csv file
    asset_list = "date", 'S&P 500', 'KOSPI', 'O', 'CVX', 'JPM', 'JNJ', 'VZ', 'MMM', 'PEP', 'SBUX', 'TLT', 'LQD', 'Korean Bonds', 'gold', 'KRW', 'USD', 'total balance USD', 'total balance KRW', 'transfer'
    amount_list = [today_str] + korean_amounts_1 + amounts_1[:1] + amounts_2 + amounts_1[1:] + [korean_bonds] + [gold] + [KRW, USD] + [total_value_USD, total_value_KRW] + [transfer]


    import csv

    # Open a new CSV file for writing
    with open('data.csv', mode='a', newline='') as file:

        # Create a writer object and write the data as a single row
        writer = csv.writer(file)
        
        # writer.writerow(asset_list)

        writer.writerow(amount_list)


    import pandas as pd

    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv('data.csv').iloc[-1]

    print(df)