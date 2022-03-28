"""
logic() function:
    Context: Called for every row in the input data.

    Input:  account - the account object
            lookback - the lookback dataframe, containing all data up until this point in time

    Output: none, but the account object will be modified on each call
"""


def logic(
    account, lookback
):  # Logic function to be used for each time interval in backtest

    today = len(lookback) - 1
