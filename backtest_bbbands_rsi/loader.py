import pandas as pd
import yfinance as yf

START_DATE = '2023-04-01'
END_DATE = '2026-05-31'

def _round_data(df: pd.DataFrame) -> pd.DataFrame:
    target_columns = ['close', 'high', 'low', 'open']
    df[target_columns] = df[target_columns].round(3)
    return df # if you directly return the rounded data, then you will lose the other colums

def _download_formatted_data(ticker, date: list, period='1d', exchange='NS'):
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

def load(ticker):
    date = [START_DATE, END_DATE]
    df = _download_formatted_data(ticker, date)
    return df

def calc_years_diff():
    start_date = pd.to_datetime(START_DATE)
    end_date = pd.to_datetime(END_DATE)


    raw_year_diff = end_date.year - start_date.year

    has_passed_anniversary = (end_date.month, end_date.day) >= (start_date.month, start_date.day)

    if not has_passed_anniversary:
        return raw_year_diff - 1
    
    return raw_year_diff
