from backtester import API_Interface as api

"""
Common stocks in S&P500:
AAPL
MSFT
AMZN
GOOG
NVDA
UNH
JNJ
FB
JPM
DIS
V
KO
PEP
LLY
TSLA


get_intraday_extended() function:
    Context: Used to get intraday_extended data from Alpha Vantage API.

    Requires: API_Key.txt located in the root folder, Access to the internet

    Input:  symbol: the stock symbol to be returned
            start_date: the starting date for the range of dates to be returned (Can set start date to "all" to return all available data)
            end_date: the ending date for the range of dates to be returned
            interval: the interval of the data to be returned (1min, 5min, 15min, 30min, 60min)
            combine: whether to combine the data into one dataframe or not, if not, saves each timeslice as it's own csv, (combine=True is recommended)

    Output: data: the dataframe containing the intraday_extended data
            OR
            data/SYMBOL_STARTDATE_ENDDATE_INTERVAL.csv: the csv file containing the intraday_extended data

"""


api.get_intraday_extended("AAPL", "all", "", "1min", True)
api.get_intraday_extended("FB", "all", "", "1min", True)
api.get_intraday_extended("MSFT", "all", "", "1min", True)
api.get_intraday_extended("AMZN", "all", "", "1min", True)
api.get_intraday_extended("GOOG", "all", "", "1min", True)
api.get_intraday_extended("NVDA", "all", "", "1min", True)
api.get_intraday_extended("UNH", "all", "", "1min", True)
api.get_intraday_extended("JNJ", "all", "", "1min", True)
# api.get_intraday_extended("FB", "all", "", "1min", True)
api.get_intraday_extended("JPM", "all", "", "1min", True)
api.get_intraday_extended("DIS", "all", "", "1min", True)
api.get_intraday_extended("V", "all", "", "1min", True)
api.get_intraday_extended("KO", "all", "", "1min", True)
api.get_intraday_extended("PEP", "all", "", "1min", True)
api.get_intraday_extended("LLY", "all", "", "1min", True)
# api.get_intraday_extended("SBUX", "all", "", "15min", True)

# api.get_intraday_extended('GOOG', 'all', '', '1min', True)
# api.get_intraday_extended('IBM', '01-01-2008', '01-03-2022', '1min', True)
# api.get_intraday_extended('TSLA', 'year1month2', 'year1month1', '60min', True, False)
# api.get_intraday_extended('TSLA', 'all', 'year1month1', '15min', True, True)
