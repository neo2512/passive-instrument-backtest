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
        alpha_df = pd.read_csv("D:\Mechanical Trading\SinTech-get-nse-data\data\index\\NIFTY ALPHA 50.csv")
        value_df = pd.read_csv("D:\Mechanical Trading\SinTech-get-nse-data\data\index\\NIFTY50 VALUE 20.csv")
        lowvol_df = pd.read_csv("D:\Mechanical Trading\SinTech-get-nse-data\data\index\\NIFTY100 LOWVOL30.csv")
        momentum_df = pd.read_csv("D:\Mechanical Trading\SinTech-get-nse-data\data\index\\NIFTY200 MOMENTUM 30.csv")
        quality_df = pd.read_csv("D:\Mechanical Trading\SinTech-get-nse-data\data\index\\NIFTY200 QUALTY30.csv")
        nifty_df = pd.read_csv("D:\Mechanical Trading\SinTech-get-nse-data\data\index\\NIFTY.csv")

        alpha_df["nClose"] = alpha_df["Close"]*0.5 + lowvol_df["Close"]*0.5
        alpha_df["Date"] = pd.to_datetime(alpha_df["Date"])
        alpha_df["Year"] = alpha_df["Date"].dt.year
        # print(alpha_df.to_string())
        # print(len(alpha_df))
        # p = alpha_df["nClose"][0]
        # print(p)
        # a = alpha_df["nClose"][len(alpha_df)-1]
        # t = alpha_df["Year"][len(alpha_df)-1] - alpha_df["Year"][0]
        #
        # print(alpha_df.head())
        # print(cagr_calc(p, a, t))
        alpha_df["alClose"] = alpha_df["nClose"].pct_change().dropna()
        alpha_df["qualClose"] = quality_df["Close"].pct_change().dropna()
        alpha_df["momClose"] = momentum_df["Close"].pct_change().dropna()
        alpha_df["valClose"] = value_df["Close"].pct_change().dropna()
        alpha_df["nifClose"] = nifty_df["Close"].pct_change().dropna()

        # print(df.dtypes)
        # print(df.to_string())
        #weightage of different indexes
        alpha_w = 0.3
        value_w = 0.1
        momentum_w = 0.5
        quality_w = 0.1
        alpha_df["fClose"] = alpha_df["alClose"]*alpha_w + alpha_df["momClose"]*momentum_w +\
                              alpha_df["qualClose"]*quality_w + alpha_df["valClose"]*value_w

        pass_df = alpha_df[["Date","valClose", "qualClose", "alClose", "momClose", "nifClose","fClose"]]
        pass_df = pass_df.set_index("Date")
        print(pass_df.head())
        # ret_index = (pass_df + 1).cumprod()
        # ret_index[0] = 1
        # print(ret_index)
        # cagr_df = cagr(ret_index["nifClose"],11*365)

        N = 255  # 255 trading days in a year
        rf = 0.01  # 1% risk free rate
        sharpes = pass_df.apply(sharpe_ratio, args=(N, rf,), axis=0)
        print(sharpes)
        sharpes.plot.bar()
        plt.show()


        cagr_ret = CAGR((pass_df+1).cumprod(), 11)
        print("--------------CAGR-----------------")
        print(cagr_ret.tail(1))
        (pass_df + 1).cumprod().plot()
        plt.legend(["Nifty Value Index", "NIFTY Quality Index", "NIFTY ALpha Low Volatility Index",
                    "NIfty Momentum Index", "NIFTY 50", "SinTech Passive Strat"])
        plt.show()

        print((pass_df + 1).cumprod()[-1:])
        max_drawdowns = pass_df.apply(max_drawdown, axis=0)
        print(max_drawdowns)
        plt.legend(["Nifty Value Index", "NIFTY Quality Index", "NIFTY ALpha Low Volatility Index",
                    "NIfty Momentum Index", "NIFTY 50", "SinTech Passive Strat"])
        max_drawdowns.plot.bar()

        plt.show()

        calmars = pass_df.mean() * 255 / abs(max_drawdowns)
        calmars.plot.bar()
        plt.ylabel('Calmar ratio')
        plt.show()

    def run_strat_monthly_tf(self):
        alpha_df = pd.read_csv("D:\Mechanical Trading\SinTech-get-nse-data\data\index\\NIFTY ALPHA 50.csv")
        value_df = pd.read_csv("D:\Mechanical Trading\SinTech-get-nse-data\data\index\\NIFTY50 VALUE 20.csv")
        lowvol_df = pd.read_csv("D:\Mechanical Trading\SinTech-get-nse-data\data\index\\NIFTY100 LOWVOL30.csv")
        momentum_df = pd.read_csv("D:\Mechanical Trading\SinTech-get-nse-data\data\index\\NIFTY200 MOMENTUM 30.csv")
        quality_df = pd.read_csv("D:\Mechanical Trading\SinTech-get-nse-data\data\index\\NIFTY200 QUALTY30.csv")
        nifty_eq_wt_df = pd.read_csv("D:\Mechanical Trading\SinTech-get-nse-data\data\index\\NIFTY50 EQL WGT.csv")
        nifty_df = pd.read_csv("D:\Mechanical Trading\SinTech-get-nse-data\data\index\\NIFTY.csv")

        alpha_df["nClose"] = alpha_df["Close"]*0.5 + lowvol_df["Close"]*0.5

        value_df["Date"] = pd.to_datetime(value_df["Date"])
        value_df["Year"] = value_df["Date"].dt.year
        value_df["Month"] = value_df["Date"].dt.month
        value_df = value_df.groupby(["Year", "Month"]).tail(1)

        momentum_df["Date"] = pd.to_datetime(momentum_df["Date"])
        momentum_df["Year"] = momentum_df["Date"].dt.year
        momentum_df["Month"] = momentum_df["Date"].dt.month
        momentum_df = momentum_df.groupby(["Year", "Month"]).tail(1)

        quality_df["Date"] = pd.to_datetime(quality_df["Date"])
        quality_df["Year"] = quality_df["Date"].dt.year
        quality_df["Month"] = quality_df["Date"].dt.month
        quality_df = quality_df.groupby(["Year", "Month"]).tail(1)

        alpha_df["Date"] = pd.to_datetime(alpha_df["Date"])
        alpha_df["Year"] = alpha_df["Date"].dt.year
        alpha_df["Month"] = alpha_df["Date"].dt.month
        alpha_df = alpha_df.groupby(["Year", "Month"]).tail(1)

        nifty_df["Date"] = pd.to_datetime(nifty_df["Date"])
        nifty_df["Year"] = nifty_df["Date"].dt.year
        nifty_df["Month"] = nifty_df["Date"].dt.month
        nifty_df = nifty_df.groupby(["Year", "Month"]).tail(1)


        nifty_eq_wt_df["Date"] = pd.to_datetime(nifty_eq_wt_df["Date"])
        nifty_eq_wt_df["Year"] = nifty_eq_wt_df["Date"].dt.year
        nifty_eq_wt_df["Month"] = nifty_eq_wt_df["Date"].dt.month
        nifty_eq_wt_df = nifty_eq_wt_df.groupby(["Year", "Month"]).tail(1)
        # print(alpha_df.to_string())
        # print(len(alpha_df))
        # p = alpha_df["nClose"][0]
        # print(p)
        # a = alpha_df["nClose"][len(alpha_df)-1]
        # t = alpha_df["Year"][len(alpha_df)-1] - alpha_df["Year"][0]
        #
        # print(alpha_df.head())
        # print(cagr_calc(p, a, t))
        alpha_df["alClose"] = alpha_df["nClose"].pct_change().dropna()
        alpha_df["qualClose"] = quality_df["Close"].pct_change().dropna()
        alpha_df["momClose"] = momentum_df["Close"].pct_change().dropna()
        alpha_df["valClose"] = value_df["Close"].pct_change().dropna()
        alpha_df["nifClose"] = nifty_df["Close"].pct_change().dropna()
        alpha_df["nifEqWtClose"] = nifty_eq_wt_df["Close"].pct_change().dropna()

        # print(df.dtypes)
        # print(df.to_string())
        #weightage of different indexes
        alpha_w = 0.3
        value_w = 0.1
        momentum_w = 0.5
        quality_w = 0.1
        alpha_df["fClose"] = alpha_df["alClose"]*alpha_w + alpha_df["momClose"]*momentum_w +\
                              alpha_df["qualClose"]*quality_w + alpha_df["valClose"]*value_w

        pass_df = alpha_df[["Date","valClose", "qualClose", "alClose", "momClose", "nifClose", "nifEqWtClose", "fClose"]]
        pass_df = pass_df.set_index("Date")
        print(pass_df.head())
        # ret_index = (pass_df + 1).cumprod()
        # ret_index[0] = 1
        # print(ret_index)
        # cagr_df = cagr(ret_index["nifClose"],11*365)

        N = 255  # 255 trading days in a year
        rf = 0.01  # 1% risk free rate
        sharpes = pass_df.apply(sharpe_ratio, args=(N, rf,), axis=0)
        print(sharpes)
        sharpes.plot.bar()
        plt.show()


        cagr_ret = CAGR((pass_df+1).cumprod(), 11)
        print("--------------CAGR-----------------")
        print(cagr_ret.tail(1))
        (pass_df + 1).cumprod().plot()
        plt.legend(["Nifty Value Index", "NIFTY Quality Index", "NIFTY ALpha Low Volatility Index",
                    "NIfty Momentum Index", "NIFTY 50", "NIFTY50 EQ WT", "SinTech Passive Strat"])
        plt.show()

        print((pass_df + 1).cumprod()[-1:])
        max_drawdowns = pass_df.apply(max_drawdown, axis=0)
        print(max_drawdowns)
        plt.legend(["Nifty Value Index", "NIFTY Quality Index", "NIFTY ALpha Low Volatility Index",
                    "NIfty Momentum Index", "NIFTY 50", "NIFTY50 EQ WT", "SinTech Passive Strat"])
        max_drawdowns.plot.bar()

        plt.show()

        calmars = pass_df.mean() * 255 / abs(max_drawdowns)
        calmars.plot.bar()
        plt.ylabel('Calmar ratio')
        plt.show()

if __name__ == "__main__":
    main_obj = PassiveStrat()
    main_obj.run_strat_monthly_tf()
    exit()