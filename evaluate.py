import csv
import pandas as pd


# Read the CSV file into a Pandas DataFrame
df = pd.read_csv('data.csv')

# Date
print(df.iloc[-3]['date'])
print(df.iloc[-2]['date'])

# Get Current Dollar Exchange Rate
USDKRW = df.iloc[-2]['USDKRW']

# Get Transfer
transfer_KRW = df.iloc[-2]['transfer_KRW']


# Balance Comparison
last_total_balance_KRW = df.iloc[-3]['total balance KRW']
last_total_balance_USD = df.iloc[-3]['total balance USD']

current_total_balance_KRW = df.iloc[-2]['total balance KRW'] - transfer_KRW
current_total_balance_USD = df.iloc[-2]['total balance USD'] - transfer_KRW / USDKRW

print("last_total_balance_KRW : ", last_total_balance_KRW, "last_total_balance_USD : ", last_total_balance_USD)
print("current_total_balance_KRW : ", current_total_balance_KRW, "current_total_balance_USD : ", current_total_balance_USD)


# Balance Comparison in Percent
change_in_KRW_pct = current_total_balance_KRW / last_total_balance_KRW
change_in_USD_pct = current_total_balance_USD / last_total_balance_USD

print("Change in KRW pct : ", change_in_KRW_pct * 100 - 100, "(", change_in_KRW_pct, ")", )
print("Change in USD pct : ", change_in_USD_pct * 100 - 100, "(", change_in_USD_pct, ")", )


# Balance Comparison in minus
change_in_KRW = current_total_balance_KRW - last_total_balance_KRW
change_in_USD = current_total_balance_USD - last_total_balance_USD

print("Change in KRW : ", change_in_KRW)
print("Change in USD : ", change_in_USD)


# Cash Comparison to get Cash Flow
last_KRW = df.iloc[-3]['KRW']
last_USD = df.iloc[-3]['USD']

current_KRW = df.iloc[-2]['KRW']
current_USD = df.iloc[-2]['USD']

cash_flow_KRW = current_KRW - last_KRW
cash_flow_USD = current_USD - last_USD

print("Cash Flow : ", cash_flow_KRW, cash_flow_USD, "(", cash_flow_USD * USDKRW, ")")
print("Total Cash Flow : ", cash_flow_KRW + cash_flow_USD * USDKRW)