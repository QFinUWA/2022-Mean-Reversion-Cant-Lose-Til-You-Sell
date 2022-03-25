import main
import main1
# Write function to sweep parameters within the logic function
# pass multiple logic functions? Inefficient
# pass different parameters along with the same funciton, less repeated code 






if __name__ == "__main__":
    # list_of_stocks = ["TSLA_2020-03-01_2022-01-20_1min"]
    list_of_stocks = [
        "TSLA_2020-03-09_2022-01-28_15min",
        "AAPL_2020-03-24_2022-02-12_15min",
    ]  # List of stock data csv's to be tested, located in "data/" folder
    list_of_stocks_proccessed = preprocess_data(list_of_stocks)  # Preprocess the data
    results = tester.test_array(
        list_of_stocks_proccessed, main.logic(), chart=True
    )  # Run backtest on list of stocks using the logic function

    # print("training period " + str(training_period))
    # print("standard deviations " + str(standard_deviations))
    df = pd.DataFrame(
        list(results),
        columns=[
            "Buy and Hold",
            "Strategy",
            "Longs",
            "Sells",
            "Shorts",
            "Covers",
            "Stdev_Strategy",
            "Stdev_Hold",
            "Stock",
        ],
    )  # Create dataframe of results
    df.to_csv("results/Test_Results.csv", index=False)  # Save results to csv