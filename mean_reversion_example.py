import pandas as pd

# import time
# import multiprocessing as mp

# local imports
from backtester import engine, tester
from backtester import API_Interface as api

training_period = 20  # How far the rolling average takes into calculation
standard_deviations = (
    3.5  # Number of Standard Deviations from the mean the Bollinger Bands sit
)

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

    training_period = v1  # How far the rolling average takes into calculation
    stop_loss_percent = v3
    today = len(lookback) - 1
    if (
        today > training_period
    ):  # If the lookback is long enough to calculate the Bollinger Bands

        if (
            account.long_or_short == "long"
            and lookback["close"][today] <= account.stoploss
        ):
            for position in account.positions:  # Close all current positions
                account.close_position(position, 1, lookback["close"][today])
            print("Stoploss hit")

        if (
            account.long_or_short == "short"
            and lookback["close"][today] >= account.takeprofit
        ):
            for position in account.positions:
                account.close_position(position, 1, lookback["close"][today])
            print("Takeprofit hit")

        if (
            lookback["close"][today] < lookback["BOLD"][today]
        ):  # If current price is below lower Bollinger Band, enter a long position
            for position in account.positions:  # Close all current positions
                account.close_position(position, 1, lookback["close"][today])
            if account.buying_power > 0:
                account.enter_position(
                    "long", account.buying_power, lookback["close"][today]
                )  # Enter a long position
                account.stoploss = lookback["close"][today] * (
                    1 - stop_loss_percent
                )  # Set stoploss
                account.long_or_short

        if (
            lookback["close"][today] > lookback["BOLU"][today]
        ):  # If today's price is above the upper Bollinger Band, enter a short position
            for position in account.positions:  # Close all current positions
                account.close_position(position, 1, lookback["close"][today])
            if account.buying_power > 0:
                account.enter_position(
                    "short", account.buying_power, lookback["close"][today]
                )  # Enter a short position
                account.takeprofit = lookback["close"][today] * (
                    1 + stop_loss_percent
                )  # Set takeprofit


"""
preprocess_data() function:
    Context: Called once at the beginning of the backtest. TOTALLY OPTIONAL. 
             Each of these can be calculated at each time interval, however this is likely slower.

    Input:  list_of_stocks - a list of stock data csvs to be processed

    Output: list_of_stocks_processed - a list of processed stock data csvs
"""


def preprocess_data(list_of_stocks, v1=None, v2=None, v3=None, v4=None):
    training_period = v1  # How far the rolling average takes into calculation
    standard_deviations = v2
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


if __name__ == "__main__":
    # list_of_stocks = ["TSLA_2020-03-01_2022-01-20_1min"]
    list_of_stocks = [
        "TSLA_2020-03-09_2022-01-28_15min",
        "AAPL_2020-03-24_2022-02-12_15min",
    ]  # List of stock data csv's to be tested, located in "data/" folder

    # loop over v1 and test for each
    for training_period in range(
        # 2, 52, 2
        30,
        32,
        2,
    ):  # Test training periods from 2 to 50 in steps of 2
        list_of_stocks_proccessed = preprocess_data(
            list_of_stocks, v1=training_period, v2=3.5, v3=0.05
        )  # Preprocess the data
        results = tester.test_array(
            list_of_stocks_proccessed,
            logic,
            chart=False,
            v1=training_period,
            v2=3.5,
            v3=0.10,
        )
        print("training period " + str(training_period))
        print("standard deviations " + str(standard_deviations))
        df = pd.DataFrame(list(results))  # Create dataframe of results
        df.to_csv(
            "results/Test_Results.csv", mode="a", header=False, index=False
        )  # Save results to csv
    # results = tester.test_array(
    #     list_of_stocks_proccessed, logic, chart=True
    # )  # Run backtest on list of stocks using the logic function

    # print("training period " + str(training_period))
    # print("standard deviations " + str(standard_deviations))
    # df = pd.DataFrame(
    #     list(results),
    #     columns=[
    #         "Buy and Hold",
    #         "Strategy",
    #         "Longs",
    #         "Sells",
    #         "Shorts",
    #         "Covers",
    #         "Stdev_Strategy",
    #         "Stdev_Hold",
    #         "Stock",
    #     ],
    # )  # Create dataframe of results
    # df.to_csv("results/Test_Results.csv", index=False)  # Save results to csv
