from nsepy import *
from dateutil.relativedelta import *
import numpy as np
import pandas as pd
import time
import random
from nsetools import *
import matplotlib.pyplot as plt
from datetime import date

class Main():
    def __init__(self):
        pass


    def run_hist_daily(self):
        from_date = date(2010,1,1)
        to_date = date(2021,10,1)
        # index_list = ["NIFTY200 MOMENTUM 30","NIFTY200 QUALTY30", "NIFTY100 LOWVOL30", "NIFTY ALPHA 50",
        #               "NIFTY50 VALUE 20"]
        index_list = ["NIFTY"]
        for ls in index_list:
            data = get_history(symbol=ls, start=from_date, end=to_date, index=True)
            print(data.to_string())
            data.to_csv("D:\Mechanical Trading\SinTech-get-nse-data\data\index\\"+ls+".csv")
        # data = get_history(symbol=index_list[1], start=from_date, end=to_date, index=True)
        # print(data.to_string())
        # data.to_csv("D:\Mechanical Trading\SinTech-get-nse-data\data\index\\"+index_list[1]+".csv")

    def run_hist_daily_option_index(self):

        month_list = np.arange(1, 9, step=1)
        print(month_list)
        yr_list = np.arange(2015, 2021, step=1)
        print(yr_list)

        for yr in yr_list:
            # loop through all the months and years
            counter = 0
            banknifty_data = pd.DataFrame()  # to use in the loop
            option_data = pd.DataFrame()
            print('Year: ', yr)
            for mnth in month_list:
                current_dt = date(yr, mnth, 1)
                start_dt = current_dt + relativedelta(months=-2)
                end_dt = max(get_expiry_date(year=yr, month=mnth))

                # print('current: ', current_dt)
                # print('start: ', start_dt)
                # print('end: ', end_dt)

                # get nifty futures data
                banknifty_fut = get_history(symbol='BANKNIFTY',
                                        start=start_dt, end=end_dt,
                                        index=True,
                                        expiry_date=end_dt)
                banknifty_data = banknifty_data.append(banknifty_fut)

                # calculate high and low values for each month; round off to get strike prices
                high = banknifty_fut['Close'].max()
                high = int(round(high / 100) * 100) + 2000  # ; print('High:', high)

                low = banknifty_fut['Close'].min()
                low = int(round(low / 100) * 100) - 2000  # ; print('Low :', low)

                for strike in range(low, high, 100):  # start, stop, step
                    """
                    get daily closing banknifty index option prices for 3 months 
                    over the entire range 
                    """
                    print("Strike: "+ str(strike))
                    time.sleep(random.randint(1,3)) # pause for random interval so as to not overwhelm the site
                    banknifty_opt = get_history(symbol='BANKNIFTY',
                                            start=start_dt, end=end_dt,
                                            index=True, option_type='PE',
                                            strike_price=strike,
                                            expiry_date=end_dt)

                    option_data = option_data.append(banknifty_opt)

                    # time.sleep(random.randint(20,50)) # pause for random interval so as to not overwhelm the site
                    banknifty_opt = get_history(symbol='BANKNIFTY',
                                            start=start_dt, end=end_dt,
                                            index=True, option_type='CE',
                                            strike_price=strike,
                                            expiry_date=end_dt)

                    option_data = option_data.append(banknifty_opt)

                counter += 1
                print('Months: ', counter)
                # print(month)
            banknifty_data.to_csv("D:\Mechanical Trading\SinTech-get-nse-data\data\\fno\\options\\index\\banknifty\\bnf"+str(yr)+"data.csv")
            option_data.to_csv("D:\Mechanical Trading\SinTech-get-nse-data\data\\fno\\options\\index\\banknifty\\option"+str(yr)+"data.csv")

    def run_hist_daily_option_stock(self):

        month_list = np.arange(1, 13, step=1)
        print(month_list)
        yr_list = np.arange(2019, 2021, step=1)
        print(yr_list)
        bank = "KOTAKBANK"
        for yr in yr_list:
            # loop through all the months and years
            counter = 0
            banknifty_data = pd.DataFrame()  # to use in the loop
            option_data = pd.DataFrame()
            print('Year: ', yr)
            for mnth in month_list:
                current_dt = date(yr, mnth, 1)
                start_dt = current_dt + relativedelta(months=-2)
                end_dt = max(get_expiry_date(year=yr, month=mnth))

                # print('current: ', current_dt)
                # print('start: ', start_dt)
                # print('end: ', end_dt)

                # get nifty futures data
                banknifty_fut = get_history(symbol=bank,
                                        start=start_dt, end=end_dt,
                                        futures=True,
                                        # index=True,
                                        expiry_date=end_dt)
                banknifty_data = banknifty_data.append(banknifty_fut)

                # calculate high and low values for each month; round off to get strike prices
                high = banknifty_fut['Close'].max()
                high = int(round(high / 100) * 100) + 100  # ; print('High:', high)

                low = banknifty_fut['Close'].min()
                low = int(round(low / 100) * 100) - 100  # ; print('Low :', low)

                for strike in range(low, high, 20):  # start, stop, step
                    """
                    get daily closing banknifty index option prices for 3 months 
                    over the entire range 
                    """
                    print("Strike: "+ str(strike))
                    time.sleep(random.randint(1,3)) # pause for random interval so as to not overwhelm the site
                    banknifty_opt = get_history(symbol=bank,
                                            start=start_dt, end=end_dt,
                                            # index=True,
                                            option_type='PE',
                                            strike_price=strike,
                                            expiry_date=end_dt)

                    option_data = option_data.append(banknifty_opt)

                    # time.sleep(random.randint(20,50)) # pause for random interval so as to not overwhelm the site
                    banknifty_opt = get_history(symbol=bank,
                                            start=start_dt, end=end_dt,
                                            # index=True,
                                            option_type='CE',
                                            strike_price=strike,
                                            expiry_date=end_dt)

                    option_data = option_data.append(banknifty_opt)

                counter += 1
                print('Months: ', counter)
                # print(month)
            banknifty_data.to_csv("D:\Mechanical Trading\SinTech-get-nse-data\data\\fno\\options\\stock\\KOTAKBANK\\kotakbank"+str(yr)+"data.csv")
            option_data.to_csv("D:\Mechanical Trading\SinTech-get-nse-data\data\\fno\\options\\stock\\KOTAKBANK\\option"+str(yr)+"data.csv")



if __name__ == "__main__":
    main_obj = Main()
    main_obj.run_hist_daily_option_stock()
    exit()