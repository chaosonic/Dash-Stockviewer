import datetime as dt
import numpy as np                         # pip install numpy
import pandas as pd                        # pip install panda
import pandas_datareader as web

import dash                                # pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
from dash_bootstrap_components._components.Col import Col
from dash_bootstrap_components._components.Row import Row

import plotly.graph_objects as go


# Get Dates From DateEntry and Convert It To Datetime
from_date = dt.datetime(2020, 1, 1)
to_date = dt.datetime.now()

#ticker = 'LYYA.F'   # Lyxor MSCI World - Frankfurt
#ticker = 'BMW.DE'   # BMW
#ticker = 'RDSA.AS'  # Royal Dutch Shell - Stuttgart
#ticker = 'AMD.F'    # AMD - Frankfurt
#ticker = 'EUNL.F'  # iShares Core MSCI World UCITS ETF USD (Acc) - Frankfurt
#ticker = 'ESP0.F'   # Van Eck Games ETF
#ticker = '3CP.SG'   # Xiaomi - Singapore??
# add something else


tickers = ['EUNL.F', 'BMW.F',  'RDSA.AS', 'AMD.F', 'ESP0.F', '3CP.SG', 'ASML.AS']
tickers_titels = ['iShares MSCI World ETF', 'BMW', 'Shell A', 'AMD', 'Van Eck Gaming ETF', 'Xiaomi', 'ASML']
#tickers_logos = ['iShares', 'BMW', 'Shell', 'AMD', 'Vaneck', 'Xiaomi']

#
tickers_logos = ["https://upload.wikimedia.org/wikipedia/commons/d/d8/Logo-ishares_2019.svg",
                 "https://upload.wikimedia.org/wikipedia/commons/4/44/BMW.svg",
                 "https://upload.wikimedia.org/wikipedia/de/7/74/Royal_Dutch_Shell.svg",
                 "https://upload.wikimedia.org/wikipedia/commons/7/7c/AMD_Logo.svg",
                 "https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Vaneck-logo-vector.png/320px-Vaneck-logo-vector.png",
                 "https://upload.wikimedia.org/wikipedia/commons/2/29/Xiaomi_logo.svg",
                 "https://upload.wikimedia.org/wikipedia/commons/6/6c/ASML_Holding_N.V._logo.svg"
                 ]

# smiley https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Mr._Smiley_Face.svg/240px-Mr._Smiley_Face.svg.png
#        https://upload.wikimedia.org/wikipedia/commons/5/51/Mr._Smiley_Face.svg
# iShares https://upload.wikimedia.org/wikipedia/commons/d/d8/Logo-ishares_2019.svg
# Shell   https://upload.wikimedia.org/wikipedia/de/7/74/Royal_Dutch_Shell.svg
# AMD    https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/AMD_Logo.svg/640px-AMD_Logo.svg.png
#        https://upload.wikimedia.org/wikipedia/commons/7/7c/AMD_Logo.svg
# BMW    https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/BMW.svg/240px-BMW.svg.png
#        https://upload.wikimedia.org/wikipedia/commons/4/44/BMW.svg
# xiaomi https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Xiaomi_logo.svg/240px-Xiaomi_logo.svg.png
#        https://upload.wikimedia.org/wikipedia/commons/2/29/Xiaomi_logo.svg
# vaneck https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Vaneck-logo-vector.png/320px-Vaneck-logo-vector.png
# ASML   https://upload.wikimedia.org/wikipedia/commons/6/6c/ASML_Holding_N.V._logo.svg

tickerIndex = 1

# set up an dictionary of pandas dataframes
# How to create an array of dataframes in Python
# https://stackoverflow.com/questions/33907776/how-to-create-an-array-of-dataframes-in-python

df_all = {}
for ticker in tickers:
    df_all[ticker] = web.DataReader(ticker, 'yahoo', from_date, to_date)


item_id = 'dropdown'
dropdown_items = [dbc.DropdownMenuItem(item, id=item_id+'_'+item) 
                  for item in tickers_titels]

dropdown_output = Output(item_id, "label")
dropdown_inputs = [Input(item_id+'_'+item, "n_clicks") for item in tickers_titels]

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
                    dbc.DropdownMenu(
                            dropdown_items, 
                            label=tickers_titels[0], 
                            addon_type="prepend",
#                            bs_size="sm",
                            id=item_id
                        )
                ]),
            ], justify="between"),  
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


# Stackoverflow: create bootstrap drop down menu in plotly dash using one function to set it up
#  https://stackoverflow.com/questions/65806214/create-bootstrap-drop-down-menu-in-plotly-dash-using-one-function-to-set-it-up
 
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
 
# 
# Plotly Dash: How to change header title based on user input?
#         https://stackoverflow.com/questions/62050548/plotly-dash-how-to-change-header-title-based-on-user-input

@app.callback(
   [Output('ticker_header', 'children')], 
   Input(item_id, "label")
   )
def update_ticker_header(label):

    return [f'{label[0]}']


# handle callbacks fpr images
# Looking for a better way to display image
#         https://community.plotly.com/t/looking-for-a-better-way-to-display-image/15672/2

@app.callback(
    Output('image_logo', 'src'), 
    Input(item_id, "label")
    )
def update_ticker_logo(label):

    tickerIndex = tickers_titels.index(label[0])

    return tickers_logos[tickerIndex]




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
    Input(item_id, "label")
)
def on_button_click(btn1, btn2, btn3, btn4, label):


    ctx = dash.callback_context

    ctx_trigger = ctx.triggered[0]['prop_id'].split('.')[0]

    if (not ctx.triggered) or (ctx_trigger == "dropdown") :
        button_id = "button_5D"
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

    df = df_all[tickers[tickers_titels.index(label[0])]]    


    trace_close = go.Scatter(x=df.index[plotLength:],
                            y=df['Close'][plotLength:],
                            name='Close',
                            line=dict(color='#000000', width = 1.5))


    data = [trace_close]

    layout = dict(
        #title='Time series with range slider and selectors',
        margin=dict(t=0, r=0, l=0, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(
            showgrid = True,
            gridcolor= 'rgba(1,1,1,1)'
        ),
        showlegend = False,
        xaxis=dict(

            
            rangeslider=dict(
                visible = False
            ),
            showgrid = True,
            gridcolor= 'rgba(1,1,1,1)',
            type='date'
        )

    )

    fig = go.Figure(data=data, layout=layout)

    sLength = len(df)
    day_start = df['Close'].iloc[sLength+plotLength-1]
    day_end   = df['Close'].iloc[sLength-1]

    fig.update_yaxes(range=[df['Close'][plotLength:].min()*.99,df['Close'][plotLength:].max()*1.01])

    if day_end >= day_start:
        return fig.update_traces(fill='tozeroy',line={'color':'green'})
    elif day_end < day_start:
        return fig.update_traces(fill='tozeroy',
                             line={'color': 'red'})

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
    #dff_rv = dff.iloc[::-1]
    #day_start = dff_rv[dff_rv['date'] == dff_rv['date'].min()]['rate'].values[0]
    #day_end = dff_rv[dff_rv['date'] == dff_rv['date'].max()]['rate'].values[0]
    
    fig = go.Figure(go.Indicator(
        mode="delta",
        value=day_end,
        #title = {"text": "1D"},
        delta={'reference': day_start, 'relative': True, 'valueformat':'.2%'}))
    
    #fig.update_traces(title_font={'size':16})
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
    Input('update', 'n_intervals'),
    Input(item_id, "label")
)
def graph_1_callback(timer1, label):

    df = df_all[tickers[tickers_titels.index(label[0])]]
    sLength = len(df)
    day_start = df['Close'].iloc[sLength-2]
    day_end   = df['Close'].iloc[sLength-1]
    
    fig = go.Figure(go.Indicator(
        mode="delta + number",
        value=day_end,
        number ={'prefix' : "€ "},
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

# Indicator Graph 5D
@app.callback(
    Output('indicator-graph', 'figure'),
    Input('update', 'n_intervals'),
    Input(item_id, "label")
)
def graph_1_callback(timer1, label):

    df = df_all[tickers[tickers_titels.index(label[0])]]
    sLength = len(df)
    day_start = df['Close'].iloc[sLength-6]
    day_end   = df['Close'].iloc[sLength-1]
    fig = indicatorPerformance(day_start, day_end)
    
    return fig

# Indicator Graph
@app.callback(
    Output('indicator-graph2', 'figure'),
    Input('update', 'n_intervals'),
    Input(item_id, "label")
)
def graph_2_callback(timer2, label):
    df = df_all[tickers[tickers_titels.index(label[0])]]
    sLength = len(df)
    day_start = df['Close'].iloc[sLength-21]
    day_end   = df['Close'].iloc[sLength-1]
    fig = indicatorPerformance(day_start, day_end) 

    return fig

# Indicator Graph
@app.callback(
    Output('indicator-graph3', 'figure'),
    Input('update', 'n_intervals'),
    Input(item_id, "label")
)
def update_graph(timer3, label):
    df = df_all[tickers[tickers_titels.index(label[0])]]
    sLength = len(df)
    day_start = df['Close'].iloc[sLength-61]
    day_end   = df['Close'].iloc[sLength-1]
    fig = indicatorPerformance(day_start, day_end)

    return fig

# Indicator Graph
@app.callback(
    Output('indicator-graph4', 'figure'),
    Input('update', 'n_intervals'),
    Input(item_id, "label")
)
def update_graph(timer4, label):
    df = df_all[tickers[tickers_titels.index(label[0])]]
    sLength = len(df)
    day_start = df['Close'].iloc[sLength-300]
    day_end   = df['Close'].iloc[sLength-1]
    fig = indicatorPerformance(day_start, day_end)

    return fig








if __name__ == '__main__':
  app.run_server(debug=True)

