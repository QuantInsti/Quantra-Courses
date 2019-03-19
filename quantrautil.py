import pandas as pd
import traceback

import fix_yahoo_finance as yf
import quandl
import iexfinance.stocks as iex
import nsepy

from quandl.errors.quandl_error import AuthenticationError

def get_quantinsti_api_key():
    """
        This function returns the Quandl's API key which is used to access quandl data
        To get your API key, sign up for a free Quandl account (https://docs.quandl.com/docs#section-authentication)
        Then, you can find your API key on Quandl account settings page
    """
    return '<<Copy paste your Quandl API Key here>>'

def get_alpha_vantage_api_key():
    """
        This function returns the Alpha vantage API key which is used to access Alpha vantage data
        To get your API key, sign up for a free Alpha vantage account (https://www.alphavantage.co/support/#api-key)        
    """    
    return '<<Copy paste your Alpha Vantage API Key here>>'   

def get_binance_api_key():
    """
        This function returns the Binance API key which is used to access crypto data.
        To get your API key, sign up for a free binance account.        
    """    
    return '<<Copy paste your Binance API Key here>>'   


def get_data(ticker, start_date='2016-01-01', end_date='2017-01-01'):
    """
        This function fetches the data from different web source such as Quandl, Yahoo finance and NSEPy
    """
    try:
        df = yf.download(ticker, start_date, end_date)
        df['Source'] = 'Yahoo'        
        return df[['Open','High','Low','Close','Adj Close','Volume','Source']]
    except:
        try:
            df = quandl.get('WIKI/'+ticker, start_date=start_date, end_date=end_date, api_key=get_quantinsti_api_key())
            df['Source'] = 'Quandl Wiki'            
            df = df.rename(columns={"Adj. Close": "Adj Close"})                        
            return df[['Open','High','Low','Close','Adj Close','Volume','Source']]
        except AuthenticationError as a:        
            print(a)        
            print("Please replace the line no. 17 in quantrautil.py file with your Quandl API Key")
        except:
            try:
                start_date = pd.to_datetime(start_date)
                end_date = pd.to_datetime(end_date)
                df = iex.stocks.get_historical_data(ticker, start=start_date, end=end_date, output_format='pandas')
                df.index.name = 'Date'
                df = df.rename(columns={'open': 'Open',
                                        'high': 'High',
                                        'low': 'Low',
                                        'close': 'Close',
                                        'volume': 'Volume',
                                       })
                df['Source'] = 'IEX'                
                return df[['Open','High','Low','Close','Volume','Source']]
            except:
                try:
                    df = quandl.get('NSE/'+ticker, start_date=start_date, end_date=end_date, api_key=get_quantinsti_api_key())
                    df['Source'] = 'Quandl NSE'                    
                    return df[['Open','High','Low','Close','Volume','Source']]
                except:
                    try:                    
                        df = nsepy.get_history(symbol=ticker, start=start_date, end=end_date)                    
                        df['Source'] = 'nsepy'
                        return df[['Open','High','Low','Close','Volume','Source']]
                    except:                                                           
                        print(traceback.print_exc())
                        
