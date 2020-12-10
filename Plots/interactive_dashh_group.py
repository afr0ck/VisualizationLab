import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

# Load CSV file from Datasets folder
df1 = pd.read_csv('../Datasets/Olympic2016Rio.csv')
df2 = pd.read_csv('../Datasets/Weather2014-15.csv')

app = dash.Dash()

# Olympic Barchart
olympic_barchart_df = df1.sort_values(by=['Total'], ascending=[False]).head(20)
olympic_barchart_data = [go.Bar(x=olympic_barchart_df['NOC'], y=olympic_barchart_df['Total'])]

# Olympic Stack Bar Chart
trace1 = go.Bar(x=olympic_barchart_df['NOC'], y=olympic_barchart_df['Gold'], name='Gold', marker={'color': '#FFD700'})
trace2 = go.Bar(x=olympic_barchart_df['NOC'], y=olympic_barchart_df['Silver'], name='Silver', marker={'color': '#9EA0A1'})
trace3 = go.Bar(x=olympic_barchart_df['NOC'], y=olympic_barchart_df['Bronze'], name='Bronze', marker={'color': '#CD7F32'})
olympic_stackbarchart_data = [trace1, trace2, trace3]

# Weather Multi Line Chart
months = ["July", "August", "September", "October", "November", "December",
          "January", "February", "March", "April", "May", "June"]
weather_max_line_df = pd.DataFrame()
weather_min_line_df = pd.DataFrame()
weather_mean_line_df = pd.DataFrame()

for x in months:
    weather_filtered_df = df2[df2['month'] == x]
    new_weather_df = weather_filtered_df.sort_values(by=['actual_max_temp'], ascending=[False]).head(31)
    maxTemp = new_weather_df.iloc[0]['actual_max_temp']
    weather_max_line_df = weather_max_line_df.append(new_weather_df.iloc[[0]])

    new_weather_df = weather_filtered_df.sort_values(by=['actual_min_temp'], ascending=[True]).head(31)
    minTemp = new_weather_df.iloc[0]['actual_min_temp']
    weather_min_line_df = weather_min_line_df.append(new_weather_df.iloc[[0]])

    meanTemp = {'month': [x], 'actual_mean_temp': [(maxTemp + minTemp) / 2]}
    weather_mean_line_df = weather_mean_line_df.append(pd.DataFrame(meanTemp, columns=['month', 'actual_mean_temp']))

weather_trace1 = go.Scatter(x=weather_max_line_df['month'], y=weather_max_line_df['actual_max_temp'], mode='lines', name='Max')
weather_trace2 = go.Scatter(x=weather_min_line_df['month'], y=weather_min_line_df['actual_min_temp'], mode='lines', name='Min')
weather_trace3 = go.Scatter(x=weather_mean_line_df['month'], y=weather_mean_line_df['actual_mean_temp'], mode='lines', name='Mean')
weather_multiline_data = [weather_trace1, weather_trace2, weather_trace3]

# Weather Bubble Chart
weather_max_df = pd.DataFrame()
weather_min_df = pd.DataFrame()
for x in months:
    # Filtering month
    weather_filtered_df = df2[df2['month'] == x]

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
weather_heatmap_data = [go.Heatmap(x=df2['day'], y=df2['month'], z=df2['record_max_temp'].values.tolist(),
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
    html.Div('2016 Rio Olympics', style={'textAlign': 'center'}),
    html.Div('Weather for July 2014 - June 2015', style={'textAlign': 'center'}),
    html.Br(),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Olympic bar chart', style={'color': '#df1e56'}),
    html.Div('This bar chart represents the total medals won by the top 20 countries in the 2016 Olympics.'),
    dcc.Graph(id='graph1',
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
    dcc.Graph(id='graph2',
              figure={
                  'data': olympic_stackbarchart_data,
                  'layout': go.Layout(title='2016 Olympics Top 20 Countries by Total Medals',
                                      xaxis={'title': 'Country'}, yaxis={'title': 'Medals'},
                                      barmode='stack')
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Line chart', style={'color': '#df1e56'}),
    html.Div('This line chart represent the temp in each month from July 2014 to June 2105'),
    dcc.Graph(id='graph3'),
    html.Div('Please select min, max, mean', style={'color': '#ef3e18', 'margin': '10px'}),
    dcc.Dropdown(
        id='select-temp',
        options=[
            {'label': 'Maximum', 'value': 'Max'},
            {'label': 'Minimum', 'value': 'Min'},
            {'label': 'Mean', 'value': 'Mean'},
        ],
        value='Max'
    ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Multi Line chart', style={'color': '#df1e56'}),
    html.Div(
        'This multi line chart represent the max, min and mean temp in each month from July 2014 to June 2105.'),
    dcc.Graph(id='graph4',
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
    dcc.Graph(id='graph5',
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
    dcc.Graph(id='graph6',
              figure={
                  'data': weather_heatmap_data,
                  'layout': go.Layout(title='Weather for July 2014 - June 2015',
                                      xaxis={'title': 'Day of Week'}, yaxis={'title': 'Month'})
              }
              )
])


@app.callback(Output('graph3', 'figure'),
              [Input('select-temp', 'value')])
def update_figure(select_temp):
    months = ["July", "August", "September", "October", "November", "December",
              "January", "February", "March", "April", "May", "June"]
    weather_max_line_df = pd.DataFrame()
    weather_min_line_df = pd.DataFrame()
    weather_mean_line_df = pd.DataFrame()

    for x in months:
        weather_filtered_df = df2[df2['month'] == x]
        new_weather_df = weather_filtered_df.sort_values(by=['actual_max_temp'], ascending=[False]).head(31)
        maxTemp = new_weather_df.iloc[0]['actual_max_temp']
        weather_max_line_df = weather_max_line_df.append(new_weather_df.iloc[[0]])

        new_weather_df = weather_filtered_df.sort_values(by=['actual_min_temp'], ascending=[True]).head(31)
        minTemp = new_weather_df.iloc[0]['actual_min_temp']
        weather_min_line_df = weather_min_line_df.append(new_weather_df.iloc[[0]])

        meanTemp = {'month': [x], 'actual_mean_temp': [(maxTemp + minTemp) / 2]}
        weather_mean_line_df = weather_mean_line_df.append(
            pd.DataFrame(meanTemp, columns=['month', 'actual_mean_temp']))

        if select_temp == 'Max':
            interactive_weather_line_df = [
                go.Scatter(x=weather_max_line_df['month'], y=weather_max_line_df['actual_max_temp'], mode='lines',
                           name='Max')]
        elif select_temp == 'Min':
            interactive_weather_line_df = [
                go.Scatter(x=weather_min_line_df['month'], y=weather_min_line_df['actual_min_temp'], mode='lines',
                           name='Min ')]
        else:
            interactive_weather_line_df = [
                go.Scatter(x=weather_mean_line_df['month'], y=weather_mean_line_df['actual_mean_temp'], mode='lines',
                           name='Mean')]

    return {'data': interactive_weather_line_df,
            'layout': go.Layout(title=select_temp + ' temp from July 2014 - June 2015',
                                xaxis={'title': 'Month'},
                                yaxis={'title': 'Temperature(F)'})}


if __name__ == '__main__':
    app.run_server()