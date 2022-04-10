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

        # Calculate the standard deviation
        df["STD"] = df["close"].rolling(training_period).std()

        # Calculate simple moving average of closing price
        df["MA"] = df["close"].rolling(training_period).mean()

        # Calculate upper and lower Bollinger Bands
        df["BB_UP"] = df["MA"] + standard_deviations * df["STD"]
        df["BB_LO"] = df["MA"] - standard_deviations * df["STD"]

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

    if today < training_period:
        return

    # Enter a long position if stock is oversold and current price is below lower Bollinger Band
    if (
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
        account.prev_bb_low = lookback["close"][today]
        account.prev_rsi_low = lookback["close"][today]

    # Enter a short position if stock is overbought and current price is above upper Bollinger Band
    elif (
        lookback["RSI"][today] > OVERBOUGHT_THRESHOLD
        and lookback["close"][today] > lookback["BB_UP"][today]
    ):
        for position in account.positions:
            account.close_position(position, 1, lookback["close"][today])
        if account.buying_power > 0:
            account.enter_position(
                "short", account.buying_power, lookback["close"][today]
            )
        account.prev_bb_high = lookback["close"][today]
        account.prev_rsi_high = lookback["close"][today]

    # elif (
    #     lookback["RSI"][today] < OVERSOLD_THRESHOLD
    #     and lookback["close"][today] > lookback["BB_LO"][today]
    # ):
    #     for position in account.positions:
    #         account.close_position(position, 1, lookback["close"][today])
    #     # position_type = "long"
    #     if account.buying_power > 0:
    #         account.enter_position(
    #             "long", account.buying_power, lookback["close"][today]
    #         )

    # Regular divergences signal a possible trend reversal.
    # Bullish: Lower low price, Higher low oscillator, downtrend to uptrend, long
    # Bearish: Higher high price, Lower high oscillator, uptrend to downtrend, short

    # Hidden divergences signal a possible trend continuation.
    # Bullish: Higher low price, Lower low oscillator, Buy the dips, long
    # Bearish: Lower high price, Higher high oscillator, Sell the rallies, short

    # source: https://www.babypips.com/learn/forex/divergence-cheat-sheet
