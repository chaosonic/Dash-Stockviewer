import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components

# -----------------------------------------------------------------------
# def renderButtons(app):
# Function to render the buttons in the layout.
# a bit like ArjanCode [Part1](https://www.youtube.com/watch?v=XOFrvzWFM7Y),
#
# -----------------------------------------------------------------------
def renderButtons(app):

# render as ButtonGroup
    return [dbc.ButtonGroup([
            dbc.Button('5D',  id="button_5D",outline=True, color="primary", size='sm'),
            dbc.Button('M',  id="button_M",outline=True, color="primary", size='sm'),
            dbc.Button('3M',  id="button_3M",outline=True, color="primary", size='sm'),
            dbc.Button('Y',  id="button_Y", outline=True, color="primary",size='sm')
    ])
    ]
# --- End def renderButtons

