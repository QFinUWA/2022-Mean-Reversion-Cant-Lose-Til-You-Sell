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

    lookback_period = v1
    today = len(lookback) - 1

    if today < lookback_period:
        return

    today_close = lookback["close"][today]
    n_day_low = min(list(lookback["low"])[today - lookback_period + 1 : today + 1])
    n_day_high = max(list(lookback["high"])[today - lookback_period + 1 : today + 1])
    top = today_close - n_day_low
    bottom = n_day_high - n_day_low
    stochastic_indicator = (top / bottom) * 100

    if stochastic_indicator >= 80:
        for position in account.positions:  # Close all current positions
            account.close_position(position, 1, lookback["close"][today])
        if account.buying_power > 0:
            account.enter_position(
                "short", account.buying_power, lookback["close"][today]
            )  # Enter a short position
    elif stochastic_indicator <= 20:
        for position in account.positions:  # Close all current positions
            account.close_position(position, 1, lookback["close"][today])
        if account.buying_power > 0:
            account.enter_position(
                "long", account.buying_power, lookback["close"][today]
            )  # Enter a long position
