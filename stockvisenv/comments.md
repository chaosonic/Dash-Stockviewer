## TODO
- [x] Refactor the 'import' declarations to `from dash import Dash, dcc, html, Input, Output
` instead of `import dash_core_components as dcc` - this is Python 3.9-stuff --> move over to virtual env. `DashTest`
- [ ] Add multi-selection [dropdown](https://dash.plotly.com/dash-core-components/dropdown) with plot-options - like short EMA/ long EMA / candlestick / Volume
- [ ] Create multiple reads for different stock-sources Yahoo, Alphavantage, Quandl yielding the same dataframe to work with --> see `DashTest\dashTest_Alphavantage.py`
- [ ] Refactor: can usage of `sLength = len(df) --> df['Close'].iloc[sLength-1]` be written with something like  `df['Close'].iloc[:]`
- [x] add moving averages (start with simple moving average) 
      hard-coded fast ema=12 and medium ema = 26
    - [x] locate the legend depending if increase or decrease- legend is selectabel
- [x] combine the logo- and the header-callback, which only take the `Input('datatable', "selected_rows")` as input, to one callback.
- [ ] Document Docker deployment

## contents of the pandas-dataframe with stock-data

The set up of the dataframe references to the dataframe returned by `yahoo-finance`.


### retrieve historical financial stock data from yahoo-finance
~~~python
import datetime as dt
import pandas as pd                        # pip install panda
import pandas_datareader as web

# Get Dates From DateEntry and Convert It To Datetime
from_date = dt.datetime(2020, 5, 1)
to_date = dt.datetime.now()

df = {}

df = web.DataReader('EUNL.F', 'yahoo', from_date, to_date) 

print(df.head(3))
print(df.tail(3))
~~~

--> results in a representation in which the first line represents the oldest date and the last line the most recent date.
~~~
                 High        Low       Open      Close  Volume  Adj Close
Date
2020-05-04  49.230000  48.522999  49.063999  48.939999   14063  48.939999
2020-05-05  50.683998  49.660000  49.679001  50.622002    4035  50.622002
2020-05-06  50.799999  50.226002  50.568001  50.388000    8595  50.388000

                 High        Low       Open      Close  Volume  Adj Close
Date
2022-09-28  70.739998  69.468002  69.926003  70.739998    6507  70.739998
2022-09-29  70.587997  68.279999  70.587997  68.674004    7540  68.674004
2022-09-30  69.396004  67.968002  68.487999  67.968002    4873  67.968002
~~~

#### Breaking change in Yahoo-API - work-around available
Dec. 15 2022 - some breaking changes in the Yahoo-API that broke compatibility with previous pandas datareader versions.
As per the discussion [on pydata/pandas-datareader](https://github.com/pydata/pandas-datareader/issues/952) and [Stackoverflow](https://stackoverflow.com/questions/74832296/typeerror-string-indices-must-be-integers-when-getting-data-of-a-stock-from-y).
A work around is implemented:
~~~python
#import pandas_datareader as web
from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()

def stockTimetrace():
    df = {}
    for ticker in tickers:
      # this line is commented out  
      #  df[ticker] = web.DataReader(ticker, 'yahoo', from_date, to_date)
      # this line is added
        df[ticker] = pdr.get_data_yahoo(ticker, 
        start=from_date, end=to_date,  progress=False)
    # print('stockTimetrace: Reading Stocks at ' + dt.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
    return df
~~~


### retrieve historical financial stock data from Alphavantage

~~~python
from alpha_vantage.timeseries import TimeSeries
from pprint import pprint

api_key = '<your AV-Key>'

ts = TimeSeries(key=api_key, output_format='pandas')
 
data, meta_data = ts.get_daily(symbol='MSFT', outputsize='compact')

# print the dataframe retrieved from Alphavantage. 
# The most recent date is on top and the oldest on the bottom
pprint(data.head(3))
pprint(data.tail(3))
print(meta_data)

# rename the data according to yahoo-format - example
data = data.rename(columns={ '1. open': 'Open', '2. high': 'High', '3. low': 'Low', '4. close': 'Close', '5. volume': 'Volume'})
data = data[[ 'High', 'Low', 'Open',  'Close', 'Volume']]
# The order of the Yahoo-dataframe is reversed to the one from Alphavantage
# for Yahoo-format reverse the dataframe
data = data.iloc[::-1]
pprint(data.head(3))
pprint(data.tail(3))

~~~


## add a datatable

[Dash dash_table.DataTable Reference](https://dash.plotly.com/datatable/reference)

Populate a dictionary with stock-performance data
~~~python
stockPeriods = [1, 5, 20, 60, 300]

def stock_performance(ticker):
    stockPerformance = {}

    df = df_all[ticker]

    sLength = len(df['Close'])
    day_end   = df['Close'].iloc[sLength-1] 

    stockPerformance[table_header[0]] = tickers_titels[tickers.index(ticker)]
    stockPerformance[table_header[1]] = day_end

    for i in range(len(stockPeriods)):
        day_start = df['Close'].iloc[sLength-stockPeriods[i]-1]
        stockPerformance[table_header[i+2]] = (day_end - day_start) / day_start

    return  stockPerformance


~~~

## add the close price as column to the datatable

- the current implementation sets the values of all columns to `percentage` with two decimal positions. This works fine, as long as only performance data is shown.
  When the close price is added, the values in the columns are also treated a percentage. 
  ~~~python
  dash_table.DataTable(id='datatable',
        columns=  [
            {"name": i, "id": i,
            'type': 'numeric',
            'format': FormatTemplate.percentage(2).sign(Sign.positive)
            } for i in table_header
        ],
        data = performance,
        editable= False,
        ...
   ~~~
   The solution is to define the format inside the column dictionary. Hence the overall columns-definition consists of three parts. The `Stock name` - no specific format, `Price` with 2 decimal precision and as € and the remaining columns `1 day, 5 days, month ....`  (time periods) as 2 decimal percentage.
   * For the price there is a specific `FormatTemplate.money(2)` - which however shows `$`-currency and no `€`. 
      * as `FormatTemplate.percentage(2).sign(Sign.positive)` is extended by `.sign(..)`, perhaps this works with `FormatTemplate.money`, too.
        Extend with `symbol(Symbol.yes).symbol_suffix('€')` like described [here](https://dash.plotly.com/datatable/data-formatting).
      * I was not able to implement the above the nice way like `columns = [{ ..} for i in table_header]`. I set up the definition of the list of columns-dictionaries stand alone.
      ~~~python
       columns = [dict(name = table_header[0], id=table_header[0])]
       tmp= {"name" :  table_header[1], "id": table_header[1], 
            'type': 'numeric',
            'format': FormatTemplate.money(2).symbol(Symbol.yes).symbol_suffix(' €')
           }
        columns.append(tmp)   

        for i in table_header[2:]:
            tmp= {"name" : i, "id":i, 
                    'type': 'numeric',
                    'format': FormatTemplate.percentage(2).sign(Sign.positive)
                }
            columns.append(tmp)   
      ~~~
     and reference it in the datatable-section as
     ~~~python
     dash_table.DataTable(id='datatable',
                        columns= columns,
     ~~~

### Links to the topic
   * [Dash table formatting decimal place](https://community.plotly.com/t/dash-table-formatting-decimal-place/34975/2) plotly-forum
   * [DataTable - Number Formatting - Using FormatTemplate](https://dash.plotly.com/datatable/data-formatting) - plotly/Dash-documentation


##  color-coding the performance-percentage. Decrease is red / Increase is green
   
In Dash, this is referred to as [conditional formatting](https://dash.plotly.com/datatable/conditional-formatting)
To color values less than 0 red, use the following inside the `dash_table.DataTable`
~~~python
style_data_conditional=([
    {
     'if': {
        'filter_query': '{{{col}}} < 0'.format(col=col) ,
        'column_id': col
         },
     'color': 'red',
     'fontWeight': 'bold'
    }
    for col in table_header[2:]
])
~~~
The above can easily be modified to set increasing / positive values to green.

### Links to the topic
   * [Conditional Formatting](https://dash.plotly.com/datatable/conditional-formatting) - plotly/Dash-documentation


## Add dropdown menu

Implement the dropdown-menu
~~~python
dbc.Row([
    dbc.Col([    
        dbc.DropdownMenu(
            dropdown_items, 
            label=tickers_titels[0], 
            addon_type="prepend",
            bs_size="sm",
            id=item_id
        )
    ]),
], justify="between"), 
~~~
[Stackoverflow: create bootstrap drop down menu in plotly dash using one function to set it up](https://stackoverflow.com/questions/65806214/create-bootstrap-drop-down-menu-in-plotly-dash-using-one-function-to-set-it-up)

Stuff to configure the dropdown-menu. 
The dropdown-menu is populated with the contents of `tickers_titels`. The item-id's are also constructed with those names
~~~python
item_id = 'dropdown'
dropdown_items = [dbc.DropdownMenuItem(item, id=item_id+'_'+item) 
                  for item in tickers_titels]

dropdown_output = Output(item_id, "label")
dropdown_inputs = [Input(item_id+'_'+item, "n_clicks") for item in tickers_titels]
~~~



The callback for the dropdown itself - it changes the label of the dropdown menu according to the selected item
~~~python
@app.callback(dropdown_output,dropdown_inputs)
def update_label(*args):
    # get the triggered item
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
    # get the label for the triggered id or return no selection
    if (np.array([n==None for n in args]).all()) or not ctx.triggered:
        label = [tickers_titels[0]]
        return label 
    else:
        return [label for label in tickers_titels if item_id+'_'+label == triggered_id]
~~~

Usage of the selected item from the dropdown-menu in other callbacks. E.g. to update a header, or a logo

[Plotly Dash: How to change header title based on user input?](https://stackoverflow.com/questions/62050548/plotly-dash-how-to-change-header-title-based-on-user-input)
The value of the dropdown-item is in List-format. Hence the `label[0]` has to be indexed.
~~~python
@app.callback(
   [Output('ticker_header', 'children')], 
   Input(item_id, "label")
   )
def update_ticker_header(label):
    return [f'{label[0]}']
~~~

A snippet to extract the dataframe of the selected share
~~~python
df = df_all[tickers[tickers_titels.index(label[0])]]    
~~~


## Specify the title of the app - this is the title displayed in the tab-header of the browser

set the tab-titel
[Dash v1.14.0 Released - Update the Tab’s Title, Removing the “Updating…” Messages, Updated DataTable Link Behavior](https://community.plotly.com/t/dash-v1-14-0-released-update-the-tabs-title-removing-the-updating-messages-updated-datatable-link-behavior/43080)


~~~python
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                title='StockViewer',
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

~~~

## change header title based on user input

~~~python
html.H1(id='ticker_header', className="card-title"),
~~~

[Plotly Dash: How to change header title based on user input?](https://stackoverflow.com/questions/62050548/plotly-dash-how-to-change-header-title-based-on-user-input)
~~~python
@app.callback(
   [Output('ticker_header', 'children')], 
   Input('datatable', "selected_rows")
   )
def update_ticker_header(chosen_rows):
    return [f'{tickers_titels[chosen_rows[0]]}']
~~~


## handle callbacks for images

[Looking for a better way to display image](https://community.plotly.com/t/looking-for-a-better-way-to-display-image/15672/2)

set up a list of image-url's
~~~python
tickers_logos = ["https://upload.wikimedia.org/wikipedia/commons/d/d8/Logo-ishares_2019.svg",
                 "https://upload.wikimedia.org/wikipedia/commons/4/44/BMW.svg",
                 "https://upload.wikimedia.org/wikipedia/de/7/74/Royal_Dutch_Shell.svg",
                 ]
~~~
which can than be referenced by the callback
~~~python
@app.callback(
    Output('image_logo', 'src'), 
    Input('datatable', "selected_rows")
    )
def update_ticker_logo(chosen_rows):
    return tickers_logos[chosen_rows[0]]

~~~

## Callback with multiple input and with multiple outputs

[Multiple outputs in Dash - Now Available!](https://community.plotly.com/t/multiple-outputs-in-dash-now-available/19437)

Either return the items separed by a comma, or return a list a described below. 
~~~python
# Indicator Graph 5D
@app.callback([
    Output('indicator-graph', 'figure'),
    Output('indicator-graph2', 'figure'),
    Output('indicator-graph3', 'figure'),
    Output('indicator-graph4', 'figure')],
    [Input('update', 'n_intervals'),
    Input('datatable', "selected_rows")]
)
def graph_1_callback(timer1, chosen_rows):

    df = df_all[tickers[chosen_rows[0]]]

    sLength = len(df)
    day_end   = df['Close'].iloc[sLength-1]

    indicators = []
    for i in stockPeriods[1:]:
        day_start = df['Close'].iloc[sLength-i-1]
        indicators.append(indicatorPerformance(day_start, day_end))
    
    return indicators


~~~

### timeline
* Initial versions: 
    * Python 3.8.5
    * dash==1.19.0
    * dash-bootstrap-components==0.11.3
    * plotly==4.14.3
    * numpy==1.20.1
    * pandas==1.2.3
    * pandas-datareader==0.10.0

* Update to Python 3.9.13 & Dash 2.6.1
    * dash==2.6.1
    * dash-bootstrap-components==1.2.1
    * plotly==5.10.0
    * numpy==1.23.2
    * pandas==1.4.4
    * pandas-datareader==0.10.0
