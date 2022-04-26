import pandas as pd

# import pandas_ta as pta

from backtester.account import Account


def preprocess_data(
    list_of_stocks: list[str], v1: int, v2: float, v3: int, v4: int
) -> list[str]:
    """
    preprocess_data() function:
        Context: Called once at the beginning of the backtest. TOTALLY OPTIONAL.
                 Each of these can be calculated at each time interval, however this is likely slower.

        Input:  list_of_stocks - a list of stock data csvs to be processed

        Output: list_of_stocks_processed - a list of processed stock data csvs"""

    standard_deviations = v1
    rsi_period = v2  # How far the rolling average takes into calculation
    k_period = v3  # How far the rolling average takes into calculation
    d_period = v4

    list_of_stocks_processed: list[str] = []
    for stock in list_of_stocks:
        df = pd.read_csv("data/" + stock + ".csv", parse_dates=[0])

        # Calculate change
        df["CHANGE"] = df["close"].diff()

        # Calculate gain and loss in absolute values
        df["CHANGE_GAIN"] = df["CHANGE"].clip(lower=0)
        df["CHANGE_LOSS"] = -df["CHANGE"].clip(upper=0)

        # Calculate simple moving average of gain and loss
        df["MA_GAIN"] = df["CHANGE_GAIN"].rolling(rsi_period).mean()
        df["MA_LOSS"] = df["CHANGE_LOSS"].rolling(rsi_period).mean()

        # Calculate rs and rsi
        df["RS"] = df["MA_GAIN"] / df["MA_LOSS"]
        df["RSI"] = 100 - (100 / (1 + df["RS"]))

        # Calculate min and max values of previous k_period
        df["N_LOW_RSI"] = df["RSI"].rolling(k_period).min()
        df["N_HIGH_RSI"] = df["RSI"].rolling(k_period).max()

        # Calculate Stochastic RSI values (%k and %d as percentage)
        df["%K_RSI"] = (
            100 * (df["RSI"] - df["N_LOW_RSI"]) / (df["N_HIGH_RSI"] - df["N_LOW_RSI"])
        )

        # # Use the %k to calculate a simple moving average over the past <d_period> values of %k
        # df["%D_RSI"] = df["%K_RSI"].rolling(d_period).mean()

        # Calculate the standard deviation
        df["STD"] = df["close"].rolling(rsi_period).std()

        # Calculate simple moving average of closing price
        df["MA"] = df["close"].rolling(rsi_period).mean()

        # Calculate upper and lower Bollinger Bands
        df["BB_UP"] = df["MA"] + standard_deviations * df["STD"]
        df["BB_LO"] = df["MA"] - standard_deviations * df["STD"]

        # Save to CSV
        df.to_csv("data/" + stock + "_Processed_bb_rsi_stoch.csv", index=False)
        list_of_stocks_processed.append(stock + "_Processed_bb_rsi_stoch")
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
    offset = v2

    OVERBOUGHT_THRESHOLD = 80 - offset
    OVERSOLD_THRESHOLD = 20 + offset
    NA = -9999999

    training_period = v1
    today = len(lookback) - 1

    if today < training_period:
        return

    # source: https://www.babypips.com/learn/forex/divergence-cheat-sheet
    # Regular divergences signal a possible trend reversal.
    # Hidden divergences signal a possible trend continuation.
    if (
        (
            lookback["%K_RSI"][today] >= OVERSOLD_THRESHOLD
            and lookback["%K_RSI"][today - 1] < OVERSOLD_THRESHOLD
            or lookback["close"][today] < lookback["BB_LO"][today]
            # and lookback["close"][today] < lookback["BB_LO"][today]
        )
        and account.prev_bb_low != NA
        and account.prev_rsi_low != NA
    ):
        # Regular Bullish: Lower low price, Higher low oscillator, downtrend to uptrend, long
        if (
            lookback["close"][today] < account.prev_bb_low
            and lookback["%K_RSI"][today] > account.prev_rsi_low
        ):
            close_and_enter("long", account, lookback, today)

        # Hidden Bullish: Higher low price, Lower low oscillator, Buy the dips, long, do not sell
        elif (
            lookback["close"][today] > account.prev_bb_low
            and lookback["%K_RSI"][today] < account.prev_rsi_low
        ):
            close_and_enter("long", account, lookback, today, close=False)

    elif (
        (
            lookback["%K_RSI"][today] <= OVERBOUGHT_THRESHOLD
            and lookback["%K_RSI"][today - 1] > OVERBOUGHT_THRESHOLD
            or lookback["close"][today] > lookback["BB_UP"][today]
            # print("%K_RSI: ", lookback["%K_RSI"][today])
            # and lookback["close"][today] > lookback["BB_UP"][today]
        )
        and account.prev_bb_high != NA
        and account.prev_rsi_high != NA
    ):
        # Regular Bearish: Higher high price, Lower high oscillator, uptrend to downtrend, short
        if (
            lookback["close"][today] > account.prev_bb_high
            and lookback["%K_RSI"][today] < account.prev_rsi_high
        ):
            close_and_enter("short", account, lookback, today)

        # Hidden Bearish: Lower high price, Higher high oscillator, Sell the rallies, short, do not cover
        elif (
            lookback["close"][today] < account.prev_bb_high
            and lookback["%K_RSI"][today] > account.prev_rsi_high
        ):
            close_and_enter("short", account, lookback, today, close=False)

    # Record the lows if the low variables are not available
    elif (
        (
            lookback["close"][today] < lookback["BB_LO"][today]
            or lookback["%K_RSI"][today] < OVERSOLD_THRESHOLD
        )
        and account.prev_bb_low == NA
        and account.prev_rsi_low == NA
    ):
        account.prev_bb_low = lookback["close"][today]
        account.prev_rsi_low = lookback["close"][today]

    # Record the highs if the high variables are not available
    elif (
        (
            lookback["close"][today] > lookback["BB_UP"][today]
            or lookback["%K_RSI"][today] > OVERBOUGHT_THRESHOLD
        )
        and account.prev_bb_high == NA
        and account.prev_rsi_high == NA
    ):
        account.prev_bb_high = lookback["close"][today]
        account.prev_rsi_high = lookback["close"][today]


def close_and_enter(
    pos: str,
    account: Account,
    lookback: pd.DataFrame,
    today: int,
    percentage: float = 1,
    /,
    *,
    close: bool = True,
    enter: bool = True,
) -> None:
    if close:
        for position in account.positions:
            account.close_position(position, percentage, lookback["close"][today])

    if enter and account.buying_power > 0:
        account.enter_position(pos, account.buying_power, lookback["close"][today])

    if pos == "long":
        account.prev_bb_low = lookback["close"][today]
        account.prev_rsi_low = lookback["close"][today]
    else:
        account.prev_bb_high = lookback["close"][today]
        account.prev_rsi_high = lookback["close"][today]
