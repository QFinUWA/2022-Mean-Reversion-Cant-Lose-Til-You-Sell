# import pandas_ta as pta
import pandas as pd

from backtester.account import Account


def preprocess_data(
    list_of_stocks: list[str], v1: int, v2=None, v3=None, v4=None, v5=None
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

        # Calculate IBS
        df["IBS"] = (df["close"] - df["low"]) / (df["high"] - df["low"])
        # Save to CSV
        df.to_csv("data/" + stock + "_Processed_rsi_ibs.csv", index=False)
        list_of_stocks_processed.append(stock + "_Processed_rsi_ibs")
    return list_of_stocks_processed


def logic(
    account: Account,
    lookback: pd.DataFrame,
    v1: int,
    v2=None,
    v3=None,
    v4=None,
    v5=None,
) -> None:
    """
    logic() function:
        Context: Called for every row in the input data.

        Input:  account - the account object
                lookback - the lookback dataframe, containing all data up until this point in time

        Output: none, but the account object will be modified on each call"""

    # RSI
    OVERBOUGHT_THRESHOLD = 90
    OVERSOLD_THRESHOLD = 10
    MAINTAIN_THRESHOLD_STAY = 40

    training_period = v1
    today = len(lookback) - 1
    position_type = ""

    IBS_PERCENTILE = 0.2

    if today < training_period:
        return

    # check if long/short positions are not within maintain threshold, and if so sell"
    for position in account.positions:
        if (position.type_ == "long" and (
            lookback["RSI"][today] > MAINTAIN_THRESHOLD_STAY
            or lookback["IBS"][today] > IBS_PERCENTILE)
        ):
            account.close_position(position, 1, lookback["close"][today])

        elif (position.type_ == "short" and (
            lookback["RSI"][today] < 1 - MAINTAIN_THRESHOLD_STAY
            or lookback["IBS"][today] < 1 - IBS_PERCENTILE)
        ):
            account.close_position(position, 1, lookback["close"][today])

    # Set a long position if stock is oversold
    if (
        lookback["RSI"][today] < OVERSOLD_THRESHOLD
        and lookback["IBS"][today] <= IBS_PERCENTILE
    ):
        position_type = "long"

    # Set a short position if stock is overbought
    elif (
        lookback["RSI"][today] > OVERBOUGHT_THRESHOLD
        and lookback["IBS"][today] >= 1 - IBS_PERCENTILE
    ):
        position_type = "short"

    else:
        return

    # Enter the position if buying power is more than 0
    if account.buying_power > 0:
        account.enter_position(
            position_type, account.buying_power, lookback["close"][today]
        )
