# import main
# Swap with importing main when example is defunct
# from logic_functions.bollinger import preprocess_data, logic
# from logic_functions.rsi import preprocess_data, logic
# from logic_functions.rsi_ta import preprocess_data, logic
# from logic_functions.bb_rsi import preprocess_data, logic
# from logic_functions.bb_rsi_stoch_nick import preprocess_data, logic
# from logic_functions.ibs import preprocess_data, logic
from logic_functions.rsi_ibs import preprocess_data, logic

from backtester import tester
import pandas as pd

"""
    Modifications to make to the code:
        Ensure that logic functions accept v1,v2,v3,v4 as parameters. These will be the values we use to loop over to sweep parameters.
        This also changed the backend backtester code


rolling_average = 3  # D% rolling average
lower_bound = 30  # Lower bound of stochastic indicator
upper_bound = 70  # upper bound of stochastic indicator
"""

BUYING_THRESHOLD = ""
MAINTAIN_THRESHOLD_STAY = ""
IBS_PERCENTILE = ""


if __name__ == "__main__":
    list_of_stocks = [
        "TSLA_2020-03-01_2022-01-20_1min",
        # "AAPL_2020-03-24_2022-02-12_1min",
    ]  # List of stock data csv's to be tested, located in "data/" folder

    # loop over v1 and test for each
    # for training_period in range(
    #     2, 52, 2
    # ):  # Test training periods from 2 to 50 in steps of 2
    for training_period in range(20, 41, 10):
        for BUYING_THRESHOLD in range(10, 11):
            for MAINTAIN_THRESHOLD_STAY in range(20, 41, 10):
                for IBS_PERCENTILE in range(1, 6, 2):
                    # for standard_deviations in range(1, 10, 1): # Test standard deviations from 1 to 9 in steps of 1. as an example, Will test each standard deviation for each training period 2-52 in steps of 2.
                    IBS_PERCENTILE = IBS_PERCENTILE / 10
                    standard_deviations = 2
                    k_period = 14
                    d_preiod = 3
                    list_of_stocks_proccessed = preprocess_data(
                        list_of_stocks,
                        v1=training_period,
                        v2=BUYING_THRESHOLD,
                        v3=MAINTAIN_THRESHOLD_STAY,
                        v4=IBS_PERCENTILE,
                    )  # Preprocess the data
                    results = tester.test_array(
                        list_of_stocks_proccessed,
                        logic,
                        chart=False,
                        v1=training_period,
                        v2=BUYING_THRESHOLD,
                        v3=MAINTAIN_THRESHOLD_STAY,
                        v4=IBS_PERCENTILE,
                    )
                    print("training period " + str(training_period))
                    print("BUYING_THRESHOLD " + str(BUYING_THRESHOLD))
                    print("MAINTAIN_THRESHOLD_STAY " + str(MAINTAIN_THRESHOLD_STAY))
                    print("IBS_PERCENTILE " + str(IBS_PERCENTILE))

                    df = pd.DataFrame(list(results))  # Create dataframe of results
                    df.to_csv(
                        "results/Test_Results.csv", mode="a", header=False, index=False
                    )  # Save results to csv
