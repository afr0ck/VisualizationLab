import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

# Load CSV file from Datasets folder
df1 = pd.read_csv('../Datasets/CoronavirusTotal.csv')
df2 = pd.read_csv('../Datasets/CoronaTimeSeries.csv')
df3 = pd.read_csv('../Datasets/Olympic2016Rio.csv')
df4 = pd.read_csv('../Datasets/Weather2014-15.csv')

app = dash.Dash()

# Bar chart data
barchart_df = df1[df1['Country'] == 'US']
barchart_df = barchart_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
barchart_df = barchart_df.groupby(['State'])['Confirmed'].sum().reset_index()
barchart_df = barchart_df.sort_values(by=['Confirmed'], ascending=[False]).head(20)
data_barchart = [go.Bar(x=barchart_df['State'], y=barchart_df['Confirmed'])]

# Stack bar chart data
stackbarchart_df = df1.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
stackbarchart_df['Unrecovered'] = stackbarchart_df['Confirmed'] - stackbarchart_df['Deaths'] - stackbarchart_df[
    'Recovered']
stackbarchart_df = stackbarchart_df[(stackbarchart_df['Country'] != 'China')]
stackbarchart_df = stackbarchart_df.groupby(['Country']).agg(
    {'Confirmed': 'sum', 'Deaths': 'sum', 'Recovered': 'sum', 'Unrecovered': 'sum'}).reset_index()
stackbarchart_df = stackbarchart_df.sort_values(by=['Confirmed'], ascending=[False]).head(20).reset_index()
trace1_stackbarchart = go.Bar(x=stackbarchart_df['Country'], y=stackbarchart_df['Unrecovered'], name='Under Treatment',
                              marker={'color': '#CD7F32'})
trace2_stackbarchart = go.Bar(x=stackbarchart_df['Country'], y=stackbarchart_df['Recovered'], name='Recovered',
                              marker={'color': '#9EA0A1'})
trace3_stackbarchart = go.Bar(x=stackbarchart_df['Country'], y=stackbarchart_df['Deaths'], name='Deaths',
                              marker={'color': '#FFD700'})
data_stackbarchart = [trace1_stackbarchart, trace2_stackbarchart, trace3_stackbarchart]

# Line Chart
line_df = df2
line_df['Date'] = pd.to_datetime(line_df['Date'])
data_linechart = [go.Scatter(x=line_df['Date'], y=line_df['Confirmed'], mode='lines', name='Death')]

# Multi Line Chart
multiline_df = df2
multiline_df['Date'] = pd.to_datetime(multiline_df['Date'])
trace1_multiline = go.Scatter(x=multiline_df['Date'], y=multiline_df['Death'], mode='lines', name='Death')
trace2_multiline = go.Scatter(x=multiline_df['Date'], y=multiline_df['Recovered'], mode='lines', name='Recovered')
trace3_multiline = go.Scatter(x=multiline_df['Date'], y=multiline_df['Unrecovered'], mode='lines', name='Under Treatment')
data_multiline = [trace1_multiline, trace2_multiline, trace3_multiline]

# Bubble chart
bubble_df = df1.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
bubble_df['Unrecovered'] = bubble_df['Confirmed'] - bubble_df['Deaths'] - bubble_df['Recovered']
bubble_df = bubble_df[(bubble_df['Country'] != 'China')]
bubble_df = bubble_df.groupby(['Country']).agg(
    {'Confirmed': 'sum', 'Recovered': 'sum', 'Unrecovered': 'sum'}).reset_index()
data_bubblechart = [
    go.Scatter(x=bubble_df['Recovered'],
               y=bubble_df['Unrecovered'],
               text=bubble_df['Country'],
               mode='markers',
               marker=dict(size=bubble_df['Confirmed'] / 200, color=bubble_df['Confirmed'] / 200, showscale=True))
]

# Heatmap
data_heatmap = [go.Heatmap(x=df2['Day'],
                           y=df2['WeekofMonth'],
                           z=df2['Recovered'].values.tolist(),
                           colorscale='Jet')]

# Olympic Barchart
olympic_barchart_df = df3.sort_values(by=['Total'], ascending=[False]).head(20)
olympic_barchart_data = [go.Bar(x=olympic_barchart_df['NOC'], y=olympic_barchart_df['Total'])]

# Olympic Stack Bar Chart
trace1 = go.Bar(x=olympic_barchart_df['NOC'], y=olympic_barchart_df['Gold'], name='Gold', marker={'color': '#FFD700'})
trace2 = go.Bar(x=olympic_barchart_df['NOC'], y=olympic_barchart_df['Silver'], name='Silver', marker={'color': '#9EA0A1'})
trace3 = go.Bar(x=olympic_barchart_df['NOC'], y=olympic_barchart_df['Bronze'], name='Bronze', marker={'color': '#CD7F32'})
olympic_stackbarchart_data = [trace1, trace2, trace3]

# Weather Line Chart & Multi Line Chart
months = ["July", "August", "September", "October", "November", "December",
          "January", "February", "March", "April", "May", "June"]
weather_max_line_df = pd.DataFrame()
weather_min_line_df = pd.DataFrame()
weather_mean_line_df = pd.DataFrame()

for x in months:
    weather_filtered_df = df4[df4['month'] == x]
    new_weather_df = weather_filtered_df.sort_values(by=['actual_max_temp'], ascending=[False]).head(31)
    maxTemp = new_weather_df.iloc[0]['actual_max_temp']
    weather_max_line_df = weather_max_line_df.append(new_weather_df.iloc[[0]])

    new_weather_df = weather_filtered_df.sort_values(by=['actual_min_temp'], ascending=[True]).head(31)
    minTemp = new_weather_df.iloc[0]['actual_min_temp']
    weather_min_line_df = weather_min_line_df.append(new_weather_df.iloc[[0]])

    meanTemp = {'month': [x], 'actual_mean_temp': [(maxTemp + minTemp) / 2]}
    weather_mean_line_df = weather_mean_line_df.append(pd.DataFrame(meanTemp, columns=['month', 'actual_mean_temp']))

weather_linechart_data = [go.Scatter(x=weather_max_line_df['month'], y=weather_max_line_df['actual_max_temp'], mode='lines', name='Temp')]

weather_trace1 = go.Scatter(x=weather_max_line_df['month'], y=weather_max_line_df['actual_max_temp'], mode='lines', name='Max')
weather_trace2 = go.Scatter(x=weather_min_line_df['month'], y=weather_min_line_df['actual_min_temp'], mode='lines', name='Min')
weather_trace3 = go.Scatter(x=weather_mean_line_df['month'], y=weather_mean_line_df['actual_mean_temp'], mode='lines', name='Mean')
weather_multiline_data = [weather_trace1, weather_trace2, weather_trace3]

# Weather Bubble Chart
weather_max_df = pd.DataFrame()
weather_min_df = pd.DataFrame()
for x in months:
    # Filtering month
    weather_filtered_df = df4[df4['month'] == x]

    # Sorting values and select max average temp
    new_weather_df = weather_filtered_df.sort_values(by=['average_max_temp'], ascending=[False]).head(31)

    weather_max_df = weather_max_df.append(new_weather_df.iloc[[0]])

    # Sorting values and select min average temp
    new_weather_df = weather_filtered_df.sort_values(by=['average_min_temp'], ascending=[True]).head(31)

    weather_min_df = weather_min_df.append(new_weather_df.iloc[[0]])

weather_bubble_data = [
    go.Scatter(x=weather_min_df["average_min_temp"],
               y=weather_max_df["average_max_temp"],
               text=weather_min_df["month"],
               mode="markers",
               marker=dict(size=weather_max_df["average_max_temp"],
                           color=weather_max_df["average_max_temp"], showscale=True))
]

# Weather Heatmap
weather_heatmap_data = [go.Heatmap(x=df4['day'], y=df4['month'], z=df4['record_max_temp'].values.tolist(),
                                   colorscale='Jet')]

# Layout
app.layout = html.Div(children=[
    html.H1(children='Python Dash',
            style={
                'textAlign': 'center',
                'color': '#ef3e18'
            }
            ),
    html.Div('Web dashboard for Data Visualization using Python', style={'textAlign': 'center'}),
    html.Div('Coronavirus COVID-19 Global Cases -  1/22/2020 to 3/17/2020', style={'textAlign': 'center'}),
    html.Br(),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Interactive Bar chart', style={'color': '#df1e56'}),
    html.Div('This bar chart represent the number of confirmed cases in the first 20 countries of selected continent.'),
    dcc.Graph(id='graph1'),
    html.Div('Please select a continent', style={'color': '#ef3e18', 'margin':'10px'}),
    dcc.Dropdown(
        id='select-continent',
        options=[
            {'label': 'Asia', 'value': 'Asia'},
            {'label': 'Africa', 'value': 'Africa'},
            {'label': 'Europe', 'value': 'Europe'},
            {'label': 'North America', 'value': 'North America'},
            {'label': 'Oceania', 'value': 'Oceania'},
            {'label': 'South America', 'value': 'South America'}
        ],
        value='Europe'
    ),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Bar chart', style={'color': '#df1e56'}),
    html.Div('This bar chart represent the number of confirmed cases in the first 20 states of the US.'),
    dcc.Graph(id='graph2',
              figure={
                  'data': data_barchart,
                  'layout': go.Layout(title='Corona Virus Confirmed Cases in The US',
                                      xaxis={'title': 'States'}, yaxis={'title': 'Number of confirmed cases'})
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Stack bar chart', style={'color': '#df1e56'}),
    html.Div(
        'This stack bar chart represent the CoronaVirus deaths, recovered and under treatment of all reported first 20 countries except China.'),
    dcc.Graph(id='graph3',
              figure={
                  'data': data_stackbarchart,
                  'layout': go.Layout(title='Corona Virus Cases in the first 20 country expect China',
                                      xaxis={'title': 'Country'}, yaxis={'title': 'Number of cases'},
                                      barmode='stack')
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Line chart', style={'color': '#df1e56'}),
    html.Div('This line chart represent the Corona Virus confirmed cases of all reported cases in the given period.'),
    dcc.Graph(id='graph4',
              figure={
                  'data': data_linechart,
                  'layout': go.Layout(title='Corona Virus Confirmed Cases From 2020-01-22 to 2020-03-17',
                                      xaxis={'title': 'Date'}, yaxis={'title': 'Number of cases'})
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Multi Line chart', style={'color': '#df1e56'}),
    html.Div(
        'This line chart represent the CoronaVirus death, recovered and under treatment cases of all reported cases in the given period.'),
    dcc.Graph(id='graph5',
              figure={
                  'data': data_multiline,
                  'layout': go.Layout(
                      title='Corona Virus Death, Recovered and under treatment Cases From 2020-01-22 to 2020-03-17',
                      xaxis={'title': 'Date'}, yaxis={'title': 'Number of cases'})
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Bubble chart', style={'color': '#df1e56'}),
    html.Div(
        'This bubble chart represent the Corona Virus recovered and under treatment of all reported countries except China.'),
    dcc.Graph(id='graph6',
              figure={
                  'data': data_bubblechart,
                  'layout': go.Layout(title='Corona Virus Confirmed Cases',
                                      xaxis={'title': 'Recovered Cases'}, yaxis={'title': 'under Treatment Cases'},
                                      hovermode='closest')
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Heat map', style={'color': '#df1e56'}),
    html.Div(
        'This heat map represent the Corona Virus recovered cases of all reported cases per day of week and week of month.'),
    dcc.Graph(id='graph7',
              figure={
                  'data': data_heatmap,
                  'layout': go.Layout(title='Corona Virus Recovered Cases',
                                      xaxis={'title': 'Day of Week'}, yaxis={'title': 'Week of Month'})
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Olympic bar chart', style={'color': '#df1e56'}),
    html.Div(
        'This bar chart represents the total medals won by the top 20 countries in the 2016 Olympics.'),
    dcc.Graph(id='graph8',
              figure={
                  'data': olympic_barchart_data,
                  'layout': go.Layout(title='2016 Olympics Top 20 Countries by Total Medals',
                                      xaxis={'title': 'Country'}, yaxis={'title': 'Medals'})
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Olympic stack bar chart', style={'color': '#df1e56'}),
    html.Div(
        'This stack bar chart represents the total gold, silver and bronze medals won by the top 20 countries in the 2016 Olympics.'),
    dcc.Graph(id='graph9',
              figure={
                  'data': olympic_stackbarchart_data,
                  'layout': go.Layout(title='2016 Olympics Top 20 Countries by Total Medals',
                                      xaxis={'title': 'Country'}, yaxis={'title': 'Medals'},
                                      barmode='stack')
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Line chart', style={'color': '#df1e56'}),
    html.Div('This line chart represent the max temp in each month from July 2014 to June 2105'),
    dcc.Graph(id='graph10',
              figure={
                  'data': weather_linechart_data,
                  'layout': go.Layout(title='Weather for July 2014 - June 2015',
                                      xaxis={'title': 'Month'}, yaxis={'title': 'Max temp (F)'})
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Multi Line chart', style={'color': '#df1e56'}),
    html.Div(
        'This multi line chart represent the max, min and mean temp in each month from July 2014 to June 2105.'),
    dcc.Graph(id='graph11',
              figure={
                  'data': weather_multiline_data,
                  'layout': go.Layout(
                      title='Weather for July 2014 - June 2015',
                      xaxis={'title': 'Month'}, yaxis={'title': 'Temperature(F)'})
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Bubble chart', style={'color': '#df1e56'}),
    html.Div(
        'This bubble chart represents the relation of min temp to max temp each month from July 2014 to June 2015.'),
    dcc.Graph(id='graph12',
              figure={
                  'data': weather_bubble_data,
                  'layout': go.Layout(title='Weather for July 2014 - June 2015',
                                      xaxis={'title': 'Min Tempterature (F)'}, yaxis={'title': 'Max Tempterature (F)'},
                                      hovermode='closest')
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Heat map', style={'color': '#df1e56'}),
    html.Div(
        'This heatmap represents the record max temperature each day of the week for months July 2014 to June 2015.'),
    dcc.Graph(id='graph13',
              figure={
                  'data': weather_heatmap_data,
                  'layout': go.Layout(title='Weather for July 2014 - June 2015',
                                      xaxis={'title': 'Day of Week'}, yaxis={'title': 'Month'})
              }
              )
])


@app.callback(Output('graph1', 'figure'),
              [Input('select-continent', 'value')])
def update_figure(selected_continent):
    filtered_df = df1[df1['Continent'] == selected_continent]

    filtered_df = filtered_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    new_df = filtered_df.groupby(['Country'])['Confirmed'].sum().reset_index()
    new_df = new_df.sort_values(by=['Confirmed'], ascending=[False]).head(20)
    data_interactive_barchart = [go.Bar(x=new_df['Country'], y=new_df['Confirmed'])]
    return {'data': data_interactive_barchart, 'layout': go.Layout(title='Corona Virus Confirmed Cases in '+selected_continent,
                                                                   xaxis={'title': 'Country'},
                                                                   yaxis={'title': 'Number of confirmed cases'})}


if __name__ == '__main__':
    app.run_server()