from nsepy import *
from dateutil.relativedelta import *
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

        # df["20High"] = df["High"].rolling(window=20).max()
        # df["10Low"] = df["Low"].rolling(window=10).min()
        #
        # high_low = df['High'] - df['Low']
        # high_close = np.abs(df['High'] - df['Close'].shift())
        # low_close = np.abs(df['Low'] - df['Close'].shift())
        #
        # ranges = pd.concat([high_low, high_close, low_close], axis=1)
        # true_range = np.max(ranges, axis=1)
        #
        # atr = true_range.rolling(20).sum() / 20
        #
        # df["atr"] = atr
        # # df = df.set_index("Date")
        #
        # df["price_change"] = df["Close"].pct_change()
        # df = df.dropna()
        #
        # df.loc[(df["High"] == df["20High"]), 'Buy'] = 'Yes'
        # df.loc[(df["High"] != df["20High"]), 'Buy'] = 'No'





        # plt.plot(df["Close"])
        # plt.plot(df["20High"])
        # plt.show()
        # df.to_csv("D:\Mechanical Trading\passive-instrument-backtest\\test.csv")
        # print(df.head(100).to_string())

    def run_strat_index(self):
        df = pd.read_csv("D:\Mechanical Trading\SinTech-get-nse-data\data\index\\NIFTY.csv")
        df["200ma"] = df["Close"].rolling(window=200).mean()
        df["price_change"] = df["Close"].pct_change()

        df["Upmove"] = df["price_change"].apply(lambda x: x if x > 0 else 0)
        df["Downmove"] = df["price_change"].apply(lambda x: abs(x) if x < 0 else 0)
        df["avg up"] = df["Upmove"].ewm(span=19).mean()
        df["avg down"] = df["Downmove"].ewm(span=19).mean()

        df["RS"] = df["avg up"] / df["avg down"]
        df["RSI"] = df["RS"].apply(lambda x: 100 - (100 / (x + 1)))

        df.loc[(df["Close"] > df["200ma"]) & (df["RSI"] < 30), 'Buy'] = 'Yes'
        df.loc[(df["Close"] < df["200ma"]) | (df["RSI"] > 30), 'Buy'] = 'No'

        df = df.dropna()
        PnL = []
        date_l = []
        price_start_dict ={}
        price_end_dict = {}
        for i in range(len(df) - 12):
            if "Yes" in df['Buy'].iloc[i]:
                for j in range(1, 11):
                    if df['RSI'].iloc[i + j] > 40:
                        PnL.append(df['Open'].iloc[i + j + 1] - df['Open'].iloc[i + 1])
                        price_start_dict[df['Date'].iloc[i + 1]] = df['Open'].iloc[i + 1]
                        price_end_dict[df['Date'].iloc[i + j + 1]] = df['Open'].iloc[i + j + 1]
                        break
                    elif j == 10:
                        PnL.append(df['Open'].iloc[i + j + 1] - df['Open'].iloc[i + 1])
                        price_start_dict[df['Date'].iloc[i + 1]] = df['Open'].iloc[i + 1]
                        price_end_dict[df['Date'].iloc[i + j + 1]] = df['Open'].iloc[i + j + 1]
        print("------NIFTY------------")
        print(PnL)
        print(price_start_dict)
        print(price_end_dict)
        positive_list = [i for i in PnL if i > 0]
        negative_list = [i for i in PnL if i < 0]
        positive = len(positive_list)
        total_trade = len(PnL)
        print("Winning Ratio: " + str((positive / total_trade)))
        if (len(positive_list) > 0):
            print("Average Gain: " + str(sum(positive_list) / len(positive_list)))
        if (len(negative_list) > 0):
            print("Average Loss: " + str(sum(negative_list) / len(negative_list)))
        if (len(positive_list) > 0):
            print("Max Gain: " + str(max(positive_list)))
        if (len(negative_list) > 0):
            print("Max Loss: " + str(min(negative_list)))



if __name__ == "__main__":
    main_obj = PassiveStrat()
    main_obj.run_strat()
    exit()