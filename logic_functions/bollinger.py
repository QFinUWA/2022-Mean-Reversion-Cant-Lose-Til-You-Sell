def logic(
    account, lookback, v1, v2, v3, v4
):  # Logic function to be used for each time interval in backtest

    training_period = v1  # How far the rolling average takes into calculation
    today = len(lookback) - 1
    if (
        today > training_period
    ):  # If the lookback is long enough to calculate the Bollinger Bands

        if (
            lookback["close"][today] < lookback["BOLD"][today]
        ):  # If current price is below lower Bollinger Band, enter a long position
            for position in account.positions:  # Close all current positions
                account.close_position(position, 1, lookback["close"][today])
            if account.buying_power > 0:
                account.enter_position(
                    "long", account.buying_power, lookback["close"][today]
                )  # Enter a long position

        if (
            lookback["close"][today] > lookback["BOLU"][today]
        ):  # If today's price is above the upper Bollinger Band, enter a short position
            for position in account.positions:  # Close all current positions
                account.close_position(position, 1, lookback["close"][today])
            if account.buying_power > 0:
                account.enter_position(
                    "short", account.buying_power, lookback["close"][today]
                )  # Enter a short position
