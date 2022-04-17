"""
logic() function:
    Context: Called for every row in the input data.

    Input:  account - the account object
            lookback - the lookback dataframe, containing all data up until this point in time

    Output: none, but the account object will be modified on each call
"""

from numpy import average


def logic(
    account, lookback, v1, v2, v3, v4, v5
):  # Logic function to be used for each time interval in backtest

    lookback_period = v1
    today = len(lookback) - 1

    if today < lookback_period:
        return

    today_close = lookback["close"][today]
    account.n_day_low.append(lookback["low"][today])
    account.n_day_high.append(lookback["high"][today])

    if len(account.n_day_low) == lookback_period + 1:
        account.n_day_low.pop(0)
    if len(account.n_day_high) == lookback_period + 1:
        account.n_day_high.pop(0)

    top = today_close - min(account.n_day_low)
    bottom = max(account.n_day_high) - min(account.n_day_low)
    k_stochastic_indicator = (top / bottom) * 100

    account.n_day_k_stochastic.append(k_stochastic_indicator)
    if len(account.n_day_k_stochastic) == 4:
        account.n_day_k_stochastic.pop(0)

    if average(account.n_day_k_stochastic) == k_stochastic_indicator:
        if k_stochastic_indicator >= 80:
            for position in account.positions:  # Close all current positions
                account.close_position(position, 1, lookback["close"][today])
            if account.buying_power > 0:
                account.enter_position(
                    "short", account.buying_power, lookback["close"][today]
                )  # Enter a short position

        elif k_stochastic_indicator <= 20:
            for position in account.positions:  # Close all current positions
                account.close_position(position, 1, lookback["close"][today])
            if account.buying_power > 0:
                account.enter_position(
                    "long", account.buying_power, lookback["close"][today]
                )  # Enter a long position
