#### Python virtual enviroment

[Installing packages using pip and virtual environments](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### **Create the virtual environment**

On Windows:

the name of the virtual environment is `stockvisenv`

`$> py -m venv stockvisenv`

#### **Activate the virtual environment**

 On Windows:

`$> .\env\Scripts\activate`

#### **Working with the virtual environment**

Installing packages only for the current project

`$> python3 -m pip install -r requirements.txt`

the `requirements.txt` looks like
~~~python
numpy
pandas
pandas_datareader
dash
dash-bootstrap-components
~~~

## Stockvisualizer

intelligent copyiing of the code from the links below.


**Contents**
* The card shows logo of the stock (hard-coded - not nice)
* the name of the stock
* The current stock price with a performance indicator over 1 day.
* initial 5 day chart of the closing price 
* buttons to modify the displayed time period 5D, 1 Month, 3 months time range
* indicators below the buttons showing the color-coded performance of the stock over these time periods
![Stockvisualizer impression](./assets/Stockvisualizer_impression.png)

### Running the app

`$> python.exe app.py`

something like this will be displayed to the terminal:
~~~
Dash is running on http://127.0.0.1:8050/

 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
~~~

Go to the browser an navigate to `http://127.0.0.1:8050/` to see something like the above. Press the buttons `5D` (5 days), `M` (month), `3M` (3 months) to modify the displayed time period.

### Improvements 

![Stockvisualizer impression](./assets/StockViewer_impression_V2.png)

* Dropdown menu with predefined stocks  - when one is selected, all the notations, indicators and line charts are updated.
* Logo and title of the selected stock in the card header. The logos are pulled from the web, but the code can be modified to serve the locally stored logos 
* added a `Y` (year) time period.
* Tab-title renamed to `StockViewer`

### Further ideas
- [ ] add a table showing all the stocks and their performance. Perhaps even a plotly heatmap.
- [ ] realy cool would be, if you can select a stock to be displayed directly from the table.

### useful Dash-tutorials
- [Dash By Plotly (Python)](https://www.youtube.com/playlist?list=PLCDERj-IUIFCaELQ2i7AwgD2M6Xvc4Slf)
- Build a Financial Dashboard - Python Dash - [Part 1](https://www.youtube.com/watch?v=iOkMaeU8dqE) & [Part 2](https://www.youtube.com/watch?v=catwYsqkhqY)
- [How To Build A Dashboard In Python – Plotly Dash Step-by-Step Tutorial](https://www.statworx.com/de/blog/how-to-build-a-dashboard-in-python-plotly-dash-step-by-step-tutorial/)

* [Python for Finance: Dash by Plotly](https://towardsdatascience.com/python-for-finance-dash-by-plotly-ccf84045b8be) - dropdown for ticker , line plot, 2 bar graphs
