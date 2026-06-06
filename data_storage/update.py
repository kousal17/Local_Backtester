'''
I will have to run this code atleast once every week! ELSE:
You will have to go to the data_info.csv file and then update the recent_update date to exactly a week ago(ie, if it thursday, then take last thursday) for 1m files, so that they don't return an error from yfinance.
You will also have to bypass the can_execute function
'''

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import pytz
import os

def get_current_folder_path():
    raw_path = os.path.dirname(os.path.abspath(__file__))
    formatted_path = raw_path.replace("\\", "/")
    return formatted_path

OS_PATH = get_current_folder_path()

DATA_PATH = OS_PATH + '//data//' # change this if you are changing the location
MAIN_PATH = OS_PATH + '//'# and this is for data_info and ticker_list

PERIODS = ['1m', '2m', '5m', '1h', '1d']
#PERIODS = ['1d']
STD_PERIODS = {'1m': 8-1, '2m': 60-1, '5m': 60-1, '1h': 730-1, '1d': "Max"} # we are also doing -1 so that today - timedelta(7) will give us a 8 day's data
# this is for how much data yfinance can give us. NOTE: 1wk and 5d are same

CONV_TABLE = {'2m': '1m', '5m': '1m', '1h': '5m', '1d': '1h'}
# this is for deriving the wanted data while updating NOTE: 1wk and 5d are same

ET = pytz.timezone('US/Eastern')
IST = pytz.timezone('Asia/Kolkata')



def check_exchange(ticker):
    base_ticker = ticker.strip().upper().split('.')[0]
    exchanges_found = []
    
    if not yf.Ticker(f"{base_ticker}.NS").history(period="1d").empty:
        exchanges_found.append('NS')
    if not yf.Ticker(f"{base_ticker}.BO").history(period="1d").empty:
        exchanges_found.append('BO')
    if not exchanges_found:
        raise ValueError(f"'{base_ticker}' is an invalid ticker.")
        
    return exchanges_found



def _get_valid_date(period):
    today = datetime.now(IST).date()
    end = today + timedelta(days=1)  # yfinance end date is exclusive

    if period == '1m':
        start = today - timedelta(days=STD_PERIODS['1m'])
    elif period in ('2m', '5m'):
        start = today - timedelta(days=STD_PERIODS[period])
    elif period == '1h':
        start = today - timedelta(days=STD_PERIODS['1h'])
    elif period == '1d':
        start = '2016-04-01'  # start of financial year, since 2015 algo trading hit mainstream

    return (str(start) if start else None, str(end))
    


def _create_header_file(ticker, exchange, period):
    if period == '1d':
        header = ['date', 'close', 'high', 'low', 'open', 'volume']
        head_df = pd.DataFrame(columns = header)
        head_df.to_csv(f"{DATA_PATH}{ticker}.{exchange}_{period}.csv", mode='w', header=True, index=False)

    else:  
        header = ['date', 'time', 'close', 'high', 'low', 'open', 'volume']
        head_df = pd.DataFrame(columns = header)
        head_df.to_csv(f"{DATA_PATH}{ticker}.{exchange}_{period}.csv", mode='w', header=True, index=False)



def _round_data(df: pd.DataFrame) -> pd.DataFrame:
    target_columns = ['close', 'high', 'low', 'open']
    df[target_columns] = df[target_columns].round(3)
    return df # if you directly return the rounded data, then you will lose the other colums



def _download_formatted_data(ticker, date: list, period, exchange):
            df = yf.download(
                tickers=f"{ticker}.{exchange}",
                start=date[0],
                end=date[1],
                auto_adjust=True,
                interval=period,
                progress=False
            ) # downloads in the standard form

            df.columns = df.columns.droplevel(1) # remove the 2nd line (the ticker line)
            df.columns = [c.lower() for c in df.columns] # converts the headers into lowercase

            if period != '1d':
                df.index = df.index.tz_convert('Asia/Kolkata').tz_localize(None) # converts the time zone
            
            df = df.reset_index() # gets the dates back from passive index to becoming a part of the csv

            if period == '1d': # no formatting needed just send the data
                return _round_data(df)
            else: # here it formats the datetime and then arranges it.
                df['date'] = df['Datetime'].dt.date
                df['time'] = df['Datetime'].dt.time

                df = df.drop(columns=['Datetime'])
                custom_headers = ['date', 'time', 'close', 'high', 'low', 'open', 'volume']
                df = df[custom_headers]
                
                return _round_data(df) 



def _append_data(df, ticker, exchange, period): # adding path so that we can use it for _add_data_info
    df.to_csv(f"{DATA_PATH}{ticker}.{exchange}_{period}.csv", mode='a', header=False, index=False) # appends the formatted and downloaded data to the created csv



def _add_data_info(ticker, exchange, period, date):
    columns = ['ticker', 'exchange', 'period', 'start_date', 'recent_update']
    data = [[str(ticker), str(exchange), str(period), str(date[0]), str(date[1])]]

    df_new = pd.DataFrame(data, columns=columns)
    df_new.to_csv(f"{MAIN_PATH}data_info.csv", mode='a', header=False, index=False)



def add_new_ticker(ticker):
    exchanges = check_exchange(ticker) # it will return a list of exchanges.
    print(f"Downloading {ticker} data")
    for exchange in exchanges:
        print(f"    -> On {exchange}")
        for period in PERIODS:
            print(f'        -> For {period} data')
            date = _get_valid_date(period) # it will return start date, end date.

            _create_header_file(ticker, exchange, period) # creates the csv file
            
            df = _download_formatted_data(ticker, date, period, exchange) # store the data into df

            _append_data(df, ticker, exchange, period) # appends the data
            
            _add_data_info(ticker, exchange, period, date) # saves the metadata of the data into data_info.csv of the
            print(f'        -> Done: From [{date[0]}, {date[1]})')



def _update_data_info(ticker, exchange, period, end):
    filename = f"{MAIN_PATH}data_info.csv"

    df = pd.read_csv(filename)

    target_row = (df['ticker'] == ticker) & (df['exchange'] == exchange) & (df['period'] == period)
    df.loc[target_row, 'recent_update'] = str(end)

    df.to_csv(filename, index=False)


def update(ticker, exchange, period, start_date):
    today = datetime.now(IST).date()
    end = today + timedelta(days=1)

    start_date_object = datetime.strptime(start_date, "%Y-%m-%d").date()
    days_passed  = (today - start_date_object).days

    if days_passed > 7:
        start_date = today - timedelta(days = 7)

    date = [str(start_date), str(end)]

    df = _download_formatted_data(ticker, date, period, exchange)
    print("    -> [Downloaded]")

    _append_data(df, ticker, exchange, period)
    print("    -> [Appended]")

    _update_data_info(ticker, exchange, period, end)
    print("    -> [Log Updated]")

    # after appending the 1m data, it should now, derive all the other data using the CONV TABLE
    # that way we have 2m and 5m from 1m data and 1h data from 5m and 1d data from 1h



def create_new():
    new_tickers = pd.read_csv(f"{MAIN_PATH}ticker_list.csv")

    if new_tickers.empty:
        print("No New Tickers found...")
        return

    saved_tickers = pd.read_csv(f"{MAIN_PATH}saved_tickers.csv")

    existing_tickers = set(saved_tickers['ticker'])

    df_new_tickers = new_tickers[~new_tickers['ticker'].isin(existing_tickers)]

    for row in new_tickers.itertuples(index=False):
        if row.ticker in existing_tickers:
            print(f"{row.ticker} is already being tracked!")
            continue
        add_new_ticker(str(row.ticker))

    df_new_tickers.to_csv(f"{MAIN_PATH}saved_tickers.csv", mode='a', header=False, index=False)
    print(f"Successfully Transferred {len(df_new_tickers)} new tickers to saved list")

    pd.DataFrame(columns=['ticker']).to_csv(f'{MAIN_PATH}ticker_list.csv', mode='w', header=True, index=False)
    print("Ticker list is reset")
        


def update_loop():
    data_info = pd.read_csv(f"{MAIN_PATH}data_info.csv")

    for row in data_info.itertuples(index=False):
        update(str(row.ticker), str(row.exchange), str(row.period), str(row.recent_update))
        print(f"Updating {str(row.ticker)}.{str(row.exchange)} for {str(row.period)} from {str(row.recent_update)}:")
        print("    -> [Initiated]")



def can_execute_program():
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    current_hour = now.hour

    if current_hour < 16:
        print(f"It is only {now.strftime('%I:%M %p')}. Wait until 4:00 PM.")
        return False

    df_log = pd.read_csv(f'{MAIN_PATH}run_log.csv')

    if not df_log.empty:
        last_run_str = df_log['date'].iloc[-1]

        last_run_date = pd.to_datetime(last_run_str)
        current_date = pd.to_datetime(today_str)

        days_passed = (current_date - last_run_date).days

        if last_run_str == today_str:
            print(f"The script has already been executed today: ({today_str}).")
            return False
        
        if days_passed > 7:
            print("WARNING: It has been more than a week, there will be missing data if you proceed.")
            
            decision = input("Please write 'STOP' to stop program, but if you want to continue with missing data write 'CONTINUE'")

            if decision == 'CONTINUE':
                return True
            
            return False

    return True



def _log_successful_run():
    now = datetime.now()
    
    df_new_entry = pd.DataFrame([[now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S")]], 
                                columns=['date', 'timestamp'])
    
    df_new_entry.to_csv(f'{MAIN_PATH}run_log.csv', mode='a', header=False, index=False)
    print("Log file updated successfully.")



if __name__ == "__main__":
    create_new()

    if can_execute_program():
        print("Updating Logic is clear to run.")
        
        update_loop()

        _log_successful_run()
