import pandas as pd

# local imports
from backtester import tester
from logic_functions.stochastic import logic

# Bollinger
standard_deviations = (
    3.5  # Number of Standard Deviations from the mean the Bollinger Bands sit
)

# Stochasic
rolling_average = 3  # D% rolling average
lower_bound = 30  # Lower bound of stochastic indicator
upper_bound = 70  # upper bound of stochastic indicator


"""
preprocess_data() function:
    Context: Called once at the beginning of the backtest. TOTALLY OPTIONAL.
             Each of these can be calculated at each time interval, however this is likely slower.

    Input:  list_of_stocks - a list of stock data csvs to be processed

    Output: list_of_stocks_processed - a list of processed stock data csvs
"""


def preprocess_data(list_of_stocks, v1=None, v2=None, v3=None, v4=None, v5=None):
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
        "AAPL_2020-03-24_2022-02-12_1min",
    ]  # List of stock data csv's to be tested, located in "data/" folder

    # loop over v1 and test for each
    for training_period in range(
        5, 52, 2
    ):  # Test training periods from 2 to 50 in steps of 2

        # print(f"training period {training_period}")
        # print("standard deviations " + str(rolling_average))

        print(f"training period {training_period}")
        print(f"rolling average {rolling_average}")
        print(f"lower bound {lower_bound}")
        print(f"upper bound: {upper_bound}")

        list_of_stocks_proccessed = preprocess_data(
            list_of_stocks,
            v1=training_period,
            v2=rolling_average,
            v3=lower_bound,
            v4=upper_bound,
        )  # Preprocess the data

        results = tester.test_array(
            list_of_stocks_proccessed,
            logic,
            chart=False,
            v1=training_period,
            v2=rolling_average,
            v3=lower_bound,
            v4=upper_bound,
        )
        df = pd.DataFrame(list(results))  # Create dataframe of results
        df.to_csv(
            "results/Test_Results.csv", mode="a", header=False, index=False
        )  # Save results to csv
