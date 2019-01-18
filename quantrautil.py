import fix_yahoo_finance as yf
import quandl
import traceback
import iexfinance as iex
import nsepy

from quandl.errors.quandl_error import AuthenticationError

# API key to access quandl data
def get_quantinsti_api_key():
    #To get your API key, sign up for a free Quandl account
    #Then, you can find your API key on Quandl account settings page
    return '<<Copy Paste your Quandl API Key here>>'

def get_data(ticker, start_date='2016-01-01', end_date='2017-01-01'):
    try:
        df = quandl.get('WIKI/'+ticker, start_date=start_date, end_date=end_date, api_key=get_quantinsti_api_key())
        df['Source'] = 'Quandl Wiki'
        return d[['Open','High','Low','Close','Volume','Source']]
    except AuthenticationError as a:        
        print(a)        
        print("Please replace the line no. 13 in quantrautil.py file with your Quandl API Key")
    except:
        try:
            df = quandl.get('NSE/'+ticker, start_date=start_date, end_date=end_date, api_key=get_quantinsti_api_key())
            df['Source'] = 'Quandl NSE'
            return df[['Open','High','Low','Close','Volume','Source']]
        except:
            try:
                start_date = pd.to_datetime(start_date)
                end_date = pd.to_datetime(end_date)
                df = iex.get_historical_data(ticker, start=start_date, end=end_date, output_format='pandas')
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
                    df = nsepy.get_history(symbol=ticker, start=start_date, end=end_date)                    
                    df['Source'] = 'nsepy'
                    return df[['Open','High','Low','Close','Volume','Source']]
                except:
                    try:
                        df = yf.download(ticker, start_date, end_date)
                        df['Source'] = 'Yahoo'
                        return df[['Open','High','Low','Close','Volume','Source']]
                    except:                                     
                        print(traceback.print_exc())
