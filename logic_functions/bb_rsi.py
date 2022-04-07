import pandas as pd

# import pandas_ta as pta

from backtester.account import Account


def preprocess_data(
    list_of_stocks: list[str], v1: int, v2: float, v3=None, v4=None
) -> list[str]:
    """
    preprocess_data() function:
        Context: Called once at the beginning of the backtest. TOTALLY OPTIONAL.
                 Each of these can be calculated at each time interval, however this is likely slower.

        Input:  list_of_stocks - a list of stock data csvs to be processed

        Output: list_of_stocks_processed - a list of processed stock data csvs"""

    training_period = v1  # How far the rolling average takes into calculation
    standard_deviations = v2
    list_of_stocks_processed: list[str] = []
    for stock in list_of_stocks:
        df = pd.read_csv("data/" + stock + ".csv", parse_dates=[0])
        # Calculate typical price and change
        df["TP"] = (df["close"] + df["low"] + df["high"]) / 3
        df["TP_CHANGE"] = df["TP"].diff()

        # Calculate gain and loss in absolute values
        df["TP_CHANGE_GAIN"] = df["TP_CHANGE"].clip(lower=0)
        df["TP_CHANGE_LOSS"] = -df["TP_CHANGE"].clip(upper=0)

        # Calculate simple moving average of gain and loss
        df["MA_TP_GAIN"] = df["TP_CHANGE_GAIN"].rolling(training_period).mean()
        df["MA_TP_LOSS"] = df["TP_CHANGE_LOSS"].rolling(training_period).mean()

        # Calculate rs and rsi
        df["RS"] = df["MA_TP_GAIN"] / df["MA_TP_LOSS"]
        df["RSI"] = 100 - (100 / (1 + df["RS"]))

        # Calculate the standard deviation
        df["STD"] = df["TP"].rolling(training_period).std()

        # Calculate simple moving average of typical price
        df["MA_TP"] = df["TP"].rolling(training_period).mean()

        # Calculate upper and lower Bollinger Bands
        df["BB_UP"] = df["MA_TP"] + standard_deviations * df["STD"]
        df["BB_LO"] = df["MA_TP"] - standard_deviations * df["STD"]

        # Save to CSV
        df.to_csv("data/" + stock + "_Processed_bb_rsi.csv", index=False)
        list_of_stocks_processed.append(stock + "_Processed_bb_rsi")
    return list_of_stocks_processed


def logic(account: Account, lookback: pd.DataFrame, v1: int, v2, v3, v4) -> None:
    """
    logic() function:
        Context: Called for every row in the input data.

        Input:  account - the account object
                lookback - the lookback dataframe, containing all data up until this point in time

        Output: none, but the account object will be modified on each call"""

    OVERBOUGHT_THRESHOLD = 70
    OVERSOLD_THRESHOLD = 30
    # NA = -9999999

    training_period = v1
    today = len(lookback) - 1
    # position_type = ""

    # old_bb_low = NA
    # old_bb_high = NA
    # new_bb_low = NA
    # new_bb_high = NA

    # old_rsi_low = NA
    # old_rsi_high = NA
    # new_rsi_low = NA
    # new_rsi_high = NA

    if today < training_period:
        return

    # Do nothing if RSI is in between the range
    if (
        lookback["RSI"][today] >= OVERSOLD_THRESHOLD
        and lookback["RSI"][today] <= OVERBOUGHT_THRESHOLD
    ):
        return

    # Set a long position if stock is oversold and current price is below lower Bollinger Band
    elif (
        lookback["RSI"][today] < OVERSOLD_THRESHOLD
        and lookback["close"][today] < lookback["BB_LO"][today]
    ):
        for position in account.positions:
            account.close_position(position, 1, lookback["close"][today])
        # position_type = "long"
        if account.buying_power > 0:
            account.enter_position(
                "long", account.buying_power, lookback["close"][today]
            )

    # Set a short position if stock is overbought and current price is above upper Bollinger Band
    elif (
        lookback["RSI"][today] > OVERBOUGHT_THRESHOLD
        and lookback["close"][today] > lookback["BB_UP"][today]
    ):
        # else:
        for position in account.positions:
            account.close_position(position, 1, lookback["close"][today])
        # position_type = "short"
        if account.buying_power > 0:
            account.enter_position(
                "short", account.buying_power, lookback["close"][today]
            )

    # Enter the position if buying power is more than 0
    # if account.buying_power > 0:
    #     account.enter_position(
    #         position_type, account.buying_power, lookback["close"][today]
    #     )
