import pandas as pd


def preprocess_data(list_of_stocks, v1=None, v2=None, v3=None, v4=None, v5=None):
    """
    preprocess_data() function:
        Context: Called once at the beginning of the backtest. TOTALLY OPTIONAL.
                 Each of these can be calculated at each time interval, however this is likely slower.

        Input:  list_of_stocks - a list of stock data csvs to be processed

        Output: list_of_stocks_processed - a list of processed stock data csvs"""

    training_period = v1  # How far the rolling average takes into calculation
    standard_deviations = v2
    list_of_stocks_processed = []
    for stock in list_of_stocks:
        df = pd.read_csv("data/" + stock + ".csv", parse_dates=[0])
        df["std"] = (
            df["close"].rolling(training_period).std()
        )  # Calculate Standard Deviation
        df["MA"] = (
            df["close"].rolling(training_period).mean()
        )  # Calculate Moving Average of Typical Price
        df["BOLU"] = (
            df["MA"] + standard_deviations * df["std"]
        )  # Calculate Upper Bollinger Band
        df["BOLD"] = (
            df["MA"] - standard_deviations * df["std"]
        )  # Calculate Lower Bollinger Band
        df.to_csv("data/" + stock + "_Processed_bb.csv", index=False)  # Save to CSV
        list_of_stocks_processed.append(stock + "_Processed_bb")
    return list_of_stocks_processed


def logic(
    account, lookback, v1, v2, v3, v4, v5
):  # Logic function to be used for each time interval in backtest
    """
    logic() function:
        Context: Called for every row in the input data.

        Input:  account - the account object
                lookback - the lookback dataframe, containing all data up until this point in time

        Output: none, but the account object will be modified on each call"""

    training_period = v1  # How far the rolling average takes into calculation
    today = len(lookback) - 1
    if (
        today > training_period
    ):  # If the lookback is long enough to calculate the Bollinger Bands

        if (
            lookback["close"][today] < lookback["BOLD"][today]
        ):  # If current price is below lower Bollinger Band, enter a long position
            for position in account.positions:  # Close all current positions
                account.close_position(position, 1, lookback["close"][today])
            if account.buying_power > 0:
                account.enter_position(
                    "long", account.buying_power, lookback["close"][today]
                )  # Enter a long position

        if (
            lookback["close"][today] > lookback["BOLU"][today]
        ):  # If today's price is above the upper Bollinger Band, enter a short position
            for position in account.positions:  # Close all current positions
                account.close_position(position, 1, lookback["close"][today])
            if account.buying_power > 0:
                account.enter_position(
                    "short", account.buying_power, lookback["close"][today]
                )  # Enter a short position
