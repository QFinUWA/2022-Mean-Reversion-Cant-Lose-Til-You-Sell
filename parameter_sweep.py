# import main
# Swap with importing main when example is defunct


# from logic_functions.bollinger import preprocess_data, logic

# from logic_functions.rsi import preprocess_data, logic

# from logic_functions.rsi_ta import preprocess_data, logic

# from logic_functions.bb_rsi import preprocess_data, logic
# from logic_functions.bb_rsi_longs_only import preprocess_data, logic

# from logic_functions.bb_rsi_stoch import preprocess_data, logic
from logic_functions.bb_rsi_stoch_longs_only import preprocess_data, logic

from backtester import tester
import pandas as pd

"""
    Modifications to make to the code:
        Ensure that logic functions accept v1,v2,v3,v4 as parameters. These will be the values we use to loop over to sweep parameters.
        This also changed the backend backtester code

"""


if __name__ == "__main__":
    # list_of_stocks = ["TSLA_2020-03-01_2022-01-20_1min"]
    list_of_stocks = [
        "TSLA_2020-03-09_2022-01-28_15min",
        "AAPL_2020-03-24_2022-02-12_15min",
        "DIS_2020-04-27_2022-03-18_15min",
        "SBUX_2020-04-27_2022-03-18_15min",
        # "TSLA_2020-03-01_2022-01-20_1min",
        # "AAPL_2020-03-24_2022-02-12_1min",
    ]  # List of stock data csv's to be tested, located in "data/" folder

    # loop over v1 and test for each
    # for training_period in range(
    #     2, 52, 2
    # ):  # Test training periods from 2 to 50 in steps of 2
    for training_period in range(14, 15):
        # for standard_deviations in range(1, 10, 1): # Test standard deviations from 1 to 9 in steps of 1. as an example, Will test each standard deviation for each training period 2-52 in steps of 2.
        standard_deviations = 2
        k_period = 14
        d_preiod = 3
        list_of_stocks_proccessed = preprocess_data(
            list_of_stocks,
            v1=standard_deviations,
            v2=training_period,
            v3=k_period,
            v4=d_preiod,
        )  # Preprocess the data
        results = tester.test_array(
            list_of_stocks_proccessed, logic, chart=True, v1=training_period
        )
        print("training period " + str(training_period))
        print("standard deviations " + str(standard_deviations))
        df = pd.DataFrame(list(results))  # Create dataframe of results
        df.to_csv(
            "results/Test_Results.csv", mode="a", header=False, index=False
        )  # Save results to csv
