from numpy import average

"""
logic() function:
    Context: Called for every row in the input data.

    Input:  account - the account object
            lookback - the lookback dataframe, containing all data up until this point in time
            v1 - training period
            v2 - rolling average period
            v3 - stochastic lower bound
            v4 - stochastic upper bound

    Output: none, but the account object will be modified on each call
"""


def logic(
    account, lookback, v1, v2, v3, v4, v5
):  # Logic function to be used for each time interval in backtest

    training_period = v1
    today = len(lookback) - 1

    if today < training_period:
        return

    today_close = lookback["close"][today]

    # Implement a queue to keep track of last n-day lows and highs.
    account.n_day_low.append(lookback["low"][today])
    if len(account.n_day_low) > training_period:
        account.n_day_low.pop(0)
    account.n_day_high.append(lookback["high"][today])
    if len(account.n_day_high) > training_period:
        account.n_day_high.pop(0)

    # Implement stochastic indicator calculations
    top = today_close - min(account.n_day_low)
    bottom = max(account.n_day_high) - min(account.n_day_low)

    if bottom == 0:
        k_stochastic_indicator = 0
    else:
        k_stochastic_indicator = (top / bottom) * 100

    # Implement a queue to keep track of last n-day k% stochastic indicators.
    account.n_day_k_stochastic.append(k_stochastic_indicator)
    if len(account.n_day_k_stochastic) > v2:
        account.n_day_k_stochastic.pop(0)

    d_stochastic_indicator = average(account.n_day_k_stochastic)

    if d_stochastic_indicator == k_stochastic_indicator:

        # Enter a long position if k% indicator is below lower bound
        if n_day_k_stochastic[-2] > v3 and n_day_k_stochastic[-1] <= v3:
            for position in account.positions:  # Close all current positions
                account.close_position(position, 1, lookback["close"][today])
            if account.buying_power > 0:
                account.enter_position(
                    "long", account.buying_power, lookback["close"][today]
                )  # Enter a long position

        # Enter a short position if k% indicator is above upper bound
        elif n_day_k_stochastic[-2] < v4 and k_stochastic_indicator >= v4:
            for position in account.positions:  # Close all current positions
                account.close_position(position, 1, lookback["close"][today])
            if account.buying_power > 0:
                account.enter_position(
                    "short", account.buying_power, lookback["close"][today]
                )  # Enter a short position
