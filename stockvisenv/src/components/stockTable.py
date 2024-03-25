from dash import Dash, dcc, html, Input, Output, ctx  # pip install dash
import dash_bootstrap_components as dbc    # pip install dash-bootstrap-components
import plotly.graph_objects as go
from dash import dash_table
from dash.dash_table import DataTable, FormatTemplate
from dash.dash_table.Format import Sign, Format, Symbol


import numpy as np                         # pip install numpy
import pandas as pd                        # pip install panda



from ..data.stockTimeTrace import tickers, tickers_titels, stockPeriods



# -----------------------------------------------------------------------
# def renderDataTable(app):
# Function for the Datatable-entry in the layout.
# a bit like ArjanCode [Part1](https://www.youtube.com/watch?v=XOFrvzWFM7Y),
#
# -----------------------------------------------------------------------
def renderDataTable(app: Dash, df_all: pd.DataFrame):

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
