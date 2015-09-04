# This is my first python study case!

__author__ = 'zhengyangqiao'

import pandas as pd
import os
import time
from datetime import datetime

from time import mktime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
style.use("dark_background")

import re

# Define path name for data location
path = "/Users/zhengyangqiao/Desktop/CS390/PythonSelf/intraQuarter"

# Define a function walk through debt and equity ratio
def Key_Stats(gather ="Total Debt/Equity (mrq)"):
    # _KeyStats path location
    statspath = path+'/_KeyStats'
    # Store Keystats into array stock_list
    stock_list = [x[0] for x in os.walk(statspath)]
    # Use Panda Data Frame
    df = pd.DataFrame(columns = ['Date',
                                 'Unix',
                                 'Ticker',
                                 'DE Ratio',
                                 'Price',
                                 'stock_p_change',
                                 'SP500',
                                 'sp500_p_change',
                                 'Difference',
                                 'Status'])

    # Load csv into data frame One step so simple
    sp500_df = pd.DataFrame.from_csv("YAHOO-INDEX_GSPC.csv")

    ticker_list = []

    # exclude the first file
    for each_dir in stock_list[1:25]:
        #
        each_file = os.listdir(each_dir)
        # Use split to tackle the last element of directory - ticker, -1 catches the
        # last element
        ticker = each_dir.split("/")[-1]
        ticker_list.append(ticker)

        starting_stock_value = False
        starting_sp500_value = False

        if len(each_file) > 0:
            for file in each_file:
                # datetime.strptime to convert filename to a time string
                date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')
                # timetuple will return a time tuple with year month day; mktime
                # will return a float number reflecting with the time
                unix_time = time.mktime(date_stamp.timetuple())
                # Construct full_file_path name
                full_file_path = each_dir + '/' + file
                source = open(full_file_path, 'r').read()

                try:
				# Split the float value from HTML
                    try:
                        value = float(source.split(gather + ':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0])
                    except Exception as e:
                        value = float(source.split(gather + ':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0])
                        # print(str(e))
                        # time.sleep(15)

                    try:
                        sp500_date = datetime.fromtimestamp(unix_time).strftime("%Y-%m-%d")
                        row = sp500_df[(sp500_df.index == sp500_date)]
                        sp500_value = float(row["Adjusted Close"])
                    except:
                        # Get rid of weekends
                        sp500_date = datetime.fromtimestamp(unix_time - 259200).strftime("%Y-%m-%d")
                        row = sp500_df[(sp500_df.index == sp500_date)]
                        sp500_value = float(row["Adjusted Close"])
                    # Get the stock price
                    try:
                        stock_price = float(source.split('</small><big><b>')[1].split('</b></big>')[0])
                    except Exception, e:
                        try:
                            stock_price = (source.split('</small><big><b>')[1].split('</b></big>')[0])
                            #<span id="yfs_l10_aig">31.80</span>'
                            stock_price = re.search(r'(\d{1,8}\.\d{1,8})',stock_price)
                            stock_price = float(stock_price.group(1))

                            print(stock_price)
                            # time.sleep(15)
                        except Exception as e:
                            try:
                                stock_price = (source.split('<span class="time_rtq_ticker">')[1].split('</span>')[0])

                                stock_price = re.search(r'(\d{1,8}\.\d{1,8})',stock_price)
                                stock_price = float(stock_price.group(1))
                            except Exception as e:
                                print(str(e))

                            # print('Latest:',stock_price)
                            # print('stock_price', str(e), ticker, file)
                            # time.sleep(15)

                        #print(str(e), ticker, file)
                    # if not is a condition which is used to check whether the list
                    # is empty or not
                    if not starting_stock_value:
                        starting_stock_value = stock_price
                    if not starting_sp500_value:
                        starting_sp500_value = sp500_value

                    stock_p_change = ((stock_price - starting_stock_value) / starting_stock_value) * 100
                    sp500_p_change = ((sp500_value - starting_sp500_value) / starting_sp500_value) * 100

                    difference = stock_p_change - sp500_p_change

                    if difference > 0:
                        status = 'outperform'
                    else:
                        status = "uderperform"

                    # pandas append more data into structure
                    df = df.append({'Date':date_stamp,
                                    'Unix':unix_time,
                                    'Ticker':ticker,
                                    'DE Ratio':value,
                                    'Price':stock_price,
                                    'stock_p_change':stock_p_change,
                                    'SP500':sp500_value,
                                    'sp500_p_change':sp500_p_change,
                                    'Difference':stock_p_change - sp500_p_change,
                                    'Status':status},
                                   ignore_index = True)

                except Exception as e:
                    pass

    for each_ticker in ticker_list:
        try:
            print("It works here")
            plot_df = df[(df['Ticker'] == each_ticker)]
            plot_df = plot_df.set_index(['Date'])

            if plot_df['Status'][-1] == "underperform":
                color = 'r'
            else:
                color = 'g'

            plot_df['Difference'].plot(label = each_ticker, color = color)
            plt.legend()

        except:
            pass


    plt.show()

    save = gather.replace(' ','').replace(')','').replace('(','').replace('/','') + ('.csv')
    print(save)
    df.to_csv(save)

Key_Stats()

