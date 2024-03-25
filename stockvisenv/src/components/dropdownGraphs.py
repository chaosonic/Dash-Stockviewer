
from dash import Dash, dcc

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
 