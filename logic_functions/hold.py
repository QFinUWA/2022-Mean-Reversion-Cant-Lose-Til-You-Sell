import pandas as pd
import time
import multiprocessing as mp

"""
logic() function:
    Context: Called for every row in the input data.

    Input:  account - the account object
            lookback - the lookback dataframe, containing all data up until this point in time

    Output: none, but the account object will be modified on each call
"""


def logic(
    account, lookback, v1, v2, v3, v4
):  # Logic function to be used for each time interval in backtest

    today = len(lookback) - 1
    if (
        today > training_period
    ):  # If the lookback is long enough to calculate the Bollinger Bands

        IBS = (lookback["close"][today] - lookback["low"][today]) / (
            lookback["high"][today] - lookback["low"][today]
        )

        if IBS < v1:
            for position in account.positions:  # Close all current positions
                account.close_position(position, 1, lookback["close"][today])
            if account.buying_power > 0:
                account.enter_position(
                    "long", account.buying_power, lookback["close"][today]
                )  # Enter a long position

        elif (
            IBS > 1 - v1
        ):  # If today's price is above the upper Bollinger Band, enter a short position
            for position in account.positions:  # Close all current positions
                account.close_position(position, 1, lookback["close"][today])
            if account.buying_power > 0:
                account.enter_position(
                    "short", account.buying_power, lookback["close"][today]
                )  # Enter a short position

        else:
            for position in account.positions:  # Close all current positions
                account.close_position(position, 1, lookback["close"][today])


"""
preprocess_data() function:
    Context: Called once at the beginning of the backtest. TOTALLY OPTIONAL. 
             Each of these can be calculated at each time interval, however this is likely slower.

    Input:  list_of_stocks - a list of stock data csvs to be processed

    Output: list_of_stocks_processed - a list of processed stock data csvs
"""


def preprocess_data(list_of_stocks):
    list_of_stocks_processed = []
    for stock in list_of_stocks:
        df = pd.read_csv("data/" + stock + ".csv", parse_dates=[0])
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
        df.to_csv("data/" + stock + "_Processed.csv", index=False)  # Save to CSV
        list_of_stocks_processed.append(stock + "_Processed")
    return list_of_stocks_processed
