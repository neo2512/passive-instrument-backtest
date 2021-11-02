from nsepy import *
from dateutil.relativedelta import *
from pandas.tseries.frequencies import to_offset
import numpy as np
import pandas as pd
import time
import random
from nsetools import *
import matplotlib.pyplot as plt
import datetime as dt


def max_drawdown( return_series):
    comp_ret = (return_series + 1).cumprod()
    peak = comp_ret.expanding(min_periods=1).max()
    dd = (comp_ret / peak) - 1
    return dd.min()

def cagr(cum_rets_series, N):
    cagr = float((cum_rets_series[-1:].values) ** (1 / (len(cum_rets_series) / N))) - 1
    return round(cagr, 3)

def compound_ret(returns_col):
    returns_col = (returns_col + 1).cumprod()
    return returns_col

def CAGR(last, periods):
    return (((last)**(1/periods))-1)*100


def take_first(array_like):
    return array_like[0]


def take_last(array_like):
    return array_like[-1]

def sharpe_ratio(return_series, N, rf):
    mean = return_series.mean() * N -rf
    sigma = return_series.std() * np.sqrt(N)
    return mean / sigma

class PassiveStrat():
    def __init__(self):
        pass


    def run_strat(self):
        stock_list = ['RELIANCE',
        'TCS',
        'HDFCBANK',
        'INFY',
        'HINDUNILVR',
        'HDFC',
        'ICICIBANK',
        'KOTAKBANK',
        'SBIN',
        'BAJFINANCE',
        'BHARTIARTL',
        'ITC',
        'HCLTECH',
        'ASIANPAINT',
        'WIPRO',
        'AXISBANK',
        'MARUTI',
        'LT',
        'ULTRACEMCO',
        'DMART',
        'ADANIGREEN',
        'BAJAJFINSV']
        for stock in stock_list:
            df = pd.read_csv("D:\Mechanical Trading\SinTech-get-nse-data\data\equity\daily\\500\\"+stock+".csv")
            df["200ma"] = df["Close"].rolling(window=200).mean()
            df["price_change"] = df["Close"].pct_change()


            df["Upmove"] = df["price_change"].apply(lambda x: x if x>0 else 0)
            df["Downmove"] = df["price_change"].apply(lambda x: abs(x) if x < 0 else 0)
            df["avg up"] = df["Upmove"].ewm(span=19).mean()
            df["avg down"] = df["Downmove"].ewm(span=19).mean()

            df["RS"] = df["avg up"]/df["avg down"]
            df["RSI"] = df["RS"].apply(lambda x: 100 - (100/(x+1)))

            df.loc[(df["Close"] > df["200ma"]) & (df["RSI"] < 30), 'Buy'] = 'Yes'
            df.loc[(df["Close"] < df["200ma"]) | (df["RSI"] > 30), 'Buy'] = 'No'

            df = df.dropna()
            PnL = []
            for i in range(len(df) - 12):
                if "Yes" in df['Buy'].iloc[i]:
                    for j in range(1, 11):
                        if df['RSI'].iloc[i + j] > 40:
                            PnL.append(df['Open'].iloc[i + j + 1] - df['Open'].iloc[i + 1])
                            break
                        elif j == 10:
                            PnL.append(df['Open'].iloc[i + j + 1] - df['Open'].iloc[i + 1])
            print("------" + stock + "------------")
            print(PnL)
            positive_list = [i for i in PnL if i > 0]
            negative_list = [i for i in PnL if i < 0]
            positive = len(positive_list)
            total_trade = len(PnL)
            print("Winning Ratio: "+ str((positive/total_trade)))
            if(len(positive_list)>0):
                print("Average Gain: "+ str(sum(positive_list) / len(positive_list)))
            if(len(negative_list)>0):
                print("Average Loss: " + str(sum(negative_list) / len(negative_list)))
            if (len(positive_list) > 0):
                print("Max Gain: " + str(max(positive_list)))
            if (len(negative_list) > 0):
                print("Max Loss: " + str(min(negative_list)))

    def run_strat_index(self):
        df = pd.read_csv("D:\Mechanical Trading\SinTech-get-nse-data\data\index\\NIFTY.csv")
        # Convert Daily to Weekly
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        df.sort_index(inplace=True)
        # df = df.loc[df.index > '2020-01-01']
        logic = {'Open': 'first',
                 'High': 'max',
                 'Low': 'min',
                 'Close': 'last',
                 'Volume': 'sum'}

        df = df.resample('W').apply(logic)
        df.index -= to_offset("6D")
        print(df.tail(10))

        df["5ema"] = df["Close"].ewm(span=5, adjust= False).mean()

        df.loc[(df["High"] < df["5ema"]) , 'Buy'] = 'Yes'
        df.loc[(df["High"] >= df["5ema"]) , 'Buy'] = 'No'

        print(df.head(200))

        df = df.dropna()
        PnL = []
        RR = 10
        date_l = []
        price_start_dict ={}
        price_end_dict = {}
        i, j, k =(0,)*3

        while i  < len(df):
            break_out_flag = False
            if "Yes" in df['Buy'].iloc[i]:
                print("start i " + str(df.index[i]))
                buy = df['High'].iloc[i]  # 2100
                sl = buy - df['Low'].iloc[i]  # 100
                j = i+1
                while j < len(df):
                    print("start j " + str(df.index[j]))
                    if df['High'].iloc[j] > df['High'].iloc[j-1]:
                        k = j + 1
                        while k < len(df):
                            print("start k " + str(df.index[k]))
                            print(df['Low'].iloc[j])
                            print( buy - sl)
                            if (df['High'].iloc[k] > buy + RR*sl):
                                print("counter")
                                PnL.append(RR*sl)
                                price_start_dict[df.index[j]] = {df['High'].iloc[j-1], sl}
                                price_end_dict[df.index[k]] = df['Close'].iloc[k]
                                j = k
                                i = k
                                break_out_flag = True
                                break
                            elif(df['Low'].iloc[k] < buy - sl):
                                print("SL counter")
                                PnL.append(-sl)
                                price_start_dict[df.index[j]] = {df['High'].iloc[j-1], sl}
                                price_end_dict[df.index[k]] = df['Close'].iloc[k]
                                j = k
                                i = k
                                break
                            k = k + 1
                    else:
                        buy = df['High'].iloc[j]  # 2100
                        sl = buy - df['Low'].iloc[j]  # 100
                    j = j + 1
                    if break_out_flag == True:
                        break
            i = i + 1


        print("------NIFTY------------")
        print(price_start_dict)
        print(price_end_dict)
        print(PnL)
        positive_list = [i for i in PnL if i > 0]
        negative_list = [i for i in PnL if i < 0]
        positive = len(positive_list)
        total_trade = len(PnL)
        print("Winning Ratio: " + str((positive / total_trade)))
        print("Total Points: " + str(sum(PnL)))
        if (len(positive_list) > 0):
            print("Average Gain: " + str(sum(positive_list) / len(positive_list)))
        if (len(negative_list) > 0):
            print("Average Loss: " + str(sum(negative_list) / len(negative_list)))
        if (len(positive_list) > 0):
            print("Max Gain: " + str(max(positive_list)))
        if (len(negative_list) > 0):
            print("Max Loss: " + str(min(negative_list)))

    def run_strat_get_best_rr(self):
        df = pd.read_csv("D:\Mechanical Trading\SinTech-get-nse-data\data\index\\NIFTY.csv")
        # Convert Daily to Weekly
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        df.sort_index(inplace=True)
        # df = df.loc[df.index > '2020-01-01']
        logic = {'Open': 'first',
                 'High': 'max',
                 'Low': 'min',
                 'Close': 'last',
                 'Volume': 'sum'}

        df = df.resample('M').apply(logic)
        # df.index -= to_offset("6D")
        print(df.tail(10))

        df["5ema"] = df["Close"].ewm(span=5, adjust= False).mean()

        df.loc[(df["High"] < df["5ema"]) , 'Buy'] = 'Yes'
        df.loc[(df["High"] >= df["5ema"]) , 'Buy'] = 'No'

        print(df.head(200))

        df = df.dropna()
        best_rr = {}
        price_start_dict ={}
        price_end_dict = {}
        for reward in range(1, 30):
            i, j, k = (0,) * 3
            PnL = list()
            while i  < len(df):
                break_out_flag = False
                if "Yes" in df['Buy'].iloc[i]:
                    # print("start i " + str(df.index[i]))
                    buy = df['High'].iloc[i]  # 2100
                    sl = buy - df['Low'].iloc[i]  # 100
                    j = i+1
                    while j < len(df):
                        # print("start j " + str(df.index[j]))
                        if df['High'].iloc[j] > df['High'].iloc[j-1]:
                            k = j + 1
                            while k < len(df):
                                # print("start k " + str(df.index[k]))
                                # print(df['Low'].iloc[j])
                                # print( buy - sl)
                                if (df['High'].iloc[k] > buy + reward*sl):
                                    # print("counter")
                                    PnL.append(reward*sl)
                                    price_start_dict[df.index[j]] = {df['High'].iloc[j-1], sl}
                                    price_end_dict[df.index[k]] = df['Close'].iloc[k]
                                    j = k
                                    i = k
                                    break_out_flag = True
                                    break
                                elif(df['Low'].iloc[k] < buy - sl):
                                    # print("SL counter")
                                    PnL.append(-sl)
                                    price_start_dict[df.index[j]] = {df['High'].iloc[j-1], sl}
                                    price_end_dict[df.index[k]] = df['Close'].iloc[k]
                                    j = k
                                    i = k
                                    break
                                k = k + 1
                        else:
                            buy = df['High'].iloc[j]  # 2100
                            sl = buy - df['Low'].iloc[j]  # 100
                        j = j + 1
                        if break_out_flag == True:
                            break
                i = i + 1


            # print("------NIFTY------------")
            # print(price_start_dict)
            # print(price_end_dict)
            # print(PnL)
            positive_list = [i for i in PnL if i > 0]
            negative_list = [i for i in PnL if i < 0]
            positive = len(positive_list)
            total_trade = len(PnL)
            print("Winning Ratio: " + str((positive / total_trade)))
            best_rr[reward] = {sum(PnL)}
            # best_rr[reward] = {str(sum(PnL)), total_trade, str((positive / total_trade)),
            #                    max(positive_list), min(negative_list)}
            # print("Total Points: " + str(sum(PnL)))
            # if (len(positive_list) > 0):
            #     print("Average Gain: " + str(sum(positive_list) / len(positive_list)))
            # if (len(negative_list) > 0):
            #     print("Average Loss: " + str(sum(negative_list) / len(negative_list)))
            # if (len(positive_list) > 0):
            #     print("Max Gain: " + str(max(positive_list)))
            # if (len(negative_list) > 0):
            #     print("Max Loss: " + str(min(negative_list)))
        print(best_rr)

if __name__ == "__main__":
    main_obj = PassiveStrat()
    main_obj.run_strat_get_best_rr()
    exit()