#import datetime as dt
#import numpy as np                         # pip install numpy
#import pandas as pd                        # pip install panda
#import pandas_datareader as web
#from pandas_datareader import data as pdr
#import yfinance as yf

from dash import Dash, dcc, html, Input, Output, ctx  # pip install dash
#from dash import dash_table
#from dash.dash_table import DataTable, FormatTemplate

from dash_bootstrap_components.themes import BOOTSTRAP

#from dash.dash_table.Format import Sign, Format, Symbol
#from collections import OrderedDict

#import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
#from dash_bootstrap_components._components.Col import Col
#from dash_bootstrap_components._components.Row import Row

#import plotly.graph_objects as go

# --- project imports
from src.data.stockTimeTrace import stockTimetrace, tickers, tickers_titels, tickers_logos, stockPeriods, from_date, to_date
#from src.components.timeIntervallButtons import renderButtons
#from src.components.timeIntervallIndicators import renderButtonIndicators
#from src.components.stockHeader import renderStockHeader
#from src.components.stockTimeSeries import renderStockTimeSeries
#from src.components.stockTable import renderDataTable
from src.components.layout import create_layout

# Get Dates From DateEntry and Convert It To Datetime
#from_date = dt.datetime(2020, 5, 1)
#to_date = dt.datetime.now()
#yf.pdr_override()

# define the dictionary of panda-dataframe that contain the stock data
#df_all = {}

#ticker = 'LYYA.F'   # Lyxor MSCI World - Frankfurt
#ticker = 'BMW.DE'   # BMW
#ticker = 'RDSA.AS'  # Royal Dutch Shell - Stuttgart
#ticker = 'AMD.F'    # AMD - Frankfurt
#ticker = 'EUNL.F'  # iShares Core MSCI World UCITS ETF USD (Acc) - Frankfurt
#ticker = 'ESP0.F'   # Van Eck Games ETF
#ticker = '3CP.SG'   # Xiaomi - Singapore??
# add something else

# 15.02.22: /\|_=)(: changed RDSA.AS to  R6C0.F
#tickers = ['EUNL.F', 'BMW.F',  'R6C0.F', 'AMD.F', 'ESP0.F', '3CP.SG', 'ASML.AS', 'IS3N.F', 'EXSA.DE']
#tickers_titels = ['iShares MSCI World ETF', 
#                  'BMW', 
#                  'Shell A', 
#                  'AMD', 
#                  'Van Eck Gaming ETF', 
#                  'Xiaomi', 
#                  'ASML',
#                  'iShares Core MSCI EM IMI',
#                  'iShares Stoxx Euro 600']


# correspondig png
# smiley https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Mr._Smiley_Face.svg/240px-Mr._Smiley_Face.svg.png
#        https://upload.wikimedia.org/wikipedia/commons/5/51/Mr._Smiley_Face.svg
# AMD    https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/AMD_Logo.svg/640px-AMD_Logo.svg.png
# BMW    https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/BMW.svg/240px-BMW.svg.png
# xiaomi https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Xiaomi_logo.svg/240px-Xiaomi_logo.svg.png
# vaneck https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Vaneck-logo-vector.png/320px-Vaneck-logo-vector.png


# stockPeriods = [1, 5, 20, 60, 300]

'''
# -----------------------------------------------------------------------
# def renderDataTable(app):
# Function for the Datatable-entry in the layout.
# a bit like ArjanCode [Part1](https://www.youtube.com/watch?v=XOFrvzWFM7Y),
#
# -----------------------------------------------------------------------
def renderDataTable(app):

    TABLE_HEADER = ['Stock name', 'Price', '1 day', '5 days', '1 Month ', '3 Months', 'Year']

 
#    @app.callback(
#       Output('datatable', 'data'), 
#      Input('update', "n_intervals")
#      )
#    def update_stockdata(timer1):
#        #print('reading stocks')
#        global df_all 
#        df_all= stockTimetrace()

#        return stockPerformanceTable()
        
    # set up the columns-dictionary for the data table
    # columns are [Stock name / 1D / 5D / M / 3M / Y]

    def stock_performance(ticker):
        stockPerformance = {}

        df = df_all[ticker]

        sLength = len(df['Close'])
        day_end   = df['Close'].iloc[sLength-1] 

        stockPerformance[TABLE_HEADER[0]] = tickers_titels[tickers.index(ticker)]
        stockPerformance[TABLE_HEADER[1]] = day_end

        for i in range(len(stockPeriods)):
            day_start = df['Close'].iloc[sLength-stockPeriods[i]-1]
            stockPerformance[TABLE_HEADER[i+2]] = (day_end - day_start) / day_start

        return  stockPerformance

    #---------------------------------------------------
    #     def stockPerformanceTable():
    #
    #--------------------------------------------------
    def stockPerformanceTable():
        performance = []
        for ticker in tickers:
            performance.append(stock_performance(ticker))

        return performance

    # performance = stockPerformance()

    #---------------------------------------------------
    #     def dataTable_columms():
    #
    # set up the columns by hand. 
    # the columns is a list of dictionaries referenced to by the dash_table.DataTable
    # The naming of the columns is as follows. And is defined by the contents of 'table_header'
    #     'Stock name' 'Price' <in €>  '1 day' <in %> '5 days' <in %> ...
    # 
    # Opposed to many tutorial examples in which the columns-list is created in one line,
    # the trouble here is, that not all colums have the same content-representation   
    # 
    # I don't know, how to combine them differently   
    #--------------------------------------------------
    def dataTable_columms():

        # set up the first column - 
        # the 'Stock name' - just a string - the column-id corresponds to the naming string itself 
        columns = [dict(name = TABLE_HEADER[0], id=TABLE_HEADER[0])]

        #print(columns)

        # set up the second column
        # the 'Price' - the special thing is the '€'-symbol is appended to the number  
        tmp= {"name" :  TABLE_HEADER[1], "id": TABLE_HEADER[1], 
              'type': 'numeric',
              'format': FormatTemplate.money(2).symbol(Symbol.yes).symbol_suffix(' €')
            }
        columns.append(tmp)   

        #print(columns)

        # set up the rest columns
        # the 'period' - the special thing is the +/- sign appended to the percentage
        for i in TABLE_HEADER[2:]:
            tmp= {"name" : i, "id":i, 
                    'type': 'numeric',
                    'format': FormatTemplate.percentage(1).sign(Sign.positive)
                }
            columns.append(tmp)   

        #print(columns[3])

        return(columns)


    #---------------------------------------------------
    # set up the Dash-DataTable 
    #---------------------------------------------------
    #dataTable = dash_table.DataTable(id='datatable',
    dataTable = DataTable(id='datatable',
        columns= dataTable_columms(),
        data = stockPerformanceTable(),
        editable= False,
        row_deletable= False,
        row_selectable="single",
        selected_rows=[0],
        style_header={
            #    'fontWeight': 'bold',
            'backgroundColor': 'rgb(200, 200, 200)',
        },
        style_cell={'fontSize':15},
        style_table={'height': '300px', 'overflowY': 'auto'},
        style_data_conditional=([
            {
            'if': {
                  'filter_query': '{{{col}}} < 0'.format(col=col) ,
                  'column_id': col
                },
            'color': 'red',
            #    'fontWeight': 'bold'
            }
            for col in TABLE_HEADER[2:]
        ]
        +
        [
            {
              'if': {
                    'filter_query': '{{{col}}} > 0'.format(col=col) ,
                    'column_id': col
                },
              'color': 'green',
                #    'fontWeight': 'bold'
            }
            for col in TABLE_HEADER[2:]
        ]
        +
        [
           {
            'if': {'column_id': TABLE_HEADER[0]},
            'textAlign': 'left',
            #    'fontWeight': 'bold'
            },
           {
            'if': {'column_id': TABLE_HEADER[1]},
            'fontWeight': 'bold'
           },
           {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(230, 230, 230)'
            }
        ]
        )
    )     
    # --- End Set-up the DataTable

    return  [
            dbc.Col([ 
                dataTable
            ])
        ]

# --- End def renderDatatable
# ----------------------------------------------------
'''
'''
# -----------------------------------------------------------------------
# def renderDropdown(app):
# Function to render the dropdown to select the things to plot in the timeseries
# * Candlesticks (OHLC)
# * short & long moving averages
# -----------------------------------------------------------------------
def renderDropdown(app):
    return [
            dcc.Dropdown(
                options={
                        'OHLC': 'Candlestick (OHLC)',
                        'EMA': 'EMA12/26',
                },
                value='EMA',
                multi=True
            )
    ]

# --- End def renderDropdown(app):
# ----------------------------------------------------
''' 

# -----------------------------------------------------------------------
# def renderStockHeader(app):
# Function to render the Header of the Stocktimeseries
# Displaying a Stock-logo, the Stock-title and the closing price with percentage indicator
# -----------------------------------------------------------------------
'''
def renderStockHeader(app: Dash):

#    tickers_logos = ["https://upload.wikimedia.org/wikipedia/commons/d/d8/Logo-ishares_2019.svg",
#                    "https://upload.wikimedia.org/wikipedia/commons/4/44/BMW.svg",
#                    "https://upload.wikimedia.org/wikipedia/de/7/74/Royal_Dutch_Shell.svg",
#                    "https://upload.wikimedia.org/wikipedia/commons/7/7c/AMD_Logo.svg",
#                    "https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Vaneck-logo-vector.png/320px-Vaneck-logo-vector.png",
#                    "https://upload.wikimedia.org/wikipedia/commons/2/29/Xiaomi_logo.svg",
#                    "https://upload.wikimedia.org/wikipedia/commons/6/6c/ASML_Holding_N.V._logo.svg",
#                    "https://upload.wikimedia.org/wikipedia/commons/d/d8/Logo-ishares_2019.svg",
#                    "https://upload.wikimedia.org/wikipedia/commons/d/d8/Logo-ishares_2019.svg"
#                    ]

    # 
    # Plotly Dash: How to change header title based on user input?
    #         https://stackoverflow.com/questions/62050548/plotly-dash-how-to-change-header-title-based-on-user-input
    # handle callbacks fpr images:
    # Looking for a better way to display image
    #         https://community.plotly.com/t/looking-for-a-better-way-to-display-image/15672/2

    @app.callback(
    [Output('ticker_header', 'children'),
    Output('image_logo', 'src')], 
    Input('datatable', "selected_rows")
    )
    def update_ticker_header(chosen_rows):
        return ([f'{tickers_titels[chosen_rows[0]]}'],tickers_logos[chosen_rows[0]] )



    #-----------------------------------------------------------------------
    # callbacks for the performance indicators
    # 
    #
    #------------------------------------------------------------------------

    # Indicator Graph 1D
    @app.callback(
        Output('indicator-graph_day', 'figure'),
        [Input('update', 'n_intervals'),
    #    Input(item_id, "label"),
        Input('datatable', "selected_rows")]
    )
    #def graph_1_callback(timer1, label, chosen_rows):
    def graph_1_callback(timer1, chosen_rows):


    #    df = df_all[tickers[tickers_titels.index(label[0])]]
        df = df_all[tickers[chosen_rows[0]]]
        sLength = len(df)
        day_start = df['Close'].iloc[sLength-2]
        day_end   = df['Close'].iloc[sLength-1]
        
        fig = go.Figure(go.Indicator(
            mode="delta + number",
            value=day_end,
            number ={'prefix' : "€ ", 'valueformat' : '.2f'},
            #title = {"text": "1D"},
            delta={'reference': day_start, 'relative': True, 'valueformat':'.2%'})
        )
        
        #fig.update_traces(title_font={'size':16})
        fig.update_traces(delta_font={'size':20})
        fig.update_traces(number_font={'size':20})
        fig.update_layout(height=50, width=120)

        if day_end >= day_start:
            fig.update_traces(delta_increasing_color='green')
        elif day_end < day_start:
            fig.update_traces(delta_decreasing_color='red')
        
        return fig


    return [
            dbc.Col([
                html.Img(id='image_logo',
                    style={"height": "3rem", "width":"8rem"},
                    )
            ]),
            #             html.H1(tickers_titels[tickerIndex], className="card-title")
            dbc.Col([
                html.H3(id='ticker_header', className="text-nowrap")
            ], width=6),
            dbc.Col([
                dcc.Graph(id='indicator-graph_day', figure={},
                        config={'displayModeBar':False})
            ])
        ]
# --- End def renderStockHeader(app):
# ----------------------------------------------------
''' 
'''
# -----------------------------------------------------------------------
# def renderStockGraph(app):
# Function to render the stock timeseries in the layout.
# a bit like ArjanCode [Part1](https://www.youtube.com/watch?v=XOFrvzWFM7Y),
#
# -----------------------------------------------------------------------
def renderStockTimeSeries(app):

    # An output-id can only have one callback.
    # use multiple inputs and determine, which one has been fired
    #     Determining which Input has fired with dash.callback_context
    #                   https://dash.plotly.com/advanced-callbacks
    # 
    @app.callback(
        Output('daily-line', 'figure'),
        [Input("button_5D", "n_clicks")],
        [Input("button_M", "n_clicks")],
        [Input("button_3M", "n_clicks")],
        [Input("button_Y", "n_clicks")],
        Input('datatable', "selected_rows")
    )
    # -- Start function "on_button_click"  --> define the TimeSeriesPlot
    def on_button_click(btn1, btn2, btn3, btn4, chosen_rows):


    #    ctx = Dash.callback_context

        # ctx_trigger = ctx.triggered[0]['prop_id'].split('.')[0]
        ctx_trigger = ctx.triggered_id

        #print(ctx.triggered, chosen_rows)
    #    if (not ctx.triggered) or (ctx_trigger == "dropdown") or (ctx_trigger == "datatable"):
        if (not ctx.triggered_id) or (ctx_trigger == "dropdown") or (ctx_trigger == "datatable"):
            button_id = "button_3M"
        else:
            button_id = ctx_trigger

        #if button_id == "dropdown":
        #    button_id = "button_5D"

        #print(button_id)

        if button_id == "button_5D":
            plotLength = -5
        elif button_id == "button_M":
            plotLength = -20
        elif button_id == "button_3M":
            plotLength = -60
        elif button_id == "button_Y":
            plotLength = -300

    #    df = df_all[tickers[tickers_titels.index(label[0])]]    
        df = df_all[tickers[chosen_rows[0]]]


        #print(chosen_rows[0])
        # print(df.head(5))

        # calculate the short/ fast moving average
        ShortEMA = df.Close.ewm(span=12, adjust = False).mean()
        # calculate the middle/medium exp. mov. average
        MiddleEMA = df.Close.ewm(span=26, adjust = False).mean()

        sLength = len(df)
        day_start = df['Close'].iloc[sLength+plotLength-1]
        day_end   = df['Close'].iloc[sLength-1]

        if day_end >= day_start:
                trace_close = go.Scatter(x=df.index[plotLength:],
                                y=df['Close'][plotLength:],
                                name='Close',
    #                         line=dict(color='#000000', width = 1.5),
                                fill='tozeroy',
                                line={'color':'green'}
                                )
                legend_x = 0.1
                legend_y = 0.95
        elif day_end < day_start:
                trace_close = go.Scatter(x=df.index[plotLength:],
                                y=df['Close'][plotLength:],
                                name='Close',
    #                         line=dict(color='#000000', width = 1.5),
                                fill='tozeroy',
                                mode='lines', 
                                line={'color':'red'}
                                )
                legend_x = 0.1
                legend_y = 0.1

        trace_EMAshort = go.Scatter(x=df.index[plotLength:],
                            y=ShortEMA[plotLength:],
                            name='ema_12',
                            line=dict(color='#0066ff', width = 1.5))

        trace_EMAmedium = go.Scatter(x=df.index[plotLength:],
                            y=MiddleEMA[plotLength:],
                            name='ema_26',
                            line=dict(color='#003380', width = 1.5))

        trace_Candlestick = go.Candlestick(x=df.index[plotLength:], 
                            open=df['Open'][plotLength:],
                            high=df['High'][plotLength:],
                            low=df['Low'][plotLength:],
                            close=df['Close'][plotLength:],
                            name='OHLC')

        data = [trace_close, trace_EMAshort ,trace_EMAmedium, trace_Candlestick ]



        layout = dict(
            #title='Time series with range slider and selectors',
            margin=dict(t=0, r=0, l=0, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=400,
            yaxis=dict(
                showgrid = True,
                gridcolor= 'LightGray'
            ),
    #        showlegend = False,
            legend=dict(
                x=legend_x,
                y=legend_y,
                # traceorder='normal',
                bgcolor='White',
                font=dict(
                    size=12,),
            ),
            xaxis=dict(
                rangeslider=dict(
                    visible = False
                ),
                showgrid = True,
                gridcolor='LightGray',
                type='date'
            )
        )

        fig = go.Figure(data=data, layout=layout)


    #    fig.update_yaxes(range=[df['Close'][plotLength:].min()*.99,df['Close'][plotLength:].max()*1.01])
        fig.update_yaxes(range=[
            np.array([df['Close'][plotLength:].min(), ShortEMA[plotLength:].min(), MiddleEMA[plotLength:].min()]).min()*.99,
            np.array([df['Close'][plotLength:].max(), ShortEMA[plotLength:].max(), MiddleEMA[plotLength:].max()]).max()*1.01
            ]
        )
        

        # if day_end >= day_start:
        #     return fig.update_traces(fill='tozeroy',line={'color':'green'})
        # elif day_end < day_start:
        #     return fig.update_traces(fill='tozeroy',
        #                          line={'color': 'red'})

        return fig
    # -- End function "on_button_click"

    return [
            dbc.Col([
                dcc.Graph(id='daily-line', figure={},
                config={'displayModeBar':False})   
            ])
        ]

# --- End function 'renderStockTimeSeries'
'''
#- 25.03.24 moved to componeents.timeIntervallButtons.py
# -----------------------------------------------------------------------
# def renderButtons(app):
# Function to render the buttons in the layout.
# a bit like ArjanCode [Part1](https://www.youtube.com/watch?v=XOFrvzWFM7Y),
#
# -----------------------------------------------------------------------
#def renderButtons(app):

# -- reslut of upgrade to Dash Version xxx 
#   the 'block'-feature does not exist anymore.  
#     return [
#         dbc.Col([
# #            dbc.Button('5D',  id="button_5D", block=True, size='sm')
#             dbc.Button('5D',  id="button_5D", size='sm')
#         ]),
#         dbc.Col([
# #            dbc.Button('M',  id="button_M",  block=True, size='sm')
#             dbc.Button('M',  id="button_M", size='sm')
#         ]),
#         dbc.Col([
# #            dbc.Button('3M',  id="button_3M",  block=True, size='sm')
#             dbc.Button('3M',  id="button_3M", size='sm')
#         ]),
#         dbc.Col([
# #            dbc.Button('Y',  id="button_Y",  block=True, size='sm')
#             dbc.Button('Y',  id="button_Y", size='sm')
#         ])
#     ]


# render as ButtonGroup - 25.03.24 moved to componeents.timeIntervallButtons.py
#    return [dbc.ButtonGroup([
#            dbc.Button('5D',  id="button_5D",outline=True, color="primary", size='sm'),
#            dbc.Button('M',  id="button_M",outline=True, color="primary", size='sm'),
#            dbc.Button('3M',  id="button_3M",outline=True, color="primary", size='sm'),
#            dbc.Button('Y',  id="button_Y", outline=True, color="primary",size='sm')
#    ])
#    ]
# --- End def renderButtons


# -----------------------------------------------------------------------
# def renderButtonIndicators(app):
# Function to render the indicators below the buttons in the layout.
# a bit like ArjanCode [Part1](https://www.youtube.com/watch?v=XOFrvzWFM7Y),
#
# -----------------------------------------------------------------------
'''
def renderButtonIndicators(app):
    
    #----------------------------------------------------------------------------------
    # function
    # set up the indicator graph showing the performace between start and end data.
    # Indicators below the buttons
    # Plotly Indicators in Python: https://plotly.com/python/indicator/
    # Plotly Reference: indicator: https://plotly.com/python/reference/indicator/
    # Input 
    #      day_start: 
    #       day_end  :
    #
    # output
    #       fig: plotly-figure object
    #----------------------------------------------------------------------------------
    def indicatorPerformance(day_start, day_end):

        fig = go.Figure(go.Indicator(
            mode="delta",
            value=day_end,
            delta={'reference': day_start, 'relative': True, 'valueformat':'.2%'}))
        
        fig.update_traces(delta_font={'size':20})
        fig.update_traces(number_font={'size':20})

        fig.update_layout(height=60, width=120)

        if day_end >= day_start:
            fig.update_traces(delta_increasing_color='green')
        elif day_end < day_start:
            fig.update_traces(delta_decreasing_color='red')
        
        return fig
    # --- End 'indicatorPerformance'


    # Indicator Graphs below the buttons
    @app.callback([
        Output('indicator-graph', 'figure'),
        Output('indicator-graph2', 'figure'),
        Output('indicator-graph3', 'figure'),
        Output('indicator-graph4', 'figure')],
        [Input('update', 'n_intervals'),
        Input('datatable', "selected_rows")]
    )
    def graph_2_callback(timer1, chosen_rows):

        df = df_all[tickers[chosen_rows[0]]]

        sLength = len(df)
        day_end   = df['Close'].iloc[sLength-1]

        indicators = []
        for i in stockPeriods[1:]:
            day_start = df['Close'].iloc[sLength-i-1]
            indicators.append(indicatorPerformance(day_start, day_end))
        
        return indicators
    # --- End 'graph_2_callback'




    # return all button-figures
    return [
            dbc.Col([
                dcc.Graph(id='indicator-graph', figure={},
                            config={'displayModeBar':False})
            ]),                            
                            
            dbc.Col([
                dcc.Graph(id='indicator-graph2', figure={},
                            config={'displayModeBar':False})
            ]),

            dbc.Col([
                dcc.Graph(id='indicator-graph3', figure={},
                          config={'displayModeBar':False})
            ]),

            dbc.Col([
                dcc.Graph(id='indicator-graph4', figure={},
                            config={'displayModeBar':False})
            ])
        ]

# --- End Function 'renderButtonIndicators(app)'
'''


# ----------------------------------------------------
# def create_layout():
# Function to set up the layout.
# a bit like ArjanCode [Part1](https://www.youtube.com/watch?v=XOFrvzWFM7Y),
#
# ----------------------------------------------------
'''
def create_layout(app: Dash, df_all: pd.DataFrame):

    return dbc.Container([
                dbc.Row([
                    dbc.Col([
                        dbc.Row(renderDataTable(app, df_all), 
                            style={"width": "45rem", 'padding': '5px'},
                            className="mt-6"),
                    #    dbc.Row(renderDropdown(app)),         
                        dbc.Card([
                                dbc.CardBody([
                                    dbc.Row(renderStockHeader(app, df_all)),
                                    dbc.Row(renderStockTimeSeries(app, df_all)),
                                    dbc.Row(renderButtons(app), 
                                    className="radio-group md-md-block"),
                                    dbc.Row(renderButtonIndicators(app, df_all), justify="between"),
                                ]),
                            ],
                            style={"width": "43rem"},
                            className="mt-3"
                        )
                    ], width=6)
                ]),

                dcc.Interval(id='update', n_intervals=0, interval=1000*3600)
            ])

# --- End 'stockTimetrace'
'''

# 24.03.24: refactor - moved to .src.data.stockTimeTrace
# ----------------------------------------------------
# def stockTimetrace():
#
# read the stock-data from Yahoo for the ticker-symbols provided by 'tickers' 
# set up a dictionary of pandas dataframes
# How to create an array of dataframes in Python
# https://stackoverflow.com/questions/33907776/how-to-create-an-array-of-dataframes-in-python
#
# ----------------------------------------------------
# def stockTimetrace():

#     df = {}

#     for ticker in tickers:
#       #  df[ticker] = web.DataReader(ticker, 'yahoo', from_date, to_date)
#         df[ticker] = pdr.get_data_yahoo(ticker, 
#         start=from_date, end=to_date,  progress=False)
#     # print('stockTimetrace: Reading Stocks at ' + dt.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
    
#     return df

# --- End 'stockTimetrace'


#df_all = stockTimetrace(tickers, [from_date, to_date])

#print(df_all[tickers[0]].head())
#print(df_all[tickers[0]].tail())

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#external_stylesheets =[dbc.themes.BOOTSTRAP]

# set the tab-titel
# Dash v1.14.0 Released - Update the Tab’s Title, Removing the “Updating…” Messages, Updated DataTable Link Behavior
#    https://community.plotly.com/t/dash-v1-14-0-released-update-the-tabs-title-removing-the-updating-messages-updated-datatable-link-behavior/43080  

# app = Dash(__name__, external_stylesheets=external_stylesheets,
#                 title='StockViewer',
#                 meta_tags=[{'name': 'viewport',
#                             'content': 'width=device-width, initial-scale=1.0'}]
#                 )

def main() -> None:


    df_all = stockTimetrace(tickers, [from_date, to_date])

    app = Dash(__name__, external_stylesheets=[BOOTSTRAP],
                    title='StockViewer',
                    meta_tags=[{'name': 'viewport',
                                'content': 'width=device-width, initial-scale=1.0'}]
                    )

    app.layout = create_layout(app, df_all)
    app.run_server(port=8060, debug=True)

if __name__ == '__main__':
#  app.run_server(host='0.0.0.0', port=8060, debug=True)
#   app.run_server(port=8060, debug=True)
    main()