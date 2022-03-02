# Stockvisualizer

This small app visualises stock data as chart and provides performance indicators for different time periods. Additionally, an overview of the stock performances of a protfolio is provided in a datatable, from which a particular stock can be selected to be displayed as chart with the performance indicators.


### Set up the development environment 
#### Python virtual enviroment

[Installing packages using pip and virtual environments](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### **Create the virtual environment**

On Windows:

the name of the virtual environment is `stockvisenv`

`$> py -m venv stockvisenv`

#### **Activate the virtual environment**

 On Windows:

`$> .\stockvisenv\Scripts\activate`

#### **Working with the virtual environment**

Installing packages only for the current project
* In VSC set select the python-version of the virtual environment

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

intelligent copying of the code from the links below.


**Contents**
* The card shows logo of the stock (hard-coded - not nice)
* the name of the stock
* The current stock price with a performance indicator over 1 day.
* initial 5 day chart of the closing price 
* buttons to modify the displayed time period 5D, 1 Month, 3 months time range
* indicators below the buttons showing the color-coded performance of the stock over these time periods

![Stockvisualizer impression](./assets/Stockvisualizer_impression.png)

### Running the app

`$> python.exe stockviewer.py`

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

#### Version 2
![Stockvisualizer impression](./assets/StockViewer_impression_V2.png)

* Dropdown menu with predefined stocks  - when one is selected, all the notations, indicators and line charts are updated.
* Logo and title of the selected stock in the card header. The logos are pulled from the web, but the code can be modified to serve the locally stored logos 
* added a `Y` (year) time period.
* Tab-title renamed to `StockViewer`

#### Version 3
![Stockvisualizer impression](./assets/StockViewer_impression_V3.png)

* add a table showing all the stocks and their performance (1D, 5D, M, 3M, Y).
* The rows of the table are selectable. The chart and the performance indicators change accordingly 
* The dropdown-menu has been disabled. In the code it has been commented out. 

### Further ideas
- Conditional datatable. 
   * either color the text depending if the value is positive (green) or negative (red) or even coloring the cell like above. But the intencity of the green or red color depends on the absolut value.
   * Perhaps even a plotly heatmap.
- Style the text of the table. Bold headers etc. More CSS or so
- [ ] multi-select inside the tabel. Compare the selected stocks inside one graph. The graph will show the percentage.  
- code cleaning: 
   - [ ] The indicators currently use 3 callback-functions. Use multiple output with one callback
   - [ ] Use the values of `stockPeriods` in the callbacks of the performance indicators.

### useful Dash-tutorials

- [Dash By Plotly (Python)](https://www.youtube.com/playlist?list=PLCDERj-IUIFCaELQ2i7AwgD2M6Xvc4Slf) - codebliss
- Thanks to [Charming Data](https://www.youtube.com/channel/UCqBFsuAz41sqWcFjZkqmJqQ) on youtube.
   - Build a Financial Dashboard - Python Dash - [Part 1](https://www.youtube.com/watch?v=iOkMaeU8dqE) & [Part 2](https://www.youtube.com/watch?v=catwYsqkhqY)
   - [How to Format the Dash DataTable](https://www.youtube.com/watch?v=S8ZcErBpfYE)
   - [DataTable (Dropdown) - Dash Plotly Python](https://www.youtube.com/watch?v=dgV3GGFMcTc)
- [How To Build A Dashboard In Python – Plotly Dash Step-by-Step Tutorial](https://www.statworx.com/de/blog/how-to-build-a-dashboard-in-python-plotly-dash-step-by-step-tutorial/)

* [Python for Finance: Dash by Plotly](https://towardsdatascience.com/python-for-finance-dash-by-plotly-ccf84045b8be) - dropdown for ticker , line plot, 2 bar graphs
