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

        # Calculate IBS
        df["IBS"] = (df["close"] - df["low"]) / (df["high"] - df["low"])

        # Save to CSV
        df.to_csv("data/" + stock + "_Processed_rsi.csv", index=False)
        list_of_stocks_processed.append(stock + "_Processed_rsi")
    return list_of_stocks_processed


def logic(
    account: Account,
    lookback: pd.DataFrame,
    v1: int,
    v2=0.05,
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

    training_period = v1
    today = len(lookback) - 1
    position_type = ""

    IBS_PERCENTILE = v2

    if today < training_period:
        return

    # IMPLMENENT LOGIC

    if account.buying_power > 0:
        account.enter_position(
            position_type, account.buying_power, lookback["close"][today]
        )
