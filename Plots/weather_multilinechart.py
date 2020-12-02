import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

# Load CSV file from Datasets folder
df = pd.read_csv('../Datasets/Weather2014-15.csv')

# Array for each month
months = ["July", "August", "September", "October", "November", "December",
          "January", "February", "March", "April", "May", "June"]

final_max_df = pd.DataFrame()
final_min_df = pd.DataFrame()
final_mean_df = pd.DataFrame()

for x in months:
    # Filtering month
    filtered_df = df[df['month'] == x]

    # Sorting values and select max temp
    new_df = filtered_df.sort_values(by=['actual_max_temp'], ascending=[False]).head(31)
    maxTemp = new_df.iloc[0]['actual_max_temp']

    final_max_df = final_max_df.append(new_df.iloc[[0]])

    # Sorting values and select min temp
    new_df = filtered_df.sort_values(by=['actual_min_temp'], ascending=[True]).head(31)
    minTemp = new_df.iloc[0]['actual_min_temp']

    final_min_df = final_min_df.append(new_df.iloc[[0]])

    # Use max and mean to find mean
    mean = {'month': [x], 'actual_mean_temp': [(maxTemp + minTemp) / 2]}

    final_mean_df = final_mean_df.append(pd.DataFrame(mean, columns=['month', 'actual_mean_temp']))

# Preparing data
trace1 = go.Scatter(x=final_max_df['month'], y=final_max_df['actual_max_temp'], mode='lines', name='Max')
trace2 = go.Scatter(x=final_min_df['month'], y=final_min_df['actual_min_temp'], mode='lines', name='Min')
trace3 = go.Scatter(x=final_mean_df['month'], y=final_mean_df['actual_mean_temp'], mode='lines', name='Mean')
data = [trace1, trace2, trace3]

# Preparing layout
layout = go.Layout(title="Weather for July 2014 - June 2015", xaxis_title="Month",
                   yaxis_title="Temperature (F)")

# Plot the figure and saving in a html file
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='weather_multilinechart.html')