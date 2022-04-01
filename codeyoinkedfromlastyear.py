import pandas as pd
from pandas import DataFrame
from talib.abstract import *
import time
import numpy as np
import multiprocessing as mp

# local imports
from gemini_modules import engine

# LOGIC FUNCTIONS
LOGIC0 = {
    "name":"standard_no_volume",
    "active": False,
    "price_start_index": 50,
    "price_end_index": 52,
    "price_multiplier": 2,
    "price_index":0,
    "volume_index":0,
    "price_long_index":0,
}

LOGIC1 = {
    "name":"standard",
    "active": False,
    "price_start_index": 22,
    "price_end_index": 25,
    "price_multiplier": 2,
    "price_index":0,
    "volume_start_index": 0,
    "volume_end_index": 25,
    "volume_multiplier": 2,
    "volume_index":0,
    "price_long_index":0,
}

LOGIC2 = {
    "name":"exp_no_volume",
    "active": True,
    "price_start_index": 0,
    "price_end_index": 25,
    "price_multiplier": 2,
    "price_index":0,
    "volume_index":0,
    "price_long_index":0,
}

LOGIC3 = {
    "name":"Crossover moving average",
    "active": False,
    "price_start_index": 0,
    "price_end_index": 25,
    "price_multiplier": 2,
    "price_index":0,
    "price_long_start_index": 0,
    "price_long_end_index": 25,
    "price_long_multiplier": 2,
    "price_long_index":0,
    "volume_index":0,
}





#Convert python dictionarys to javascripts ones for cleaner code :D
class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self
LOGIC0 = AttrDict(LOGIC0)
LOGIC1 = AttrDict(LOGIC1)
LOGIC2 = AttrDict(LOGIC2)
LOGIC3 = AttrDict(LOGIC3)


price_window = None
price_window_long = None
price_array = None
volume_array = None
volume_window = None


def updateglobals(logic_function):
    global price_window,price_array,volume_array,volume_window,price_window_long
    price_array = np.array([])
    volume_array = np.array([])
    price_window = logic_function.price_index
    volume_window = logic_function.volume_index
    price_window_long = logic_function.price_long_index



def logic0(account, lookback):
    global price_window,price_array
    try:
        today = len(lookback)-1
        price_array = np.append(price_array,lookback['close'][today])
        if(len(price_array) > price_window):
            price_array = np.delete(price_array,0) 

        if(today > price_window and len(price_array)>0):
            price_moving_average = np.mean(price_array) 
            if(lookback['close'][today] <= price_moving_average):
                    if(account.buying_power > 0):
                        account.enter_position('long', account.buying_power, lookback['close'][today]*1.0001)
            else:
                if(lookback['close'][today] >= price_moving_average):
                    for position in account.positions:
                        account.close_position(position, 1, lookback['close'][today]*0.9999)
    except Exception as e:
        print(e)
    pass  # Handles lookback errors in beginning of dataset



def logic1(account, lookback):
    global price_array,volume_array
    try:
        today = len(lookback)-1
        price_array = np.append(price_array,lookback['close'][today])
        volume_array = np.append(volume_array,lookback['volume'][today])

        if(len(price_array) > price_window):
            price_array = np.delete(price_array,0)
        
        if(len(volume_array) > volume_window):
            volume_array = np.delete(volume_array,0)    
        
        if(today > price_window and today > volume_window and len(price_array) > 0 and len(volume_array) > 0): 
            price_moving_average = np.mean(price_array)
            volume_moving_average = np.mean(volume_array)  
            if(lookback['close'][today] <= price_moving_average):
                if(lookback['volume'][today] >= volume_moving_average):
                    if(account.buying_power > 0):
                        account.enter_position('long', account.buying_power, lookback['close'][today]*1.0001)
            else:
                if(lookback['close'][today] >= price_moving_average):
                    if(lookback['volume'][today] <= volume_moving_average):
                        for position in account.positions:
                                account.close_position(position, 1, lookback['close'][today]*0.9999)
    except Exception as e:
        print(e)
    pass  # Handles lookback errors in beginning of dataset

def logic2(account, lookback):
    try:
        today = len(lookback)-1
        if(today > price_window and price_window != 0):
            exp_price_moving_average = lookback['close'].ewm(span=price_window).mean()[today]  # update PMA
            if(lookback['close'][today] <= exp_price_moving_average):
                if(account.buying_power > 0):
                    account.enter_position('long', account.buying_power, lookback['close'][today]*1.0001)
                    #print("bought at" + str(lookback["date"][today]))
            else:
                if(lookback['close'][today] >= exp_price_moving_average):
                    for position in account.positions:
                            account.close_position(position, 1, lookback['close'][today]*0.9999)
                            #print("sold at" + str(lookback["date"][today]))
    except Exception as e:
        print(e)
    pass 


def logic3(account, lookback):
    try:
        today = len(lookback)-1
        yesterday = len(lookback)-2

        if(today > price_window_long): 
            long_price_moving_average = lookback['close'].rolling(window=price_window_long).mean()[today]  # update long average
            short_price_moving_average = lookback['close'].rolling(window=price_window).mean()[today]  # update short average
            yesterday_long_price_moving_average = lookback['close'].rolling(window=price_window_long).mean()[yesterday]  # yesterday long average
            yesterday_short_price_moving_average = lookback['close'].rolling(window=price_window).mean()[yesterday]  # yesterday short average
            
            if(yesterday_short_price_moving_average < yesterday_long_price_moving_average and short_price_moving_average >= long_price_moving_average):
                    if(account.buying_power > 0):
                        account.enter_position('long', account.buying_power, lookback['close'][today]*1.0001)
            else:
                if(yesterday_long_price_moving_average < yesterday_short_price_moving_average and long_price_moving_average >= short_price_moving_average):
                        for position in account.positions:
                                account.close_position(position, 1, lookback['close'][today]*0.9999)

    except Exception as e:
        print(e)
    pass  # Handles lookback errors in beginning of dataset



list_of_coins = ["USDT_ADA","USDT_BTC","USDT_ETH","USDT_LTC","USDT_XRP","USDT_DASH","USDT_NEO"]

lock = mp.Lock()
def backtest_coin(results,coin,logic_function,logic):
    df = pd.read_csv("data/" + coin + ".csv", parse_dates=[0])
    updateglobals(logic_function)
    backtest = engine.backtest(df)
    backtest.start(1000, logic)
    lock.acquire()
    data = backtest.results()
    data.extend([coin,logic_function.name,logic_function.volume_index,logic_function.price_index,logic_function.price_long_index]) #coinname
    results.append(data)
    lock.release()


if __name__ == "__main__":
    print("Running Algorithms...")
    manager = mp.Manager()
    results = manager.list()
    starttime = time.time()
    if(LOGIC0.active):
        for price_window in range(LOGIC0.price_start_index,LOGIC0.price_end_index):
            print("LOGIC 1: COMPLETED: " + str(price_window) + " REMAINING: "+  str(LOGIC0.price_end_index) )
            LOGIC0.price_index = price_window*LOGIC0.price_multiplier
            processes = []
            for coin in list_of_coins:
                p = mp.Process(target=backtest_coin, args=(results,coin,LOGIC0,logic0))
                processes.append(p)
                p.start()
            for process in processes:
                process.join()
                processes.remove(process)
    print("Done Logic 0")
    if(LOGIC1.active):
        for price_window in range(LOGIC1.price_start_index,LOGIC1.price_end_index):
            LOGIC1.price_index = price_window*LOGIC1.price_multiplier
            for volume_window in range(LOGIC1.volume_start_index,LOGIC1.volume_end_index):
                print("LOGIC 0: COMPLETED: " + str(price_window) +":"+ str(volume_window) + " REMAINING: "+ str(LOGIC1.price_end_index) + ":"+str(LOGIC1.volume_end_index) )
                LOGIC1.volume_index = volume_window*LOGIC1.volume_multiplier
                processes = []
                for coin in list_of_coins:
                    p = mp.Process(target=backtest_coin, args=(results,coin,LOGIC1,logic1))
                    processes.append(p)
                    p.start()
                for process in processes:
                    process.join()
                    processes.remove(process)
    print("Done Logic 1")
    if(LOGIC2.active):
        for price_window in range(LOGIC2.price_start_index,LOGIC2.price_end_index):
            LOGIC2.price_index = price_window*LOGIC2.price_multiplier 
            processes = []
            for coin in list_of_coins:
                p = mp.Process(target=backtest_coin, args=(results,coin,LOGIC2,logic2))
                processes.append(p)
                p.start()
            for process in processes:
                process.join()
                processes.remove(process)
    print("Done Logic 2")
    if(LOGIC3.active):
        for price_window in range(LOGIC3.price_start_index,LOGIC3.price_end_index):
            print("logic 3", price_window)
            LOGIC3.price_index = price_window*LOGIC3.price_multiplier
            for price_window_long in range(LOGIC3.price_long_start_index,LOGIC3.price_long_end_index):
                LOGIC3.price_long_index = price_window_long*LOGIC3.price_long_multiplier
                processes = []
                for coin in list_of_coins:
                    p = mp.Process(target=backtest_coin, args=(results,coin,LOGIC3,logic3))
                    processes.append(p)
                    p.start()
                for process in processes:
                    process.join()
                    processes.remove(process)



    df = DataFrame(list(results),columns=["Buy and Hold","Strategy","Longs","Sells","Shorts","Covers","Stdev_Strategy","Stdev_Hold","Coin",'Strategy_Name','Volume_Window','Price_Window','Long_Price_Window'])
    df.to_csv("resultsbugtest.csv",index =False)
    print("Done")
    print('That took {} seconds'.format(time.time() - starttime))