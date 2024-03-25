from pandas_datareader import data as pdr
import datetime as dt
import yfinance as yf

# The final idea behind this file, is that here all 
# the data will be read or imported. 
# currently, there are to many loose variables


#ticker = 'LYYA.F'   # Lyxor MSCI World - Frankfurt
#ticker = 'BMW.DE'   # BMW
#ticker = 'RDSA.AS'  # Royal Dutch Shell - Stuttgart
#ticker = 'AMD.F'    # AMD - Frankfurt
#ticker = 'EUNL.F'  # iShares Core MSCI World UCITS ETF USD (Acc) - Frankfurt
#ticker = 'ESP0.F'   # Van Eck Games ETF
#ticker = '3CP.SG'   # Xiaomi - Singapore??
# add something else

# 15.02.22: /\|_=)(: changed RDSA.AS to  R6C0.F
tickers = ['EUNL.F', 'BMW.F',  'R6C0.F', 'AMD.F', 'ESP0.F', '3CP.SG', 'ASML.AS', 'IS3N.F', 'EXSA.DE']
tickers_titels = ['iShares MSCI World ETF', 
                  'BMW', 
                  'Shell A', 
                  'AMD', 
                  'Van Eck Gaming ETF', 
                  'Xiaomi', 
                  'ASML',
                  'iShares Core MSCI EM IMI',
                  'iShares Stoxx Euro 600']

tickers_logos = ["https://upload.wikimedia.org/wikipedia/commons/d/d8/Logo-ishares_2019.svg",
                 "https://upload.wikimedia.org/wikipedia/commons/4/44/BMW.svg",
                 "https://upload.wikimedia.org/wikipedia/de/7/74/Royal_Dutch_Shell.svg",
                 "https://upload.wikimedia.org/wikipedia/commons/7/7c/AMD_Logo.svg",
                 "https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Vaneck-logo-vector.png/320px-Vaneck-logo-vector.png",
                 "https://upload.wikimedia.org/wikipedia/commons/2/29/Xiaomi_logo.svg",
                 "https://upload.wikimedia.org/wikipedia/commons/6/6c/ASML_Holding_N.V._logo.svg",
                 "https://upload.wikimedia.org/wikipedia/commons/d/d8/Logo-ishares_2019.svg",
                 "https://upload.wikimedia.org/wikipedia/commons/d/d8/Logo-ishares_2019.svg"
                ]



# something
stockPeriods = [1, 5, 20, 60, 300]

# Get Dates From DateEntry and Convert It To Datetime
from_date = dt.datetime(2020, 5, 1)
to_date = dt.datetime.now()

yf.pdr_override()


# ----------------------------------------------------
# def stockTimetrace():
#
# read the stock-data from Yahoo for the ticker-symbols provided by 'tickers' 
# set up a dictionary of pandas dataframes
# How to create an array of dataframes in Python
# https://stackoverflow.com/questions/33907776/how-to-create-an-array-of-dataframes-in-python
#
# ----------------------------------------------------
def stockTimetrace(tickers, timeInterval):

    df = {}

    for ticker in tickers:
      #  df[ticker] = web.DataReader(ticker, 'yahoo', from_date, to_date)
        df[ticker] = pdr.get_data_yahoo(ticker, 
        start=timeInterval[0], end=timeInterval[1],  progress=False)
    # print('stockTimetrace: Reading Stocks at ' + dt.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
    
    return df

# --- End 'stockTimetrace'
