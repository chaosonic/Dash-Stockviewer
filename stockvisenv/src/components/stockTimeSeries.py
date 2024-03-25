from dash import Dash, dcc, Input, Output, ctx  # pip install dash
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import plotly.graph_objects as go

import numpy as np                         # pip install numpy
import pandas as pd                        # pip install panda



from ..data.stockTimeTrace import tickers


# -----------------------------------------------------------------------
# def renderStockGraph(app):
# Function to render the stock timeseries in the layout.
# a bit like ArjanCode [Part1](https://www.youtube.com/watch?v=XOFrvzWFM7Y),
#
# -----------------------------------------------------------------------
def renderStockTimeSeries(app: Dash, df_all: pd.DataFrame):

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
