import pandas as pd
import os
import pandas_datareader.data as web
import datetime
import fix_yahoo_finance as yf
'''
deteled stock:
NCZ-PA: fund
BKCH: established in 2019-02-08
IBO: only have data in 2018-04-06
BFL: seems not a stocks any more
"BBRX","Braeburn Pharmaceuticals, Inc.","n/a","n/a","n/a","n/a","n/a","https://www.nasdaq.com/symbol/bbrx",
"ATEST","NASDAQ TEST STOCK","25","n/a","n/a","n/a","n/a","https://www.nasdaq.com/symbol/atest",
"ATEST.A","NASDAQ TEST STOCK","n/a","n/a","n/a","n/a","n/a","https://www.nasdaq.com/symbol/atest.a",
"ATEST.B","NASDAQ TEST STOCK","n/a","n/a","n/a","n/a","n/a","https://www.nasdaq.com/symbol/atest.b",
"ATEST.C","NASDAQ TEST STOCK","n/a","n/a","n/a","n/a","n/a","https://www.nasdaq.com/symbol/atest.c",
"RILYG","B. Riley Financial, Inc.","24.56","n/a","n/a","Miscellaneous","Business Services","https://www.nasdaq.com/symbol/rilyg",
"RILYH","B. Riley Financial, Inc.","25.84","n/a","n/a","Miscellaneous","Business Services","https://www.nasdaq.com/symbol/rilyh",
"RILYI","B. Riley Financial, Inc.","25.47","n/a","n/a","Miscellaneous","Business Services","https://www.nasdaq.com/symbol/rilyi",
"RILYL","B. Riley Financial, Inc.","25.468","n/a","n/a","Miscellaneous","Business Services","https://www.nasdaq.com/symbol/rilyl",
"RILYZ","B. Riley Financial, Inc.","24.81","n/a","n/a","Miscellaneous","Business Services","https://www.nasdaq.com/symbol/rilyz",
"BH.A","Biglari Holdings Inc.","n/a","n/a","n/a","n/a","n/a","https://www.nasdaq.com/symbol/bh.a",
"CPTAG","Capitala Finance Corp.","25","n/a","n/a","n/a","n/a","https://www.nasdaq.com/symbol/cptag",
"CPTAL","Capitala Finance Corp.","25.2475","n/a","n/a","n/a","n/a","https://www.nasdaq.com/symbol/cptal",
"GIG~","GigCapital, Inc.","0.24","n/a","n/a","n/a","n/a","https://www.nasdaq.com/symbol/gig~",
"JPM-PB.CL","J P Morgan Chase & Co","n/a","n/a","n/a","n/a","n/a","https://www.nasdaq.com/symbol/jpm-Pb.cl",
"PRN","Invesco DWA Industrials Momentum ETF","59.48","$95.17M","n/a","n/a","n/a","https://www.nasdaq.com/symbol/prn",

'''


def get_data(stocks_data_frame, start=datetime.datetime(2009, 1, 1), end=datetime.datetime(2018, 12, 31)):
    total = len(stocks_data_frame['Symbol'])
    finished = 1
    for code in stocks_data_frame['Symbol']:
        temp = code
        code = code.replace('.', '-')
        if os.path.exists(code + '.csv'):
            finished += 1
            print('\r%d/%d  We are downloading %s' % (finished, total, code), end='', flush=True)
            continue    # this line is try to continue the work finished
        print('\r%d/%d  We are downloading %s' % (finished, total, code), end='', flush=True)
        try:
            data = web.get_data_yahoo(code, start, end)
        except:
            pass
            error_log = open('error_log.txt', 'a+')  # create an error log
            error_log.write(temp+'\n')
            error_log.close()
            finished += 1
            continue
        data.reset_index(inplace=True)
        data.to_csv(code+'.csv', index=False)
        finished += 1


def get_all_data(market_name):
    os.chdir(root_dir)
    df = pd.read_csv(market_name+'.csv')
    os.chdir('./'+market_name)
    print('Now we are downloading %s' % market_name)
    df = ensure_date_is_valid(df, 2019)  # the time range is end in 2018-12-31
    df = del_warrants_and_units(df)    # delete warrants stock
    get_data(df)


def ensure_date_is_valid(stock_data_frame, ipoyear):
    '''
    :param stock_data_frame: the dataframe
    :param ipoyear: will delete the stock whose first IPOyear is bigger than the ipoyear variable.
    This function is to ensure the range of time u required is valid because the first IPO year of a stock could be
    after ur time range.
    '''
    result = stock_data_frame
    this_year = int(str(datetime.date.today())[0:4])
    for year in range(ipoyear, this_year+1):
        result = result.loc[(result['IPOyear'] != year), :]
    return result


def del_warrants_and_units(stock_data_frame):
    '''
    :param stock_data_frame:
    :return: this function is to delete the warrant stock in the stock_data_frame
    '''
    delete_list = []
    for code in stock_data_frame['Symbol']:
        if '.WS' in code or '.U' in code:
            delete_list.append(code)
            continue  # if the stock name contain .WS that means its a warrants.
        if len(code) >= 5:
            if code[4] == 'W' or code[4] == 'U':
                delete_list.append(code)
                continue    # NYSE and NASDAQ have different identifier format
    if 'HE-PU' in delete_list:
        delete_list.remove('HE-PU')
    # this is the only special case which satisfies all the condition above but not a warrants or units
    return stock_data_frame.loc[~(stock_data_frame['Symbol'].isin(delete_list)), :]


# yf.pdr_override()   # core process of yf, giving internet support to visit yahoo finance

# market_list = {'NASDAQ', 'NYSE', 'AMEX'}
market_list = {'NASDAQ'}
# save root dir of the project
root_dir = os.getcwd()
if __name__ == '__main__':
    # mkdir for data
    for name in market_list:
        flag = os.path.exists('./'+name)
        if flag:
            print("%s path is existing!\n" % name)
        else:
            os.mkdir('./' + name)

    # main
    for x in market_list:
        get_all_data(x)
    os.chdir(root_dir)
    if os.path.exists('./NASDAQ'):
        os.chdir('./NASDAQ')
        data = web.get_data_yahoo('PRN', datetime.datetime(2009, 1, 1), datetime.datetime(2018, 12, 31))
        data.to_csv('PRN~.csv', index=False)  # PRN is a reserved name in win os





