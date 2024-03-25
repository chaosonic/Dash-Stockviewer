from dash import Dash  # pip install dash
from dash_bootstrap_components.themes import BOOTSTRAP

# --- project imports
from src.data.stockTimeTrace import stockTimetrace, tickers, from_date, to_date
from src.components.layout import create_layout




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