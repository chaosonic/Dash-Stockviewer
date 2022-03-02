import datetime as dt
import numpy as np                         # pip install numpy
import pandas as pd                        # pip install panda
import pandas_datareader as web

import dash                                # pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_table

import dash_table.FormatTemplate as FormatTemplate
from dash_table.Format import Sign, Format, Symbol
from collections import OrderedDict

import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
from dash_bootstrap_components._components.Col import Col
from dash_bootstrap_components._components.Row import Row

import plotly.graph_objects as go


# Get Dates From DateEntry and Convert It To Datetime
from_date = dt.datetime(2020, 5, 1)
to_date = dt.datetime.now()

#ticker = 'LYYA.F'   # Lyxor MSCI World - Frankfurt
#ticker = 'BMW.DE'   # BMW
#ticker = 'RDSA.AS'  # Royal Dutch Shell - Stuttgart
#ticker = 'AMD.F'    # AMD - Frankfurt
#ticker = 'EUNL.F'  # iShares Core MSCI World UCITS ETF USD (Acc) - Frankfurt
#ticker = 'ESP0.F'   # Van Eck Games ETF
#ticker = '3CP.SG'   # Xiaomi - Singapore??
# add something else

# 15.02.22: /\|_=)(: changed RDSA.AS to  R6C0.F
tickers = ['EUNL.F', 'BMW.F',  'R6C0.F', 'AMD.F', 'ESP0.F', '3CP.SG', 'ASML.AS', 'IS3N.F']
tickers_titels = ['iShares MSCI World ETF', 
                  'BMW', 
                  'Shell A', 
                  'AMD', 
                  'Van Eck Gaming ETF', 
                  'Xiaomi', 
                  'ASML',
                  'iShares Core MSCI EM IMI']

tickers_logos = ["https://upload.wikimedia.org/wikipedia/commons/d/d8/Logo-ishares_2019.svg",
                 "https://upload.wikimedia.org/wikipedia/commons/4/44/BMW.svg",
                 "https://upload.wikimedia.org/wikipedia/de/7/74/Royal_Dutch_Shell.svg",
                 "https://upload.wikimedia.org/wikipedia/commons/7/7c/AMD_Logo.svg",
                 "https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Vaneck-logo-vector.png/320px-Vaneck-logo-vector.png",
                 "https://upload.wikimedia.org/wikipedia/commons/2/29/Xiaomi_logo.svg",
                 "https://upload.wikimedia.org/wikipedia/commons/6/6c/ASML_Holding_N.V._logo.svg",
                 "https://upload.wikimedia.org/wikipedia/commons/d/d8/Logo-ishares_2019.svg"
                 ]

# correspondig png
# smiley https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Mr._Smiley_Face.svg/240px-Mr._Smiley_Face.svg.png
#        https://upload.wikimedia.org/wikipedia/commons/5/51/Mr._Smiley_Face.svg
# AMD    https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/AMD_Logo.svg/640px-AMD_Logo.svg.png
# BMW    https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/BMW.svg/240px-BMW.svg.png
# xiaomi https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Xiaomi_logo.svg/240px-Xiaomi_logo.svg.png
# vaneck https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Vaneck-logo-vector.png/320px-Vaneck-logo-vector.png


# set up the columns-dictionary for the data table
# columns are [Stock name / 1D / 5D / M / 3M / Y]
table_header = ['Stock name', 'Price', '1 day', '5 days', '1 Month ', '3 Months', 'Year']

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


# tickerIndex = 1

# set up a dictionary of pandas dataframes
# How to create an array of dataframes in Python
# https://stackoverflow.com/questions/33907776/how-to-create-an-array-of-dataframes-in-python

df_all = {}
performance = []
for ticker in tickers:
    df_all[ticker] = web.DataReader(ticker, 'yahoo', from_date, to_date)
    performance.append(stock_performance(ticker))

# set up the columns by hand - the columns-list of dictionaries is referenced by the dash_table.DataTable
# I don't know, how to combine the different 
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

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

external_stylesheets =[dbc.themes.BOOTSTRAP]

# set the tab-titel
# Dash v1.14.0 Released - Update the Tab’s Title, Removing the “Updating…” Messages, Updated DataTable Link Behavior
#    https://community.plotly.com/t/dash-v1-14-0-released-update-the-tabs-title-removing-the-updating-messages-updated-datatable-link-behavior/43080  

app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                title='StockViewer',
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )


app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([ 
                    dash_table.DataTable(id='datatable',
                        columns= columns,
                        data = performance,
                        editable= False,
                        row_deletable= False,
                        row_selectable="single",
                        selected_rows=[0],
                        style_header={
                            'fontWeight': 'bold',
                            'backgroundColor': 'rgb(200, 200, 200)',
                        },
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
                        ]
                        +
                        [
                            {
                                'if': {
                                    'filter_query': '{{{col}}} > 0'.format(col=col) ,
                                    'column_id': col
                                },
                                'color': 'green',
                                'fontWeight': 'bold'
                            }
                            for col in table_header[2:]
                        ]
                        +
                        [
                           {
                                'if': {'column_id': 'Stock name'},
                                'textAlign': 'left',
                                'fontWeight': 'bold'
                           },
                           {
                                'if': {'column_id': 'Price'},
                                'fontWeight': 'bold'
                           },
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(230, 230, 230)'
                            }
                        ]
                        )
                    )
                ])
            ], style={"width": "50rem"},
            className="mt-3"),     
            dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                                html.Img(id='image_logo',
                                style={"width": "8rem"},
                                ),
#                                html.H1(tickers_titels[tickerIndex], className="card-title")
                                html.H1(id='ticker_header', className="card-title"),
                                dcc.Graph(id='indicator-graph_day', figure={},
                                          config={'displayModeBar':False})
                        ], justify="between"),
                        dbc.Row([
                            dbc.Col([
                                dcc.Graph(id='daily-line', figure={},
                                          config={'displayModeBar':False})
                            ])
                        ]),
                        dbc.Row([
                            dbc.Col([
                                dbc.Button('5D',  id="button_5D", block=True)
                            ]),
                            dbc.Col([
                                dbc.Button('M',  id="button_M",  block=True)
                            ]),
                            dbc.Col([
                                dbc.Button('3M',  id="button_3M",  block=True)
                            ]),
                            dbc.Col([
                                dbc.Button('Y',  id="button_Y",  block=True)
                            ])
                        ], justify="between"),
                        dbc.Row([
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
                        ], justify="between"), 

                    ]),
                ],
                style={"width": "50rem"},
                className="mt-3"
            )
        ], width=6)
    ], justify='center'),

    dcc.Interval(id='update', n_intervals=0, interval=1000*600)
])

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
def on_button_click(btn1, btn2, btn3, btn4, chosen_rows):


    ctx = dash.callback_context

    ctx_trigger = ctx.triggered[0]['prop_id'].split('.')[0]

    #print(ctx.triggered, chosen_rows)
    if (not ctx.triggered) or (ctx_trigger == "dropdown") or (ctx_trigger == "datatable"):
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



    data = [trace_close, trace_EMAshort ,trace_EMAmedium ]



    layout = dict(
        #title='Time series with range slider and selectors',
        margin=dict(t=0, r=0, l=0, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
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
                 size=16,),
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



#----------------------------------------------------------------------------------
# function
# set up the indicator graph showing the performace between start and end data
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
    
    fig.update_traces(delta_font={'size':25})
    fig.update_traces(number_font={'size':25})
    fig.update_layout(height=80, width=150)

    if day_end >= day_start:
        fig.update_traces(delta_increasing_color='green')
    elif day_end < day_start:
        fig.update_traces(delta_decreasing_color='red')
    
    return fig

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
    fig.update_traces(delta_font={'size':30})
    fig.update_traces(number_font={'size':30})
    fig.update_layout(height=100, width=150)

    if day_end >= day_start:
        fig.update_traces(delta_increasing_color='green')
    elif day_end < day_start:
        fig.update_traces(delta_decreasing_color='red')
    
    return fig

# Indicator Graphs below the buttons
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









if __name__ == '__main__':
  app.run_server(debug=True)
