import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, ctx  # pip install dash
import pandas as pd                        # pip install panda
from ..data.stockTimeTrace import tickers, stockPeriods

# -----------------------------------------------------------------------
# def renderButtonIndicators(app):
# Function to render the indicators below the buttons in the layout.
# a bit like ArjanCode [Part1](https://www.youtube.com/watch?v=XOFrvzWFM7Y),
#
# -----------------------------------------------------------------------
def renderButtonIndicators(app: Dash, df_all: pd.DataFrame) -> go.Figure: 
    
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


