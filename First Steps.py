import yfinance as yf
import pandas as pd

# Pushing to main

# Show all columns without truncation
pd.set_option('display.max_columns', None)

# Increase column width so long strings don't get cut off
pd.set_option('display.max_colwidth', None)

# Optional: Expand overall display width
pd.set_option('display.width', 200)


stocks = ["AAPL","MSFT","GOOG","AMZN","TSLA","NVDA","META","BRK-B","V","JNJ","XOM","WMT","JPM",
          "PG","MA","HD","CVX","ABBV","KO","PEP","MRK","BAC","LLY","AVGO","PFE","COST","T","DIS",
          "CSCO","DHR","VZ","ABT","CRM","ACN","ADBE","UPS","WFC","INTC","SCHW","NFLX","CVS","TXN","UNH",
          "ORCL","IBM","MCD","PM","CAT","HON","SBUX"]

ALPHA = .03

# note: in simple exponential smoothing, the one-step-ahead forecast is the
#       most recently smoothed value
def closing(alpha):
    predictions = []
    actual = []
    diff = []
    pred_diff = []
    for stock in stocks:
        ticker = yf.Ticker(stock)
        hist = ticker.history(period="20d")
        hist.head()
        closing_prices = hist["Close"]
        close_prices = closing_prices.values
        # Removing today's close and adding it to the actual array
        actual.append(close_prices[-1])
        close_prices = close_prices[:-1]
        # I took the last 20 days and put it in the exponential smoothing function then return last element
        result = [close_prices[0]]
        for i in range(1, len(close_prices)):
            # go value by value and
            smoothed = alpha * close_prices[i] + (1 - alpha) * result[-1]
            result.append(smoothed)
        predictions.append(result[-1])
        diff.append(close_prices[-1] - close_prices[-2])
        pred_diff.append(result[-1] - close_prices[-2])

    # Create table
    df = pd.DataFrame({
        "Stock" : stocks,
        "Today's Price" : actual,
        "Today's Prediction" : predictions,
        "Price Difference": diff,
        "Predicted Difference": pred_diff
    })
    print("Using the closing price historical data, we can observe these predictions next to actual prices:")
    print(df)
    correct = analytics(diff, pred_diff)
    print(f"\nThe percentage of stock moves that were predicted correctly was {correct * 100: .2f}%")

def opening(alpha):
    predictions = []
    actual = []
    diff = []
    pred_diff = []
    for stock in stocks:
        ticker = yf.Ticker(stock)
        hist = ticker.history(period="20d")
        hist.head()
        opening_prices = hist["Open"]
        closing_prices = hist["Close"]
        close_prices = closing_prices.values
        open_prices = opening_prices.values
        # Removing today's close and adding it to the actual array
        actual.append(close_prices[-1])
        close_prices = close_prices[:-1]
        # I took the last 20 days and put it in the exponential smoothing function then return last element
        result = [close_prices[0]]
        # print(opening_prices.len == closing_prices.len)
        for i in range(1, len(close_prices)):
            # go value by value and
            smoothed = alpha * open_prices[i] + (1 - alpha) * result[-1]
            result.append(smoothed)
            smoothed = alpha * close_prices[i] + (1 - alpha) * result[-1]
            result.append(smoothed)
        predictions.append(result[-1])
        diff.append(close_prices[-1] - close_prices[-2])
        pred_diff.append(result[-1] - close_prices[-2])
    print("Using the open AND close price historical data, we can observe these predictions next to actual prices:")
    df = pd.DataFrame({
        "Stock": stocks,
        "Today's Price": actual,
        "Today's Prediction": predictions,
        "Price Difference": diff,
        "Predicted Difference": pred_diff
    })
    print(df)
    correct = analytics(diff, pred_diff)
    print(f"\nThe percentage of stock moves that were predicted correctly was {correct * 100: .2f}%")


def menu():
    print("\t\t\tStock Prediction Simulator\n"
          "\t___________________________________________\n"
          "1.) Use closing prices\n"
          "2.) Use opening and closing prices\n"
          "3.) Exit\n")
    choice = input("Enter your choice: ")
    return choice

def run():
    choice = 0
    while choice != 3:
        choice = menu()
        if choice == "3":
            return
        alpha = float(input("Enter desired alpha: "))
        while alpha < 0 or alpha > 1:
            alpha = input("Enter a valid alpha (0 < alpha < 1): ")
        if choice == "1":
            closing(alpha)
        else:
            opening(alpha)

def analytics(diff, pred_diff):
    correct = 0
    for i in range(50):
        if (diff[i] / pred_diff[i]) > 0:
            correct += 1
    return correct / 50

run()
