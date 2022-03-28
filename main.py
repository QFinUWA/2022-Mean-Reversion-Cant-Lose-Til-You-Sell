import pandas as pd
import os

# TODO LIST ALL PROCESSED CSVs
# local imports
from backtester import tester
from logic_functions.stochastic import logic

training_period = 20  # How far the rolling average takes into calculation
standard_deviations = (
    3.5  # Number of Standard Deviations from the mean the Bollinger Bands sit
)


"""
preprocess_data() function:
    Context: Called once at the beginning of the backtest. TOTALLY OPTIONAL.
             Each of these can be calculated at each time interval, however this is likely slower.

    Input:  list_of_stocks - a list of stock data csvs to be processed

    Output: list_of_stocks_processed - a list of processed stock data csvs
"""


def preprocess_data(list_of_stocks):
    for stock in list_of_stocks:
        if os.path.exists(f"data/{stock}_Processed.csv"):
            continue

        df = pd.read_csv(f"data/{stock}.csv", parse_dates=[0])
        df["TP"] = (df["close"] + df["low"] + df["high"]) / 3  # Calculate Typical Price
        df["std"] = (
            df["TP"].rolling(training_period).std()
        )  # Calculate Standard Deviation
        df["MA-TP"] = (
            df["TP"].rolling(training_period).mean()
        )  # Calculate Moving Average of Typical Price
        df["BOLU"] = (
            df["MA-TP"] + standard_deviations * df["std"]
        )  # Calculate Upper Bollinger Band
        df["BOLD"] = (
            df["MA-TP"] - standard_deviations * df["std"]
        )  # Calculate Lower Bollinger Band
        df.to_csv(f"data/{stock}_Processed.csv", index=False)  # Save to CSV


if __name__ == "__main__":
    # list_of_stocks = ["TSLA_2020-03-01_2022-01-20_1min"]
    list_of_stocks = [
        "TSLA_2020-03-09_2022-01-28_15min",
        "AAPL_2020-03-24_2022-02-12_15min",
    ]  # List of stock data csv's to be tested, located in "data/" folder

    preprocess_data(list_of_stocks)  # Preprocess the data

    list_of_stocks_processed = [stock + "_Processed" for stock in list_of_stocks]

    results = tester.test_array(
        list_of_stocks_processed, logic, chart=True
    )  # Run backtest on list of stocks using the logic function

    print("training period " + str(training_period))
    print("standard deviations " + str(standard_deviations))
    df = pd.DataFrame(
        list(results),
        columns=[
            "Buy and Hold",
            "Strategy",
            "Longs",
            "Sells",
            "Shorts",
            "Covers",
            "Stdev_Strategy",
            "Stdev_Hold",
            "Stock",
        ],
    )  # Create dataframe of results
    df.to_csv("results/Test_Results.csv", index=False)  # Save results to csv
