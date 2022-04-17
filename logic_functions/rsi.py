# import pandas_ta as pta
import pandas as pd

from backtester.account import Account


def preprocess_data(
    list_of_stocks: list[str], v1: int, v2=None, v3=None, v4=None
) -> list[str]:
    """
    preprocess_data() function:
        Context: Called once at the beginning of the backtest. TOTALLY OPTIONAL.
                 Each of these can be calculated at each time interval, however this is likely slower.

        Input:  list_of_stocks - a list of stock data csvs to be processed

        Output: list_of_stocks_processed - a list of processed stock data csvs"""

    training_period = v1  # How far the rolling average takes into calculation
    list_of_stocks_processed: list[str] = []
    for stock in list_of_stocks:
        df = pd.read_csv("data/" + stock + ".csv", parse_dates=[0])

        # Calculate change
        df["CHANGE"] = df["close"].diff()

        # Calculate gain and loss in absolute values
        df["CHANGE_GAIN"] = df["CHANGE"].clip(lower=0)
        df["CHANGE_LOSS"] = -df["CHANGE"].clip(upper=0)

        # Calculate simple moving average of gain and loss
        df["MA_GAIN"] = df["CHANGE_GAIN"].rolling(training_period).mean()
        df["MA_LOSS"] = df["CHANGE_LOSS"].rolling(training_period).mean()

        # Calculate rs and rsi
        df["RS"] = df["MA_GAIN"] / df["MA_LOSS"]
        df["RSI"] = 100 - (100 / (1 + df["RS"]))

        # Save to CSV
        df.to_csv("data/" + stock + "_Processed_rsi.csv", index=False)
        list_of_stocks_processed.append(stock + "_Processed_rsi")
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

    training_period = v1
    today = len(lookback) - 1
    position_type = ""

    if today < training_period:
        return

    # Do nothing if RSI is in between the range
    if (
        lookback["RSI"][today] >= OVERSOLD_THRESHOLD
        and lookback["RSI"][today] <= OVERBOUGHT_THRESHOLD
    ):
        return

    # Set a long position if stock is oversold
    elif lookback["RSI"][today] < OVERSOLD_THRESHOLD:
        for position in account.positions:
            account.close_position(position, 1, lookback["close"][today])
        position_type = "long"

    # Set a short position if stock is overbought
    # if lookback["RSI"][today] > OVERBOUGHT_THRESHOLD:
    else:
        for position in account.positions:
            account.close_position(position, 1, lookback["close"][today])
        position_type = "short"

    # Enter the position if buying power is more than 0
    if account.buying_power > 0:
        account.enter_position(
            position_type, account.buying_power, lookback["close"][today]
        )
