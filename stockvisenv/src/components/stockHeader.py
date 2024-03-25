from dash import Dash, dcc, html, Input, Output, ctx  # pip install dash
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import plotly.graph_objects as go

import pandas as pd                        # pip install panda



from ..data.stockTimeTrace import tickers, tickers_titels, tickers_logos



# -----------------------------------------------------------------------
# def renderStockHeader(app):
# Function to render the Header of the Stocktimeseries
# Displaying a Stock-logo, the Stock-title and the closing price with percentage indicator
# -----------------------------------------------------------------------
def renderStockHeader(app: Dash, df_all: pd.DataFrame):

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
 