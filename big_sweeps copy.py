# from logic_functions.bollinger import preprocess_data, logic

# from logic_functions.rsi import preprocess_data, logic

# from logic_functions.rsi_ta import preprocess_data, logic


# from cv2 import threshold, trace
import backtester
import time

import logic_functions.stochastic as stochastic
import logic_functions.rsi as rsi
import logic_functions.bollinger as bollinger
import logic_functions.bb_rsi_longs_only as bb_rsi_longs_only
import logic_functions.rsi_ibs as rsi_ibs
import logic_functions.bb_rsi_stoch as bb_rsi_stoch

import logic_functions.rsi_stochastic as rsi_stochastic

# import logic_functions.bb_rsi_stop_loss

from backtester import tester
import pandas as pd

"""
    Modifications to make to the code:
        Ensure that logic functions accept v1,v2,v3,v4 as parameters. These will be the values we use to loop over to sweep parameters.
        This also changed the backend backtester code

"""


if __name__ == "__main__":
    starttime = time.time()
    print("time taken: ", time.time() - starttime)
    # list_of_stocks = ["TSLA_2020-03-01_2022-01-20_1min"]
    list_of_stocks = [
        "AAPL_2020-04-18_2022-03-09_1min",
        # "AMZN_2020-04-18_2022-03-09_1min",
        # "GOOG_2020-04-18_2022-03-09_1min",
        "MSFT_2020-04-18_2022-03-09_1min",
        # "FB_2020-04-18_2022-03-09_1min",
        # "JNJ_2020-04-18_2022-03-09_1min",
        "JPM_2020-04-18_2022-03-09_1min",
        # "KO_2020-04-18_2022-03-09_1min",
        # "LLY_2020-04-18_2022-03-09_1min",
        "NVDA_2020-04-18_2022-03-09_1min",  # end of 10
        # "PEP_2020-04-18_2022-03-09_1min",
        # "TSLA_2020-03-01_2022-01-20_1min",
        # "UNH_2020-04-18_2022-03-09_1min",
        # "V_2020-04-18_2022-03-09_1min",
    ]  # List of stock data csv's to be tested, located in "data/" folder
    totalruns = 0
    totalnumofruns = 50 + 30 + 120 + 150 + 600 + 120 + 600
    # for training_period in range(2, 50, 5):  # 10 loops
    #     print("time taken: ", time.time() - starttime)
    #     print("Training period: " + str(training_period))
    #     print(
    #         "Training period loop number: "
    #         + str(((training_period - 2) / 5) + 1)
    #         + "/10"
    #     )

    #     for standard_deviation in range(1, 3):  # 5 loops
    #         print("time taken: ", time.time() - starttime)
    #         totalruns += 1
    #         print("total runs: " + str(totalruns) + "/" + str(totalnumofruns))
    #         print("Standard deviation: " + str(standard_deviation) + "/3")
    #         list_of_stocks_proccessed = (
    #             bollinger.preprocess_data(  # 10 stocks (all 10 at once)
    #                 list_of_stocks, v1=training_period, v2=standard_deviation
    #             )
    #         )  # Preprocess the data

    #         # Bollinger Only
    #         results = tester.test_array(
    #             list_of_stocks_proccessed,
    #             bollinger.logic,
    #             chart=False,
    #             v1=training_period,
    #             v2=standard_deviation,
    #         )  # Run the backtester
    #         df = pd.DataFrame(list(results))  # Create dataframe of results
    #         df.columns = [
    #             "Buy and Hold",
    #             "Strategy",
    #             "Longs",
    #             "Sells",
    #             "Shorts",
    #             "Covers",
    #             "Trades",
    #             "Stdev_Strategy",
    #             "Stdev_Hold",
    #             "Stock",
    #             "v1",
    #             "v2",
    #             "v3",
    #             "v4",
    #             "v5",
    #         ]
    #         if training_period == 2 and standard_deviation == 1:
    #             df.to_csv(
    #                 "results/Test_Results_Bollinger.csv",
    #                 mode="a",
    #                 header=True,
    #                 index=False,
    #             )  # Save results to csv
    #         else:
    #             df.to_csv(
    #                 "results/Test_Results_Bollinger.csv",
    #                 mode="a",
    #                 header=False,
    #                 index=False,
    #             )  # Save results to csv

    # for training_period in range(2, 50, 5):  # 10 loops
    #     print("time taken: ", time.time() - starttime)
    #     print("Training period: " + str(training_period))
    #     print(
    #         "Training period loop number: "
    #         + str(((training_period - 2) / 5) + 1)
    #         + "/10"
    #     )
    #     for offset in range(-10, 11, 10):  # 3 loops
    #         print("time taken: ", time.time() - starttime)
    #         totalruns += 1
    #         print("total runs: " + str(totalruns) + "/" + str(totalnumofruns))
    #         print("threshold offset: " + str(offset))
    #         list_of_stocks_proccessed = (
    #             rsi.preprocess_data(  # 10 stocks (all 10 at once)
    #                 list_of_stocks, v1=training_period
    #             )
    #         )  # Preprocess the data
    #         # RSI Only
    #         results = tester.test_array(
    #             list_of_stocks_proccessed,
    #             rsi.logic,
    #             chart=False,
    #             v1=training_period,
    #             v2=80 - offset,  # v2 = [90, 80, 70]
    #             v3=20 + offset,  # v3 = [10, 30, 30]
    #         )  # Run the backtester
    #         df = pd.DataFrame(list(results))  # Create dataframe of results
    #         df.columns = [
    #             "Buy and Hold",
    #             "Strategy",
    #             "Longs",
    #             "Sells",
    #             "Shorts",
    #             "Covers",
    #             "Trades",
    #             "Stdev_Strategy",
    #             "Stdev_Hold",
    #             "Stock",
    #             "v1",
    #             "v2",
    #             "v3",
    #             "v4",
    #             "v5",
    #         ]
    #         if training_period == 2 and offset == -10:
    #             df.to_csv(
    #                 "results/Test_Results_RSI.csv",
    #                 mode="a",
    #                 header=True,
    #                 index=False,
    #             )  # Save results to csv
    #         else:
    #             df.to_csv(
    #                 "results/Test_Results_RSI.csv",
    #                 mode="a",
    #                 header=False,
    #                 index=False,
    #             )  # Save results to csv
    # for training_period in range(2, 50, 5):  # 10 loops
    #     print("time taken: ", time.time() - starttime)
    #     print("Training period: " + str(training_period))
    #     print(
    #         "Training period loop number: "
    #         + str(((training_period - 2) / 5) + 1)
    #         + "/10"
    #     )
    #     for offset in range(-10, 11, 10):  # 3 loops
    #         print("time taken: ", time.time() - starttime)
    #         print("threshold offset: " + str(offset))
    #         for rolling_average in [2, 3, 5, 10]:  # 4 loops
    #             if rolling_average < training_period:
    #                 totalruns += 1
    #                 print("rolling average: " + str(rolling_average))
    #                 print("total runs: " + str(totalruns) + "/" + str(totalnumofruns))
    #                 results = tester.test_array(
    #                     list_of_stocks,
    #                     stochastic.logic,
    #                     chart=False,
    #                     v1=training_period,
    #                     v2=80 - offset,  # v2 = [90, 80, 70]
    #                     v3=20 + offset,  # v3 = [10, 30, 30]
    #                     v4=min(rolling_average, training_period),
    #                 )
    #                 df = pd.DataFrame(list(results))  # Create dataframe of results
    #                 df.columns = [
    #                     "Buy and Hold",
    #                     "Strategy",
    #                     "Longs",
    #                     "Sells",
    #                     "Shorts",
    #                     "Covers",
    #                     "Trades",
    #                     "Stdev_Strategy",
    #                     "Stdev_Hold",
    #                     "Stock",
    #                     "v1",
    #                     "v2",
    #                     "v3",
    #                     "v4",
    #                     "v5",
    #                 ]
    #                 if training_period == 2 and offset == -10 and rolling_average == 2:
    #                     df.to_csv(
    #                         "results/Test_Results_Stochastic.csv",
    #                         mode="a",
    #                         header=True,
    #                         index=False,
    #                     )
    #                 else:
    #                     df.to_csv(
    #                         "results/Test_Results_Stochastic.csv",
    #                         mode="a",
    #                         header=False,
    #                         index=False,
    #                     )  # Save results to csv
    # for training_period in range(2, 50, 5):  # 10 loops
    #     print("time taken: ", time.time() - starttime)
    #     print("Training period: " + str(training_period))
    #     print(
    #         "Training period loop number: "
    #         + str(((training_period - 2) / 5) + 1)
    #         + "/10"
    #     )
    #     for standard_deviation in range(1, 3):  # 5 loops
    #         print("time taken: ", time.time() - starttime)
    #         print("Standard deviation: " + str(standard_deviation) + "/3")
    #         for offset in range(-10, 11, 10):  # 3 loops
    #             print("time taken: ", time.time() - starttime)
    #             totalruns += 1
    #             print("threshold offset: " + str(offset))
    #             print("total runs: " + str(totalruns) + "/" + str(totalnumofruns))
    #             list_of_stocks_proccessed = (
    #                 bb_rsi_longs_only.preprocess_data(  # 10 stocks (all 10 at once)
    #                     list_of_stocks, v1=training_period, v2=standard_deviation
    #                 )
    #             )  # Preprocess the data
    #             results = tester.test_array(
    #                 list_of_stocks_proccessed,
    #                 bb_rsi_longs_only.logic,
    #                 chart=False,
    #                 v1=training_period,
    #                 v2=standard_deviation,
    #                 v3=80 - offset,  # v2 = [90, 80, 70]
    #                 v4=20 + offset,  # v3 = [10, 30, 30]
    #             )  # Run the backtester
    #             df = pd.DataFrame(list(results))  # Create dataframe of results
    #             df.columns = [
    #                 "Buy and Hold",
    #                 "Strategy",
    #                 "Longs",
    #                 "Sells",
    #                 "Shorts",
    #                 "Covers",
    #                 "Trades",
    #                 "Stdev_Strategy",
    #                 "Stdev_Hold",
    #                 "Stock",
    #                 "v1",
    #                 "v2",
    #                 "v3",
    #                 "v4",
    #                 "v5",
    #             ]
    #             if training_period == 2 and offset == -10 and standard_deviation == 1:
    #                 df.to_csv(
    #                     "results/Test_Results_BB_RSI_Longs.csv",
    #                     mode="a",
    #                     header=True,
    #                     index=False,
    #                 )
    #             else:
    #                 df.to_csv(
    #                     "results/Test_Results_BB_RSI_Longs.csv",
    #                     mode="a",
    #                     header=False,
    #                     index=False,
    #                 )  # Save results to csv
    # for training_period in range(20, 50, 5):  # 10 loops fgreggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg
    training_period = 30
    standard_deviation = 3
    offset = 0
    k_period = 20
    # for training_period in range(14, 15, 5):  # 10 loops
    print("time taken: ", time.time() - starttime)
    print("Training period: " + str(training_period))
    print(
        "Training period loop number: " + str(((training_period - 2) / 5) + 1) + "/10"
    )
    # for standard_deviation in range(3, 4):  # 5 loops / 1 loop
    # for standard_deviation in range(2, 3, 2):  # 5 loops
    print("time taken: ", time.time() - starttime)
    print("Standard deviation: " + str(standard_deviation) + "/3")
    # for offset in range(-10, 11, 10):  # 3 loops
    # for offset in range(-10, 0, 10):
    print("time taken: ", time.time() - starttime)
    print("threshold offset: " + str(offset))
    print("total runs: " + str(totalruns) + "/" + str(totalnumofruns))
    # for k_period in range(8, 21, 6):  # 5 loops
    # for k_period in [5, 14]:
    print("time taken: ", time.time() - starttime)
    # if k_period < training_period:
    print("k_period: " + str(k_period))
    totalruns += 1
    list_of_stocks_proccessed = (
        bb_rsi_stoch.preprocess_data(  # 10 stocks (all 10 at once)
            list_of_stocks,
            v1=standard_deviation,
            v2=training_period,
            v3=k_period,
            v4=offset,
        )
    )  # Preprocess the data
    results = tester.test_array(
        list_of_stocks_proccessed,
        bb_rsi_stoch.logic,
        chart=True,
        v1=training_period,
        v2=offset,
        v3=min(k_period, training_period),  # v2 = [90, 80, 70]
        v4=standard_deviation
        # v4=20 + offset,  # v3 = [10, 30, 30]
        # v5=min(k_period, training_period),
    )  # Run the backtester
    df = pd.DataFrame(list(results))  # Create dataframe of results
    df.columns = [
        "Buy and Hold",
        "Strategy",
        "Longs",
        "Sells",
        "Shorts",
        "Covers",
        "Trades",
        "Stdev_Strategy",
        "Stdev_Hold",
        "Stock",
        "v1",
        "v2",
        "v3",
        "v4",
        "v5",
    ]
    if (
        training_period == 2
        and offset == -10
        and standard_deviation == 1
        and k_period == 2
    ):
        df.to_csv(
            "results/Test_Results_final_algo.csv",
            mode="a",
            header=True,
            index=False,
        )
    else:
        df.to_csv(
            "results/Test_Results_final_algo.csv",
            mode="a",
            header=False,
            index=False,
        )  # Save results to csv
    # for training_period in range(2, 50, 5):  # 10 loops
    #     print("time taken: ", time.time() - starttime)
    #     print("Training period: " + str(training_period))
    #     print(
    #         "Training period loop number: "
    #         + str(((training_period - 2) / 5) + 1)
    #         + "/10"
    #     )
    #     for offset in range(-10, 11, 10):  # 3 loops
    #         print("time taken: ", time.time() - starttime)
    #         print("threshold offset: " + str(offset))
    #         print("total runs: " + str(totalruns) + "/" + str(totalnumofruns))
    #         for rolling_average in [2, 3, 5, 10]:  # 4 loops
    #             print("time taken: ", time.time() - starttime)
    #             if rolling_average < training_period:
    #                 print("rolling average: " + str(rolling_average))
    #                 totalruns += 1
    #                 list_of_stocks_proccessed = (
    #                     rsi_stochastic.preprocess_data(  # 10 stocks (all 10 at once)
    #                         list_of_stocks, v1=training_period
    #                     )
    #                 )  # Preprocess the data
    #                 results = tester.test_array(
    #                     list_of_stocks_proccessed,
    #                     rsi_stochastic.logic,
    #                     chart=False,
    #                     v1=training_period,
    #                     v2=80 - offset,  # v2 = [90, 80, 70]
    #                     v3=20 + offset,  # v3 = [10, 30, 30]
    #                     v4=min(rolling_average, training_period),
    #                 )  # Run the backtester
    #             df = pd.DataFrame(list(results))  # Create dataframe of results
    #             df.columns = [
    #                 "Buy and Hold",
    #                 "Strategy",
    #                 "Longs",
    #                 "Sells",
    #                 "Shorts",
    #                 "Covers",
    #                 "Trades",
    #                 "Stdev_Strategy",
    #                 "Stdev_Hold",
    #                 "Stock",
    #                 "v1",
    #                 "v2",
    #                 "v3",
    #                 "v4",
    #                 "v5",
    #             ]
    #             if training_period == 2 and offset == -10 and rolling_average == 2:
    #                 df.to_csv(
    #                     "results/Test_Results_RSI_Stochastic.csv",
    #                     mode="a",
    #                     header=True,
    #                     index=False,
    #                 )
    #             else:
    #                 df.to_csv(
    #                     "results/Test_Results_RSI_Stochastic.csv",
    #                     mode="a",
    #                     header=True,
    #                     index=False,
    #                 )  # Save results to csv
    # for training_period in range(2, 50, 5):  # 10 loops
    #     print("time taken: ", time.time() - starttime)
    #     print("Training period: " + str(training_period))
    #     print(
    #         "Training period loop number: "
    #         + str(((training_period - 2) / 5) + 1)
    #         + "/10"
    #     )
    #     for standard_deviation in range(1, 3):  # 5 loops
    #         print("time taken: ", time.time() - starttime)
    #         print("Standard deviation: " + str(standard_deviation) + "/3")
    #         for offset in range(-10, 11, 10):  # 3 loops
    #             print("time taken: ", time.time() - starttime)
    #             print("threshold offset: " + str(offset))
    #             for stop_loss in [0.05, 0.10, 0.15, 0.20]:  # 4 loops
    #                 print("time taken: ", time.time() - starttime)
    #                 if rolling_average < training_period:
    #                     print("rolling average: " + str(rolling_average))
    #                     print(
    #                         "total runs: " + str(totalruns) + "/" + str(totalnumofruns)
    #                     )
    #                     totalruns += 1
    #                     list_of_stocks_proccessed = bb_rsi_stop_loss.preprocess_data(  # 10 stocks (all 10 at once)
    #                         list_of_stocks, v1=training_period
    #                     )  # Preprocess the data
    #                     results = tester.test_array(
    #                         list_of_stocks_proccessed,
    #                         bb_rsi_stop_loss.logic,
    #                         chart=False,
    #                         v1=training_period,
    #                         v2=standard_deviation,
    #                         v3=80 - offset,  # v2 = [90, 80, 70]
    #                         v4=20 + offset,  # v3 = [10, 30, 30]
    #                         v5=min(rolling_average, training_period),
    #                     )  # Run the backtester
    #                 df = pd.DataFrame(list(results))  # Create dataframe of results
    #                 df.columns = [
    #                     "Buy and Hold",
    #                     "Strategy",
    #                     "Longs",
    #                     "Sells",
    #                     "Shorts",
    #                     "Covers",
    #                     "Trades",
    #                     "Stdev_Strategy",
    #                     "Stdev_Hold",
    #                     "Stock",
    #                     "v1",
    #                     "v2",
    #                     "v3",
    #                     "v4",
    #                     "v5",
    #                 ]
    #                 if (
    #                     training_period == 2
    #                     and offset == -10
    #                     and standard_deviation == 1
    #                     and stop_loss == 0.05
    #                 ):
    #                     df.to_csv(
    #                         "results/Test_Results_BB_RSI_Stop_Loss.csv",
    #                         mode="a",
    #                         header=True,
    #                         index=False,
    #                     )
    #                 else:
    #                     df.to_csv(
    #                         "results/Test_Results_BB_RSI_stop_loss.csv",
    #                         mode="a",
    #                         header=True,
    #                         index=False,
    #                     )  # Save results to csv

    # for training_period in range(10, 50, 5):  # 10 loops
    #     # for training_period in range(14, 15, 5):  # 10 loops
    #     print("time taken: ", time.time() - starttime)
    #     print("Training period: " + str(training_period))
    #     print(
    #         "Training period loop number: "
    #         + str(((training_period - 2) / 5) + 1)
    #         + "/10"
    #     )
    #     for standard_deviation in range(2, 4):
    #         list_of_stocks_proccessed = (
    #             rsi_ibs.preprocess_data(  # 10 stocks (all 10 at once)
    #                 list_of_stocks,
    #                 v1=standard_deviation,
    #             )
    #         )  # Preprocess the data
    #         results = tester.test_array(
    #             list_of_stocks_proccessed,
    #             rsi_ibs.logic,
    #             chart=False,
    #             v1=training_period,
    #         )  # Run the backtester
    #         df = pd.DataFrame(list(results))  # Create dataframe of results
    #         df.columns = [
    #             "Buy and Hold",
    #             "Strategy",
    #             "Longs",
    #             "Sells",
    #             "Shorts",
    #             "Covers",
    #             "Trades",
    #             "Stdev_Strategy",
    #             "Stdev_Hold",
    #             "Stock",
    #             "v1",
    #             "v2",
    #             "v3",
    #             "v4",
    #             "v5",
    #         ]
    #         if (
    #             training_period == 2
    #             and offset == -10
    #             and standard_deviation == 1
    #             and k_period == 2
    #         ):
    #             df.to_csv(
    #                 "results/Test_Results_rsi_ibs.csv",
    #                 mode="a",
    #                 header=True,
    #                 index=False,
    #             )
    #         else:
    #             df.to_csv(
    #                 "results/Test_Results_rsi_ibs.csv",
    #                 mode="a",
    #                 header=False,
    #                 index=False,
    #             )  # Save results to csv
""" 
    To test:    Bollinger Bands,                                            standard deviation - 10*5 = 50
                RSI,                                                        Upper + Lower Threshold - 10*3 = 30
                Stochastic w/ Average,                                      Upper + Lower Threshold, Rolling average - 10*3*4 = 120
                Bollinger + RSI (longs only),                               standard deviation, Upper + Lower Threshold - 10*5*3 = 150
                Bollinger + RSI + Stochastic w/ Average,                    standard deviation, Upper + Lower Threshold, Rolling average - 10*5*3*4 = 600
                Stochastic + RSI                                            Upper + Lower Threshold, Rolling average - 10*3*4 = 120

                Bollinger + RSI (longs only) + Stop Losses,                 standard deviation, Upper + Lower Threshold, Stop Losses - 10*5*3*4 = 600 TEST THIS THEN SEE IF STOPLOSSES ARE GOOD, IF SO THEN ADD TO OTHERS
                Bollinger + RSI + Stochastic w/ Average + Stop Losses,      standard deviation, Upper + Lower Threshold, Rolling average, Stop losses - 10*5*3*4*6 = 3600



"""
