from dash import Dash, dcc, html, Input, Output, ctx  # pip install dash
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import plotly.graph_objects as go

import pandas as pd                        # pip install panda


# --- project imports
from ..data.stockTimeTrace import tickers, tickers_titels, tickers_logos


from src.components.timeIntervallButtons import renderButtons
from src.components.timeIntervallIndicators import renderButtonIndicators
from src.components.stockHeader import renderStockHeader
from src.components.stockTimeSeries import renderStockTimeSeries
from src.components.stockTable import renderDataTable



# ----------------------------------------------------
# def create_layout():
# Function to set up the layout.
# a bit like ArjanCode [Part1](https://www.youtube.com/watch?v=XOFrvzWFM7Y),
#
# ----------------------------------------------------
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

# --- End 'create_layout'
